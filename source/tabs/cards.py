import os
import tkinter as tk
from tkinter import ttk
from widgets import ImageTooltip
from constants import (CARD_NAMES, CARD_IMAGES)

CARD_IDS = range(1, 55)

class CardsTab(ttk.Frame):
    def __init__(self, parent, progress_text_var=None):
        super().__init__(parent)
        self.entries = {}
        self.toggle_all_var = tk.IntVar()
        self.progress_text = progress_text_var
        self.missing_cards_var = tk.StringVar(value="All")

        self._build_ui()
        self.update_progress()
        self.update_missing_cards()
    
    def on_change(self, event=None):
        self.update_progress()
        self.update_missing_cards()
    
    def is_collected(self, entry):
        value = entry.get().strip()
        return value.isdigit() and int(value) > 0

    def _build_ui(self):
        # Header row
        ttk.Label(self, text="Creepy Treat Cards").grid(
            row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Checkbutton(self, text="Toggle All", variable=self.toggle_all_var,
                        command=self.toggle_all_cards).grid(row=0, column=1, padx=2, pady=5)
        ttk.Label(self, textvariable=self.progress_text).grid(
            row=0, column=2, padx=10, pady=5, sticky="w")

        # Card entries grid
        cards_per_col = 18
        start_row = 1
        for i, card_num in enumerate(CARD_IDS):
            col = (i // cards_per_col) * 2
            row = start_row + (i % cards_per_col)

            card_name = CARD_NAMES.get(card_num, f"Card {card_num}")
            img_path = CARD_IMAGES.get(card_num)

            lbl = ttk.Label(self, text=card_name)
            lbl.grid(row=row, column=col, sticky='w', padx=10, pady=2)
    
            if img_path and os.path.isfile(img_path):
                self._attach_image_tooltip(lbl, img_path)

            entry = tk.Entry(self, width=8)
            entry.grid(row=row, column=col + 1, sticky='w', padx=5, pady=2)
            entry.bind("<KeyRelease>", self.on_change)

            self.entries[card_num] = entry

        # Missing cards section
        last_row = start_row + cards_per_col * \
            ((len(CARD_IDS) + cards_per_col - 1) // cards_per_col)
        missing_frame = ttk.Frame(self)
        missing_frame.grid(row=last_row, column=0, columnspan=10, sticky="ew")
        missing_frame.columnconfigure(1, weight=1)

        ttk.Label(missing_frame, text="Missing Cards:").grid(
            row=0, column=0, padx=10, pady=5, sticky="w")
        self.missing_cards_label = ttk.Label(
            missing_frame,
            textvariable=self.missing_cards_var,
            anchor="w",
            wraplength=400
        )
        self.missing_cards_label.grid(
            row=0, column=1, sticky="ew", padx=10, pady=5
)

        # Auto-wrap
        self.bind("<Configure>", self._update_wrap)
    
    def reload_cards(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.entries.clear()
        self._build_ui()
        self.update_progress()
        self.update_missing_cards()

    def _attach_image_tooltip(self, widget, img_path):
        """Attach an image tooltip (like your ImageTooltip)"""
        ImageTooltip(widget, img_path)

    def _update_wrap(self, event=None):
        width = self.winfo_width()
        if width > 150:
            self.missing_cards_label.config(wraplength=width - 150)

    def update_progress(self):
        total = len(self.entries)
        collected = sum(1 for e in self.entries.values() if self.is_collected(e))
        percent = (collected / total) * 100 if total > 0 else 0
        self.progress_text.set(
            f"{collected} / {total} ({percent:.0f}%)")

    def update_missing_cards(self):
        missing = [CARD_NAMES.get(num, f"Card {num}")
            for num, e in self.entries.items()
            if not self.is_collected(e)
        ]
        if all(not e.get().strip() or e.get().strip() == "0" for e in self.entries.values()):
            self.missing_cards_var.set("All")
        elif all(e.get().strip() and int(e.get().strip()) > 0 for e in self.entries.values()):
            self.missing_cards_var.set("None")
        else:
            self.missing_cards_var.set(", ".join(missing))

    def toggle_all_cards(self):
        val = "1" if self.toggle_all_var.get() else "0"
        for e in self.entries.values():
            e.delete(0, tk.END)
            e.insert(0, val)
        self.update_progress()
        self.update_missing_cards()