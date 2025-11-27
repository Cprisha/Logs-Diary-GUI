import tkinter as tk
from tkinter import simpledialog, messagebox
from database import diary_sections, folder_exists, write_entry, logs_input, read_entry


def start_diary_app():
    root = tk.Tk()
    root.title("Diary App")
    root.geometry("400x400")
    tk.Label(root, text="Select").place(x=13, y=13)

    section_frame = tk.Frame(root)
    section_frame.pack()

    def refresh_sections():
        for widget in section_frame.winfo_children():
            widget.destroy()

        for section in diary_sections():
            tk.Button(section_frame, text=section, command=lambda sec=section: open_section(sec)).pack(pady=2)

    def add_section():
        name = simpledialog.askstring("Add a new section", "Enter the section's name:")
        if name:
            folder_exists(name)
            refresh_sections()

    tk.Button(root, text="Add New SECTION", command=add_section).pack(pady=10)
    refresh_sections()

    root.mainloop()


def open_section(section_name):
    win = tk.Toplevel()
    win.title(f"Entries for {section_name}")
    win.geometry("500x600")

    frame = tk.Frame(win)
    frame.pack(pady=10, fill='both', expand=True)

    def refresh_entries():
        for widget in frame.winfo_children():
            widget.destroy()

        for subject in logs_input(section_name):
            entry_frame = tk.Frame(frame, bd=1, relief='solid', padx=5, pady=5)
            entry_frame.pack(fill='x', pady=5)

            tk.Label(entry_frame, text=f"Title: {subject}", font=("Arial", 10, "bold")).pack(anchor='w')

            def view_entry_content(subject=subject):
                view_win = tk.Toplevel(win)
                view_win.title(f"View Entry")
                view_win.geometry("400x400")

                content = read_entry(section_name, subject)
                text = tk.Text(view_win, wrap="word", height=15, width=40)
                text.insert("1.0", content)
                text.config(state=tk.DISABLED)
                text.pack(pady=10)

            tk.Button(entry_frame, text="View", command=view_entry_content).pack(side='right', padx=5)

            def edit_entry_callback(subject=subject):
                def edit_entry():
                    old_content = read_entry(section_name, subject)
                    new_content = simpledialog.askstring("Edit", f"Editing: {subject}", initialvalue=old_content)
                    if new_content:
                        write_entry(section_name, subject, new_content)
                        refresh_entries()

                return edit_entry

            def delete_entry_callback(subject = subject):
                def delete_entry():
                    confirm = messagebox.askyesno("Delete", f"Delete {subject}?")
                    if confirm:
                        write_entry(section_name, subject, "")
                        refresh_entries()

                return delete_entry

            tk.Button(entry_frame, text="Edit", command=edit_entry_callback(subject)).pack(side='left', padx=5)
            tk.Button(entry_frame, text="Delete", command=delete_entry_callback(subject)).pack(side='left', padx=5)

    def add_log_entry():
        subject = simpledialog.askstring("Subject", "Enter log subject:")
        if subject:
            new_win = tk.Toplevel(win)
            new_win.title("Enter Content")
            new_win.geometry("400x400")

            tk.Label(new_win, text="What was your day like today?").pack(pady=10)

            text_box = tk.Text(new_win, height=10, width=40)
            text_box.pack(pady=10)

            scrollbar = tk.Scrollbar(new_win, command=text_box.yview)
            scrollbar.pack(side="right", fill="y")
            text_box.config(yscrollcommand=scrollbar.set)

            def save_entry():
                content = text_box.get("1.0", "end-1c")
                if content.strip():
                    write_entry(section_name, subject, content)
                    messagebox.showinfo("Success", "Entry added!")
                    new_win.destroy()
                    refresh_entries()
                else:
                    messagebox.showerror("Error", "Diary entry cannot be empty.")

            tk.Button(new_win, text="Save Entry", command=save_entry).pack(pady=10)

    tk.Button(win, text="Add New Entry", command=add_log_entry).pack(pady=5)
    refresh_entries()
