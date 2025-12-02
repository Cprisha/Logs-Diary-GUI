
## Why this code
As I grew up, I realized that maintaining a diary is not about being cool or a compulsion. It is just an optional task of self-discipline, and self-reflection, that is best incorporated in one’s daily life. However, in a physical copy, little does the privacy survive when you live in a joint Indian Marwari family. By the dinner, what was written in it would have already reached that one cousin who I have never met. Not the best experience, though lowkey iconic. 
This compelled me to shift my diary from a pen and a notebook to digital. Then, I thought, why not my own code: not like anyone who has access to my laptop other than me will check out my python IDLE in search of my secrets, right?

---

## Libraries- How? Where? Which?
- OpenCV: This is primarily used to handle the webcam access of the system and real time face capture. It also converts the color format into one compatible for face_recognition. 
- face_recognition: It compares the live webcam input with the stored face recognition data. It is responsible for the face lock feature.
- numpy: It saves, loads and handles the face encodings in the form of numeric arrays as ‘face_data.npy’ binary files.
- tkinter: tkinter is imported as tk, and from the tkinter library, we import messagebox and simpledialog.
  - tk: It serves as the main GUI framework for the application
  - messagebox: It is used to create the pop ups while closing the window, to show an error message etc. while the code is running
  - simpledialog
- OS: It is used for folder/file handling. Creates a Logs directory for storing the data base.
- time: It is used to set the time in which the face recognition runs
- random: It is used to display one of the poems randomly on the face recognition window.
- sqlite3: It helps to manage, create the local database to store entries. Provides the SQL commands for creating, inserting, updating, and deleting the diary entries.

---

## MVP structure:
- [main.py](main.py) - the final code which has to be run
- [face_lock.py](face_lock.py) - has the code for the face lock and poems flashing
- [database.py](database.py) - has the code with regard to file handling and editing
- [ui.py](ui.py) - has the GUI related code

---

## Future Upgrades
- An option to add dates to entries, tags to entries and colors to them as well- based on the mood.
- Themes for the GUI application
- A search bar to navigate through the logs/diary entries
- A more secure face lock
- Option to add voice notes and images
- The option to add stickers, texts in different fonts- the ability to make it look like a journal.

---
