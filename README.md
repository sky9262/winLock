
# winLock

This is a tiny software to lock a folder, without compression and encryption in windows. it’s super convenient and fast。


<mark>Note: It is only for windows (not linux). </mark>

## Usage Demonstration

![Usage](./Usage.gif)
## Installation

Install winLock

```bash
  git clone https://github.com/sky9262/winLock.git
  cd winLock
  pip install requirements.txt
```
    
## Explanation 

This is a Python script that creates a graphical user interface using the Tkinter module. It allows a user to select a folder and then lock it by creating a Visual Basic Script (VBS) file and a shortcut. The locked folder is then hidden from view using Windows' "hidden" attribute. The locked folder can be unlocked by clicking on the shortcut and entering a password.

The code imports several modules: Tkinter, filedialog, messagebox, win32com.client, subprocess, os, and pythoncom.

The script creates a `tkinter` window with three widgets: a label, an entry field, and a button for selecting the folder to be locked. The window also has two password entry fields and a button for checking and locking the selected folder. When the folder is locked, a shortcut file is created on the desktop that can be used to unlock the folder. The script also displays a list of locked folders as buttons that can be clicked to unlock the folders.

Finally, the script enters the Tkinter main event loop using the mainloop() method to display the GUI and allow the user to interact with it.
## Authors

- [@sky9262](https://www.github.com/sky9262)


## Connect with me
[![blog](https://img.shields.io/badge/blog-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://sky9262.tistory.com/)

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sky9262/)

[![Instagram](https://img.shields.io/badge/Instagram-ffffff?style=for-the-badge&logo=instagram&logoColor=dd2a7b)](https://www.instagram.com/sky926296/)

[![github](https://img.shields.io/badge/github-000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sky9262/)
