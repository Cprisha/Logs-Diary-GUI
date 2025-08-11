# Diary GUI

A private digital diary, built in Python, featuring a log-writing space with face recognition-based access.

## Libraries Used

1. OpenCV  
2. `face_recognition`  
3. SQLite  
4. `tkinter`

---

## Features

- Face recognition-based login  
- Simple diary interface with add, edit, and delete entry options  
- Local data storage using SQLite  
- Poem display while face recognition is in progress

---

## How to Run the Project

1. Clone the repository or download the files  
2. Install dependencies:

   ```bash
   pip install opencv-python face_recognition
   ```

3. Make sure your webcam is connected  
4. Run the script.

---

## Notes

- The app will ask you to register your face on the first run  
- All diary data is stored locally in `Logs/diary.db`  
- `poems.txt` is optional but adds a creative touch  
- Do not share your `face_data.npy` file—it is unique to your face
- For the full project breakdown, including libraries used, personal motivation, and future upgrades, check out the detailed PDF:
[View LogsDiaryGUI.pdf](LogsDiaryGUI.pdf)

