import os
import tkinter as tk
from tkinter import ttk
from widgets import ImageTooltip
from constants import (BATTLE_ITEM_NAMES, BATTLE_STAMP_IMAGES)

class BattleStampsTab(ttk.Frame):
    def __init__(self, parent, progress_text_var=None):
        super().__init__(parent)
        self.entries = {}
        self.toggle_all_var = tk.IntVar()
        self.progress_text = progress_text_var
        self.missing_stamps_var = tk.StringVar(value="All")

        self._build_ui()
        self.update_progress()
        self.update_missing_stamps()

    def _build_ui(self):
        # Header row
        ttk.Label(self, text="Battle Stamps").grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )
        ttk.Checkbutton(
            self, text="Toggle All", variable=self.toggle_all_var,
            command=self.toggle_all_stamps
        ).grid(row=0, column=1, padx=2, pady=5)

        ttk.Label(self, textvariable=self.progress_text).grid(
            row=0, column=2, padx=10, pady=5, sticky="w"
        )

        # Stamp entries grid
        items_per_col = 9
        start_row = 1
        for i, (stamp_num, name) in enumerate(BATTLE_ITEM_NAMES.items()):
            row = start_row + (i % items_per_col)
            col = (i // items_per_col) * 2

            lbl = ttk.Label(self, text=name)
            lbl.grid(row=row, column=col, sticky='w', padx=10, pady=2)

            # Image tooltip
            img_path = BATTLE_STAMP_IMAGES.get(stamp_num)
            if img_path and os.path.isfile(img_path):
                ImageTooltip(lbl, img_path)

            entry = tk.Entry(self, width=8)
            entry.grid(row=row, column=col + 1, sticky='w', padx=5, pady=2)
            entry.bind("<KeyRelease>", lambda e: [
                       self.update_progress(), self.update_missing_stamps()])
            self.entries[stamp_num] = entry

        # Missing stamps section
        last_row = start_row + (len(BATTLE_ITEM_NAMES) //
                                items_per_col + 1) * items_per_col
        missing_frame = ttk.Frame(self)
        missing_frame.grid(row=last_row, column=0, columnspan=10, sticky="ew")
        missing_frame.columnconfigure(1, weight=1)

        ttk.Label(missing_frame, text="Missing Stamps:").grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )
        ttk.Label(missing_frame, textvariable=self.missing_stamps_var, anchor="w", wraplength=400).grid(
            row=0, column=1, sticky="ew", padx=10, pady=5
        )

        # Auto-wrap
        self.bind("<Configure>", self._update_wrap)

    def _update_wrap(self, event=None):
        width = self.winfo_width()
        if width > 150:
            # Only one missing stamps label exists
            self.children.get(list(self.children.keys())[-1]).children.get(list(self.children.get(
                list(self.children.keys())[-1]).children.keys())[1]).config(wraplength=width - 150)

    def update_progress(self):
        total = len(self.entries)
        collected = sum(
            1 for e in self.entries.values() if e.get().strip().isdigit() and int(e.get().strip()) > 0
        )
        percent = (collected / total) * 100 if total > 0 else 0
        if self.progress_text:
            self.progress_text.set(
                f"{collected} / {total} ({percent:.0f}%)")

    def update_missing_stamps(self):
        missing = [
            BATTLE_ITEM_NAMES.get(num, f"Stamp {num}") for num, e in self.entries.items()
            if not e.get().strip() or e.get().strip() == "0"
        ]
        if all(not e.get().strip() or e.get().strip() == "0" for e in self.entries.values()):
            self.missing_stamps_var.set("All")
        elif all(e.get().strip() and int(e.get().strip()) > 0 for e in self.entries.values()):
            self.missing_stamps_var.set("None")
        else:
            self.missing_stamps_var.set(", ".join(missing))

    def toggle_all_stamps(self):
        val = "1" if self.toggle_all_var.get() else "0"
        for e in self.entries.values():
            e.delete(0, tk.END)
            e.insert(0, val)
        self.update_progress()
        self.update_missing_stamps()