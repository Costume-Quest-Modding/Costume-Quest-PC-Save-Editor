import tkinter as tk
from tkinter import ttk
import saveio
from widgets import Tooltip
from constants import (NAMES, COSTUME_DISPLAY_NAMES, COSTUME_OPTIONS)

class SummaryTab(ttk.Frame):
    def __init__(self, parent, battle_progress_text, cards_progress_text):
        super().__init__(parent)

        self.battle_progress_text = battle_progress_text
        self.cards_progress_text = cards_progress_text

        self._build_ui()

    def _build_ui(self):
        row = 0
        ttk.Label(self, text="Player Info").grid(
            row=0, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(self, text="World & Position").grid(
            row=0, column=2, sticky="w", padx=10, pady=5)
        ttk.Label(self, text="Apple Bobbing High Scores").grid(
            row=8, column=2, sticky="w", padx=10, pady=5)
        ttk.Label(self, text="Misc. Stats").grid(
            row=13, column=2, sticky="w", padx=10, pady=5)
        row += 1

        # ---------------------------------------------------------
        #  SECTION 1 — Player Info
        # ---------------------------------------------------------

        level_label = ttk.Label(self, text="Level:").grid(
            row=row, column=0, sticky="w", padx=25)
        level_label = ttk.Label(self, textvariable=saveio.AppState.level_var,
                                width=33)
        level_label.grid(row=row, column=1, sticky="w", padx=25, pady=5)
        Tooltip(level_label, "This is your character's current level.")
        row += 1

        xp_label = ttk.Label(self, text="XP:").grid(
            row=row, column=0, sticky="w", padx=25, pady=5)
        xp_label = ttk.Label(self, textvariable=saveio.AppState.xp_var,
                            width=33)
        xp_label.grid(row=row, column=1, padx=25, pady=5)
        Tooltip(xp_label, "This is your character's current XP.")
        row += 1

        candy_label = ttk.Label(self, text="Candy:").grid(
            row=row, column=0, sticky="w", padx=25)
        candy_label = ttk.Label(self, textvariable=saveio.AppState.candy_var,
                                width=33)
        candy_label.grid(row=row, column=1, padx=25, pady=5)
        Tooltip(candy_label, "This is your current amount of candy.")
        row += 1

        totalcandy_label = ttk.Label(self, text="Total Candy:").grid(
            row=row, column=0, sticky="w", padx=25)
        totalcandy_label = ttk.Label(self, textvariable=saveio.AppState.total_candy_var,
                                    width=33)
        totalcandy_label.grid(row=row, column=1, padx=25, pady=5)
        Tooltip(totalcandy_label,
                "This is your total amount of candy collected.\n"
                "Doesn't decrease when you spend candy, essentially tracking lifetime candy collection.")
        row += 1

        # ---------------------------------------------------------
        #  SECTION 2 — COLLECTION PROGRESS
        # ---------------------------------------------------------

        ttk.Label(self, text="Collections").grid(
            row=row, column=0, sticky="w", padx=10, pady=5)
        row += 1

        # Battle Stamps
        battlestamps_label = ttk.Label(self, text="Battle Stamps:").grid(
            row=row, column=0, sticky="w", padx=25, pady=5
        )
        battlestamps_label = ttk.Label(
            self, textvariable=self.battle_progress_text)
        battlestamps_label.grid(
            row=row, column=1, sticky="w", padx=25, pady=5
        )
        Tooltip(battlestamps_label,
                "Shows how many battle stamps you have collected.\n"
                "Hover over names in the Battle Stamps tab for stamp images.")
        row += 1

        # Cards
        cards_label = ttk.Label(self, text="Cards:").grid(
            row=row, column=0, sticky="w", padx=25, pady=5)
        
        cards_label = ttk.Label(self, textvariable=self.cards_progress_text)
        cards_label.grid(
            row=row, column=1, sticky="w", padx=25, pady=5)
        Tooltip(cards_label, "Shows how many cards you have collected.\n"
                "Hover over names in the Cards tab for card images.")
        row += 1

        ttk.Label(self, text="Costumes:").grid(
            row=row, column=0, sticky="w", padx=25, pady=5)
        row += 1

        ttk.Label(self, text="Equipped Costumes:").grid(
            row=row, column=0, padx=35, pady=5)

        saveio.AppState.costume_display_vars = [tk.StringVar() for _ in NAMES]
        for i, name in enumerate(NAMES):
            if not saveio.AppState.costume_vars[i].get():
                saveio.AppState.costume_vars[i].set(COSTUME_OPTIONS[i])
            display_name = COSTUME_DISPLAY_NAMES.get(
                saveio.AppState.costume_vars[i].get(),
                saveio.AppState.costume_vars[i].get())  # fallback to internal name
            saveio.AppState.costume_display_vars[i].set(f"{name}: {display_name}")
            lbl = ttk.Label(
                self, textvariable=saveio.AppState.costume_display_vars[i])
            lbl.grid(row=row, column=1, padx=25, pady=5, sticky="w")
            Tooltip(
                lbl, f"This shows the currently equipped costume for {name}.\nYou can change it in the Costumes tab.")
            saveio.AppState.costume_vars[i].trace_add(
                "write",
                lambda *args, idx=i, nm=name: saveio.AppState.costume_display_vars[idx].set(
                    f"{nm}: {COSTUME_DISPLAY_NAMES.get(saveio.AppState.costume_vars[idx].get(), saveio.AppState.costume_vars[idx].get())}"
                ),
            )
            row += 1

        # ---------------------------------------------------------
        #  SECTION 3 — WORLD & POSITION
        # ---------------------------------------------------------
        row = 1
        map_label = ttk.Label(self, text="World:").grid(
            row=row, column=2, sticky="w", padx=25)
        map_label = ttk.Label(self, textvariable=saveio.AppState.selected_world,
                            width=33)
        map_label.grid(row=row, column=3, padx=25)
        Tooltip(map_label, "This is the world you are currently in.")
        row += 1

        positions = [
            ("Player Position:", saveio.AppState.player_position_vars),
            ("Camera Position:", saveio.AppState.camera_position_vars)
        ]

        for label_text, vars_list in positions:
            ttk.Label(self, text=label_text).grid(
                row=row, column=2, sticky="w", padx=25, pady=5
            )
            for i, axis in enumerate(["X", "Y", "Z"]):
                ttk.Label(self, text=f"{axis}:").grid(
                    row=row + i, column=3, sticky="w", padx=25, pady=5
                )
                value_label = ttk.Label(
                    self, textvariable=vars_list[i], width=15)
                value_label.grid(
                    row=row + i, column=3, sticky="w", padx=40, pady=5
                )
                Tooltip(
                    value_label,
                    f"{label_text} {axis}-coordinate in the world.\n"
                    "Changes if you move the player in-game or via teleport.\n"
                    "Camera position does nothing in the save file and is likely unused."
                )
            row += 3  # move row counter past this block

        # ---------------------------------------------------------
        #  SECTION 4 — MISC. STATS
        # ---------------------------------------------------------
        bobbing_stats = [
            ("Suburbs:", saveio.AppState.suburbsbobbing_var),
            ("Autumn Haven Mall:", saveio.AppState.mallbobbing_var),
            ("Fall Valley:", saveio.AppState.countrybobbing_var)
        ]
        row = 9
        for label_text, var in bobbing_stats:
            ttk.Label(self, text=label_text).grid(
                row=row, column=2, sticky="w", padx=25, pady=5)
            ttk.Label(self, textvariable=var, width=33, anchor="w").grid(
                row=row, column=3, sticky="w", padx=25, pady=5)
            row += 1

        misc_stats = [
            ("Robot Ramp Jumps:", saveio.AppState.robotjumps_var),
            ("Monster Pail Bashes:", saveio.AppState.monsterbashes_var),
        ]
        row = 14
        for label_text, var in misc_stats:
            ttk.Label(self, text=label_text).grid(
                row=row, column=2, sticky="w", padx=25, pady=5)
            ttk.Label(self, textvariable=var, width=33, anchor="w").grid(
                row=row, column=3, sticky="w", padx=25, pady=5)
            row += 1