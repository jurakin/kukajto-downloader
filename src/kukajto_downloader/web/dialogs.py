# borrowed from https://github.com/brentvollebregt/auto-py-to-exe/blob/master/auto_py_to_exe/dialogs.py

import sys
try:
    from tkinter import Tk
except ImportError:
    try:
        from Tkinter import Tk
    except ImportError:
        # If no versions of tkinter exist (most likely linux) provide a message
        if sys.version_info.major < 3:
            print("Error: Tkinter not found")
            print('For linux, you can install Tkinter by executing: "sudo apt-get install python-tk"')
            sys.exit(1)
        else:
            print("Error: tkinter not found")
            print('For linux, you can install tkinter by executing: "sudo apt-get install python3-tk"')
            sys.exit(1)
try:
    from tkinter.filedialog import asksaveasfilename
except ImportError:
    from tkFileDialog import asksaveasfilename


def ask_file_save_location(title=None):
    """ Ask the user where to save a file """
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    file_types = [('All files', '*')]
    file_path = asksaveasfilename(parent=root, filetypes=file_types, title=title)
    root.update()

    if bool(file_path):
        return file_path
    else:
        return None