from face_lock import face_lock
from ui import start_diary_app

if __name__ == "__main__":
    if face_lock():
        start_diary_app()
    else:
        print("Authentication failed.")
