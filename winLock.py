import tkinter as tk
from tkinter import filedialog, messagebox, Button, Frame
import win32com.client
from subprocess import call
import os
from pythoncom import IID_IPersistFile, CoCreateInstance, CLSCTX_INPROC_SERVER
from win32com.shell import shell

folder_path = ""
password = ""

def lock(path):
    call(["attrib", "+H", "+S", "+R", path])
    return path

def unlock(name):
    home = os.path.expanduser("~")
    vbs_file_path = f"{home}\\{name}_sky9262.vbs"
    with open(vbs_file_path) as f:
        first_line = f.readline()
        main_folder = (
            first_line.replace("REM ", "").replace("\n", "").replace("\\\\", "\\")
        )

    shortcut_path = main_folder + ".lnk"
    call(["attrib", "-H", "-S", "-R", main_folder])
    call(["attrib", "-H", "-S", "-R", vbs_file_path])

    os.remove(shortcut_path)
    os.remove(vbs_file_path)
    refresh_buttons()

def change_icon(shortcut_path, icon_index=165):
    shell_obj = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell_obj.CreateShortCut(shortcut_path)
    shortcut.IconLocation = f"%SystemRoot%\\system32\\imageres.dll,{icon_index}"
    shortcut.Save()

def createVBS(folder_path, password):
    home_dir = os.path.expanduser("~")
    folder_name = folder_path.split("\\")[-1]
    vbs_folder_path = folder_path.replace("\\\\", "\\")

    filename = os.path.join(home_dir, f"{folder_name}_sky9262.vbs")
    contents = f"""REM {folder_path}
Dim sInput
sInput = InputBox("Enter the Password", "Password Required - sky9262")
If sInput = "{password}" Then
    MsgBox "Correct Password. Please wait...", vbSystemModal, "Successful - sky9262"
    Set objShell = CreateObject("Shell.Application") 
    strPath = "{vbs_folder_path}"
    objShell.Explore strPath 
Else
    MsgBox "Wrong password!!!", vbSystemModal, "Failed - sky9262"
End If"""

    with open(filename, "w") as f:
        f.write(contents)
    lock(filename)
    return filename

def create_shortcut(file_path, shortcut_path):
    file_name = file_path.split("\\")[-1].replace(".vbs", "")
    shortcut = CoCreateInstance(
        shell.CLSID_ShellLink, None, CLSCTX_INPROC_SERVER, shell.IID_IShellLink
    )
    shortcut.SetPath(file_path)
    shortcut.SetDescription("LockFolder - sky9262")
    shortcut.SetIconLocation("%SystemRoot%\\system32\\imageres.dll", 165)

    persist_file = shortcut.QueryInterface(IID_IPersistFile)
    persist_file.Save(os.path.join(shortcut_path + ".lnk"), 0)


def choose_folder():
    global folder_path
    folder_path = filedialog.askdirectory().replace("/", "\\\\")
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(0, folder_path)

def check_password():
    global password
    entered_password = password_entry.get()
    confirm_password = confirm_password_entry.get()
    if password == "":
        messagebox.showerror("Error", "Password cannot be empty!")
    elif entered_password == confirm_password:
        password = entered_password
        create_shortcut(createVBS(lock(folder_path), password), folder_path)
        messagebox.showinfo("Success", "Locked!")
        root.destroy()
    else:
        messagebox.showerror("Error", "Passwords do not match!")

def create_button(filename):
    button = Button(
        frame,
        text=filename,
        command=lambda: unlock(filename),
        bg="#e74c3c",
        fg="#ecf0f1",
        font=("Arial", 10),
    )
    button.pack(padx=10, pady=10, side=tk.BOTTOM)


def refresh_buttons():
    for widget in frame.winfo_children():
        widget.destroy()
    for filename in os.listdir(os.path.expanduser("~")):
        if "sky9262" in filename:
            create_button(filename.replace("_sky9262.vbs", ""))


def show_files():
    refresh_buttons()

root = tk.Tk()
root.title("Lock Folder - sky9262")

root.configure(bg="#2c3e50")

frame = Frame(root, bg="#2c3e50")
frame.pack(padx=10, pady=10)

win_width = 400
win_height = 350
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width / 2) - (win_width / 2))
y = int((screen_height / 2) - (win_height / 2))
root.geometry(f"{win_width}x{win_height}+{x}+{y}")

folder_path_label = tk.Label(
    root, text="Select Folder:", bg="#2c3e50", fg="#ecf0f1", font=("Arial", 12)
)
folder_path_entry = tk.Entry(root, width=50)
folder_path_button = tk.Button(
    root,
    text="Browse",
    command=choose_folder,
    bg="#3498db",
    fg="#ecf0f1",
    font=("Arial", 10),
)

password_label = tk.Label(
    root, text="Password:", bg="#2c3e50", fg="#ecf0f1", font=("Arial", 12)
)
password_entry = tk.Entry(root, width=20, show="*")

confirm_password_label = tk.Label(
    root, text="Confirm Password:", bg="#2c3e50", fg="#ecf0f1", font=("Arial", 12)
)
confirm_password_entry = tk.Entry(root, width=20, show="*")

submit_button = tk.Button(
    root,
    text="Lock",
    command=check_password,
    bg="#27ae60",
    fg="#ecf0f1",
    font=("Arial", 10),
)

# add widgets to the window
folder_path_label.pack(pady=(0, 5))
folder_path_entry.pack(pady=(0, 5))
folder_path_button.pack(pady=(0, 10))

password_label.pack(pady=(0, 5))
password_entry.pack(pady=(0, 5))

confirm_password_label.pack(pady=(0, 5))
confirm_password_entry.pack(pady=(0, 5))

submit_button.pack(pady=(0, 10))

unlock_button = tk.Button(
    root,
    text="Unlock",
    command=show_files,
    bg="#e74c3c",
    fg="#ecf0f1",
    font=("Arial", 10),
)
unlock_button.pack(side=tk.BOTTOM)

# run the main loop
root.iconbitmap(r".\\winLock.ico")
root.mainloop()