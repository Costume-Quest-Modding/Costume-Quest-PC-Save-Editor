import os
import saveio
from tabs.stamps import BattleStampsTab
from tabs.cards import CardsTab
from tabs.quests import QuestsTab
from tabs.costumes import CostumesTab
from tabs.stats import StatsTab
from tabs.summary import SummaryTab
from state import AppState
import tkinter as tk
from tkinter import ttk, messagebox
from widgets import Tooltip, ImageTooltip, create_vector_editor
from constants import (
    NAMES, COSTUME_OPTIONS, COSTUME_DISPLAY_NAMES,
    WORLD_PATHS, DEBUG_TELEPORTS, QUESTS
)

# ---------- UI builder ----------


def create_menu(root, frames_refs):
    def make_menu(parent):
        return tk.Menu(parent, tearoff=0)

    menu_bar = make_menu(root)

    file_menu = make_menu(menu_bar)
    file_menu.add_command(
        label="Open", command=lambda: _open_and_fill(root, frames_refs))
    file_menu.add_command(label="Save", command=lambda: saveio.save_changes(
        saveio.AppState, frames_refs["Cards"].entries, frames_refs["Battle Stamps"].entries))
    file_menu.add_command(label="Save As...", command=lambda: saveio.save_as(
        saveio.AppState, frames_refs["Cards"].entries, frames_refs["Battle Stamps"].entries))
    file_menu.add_command(label="Backup Save File", command=saveio.backup_save)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    help_menu = make_menu(menu_bar)
    help_menu.add_command(
        label="How to Use",
        command=lambda: messagebox.showinfo(
            "How to Use",
            "=== Costume Quest Save Editor Help ===\n\n"
            "Navigation:\n"
            " - Use the main tabs to access different sections (Summary, Battle Stamps, Cards, etc.).\n"
            " - Click on entries or dropdowns to edit your save file values.\n\n"
            "File Menu:\n"
            " - Open: Load a Costume Quest save file.\n"
            " - Save: Save changes to the current file.\n"
            " - Save As...: Save to a new file location (.json or .txt allowed).\n"
            " - Backup Save File: Make a backup of your current save.\n\n"
            "Tips:\n"
            " - Hover over labels for more info (tooltips).\n"
            " - Ensure you save changes before closing the editor."
        )
    )
    help_menu.add_command(
        label="About",
        command=lambda: messagebox.showinfo(
            "About",
            "Costume Quest PC Save Editor - Alpha Version 1.2\n"
            "Made by: DeathMaster001\n\n"
            "A save editor for Costume Quest (PC/Steam).\n"
            "Edit player stats, costumes, quests, cards, battle stamps, and more."
        )
    )
    menu_bar.add_cascade(label="Help", menu=help_menu)

    root.config(menu=menu_bar)


def _open_and_fill(root, frames_refs):
    ok = saveio.open_save_dialog()
    if not ok:
        return

    saveio.populate_entries_from_state(
        frames_refs["Cards"].entries, frames_refs["Battle Stamps"].entries)
    if hasattr(frames_refs["Battle Stamps"], "update_progress"):
        frames_refs["Battle Stamps"].update_progress()
    if hasattr(root, "_tracker_win") and root._tracker_win and root._tracker_win.winfo_exists():
        if hasattr(root._tracker_win, "update_applebobbing_progress"):
            root._tracker_win.update_applebobbing_progress()
    
    messagebox.showinfo(
        "Costume Quest Save Loaded",
        "Save file loaded successfully."
    )


def create_tabs(root):
    notebook = ttk.Notebook(root)

    #Shared progress variables
    battle_progress_text = tk.StringVar(value="0 / 0 (0%)")
    cards_progress_text = tk.StringVar(value="0 / 0 (0%)")

    frames = {}

    # Create SummaryTab instance
    summary_frame = SummaryTab(
        notebook,
        battle_progress_text = battle_progress_text,
        cards_progress_text = cards_progress_text
    )
    frames["Summary"] = summary_frame

    # Create BattleStampsTab instance
    battlestamps_frame = BattleStampsTab(
        notebook,
        progress_text_var = battle_progress_text
    )
    frames["Battle Stamps"] = battlestamps_frame

    # Create CardsTab instance
    cards_frame = CardsTab(
        notebook,
        progress_text_var=cards_progress_text
    )
    frames["Cards"] = cards_frame

    # Create CostumesTab instance
    progress_var = tk.StringVar(value="0 / 0 (0%)")
    costumes_frame = CostumesTab(
        notebook,
        progress_var
    )
    frames["Costumes"] = costumes_frame

    # Create StatsTab instance
    stats_frame = StatsTab(notebook)
    frames["Stats & World"] = stats_frame

    # Create QuestsTab instance
    quests_frame = QuestsTab(notebook)
    frames["Quests"] = quests_frame

    # Add tabs in the desired order
    notebook.add(frames["Summary"], text="Summary")
    notebook.add(frames["Battle Stamps"], text="Battle Stamps")
    notebook.add(frames["Cards"], text="Cards")
    notebook.add(frames["Costumes"], text="Costumes")
    notebook.add(frames["Stats & World"], text="Stats & World")
    notebook.add(frames["Quests"], text="Quests")

    return notebook, frames