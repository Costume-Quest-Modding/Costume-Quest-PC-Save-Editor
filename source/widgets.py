import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

# Creates a editor for vectors (PlayerPosition and CameraPosition)
def create_vector_editor(parent, label_text, variables, state="normal"):
    frame = ttk.Frame(parent)
    frame.columnconfigure(1, weight=1)
    ttk.Label(frame, text=label_text).grid(row=0, column=0, sticky="w")
    for i, (axis, var) in enumerate(zip(["X", "Y", "Z"], variables)):
        ttk.Label(frame, text=f"{axis}:").grid(
            row=i + 1, column=1, padx=10, pady=2)
        if state == "readonly":  # use label instead of entry
            ttk.Label(frame, textvariable=var).grid(
                row=i + 1, column=2, padx=10, pady=2, sticky="w")
        else:  # normal editable entry
            ttk.Entry(frame, textvariable=var, state=state).grid(
                row=i + 1, column=2, padx=10, pady=2, sticky="w")
    return frame

# Simple text tooltip for any widget
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + 10
        y = self.widget.winfo_rooty() + 10
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify="left",
                         background="#ffffe0", relief="solid", borderwidth=1,
                         font=("Segoe UI", 9))
        label.pack(ipadx=4, ipady=2)

    def hide(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

class ImageTooltip:
    """
    Tooltip for showing images (cards or battle stamps) on hover.
    Automatically scales 64x64 stamps to 128x128 for better visibility.
    Keeps pixel art crisp using Image.NEAREST.
    """

    def __init__(self, widget, img_path):
        self.widget = widget
        self.img_path = img_path
        self.tip_window = None
        self.photo = None

        widget.bind("<Enter>", self._show_tooltip)
        widget.bind("<Leave>", self._hide_tooltip)

    def _show_tooltip(self, event=None):
        if self.tip_window:
            return

        if not self.img_path or not os.path.isfile(self.img_path):
            return

        # Load image
        img = Image.open(self.img_path)
        w, h = img.size

        self.photo = ImageTk.PhotoImage(img)

        # Create tooltip window
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)


        bg = "#9b9b9b"
        tw.configure(bg=bg)
        x = self.widget.winfo_pointerx() + 10
        y = self.widget.winfo_pointery() + 10
        tw.wm_geometry(f"+{x}+{y}")

        # Display image
        lbl = tk.Label(tw, image=self.photo,
                       borderwidth=0, highlightthickness=0)
        lbl.pack()

    def _hide_tooltip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None