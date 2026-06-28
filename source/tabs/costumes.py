import tkinter as tk
from tkinter import ttk
import saveio
from constants import (COSTUME_OPTIONS, NAMES)

class CostumesTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self._build_ui()

    def _build_ui(self):

    # ---------- Costumes Frame ----------
        row = 0

        ttk.Label(self, text="Costumes").grid(
            row=row, column=0, padx=10, pady=5, sticky="w")
        # Card entries grid
        costumes_per_col = 5
        start_row = 0
        for i, name in enumerate(COSTUME_OPTIONS):
            col = (i // costumes_per_col)
            row = start_row + (i % costumes_per_col)

            ttk.Checkbutton(
                self,
                text=name,
                width=15
            ).grid(row=row, column=col + 1, sticky="w", padx=10, pady=5)

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