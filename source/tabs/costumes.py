import os
import tkinter as tk
from tkinter import ttk
import saveio
from widgets import ImageTooltip
from constants import (COSTUME_DISPLAY_NAMES, COSTUME_IMAGES, COSTUME_OPTIONS, NAMES)

class CostumesTab(ttk.Frame):
    def __init__(self, parent, progress_text_var=None):
        super().__init__(parent)
        self.entries = {}
        self.image_tooltips = []
        self.toggle_all_var = tk.StringVar(value="0")
        self.progress_text = progress_text_var
        self.missing_costumes_var = tk.StringVar(value="All")

        self._build_ui()
        self.toggle_all_costumes()
        self.update_progress()
        self.update_missing_costumes()

    def _build_ui(self):
        row = 0

        ttk.Label(self, text="Costumes").grid(
            row=row, column=0, padx=10, pady=5, sticky="w"
        )
        
        ttk.Checkbutton(self, text="Toggle All", variable=self.toggle_all_var, command=self.toggle_all_costumes).grid(
            row=row, column=1, padx=10, pady=5, sticky="w"
        )
        
        ttk.Label(self, textvariable=self.progress_text).grid(
            row=0, column=2, padx=10, pady=5, sticky="w"
        )

        ttk.Separator(self, orient="horizontal").grid(
            row=1, column=0, columnspan=10, sticky="ew", padx=10, pady=5
        )

        # Costume entries grid
        costumes_per_col = 3
        start_row = 2

        # Keep stamp names and entries together
        # Let unused horizontal space remain at the right
        for col in range(20):
            self.columnconfigure(col, weight=0)

        self.columnconfigure(9, weight=1)

        for i, (costume_num, name) in enumerate(COSTUME_DISPLAY_NAMES.items()):
            col = (i // costumes_per_col)
            row = start_row + (i % costumes_per_col)

            var = tk.StringVar(value="0")
            var.trace_add("write", lambda *args: self.on_change())

            check = ttk.Checkbutton(
                self,
                text=name,
                variable=var,
                onvalue="1",
                offvalue="0",
                width=15
            )
            check.grid(row=row, column=col, sticky="w", padx=10, pady=5)
            
        
            # Image tooltip
            img_path = COSTUME_IMAGES.get(costume_num)

            if img_path and os.path.isfile(img_path):
                tooltip = ImageTooltip(check, img_path)
                self.image_tooltips.append(tooltip)

            self.entries[costume_num] = var

        row += 6

        ttk.Separator(self, orient="horizontal").grid(
            row=row, column=0, columnspan=10, sticky="ew", padx=10, pady=5
        )
        row += 1

        ttk.Label(self, text="Costume Pieces").grid(
            row=row, column=0, padx=10, pady=5, sticky="w")
        row += 1

    # Missing costumes section
        ttk.Separator(self, orient="horizontal").grid(
            row=row, column=0, columnspan=10, sticky="ew", padx=10, pady=5
        )
        row += 1

        missing_frame = ttk.Frame(self)
        missing_frame.grid(
            row=row, column=0, columnspan=10, sticky="ew"
        )
        missing_frame.columnconfigure(1, weight=1)

        ttk.Label(missing_frame, text="Missing Costumes:").grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )

        self.missing_costumes_label = ttk.Label(
            missing_frame,
            textvariable=self.missing_costumes_var,
            anchor="w",
            wraplength=400
        )
        self.missing_costumes_label.grid(
            row=0, column=1, sticky="ew", padx=10, pady=5
        )

        # Auto-wrap
        self.bind("<Configure>", self._update_wrap)

    def _update_wrap(self, event=None):
        width = self.winfo_width()
        if width > 150:
            self.missing_costumes_label.configure(
                wraplength=width - 150
            )

    def update_missing_costumes(self):
        owned = {
            costume_num
            for costume_num, var in self.entries.items()
            if var.get() == "1"
        }

        if not owned:
            self.missing_costumes_var.set("All")
        elif len(owned) == len(self.entries):
            self.missing_costumes_var.set("None")
        else:
            missing = [
                name
                for costume_num, name in COSTUME_DISPLAY_NAMES.items()
                if costume_num not in owned
            ]
            self.missing_costumes_var.set(", ".join(missing))

    def toggle_all_costumes(self):
        val = self.toggle_all_var.get()

        for var in self.entries.values():
            var.set(val)

        self.on_change()

    def update_progress(self):
        total = len(self.entries)
        collected = sum(1 for var in self.entries.values() if var.get() == "1")
        percent = (collected / total) * 100 if total > 0 else 0
        self.progress_text.set(f"{collected} / {total} ({percent:.0f}%)")
        
    def on_change(self, event=None):
        self.update_progress()
        self.update_missing_costumes()