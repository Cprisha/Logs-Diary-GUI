import cv2
import face_recognition
import numpy as np
import tkinter as tk
from tkinter import messagebox
import os
import time
import random
import sqlite3
from tkinter import simpledialog

os.makedirs("Logs", exist_ok=True)
KNOWN_FACE_PATH = "Logs/face_data.npy"

Base_directory = "Logs"
os.makedirs(Base_directory, exist_ok=True)
db_path = os.path.join(Base_directory, "diary.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()


root = tk.Tk()
root.title("Diary App")
root.geometry("400x400")
tk.Label(root, text="Select").place(x=13, y=13)

section_frame = tk.Frame(root)
section_frame.pack()

poem = ""
try:
    with open("poems.txt", "r", encoding="utf-8") as f:
        poems = [line.strip() for line in f if line.strip()]
        poem = random.choice(poems) if poems else "No poems available."
except FileNotFoundError:
    poem = "poems.txt not found. Place a text file with poetry lines."

class screening(tk.Tk):
    def __init__(self, poem_text):
        super().__init__()
        self.overrideredirect(True)
        self.attributes('-fullscreen', True)
        self.configure(bg="black")

        label = tk.Label(self, text=poem_text, font=("Helvetica", 28), fg="white", bg="black", wraplength=1000, justify="center")
        label.pack(expand=True)

    def program_exit(self):
        self.destroy()

def register_face():
    cam = cv2.VideoCapture(0)
    messagebox.showinfo("Face Registration", "No face data found. Please look at the camera...")

    while True:
        ret, frame = cam.read()
        if not ret:
            continue
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locs = face_recognition.face_locations(rgb)
        if locs:
            encs = face_recognition.face_encodings(rgb, locs)
            if encs:
                np.save(KNOWN_FACE_PATH, encs[0])
                messagebox.showinfo("Success", "Face registered successfully!")
                break
        cv2.imshow("Register Face (Press 'q' to cancel)", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

def authentication(timeout=15):
    splash = screening(poem)
    splash.update()

    known_face = np.load(KNOWN_FACE_PATH)
    cam = cv2.VideoCapture(0)
    success = False
    start = time.time()

    while time.time() - start < timeout:
        ret, frame = cam.read()
        if not ret:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locs = face_recognition.face_locations(rgb)
        encs = face_recognition.face_encodings(rgb, locs)

        for enc in encs:
            matches = face_recognition.compare_faces([known_face], enc)
            if True in matches:
                success = True
                break

        splash.update()
        if success:
            break

    cam.release()
    splash.program_exit()
    return success

def FaceLock():
    if not os.path.exists(KNOWN_FACE_PATH):
        register_face()

    if authentication():
        return True
    else:
        messagebox.showerror("Access Denied", "Face not recognized.")
        return False

if __name__ == "__main__":
    if FaceLock():
        root.mainloop()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section TEXT NOT NULL,
    subject TEXT NOT NULL,
    body TEXT NOT NULL,
    UNIQUE(section, subject)
)
""")

conn.commit()

def diary_section():
    cursor.execute("SELECT name FROM sections")
    return [row[0] for row in cursor.fetchall()]

def folder_exists(section):
    cursor.execute("INSERT OR IGNORE INTO sections (name) VALUES (?)", (section,))
    conn.commit()

def logs_input(section):
    cursor.execute("SELECT subject FROM entries WHERE section = ?", (section,))
    return [row[0] for row in cursor.fetchall()]

def safe_write_file(section, subject, content):
    try:
        cursor.execute("""
            INSERT INTO entries (section, subject, body) VALUES (?, ?, ?)
            ON CONFLICT(section, subject) DO UPDATE SET body=excluded.body
        """, (section, subject, content))
        conn.commit()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to write the entry: {str(e)}")

def section_open(name):
    win = tk.Toplevel(root)
    win.title(f"Enteries for {name}")
    win.geometry("500x600")

    frame = tk.Frame(win)
    frame.pack(pady=10, fill='both', expand=True)

    def refresh():
        for widget in frame.winfo_children():
            widget.destroy()

        logs_entry = logs_input(name)
        for file in logs_entry:
            # Frame for each entry
            entry_log = tk.Frame(frame, bd=1, relief='solid', padx=5, pady=5)
            entry_log.pack(fill='x', pady=5)

            tk.Label(entry_log, text=f"Title: {file}", font=("Arial", 10, "bold")).pack(anchor='w')

            def view_log_content(subject=file):
                view_win = tk.Toplevel(root)
                view_win.title(f"View Entry")
                view_win.geometry("400x400")

                cursor.execute("SELECT body FROM entries WHERE section=? AND subject=?", (name, subject))
                content = cursor.fetchone()
                if content:
                    content_text = tk.Text(view_win, wrap="word", height=15, width=40)
                    content_text.insert("1.0", content[0])
                    content_text.config(state=tk.DISABLED)
                    content_text.pack(pady=10)

            tk.Button(entry_log, text="View", command=view_log_content).pack(side='right', padx=5)

            btn_frame = tk.Frame(entry_log)
            btn_frame.pack(anchor='e')

            def make_edit_callback(subject=file):
                def edit_log():
                    cursor.execute("SELECT body FROM entries WHERE section=? AND subject=?", (name, subject))
                    old = cursor.fetchone()[0]
                    new_body = simpledialog.askstring("Edit", f"Editing: {subject}", initialvalue=old)
                    if new_body is not None:
                        safe_write_file(name, subject, new_body)
                        refresh()
                return edit_log

            def make_delete_callback(subject=file):
                def delete_log():
                    confirm = messagebox.askyesno("Delete", f"Delete: {subject}?")
                    if confirm:
                        cursor.execute("DELETE FROM entries WHERE section=? AND subject=?", (name, subject))
                        conn.commit()
                        refresh()
                return delete_log

            tk.Button(btn_frame, text="Edit", command=make_edit_callback(subject=file)).pack(side='left', padx=5)
            tk.Button(btn_frame, text="Delete", command=make_delete_callback(subject=file)).pack(side='left', padx=5)

    def add_log():
        subject = simpledialog.askstring("Subject", "Enter log subject:")
        if not subject:
            return

        new_win = tk.Toplevel(root)
        new_win.title("Enter Content")
        new_win.geometry("400x400")

        tk.Label(new_win, text="So, what was your day like today:").pack(pady=10)

        text_box = tk.Text(new_win, height=10, width=40)
        text_box.pack(pady=10)

        scrollbar = tk.Scrollbar(new_win, command=text_box.yview)
        scrollbar.pack(side="right", fill="y")
        text_box.config(yscrollcommand=scrollbar.set)

        def save_entry():
            body = text_box.get("1.0", "end-1c")
            if not body.strip():
                messagebox.showerror("Error", "Diary body cannot be empty!")
                return

            folder_exists(name)
            safe_write_file(name, subject, body)
            messagebox.showinfo("Success", "Entry added successfully!")
            new_win.destroy()
            refresh()

        tk.Button(new_win, text="Save Entry", command=save_entry).pack(pady=10)

    tk.Button(win, text="Add New Entry", command=add_log).pack(pady=5)
    refresh()

def refresh_section():
    for widget in section_frame.winfo_children():
        widget.destroy()

    for person in diary_section():
        tk.Button(section_frame, text=person, command=lambda p=person: section_open(p)).pack(pady=2)

def add_section():
    name = simpledialog.askstring("Add a new section to your diary", "Enter the section's name:")
    if name:
        name = name.strip()
        if not name:
            messagebox.showerror("Invalid Section Name", "No Section name entered")
            return
        folder_exists(name)
        refresh_section()

tk.Button(root, text="Add New SECTION", command=add_section).pack(pady=10)
refresh_section()


root.mainloop()
