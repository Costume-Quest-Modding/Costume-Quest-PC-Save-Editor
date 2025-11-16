# main.py
import os
import saveio
import ui
from ttkthemes import ThemedTk


def main():
    root = ThemedTk(theme="winxpblue")
    root.title("Costume Quest PC Save Editor")
    root.geometry("800x650")
    root.minsize(800, 650)

    # initialize Tk variables inside AppState
    saveio.AppState.init_vars(root)

    # build UI tabs + frames
    notebook, frames_map = ui.create_tabs(root)
    notebook.pack(fill="both", expand=True)

    # menu needs access to frames map so save/load can use their entries
    ui.create_menu(root, frames_map)

    # apply default theme
    ui.apply_theme(root, "light")

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
