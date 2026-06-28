import tkinter as tk
from tkinter import ttk
import saveio
from constants import (COSTUME_OPTIONS, NAMES)

class CostumesTab(ttk.Frame):
    def __init__(self, parent, progress_text_var=None):
        super().__init__(parent)

        self.entries = {}
        self.toggle_all_var = tk.StringVar(value="0")
        self.missing_costumes_var = tk.StringVar(value="All")
        self.progress_text = progress_text_var

        self._build_ui()
        self.toggle_all_costumes()
        self.update_progress()
        self.update_missing_costumes()

    def _build_ui(self):
        row = 0

        ttk.Label(self, text="Costumes").grid(
            row=row, column=0, padx=10, pady=5, sticky="w")
        ttk.Checkbutton(self, text="Toggle All", variable=self.toggle_all_var,
                        command=self.toggle_all_costumes).grid(row=row, column=1, sticky="w", padx=10, pady=5)
        ttk.Label(self, textvariable=self.progress_text).grid(
            row=0, column=2, padx=10, pady=5, sticky="w")
        # Card entries grid
        costumes_per_col = 5
        start_row = 1
        for i, name in enumerate(COSTUME_OPTIONS):
            col = (i // costumes_per_col)
            row = start_row + (i % costumes_per_col)

            var = tk.StringVar(value="0")
            var.trace_add("write", lambda *args: self.on_change())
            ttk.Checkbutton(
                self,
                text=name,
                variable=var,
                onvalue="1",
                offvalue="0",
                width=15
            ).grid(row=row, column=col + 1, sticky="w", padx=10, pady=5)
        
            self.entries[name] = var

        row += 6

        ttk.Label(self, text="Costume Pieces").grid(
            row=row, column=0, padx=10, pady=5, sticky="w")
        row += 1

        ttk.Label(self, text="Equipped Costumes").grid(
            row=row, column=0, padx=10, pady=5, sticky="w")

        for i, name in enumerate(NAMES):
            ttk.Label(self, text=name).grid(
                row=row, column=1, padx=10, pady=5)

            ttk.Combobox(
                self,
                textvariable=saveio.AppState.costume_vars[i],
                values=COSTUME_OPTIONS,
                width=15
            ).grid(row=row, column=2, sticky="w", padx=10, pady=5)
            row += 1

    def update_missing_costumes(self):
        owned = {
            name for name, var in self.entries.items()
            if var.get() == "1"
        }

        if not owned:
            self.missing_costumes_var.set("All")
        elif len(owned) == len(COSTUME_OPTIONS):
            self.missing_costumes_var.set("None")
        else:
            missing = [c for c in COSTUME_OPTIONS if c not in owned]
            self.missing_costumes_var.set(", ".join(missing))

    def toggle_all_costumes(self):
        val = self.toggle_all_var.get()

        for var in self.entries.values():
            var.set(val)

        self.update_progress()
        self.update_missing_costumes()

    def update_progress(self):
        total = len(self.entries)
        collected = sum(1 for var in self.entries.values() if var.get() == "1")
        percent = (collected / total) * 100 if total > 0 else 0
        self.progress_text.set(f"{collected} / {total} ({percent:.0f}%)")
        
    def on_change(self, event=None):
        self.update_progress()
        self.update_missing_costumes()