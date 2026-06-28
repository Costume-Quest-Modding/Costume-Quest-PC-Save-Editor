import tkinter as tk
from tkinter import ttk
import saveio
from widgets import create_vector_editor
from constants import (WORLD_PATHS, DEBUG_TELEPORTS)

class StatsTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self._build_ui()

    def _build_ui(self):

    # ---------- Stats & World Frame ----------
        row = 0
        ttk.Label(self, text="Stats").grid(
            row=row, column=0, sticky="w", padx=10, pady=5)
        row += 1

        ttk.Label(self, text="Level:").grid(
            row=row, column=0, sticky="w", padx=25, pady=5)
        level_dropdown = ttk.Combobox(
            self,
            textvariable=saveio.AppState.level_var,
            values=[str(i) for i in range(1, 11)],
            width=31,
            state="readonly",
        )
        level_dropdown.grid(row=row, column=1, sticky="w", padx=25, pady=5)

        for event in ("<<ComboboxSelected>>", "<FocusOut>", "<Return>"):
            level_dropdown.bind(event, saveio.update_xp_from_level)
        row += 1

        ttk.Label(self, text="XP:").grid(
            row=row, column=0, sticky="w", padx=25, pady=5)
        ttk.Entry(self, textvariable=saveio.AppState.xp_var, width=33).grid(
            row=row, column=1, padx=25, pady=5, sticky="w")
        row += 1

        ttk.Label(self, text="Candy:").grid(
            row=row, column=0, sticky="w", padx=25, pady=5)
        ttk.Entry(self, textvariable=saveio.AppState.candy_var, width=33).grid(
            row=row, column=1, padx=25, pady=5, sticky="w")
        row += 2

        ttk.Label(self, text="World, Location and Position").grid(
            row=row, column=0, padx=10, pady=5, sticky="w")
        row += 1
        ttk.Label(self, text="World:").grid(
            row=row, column=0, padx=25, pady=5, sticky="w")
        ttk.Combobox(self, textvariable=saveio.AppState.selected_world, values=list(
            WORLD_PATHS.keys()), width=31, state="readonly").grid(row=row, column=1, padx=25, pady=5, sticky="w")
        row += 1

        # Location dropdown variable
        location_var = tk.StringVar(value="")  # initially empty

        ttk.Label(self, text="Location:").grid(
            row=row, column=0, padx=25, pady=5, sticky="w")
        location_cb = ttk.Combobox(
            self, textvariable=location_var, values=[], width=31, state="readonly")
        location_cb.grid(row=row, column=1, padx=25, pady=5, sticky="w")
        row += 1

        def update_locations(*args):
            world = saveio.AppState.selected_world.get()
            if world in DEBUG_TELEPORTS:
                location_cb["values"] = list(DEBUG_TELEPORTS[world].keys())
                location_var.set("")  # reset selection
            else:
                location_cb["values"] = []
                location_var.set("")

        saveio.AppState.selected_world.trace_add("write", update_locations)

        def teleport_to_location(*args):
            world = saveio.AppState.selected_world.get()
            location = location_var.get()
            if world in DEBUG_TELEPORTS and location in DEBUG_TELEPORTS[world]:
                x, y, z = DEBUG_TELEPORTS[world][location]
                vars = saveio.AppState.player_position_vars
                vars[0].set(x)
                vars[1].set(y)
                vars[2].set(z)

        location_var.trace_add("write", teleport_to_location)

        player_position_frame2 = create_vector_editor(
            self, "Player Position:", saveio.AppState.player_position_vars)
        player_position_frame2.grid(
            row=row, column=0, columnspan=2, sticky="w", padx=25, pady=5)
        row += 1

        camera_position_frame2 = create_vector_editor(
            self, "Camera Position:", saveio.AppState.camera_position_vars)
        camera_position_frame2.grid(
            row=row, column=0, columnspan=2, sticky="w", padx=25, pady=5)