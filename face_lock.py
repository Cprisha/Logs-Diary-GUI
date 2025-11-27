import cv2
import face_recognition
import numpy as np
import time
import tkinter as tk
import random
from tkinter import messagebox
import os
import importlib.resources

BASE_DIR = "Logs"
os.makedirs(BASE_DIR, exist_ok=True)
KNOWN_FACE_PATH = os.path.join(BASE_DIR, "face_data.npy")


def load_poem():
    try:
        with importlib.resources.open_text('Logs', 'poems.txt') as f:
            lines = [line.strip() for line in f if line.strip()]
            return random.choice(lines) if lines else "No poems available."
    except FileNotFoundError:
        return "poems.txt not found."


class SplashScreen(tk.Tk):
    def __init__(self, poem_text):
        super().__init__()
        self.overrideredirect(True)
        self.attributes('-fullscreen', True)
        self.configure(bg="black")
        tk.Label(
            self,
            text=poem_text,
            font=("Helvetica", 28),
            fg="white",
            bg="black",
            wraplength=1000,
            justify="center"
        ).pack(expand=True)

    def close(self):
        self.destroy()


def register_face():
    cam = cv2.VideoCapture(0)
    messagebox.showinfo("Face Registration", "Look at the camera...")

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
                messagebox.showinfo("Success", "Face registered!")
                break

        cv2.imshow("Register Face (press q to cancel)", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


def authenticate(timeout=15):
    poem_text = load_poem()  # Load the poem text
    splash = SplashScreen(poem_text)
    splash.update()

    known_face = np.load(KNOWN_FACE_PATH)
    cam = cv2.VideoCapture(0)
    start = time.time()

    success = False
    while time.time() - start < timeout:
        ret, frame = cam.read()
        if not ret:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locs = face_recognition.face_locations(rgb)
        encs = face_recognition.face_encodings(rgb, locs)

        for enc in encs:
            if True in face_recognition.compare_faces([known_face], enc):
                success = True
                break

        splash.update()
        if success:
            break

    cam.release()
    splash.close()
    return success


def face_lock():
    if not os.path.exists(KNOWN_FACE_PATH):
        register_face()

    if authenticate():
        return True
    else:
        messagebox.showerror("Access Denied", "Face not recognized.")
        return False
