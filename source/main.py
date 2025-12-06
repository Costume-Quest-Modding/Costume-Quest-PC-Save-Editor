# main.py
import os
import saveio
import ui
import tkinter as tk
from tkinter import ttk


def main():
    # Create main window with a default ttk theme
    root = tk.Tk()
    root.title("Costume Quest PC Save Editor")
    root.geometry("800x600")
    root.minsize(800, 600)

    style = ttk.Style()
    style.theme_use('clam')

    # initialize Tk variables inside AppState
    saveio.AppState.init_vars(root)

    # build UI tabs + frames
    notebook, frames_map = ui.create_tabs(root)
    notebook.pack(fill="both", expand=True)

    # menu needs access to frames map so save/load can use their entries
    ui.create_menu(root, frames_map)

    # set icon if available
    import constants
    icon_path = os.path.join(constants.BASE_DIR, "icon.ico")
    if os.path.exists(icon_path):
        try:
            root.iconbitmap(icon_path)
        except Exception:
            pass

    root.mainloop()


if __name__ == "__main__":
    main()
