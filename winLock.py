import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import *
import win32com.client
import subprocess
import os
import pythoncom
from win32com.shell import shell


folder_path = ""
password = ""

def lock(path):
    # lock the file/folder
    subprocess.call(["attrib", "+H", "+S", "+R", path])
    return path

def unlock(name):
    home = os.path.expanduser("~")
    vbs_file_path = f"{home}\\{name}_sky9262.vbs"
    with open(vbs_file_path) as f:
        first_line = f.readline()
        # print(first_line.split(" ")) #['REM', 'D:\\\\OS', '1111\n']
        main_folder = first_line.replace("REM ","").replace("\n","").replace("\\\\","\\")
        # old_pass = first_line.split(" ")[2].strip('\n')

    shortcut_path = main_folder+".lnk"
    # lock the file/folder
    subprocess.call(["attrib", "-H", "-S", "-R", main_folder])
    subprocess.call(["attrib", "-H", "-S", "-R", vbs_file_path])

    os.remove(shortcut_path)
    os.remove(vbs_file_path)
    refresh_buttons()

def change_icon(shortcut_path):
    # Index of the icon in the imageres.dll file
    icon_index = 165  # Change this to the index of the icon you want to use

    # Create a Shell object
    shell = win32com.client.Dispatch("WScript.Shell")

    # Get the shortcut object
    shortcut = shell.CreateShortCut(shortcut_path)

    # Set the icon of the shortcut
    shortcut.IconLocation = "%SystemRoot%\\system32\\imageres.dll," + str(icon_index)

    # Save the shortcut
    shortcut.Save()

def createVBS(folder_path, password):
    # Get the path to the user's home directory
    home_dir = os.path.expanduser("~")
    folder_name = folder_path.split("\\")[-1]
    vbs_folder_path = folder_path.replace("\\\\","\\")

    # Define the name and contents of the VBScript file
    filename = os.path.join(home_dir, f"{folder_name}_sky9262.vbs")
    contents = f'''REM {folder_path}
Dim sInput
sInput = InputBox("Enter the Password", "Password Required - sky9262")
'MsgBox "You entered:" & sInput
If sInput = "{password}" Then
    MsgBox "Correct Password. Please wait...", vbSystemModal, "Successful - sky9262"
    Set objShell = CreateObject("Shell.Application") 
    strPath = "{vbs_folder_path}"
    objShell.Explore strPath 
Else
    MsgBox "Wrong password!!!", vbSystemModal, "Failed - sky9262"
End If'''

    # Write the contents to the file
    with open(filename, 'w') as f:
        f.write(contents)
    lock(filename)
    return filename

def create_shortcut(file_path, shortcut_path):
    file_name = file_path.split("\\")[-1].replace(".vbs","")
    shortcut = pythoncom.CoCreateInstance (
    shell.CLSID_ShellLink,
    None,
    pythoncom.CLSCTX_INPROC_SERVER,
    shell.IID_IShellLink
    )
    shortcut.SetPath (file_path)
    shortcut.SetDescription ("LockFolder - sky9262")
    shortcut.SetIconLocation ("%SystemRoot%\\system32\\imageres.dll", 165)

    persist_file = shortcut.QueryInterface (pythoncom.IID_IPersistFile)
    persist_file.Save (os.path.join (shortcut_path+".lnk"), 0)

def choose_folder():
    ask_folder_path = filedialog.askdirectory()
    global folder_path 
    folder_path = ask_folder_path.replace("/","\\\\")
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(0, ask_folder_path)

def check_password():
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()
    if password == confirm_password:
        password = password
        create_shortcut(createVBS(lock(folder_path),password),folder_path)
        messagebox.showinfo("Success", "Locked!")
        root.destroy()
    else:
        messagebox.showerror("Error", "Passwords do not match!")

def create_button(filename):
    button = Button(frame, text=filename, command=lambda: unlock(filename))
    button.pack(side=BOTTOM)

def refresh_buttons():
    # clear the frame
    for widget in frame.winfo_children():
        widget.destroy()
    # recreate the buttons
    for filename in os.listdir(os.path.expanduser("~")):
        if "sky9262" in filename:
            create_button(filename.replace("_sky9262.vbs",""))

def show_files():
    refresh_buttons()


# create the main window
root = tk.Tk()
root.title("Lock Folder - sky9262")
frame = Frame(root)
frame.pack()

# set the window size and position
win_width = 400
win_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width/2) - (win_width/2))
y = int((screen_height/2) - (win_height/2))
root.geometry(f"{win_width}x{win_height}+{x}+{y}")

# create widgets for selecting folder and password
folder_path_label = tk.Label(root, text="Select Folder:")
folder_path_entry = tk.Entry(root, width=50)
folder_path_button = tk.Button(root, text="Browse", command=choose_folder)

password_label = tk.Label(root, text="Password:")
password_entry = tk.Entry(root, width=20, show="*")

confirm_password_label = tk.Label(root, text="Confirm Password:")
confirm_password_entry = tk.Entry(root, width=20, show="*")

submit_button = tk.Button(root, text="Lock", command=check_password)

# add widgets to the window
folder_path_label.pack()
folder_path_entry.pack()
folder_path_button.pack()

password_label.pack()
password_entry.pack()

confirm_password_label.pack()
confirm_password_entry.pack()

submit_button.pack()

button = tk.Button(root, text="Unlock", command=show_files)
button.pack(side=BOTTOM)

# run the main loop
root.iconbitmap(r'.\\winLock.ico')
root.mainloop()
