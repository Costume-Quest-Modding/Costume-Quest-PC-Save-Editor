import tkinter as tk
from tkinter import ttk
from .. import saveio
from ..widgets import create_vector_editor
from ..constants import (BATTLE_ITEM_NAMES, COSTUME_OPTIONS, NAMES, WORLD_PATHS, DEBUG_TELEPORTS)

class StatsTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self._build_ui()

    def _build_ui(self):
        # Left side: existing Stats and World controls
        left_frame = ttk.Frame(self)
        left_frame.grid(row=0, column=0, sticky="nw")

        # Right side: Equips
        equips_frame = ttk.Frame(self)
        equips_frame.grid(row=0, column=1, sticky="nw", padx=20)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        row = 0

        ttk.Label(left_frame, text="Stats").grid(
            row=row, column=0, sticky="w", padx=10, pady=5)
        row += 1

        ttk.Separator(left_frame, orient="horizontal").grid(
            row=row, column=0, columnspan=2, sticky="ew", padx=10, pady=5
        )
        row += 1

        for col in range(20):
            left_frame.columnconfigure(col, weight=0)

        left_frame.columnconfigure(1, weight=1)

        ttk.Label(left_frame, text="Level:").grid(
            row=row, column=0, sticky="w", padx=25, pady=5)
        level_dropdown = ttk.Combobox(
            left_frame,
            textvariable=saveio.AppState.level_var,
            values=[str(i) for i in range(1, 11)],
            width=25,
            state="readonly",
        )
        level_dropdown.grid(row=row, column=1, sticky="w", padx=25, pady=5)

        for event in ("<<ComboboxSelected>>", "<FocusOut>", "<Return>"):
            level_dropdown.bind(event, saveio.update_xp_from_level)
        row += 1

        ttk.Label(left_frame, text="XP:").grid(
            row=row, column=0, sticky="w", padx=25, pady=5)
        ttk.Entry(left_frame, textvariable=saveio.AppState.xp_var, width=25).grid(
            row=row, column=1, padx=25, pady=5, sticky="w")
        row += 1

        ttk.Label(left_frame, text="Candy:").grid(
            row=row, column=0, sticky="w", padx=25, pady=5)
        ttk.Entry(left_frame, textvariable=saveio.AppState.candy_var, width=25).grid(
            row=row, column=1, padx=25, pady=5, sticky="w")
        row += 2

        ttk.Label(left_frame, text="World Info").grid(
            row=row, column=0, padx=10, pady=5, sticky="w")
        row += 1

        ttk.Separator(left_frame, orient="horizontal").grid(
            row=row, column=0, columnspan=2, sticky="ew", padx=10, pady=5
        )
        row += 1

        ttk.Label(left_frame, text="World:").grid(
            row=row, column=0, padx=25, pady=5, sticky="w")
        ttk.Combobox(left_frame, textvariable=saveio.AppState.selected_world, values=list(
            WORLD_PATHS.keys()), width=25, state="readonly").grid(row=row, column=1, padx=25, pady=5, sticky="w")
        row += 1

        # Location dropdown variable
        location_var = tk.StringVar(value="")  # initially empty

        ttk.Label(left_frame, text="Location:").grid(
            row=row, column=0, padx=25, pady=5, sticky="w")
        location_cb = ttk.Combobox(
            left_frame, textvariable=location_var, values=[], width=25, state="readonly")
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
            left_frame, "Player Position:", saveio.AppState.player_position_vars)
        player_position_frame2.grid(
            row=row, column=0, columnspan=2, sticky="w", padx=25, pady=5)
        row += 1

        camera_position_frame2 = create_vector_editor(
            left_frame, "Camera Position:", saveio.AppState.camera_position_vars)
        camera_position_frame2.grid(
            row=row, column=0, columnspan=2, sticky="w", padx=25, pady=5)

        # Equips section
        ttk.Label(equips_frame, text="Equipment").grid(
            row=0, column=0, sticky="w", padx=10, pady=5
        )

        ttk.Separator(equips_frame, orient="horizontal").grid(
            row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=5
        )

        ttk.Label(equips_frame, text="Costumes:").grid(
            row=2, column=0, columnspan=2, padx=25, pady=5, sticky="w"
        )

        row = 3

        for i, name in enumerate(NAMES):
            ttk.Label(equips_frame, text=name).grid(
                row=row, column=0, padx=50, pady=5, sticky="w"
            )

            ttk.Combobox(
                equips_frame,
                textvariable=saveio.AppState.costume_vars[i],
                values=COSTUME_OPTIONS,
                width=30
            ).grid(row=row, column=1, sticky="w", padx=10, pady=5)

            row += 1

        ttk.Label(equips_frame, text="Battle Stamps:").grid(
            row=row, column=0, columnspan=2, padx=25, pady=5, sticky="w"
        )
        row += 1

        saveio.AppState.stamp_dropdowns = []

        for i, name in enumerate(NAMES):
            ttk.Label(equips_frame, text=name).grid(
                row=row, column=0, padx=50, pady=5, sticky="w"
            )

            dropdown = ttk.Combobox(
                equips_frame,
                textvariable=saveio.AppState.stamp_vars[i],
                values=["None"] + list(BATTLE_ITEM_NAMES.values()),
                width=30
            )
            dropdown.grid(row=row, column=1, sticky="w", padx=10, pady=5)

            saveio.AppState.stamp_dropdowns.append(dropdown)

            row += 1

        equips_frame.columnconfigure(0, weight=1)
        equips_frame.columnconfigure(2, weight=1)