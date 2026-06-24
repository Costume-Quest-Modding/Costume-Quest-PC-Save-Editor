import os
import saveio
from tabs.stamps import BattleStampsTab
from tabs.cards import CardsTab
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
    frames = {
        "Summary": ttk.Frame(notebook),
        "Stats & World": ttk.Frame(notebook),
        "Battle Stamps": ttk.Frame(notebook),
        "Costumes": ttk.Frame(notebook),
        "Quests": ttk.Frame(notebook),
    }

    # Create CardsTab instance
    cards_progress_text = tk.StringVar(value="0 / 0 (0%)")
    cards_frame = CardsTab(notebook, progress_text_var=cards_progress_text)
    frames["Cards"] = cards_frame

    battle_progress_text = tk.StringVar(value="0 / 0 (0%)")
    battlestamps_frame = BattleStampsTab(
        notebook, progress_text_var=battle_progress_text)
    frames["Battle Stamps"] = battlestamps_frame

    # Add tabs in the desired order
    notebook.add(frames["Summary"], text="Summary")
    notebook.add(frames["Stats & World"], text="Stats & World")
    notebook.add(frames["Battle Stamps"], text="Battle Stamps")
    notebook.add(frames["Cards"], text="Cards")
    notebook.add(frames["Costumes"], text="Costumes")
    notebook.add(frames["Quests"], text="Quests")

    # ---------- Summary Frame ----------
    summary_frame = frames["Summary"]
    row = 0
    ttk.Label(summary_frame, text="Player Info").grid(
        row=0, column=0, sticky="w", padx=10, pady=5)
    ttk.Label(summary_frame, text="World & Position").grid(
        row=0, column=2, sticky="w", padx=10, pady=5)
    ttk.Label(summary_frame, text="Apple Bobbing High Scores").grid(
        row=8, column=2, sticky="w", padx=10, pady=5)
    ttk.Label(summary_frame, text="Misc. Stats").grid(
        row=13, column=2, sticky="w", padx=10, pady=5)
    row += 1

    # ---------------------------------------------------------
    #  SECTION 1 — Player Info
    # ---------------------------------------------------------

    level_label = ttk.Label(summary_frame, text="Level:").grid(
        row=row, column=0, sticky="w", padx=25)
    level_label = ttk.Label(summary_frame, textvariable=saveio.AppState.level_var,
                            width=33)
    level_label.grid(row=row, column=1, sticky="w", padx=25, pady=5)
    Tooltip(level_label, "This is your character's current level.")
    row += 1

    xp_label = ttk.Label(summary_frame, text="XP:").grid(
        row=row, column=0, sticky="w", padx=25, pady=5)
    xp_label = ttk.Label(summary_frame, textvariable=saveio.AppState.xp_var,
                         width=33)
    xp_label.grid(row=row, column=1, padx=25, pady=5)
    Tooltip(xp_label, "This is your character's current XP.")
    row += 1

    candy_label = ttk.Label(summary_frame, text="Candy:").grid(
        row=row, column=0, sticky="w", padx=25)
    candy_label = ttk.Label(summary_frame, textvariable=saveio.AppState.candy_var,
                            width=33)
    candy_label.grid(row=row, column=1, padx=25, pady=5)
    Tooltip(candy_label, "This is your current amount of candy.")
    row += 1

    totalcandy_label = ttk.Label(summary_frame, text="Total Candy:").grid(
        row=row, column=0, sticky="w", padx=25)
    totalcandy_label = ttk.Label(summary_frame, textvariable=saveio.AppState.total_candy_var,
                                 width=33)
    totalcandy_label.grid(row=row, column=1, padx=25, pady=5)
    Tooltip(totalcandy_label,
            "This is your total amount of candy collected.\n"
            "Doesn't decrease when you spend candy, essentially tracking lifetime candy collection.")
    row += 1

    # ---------------------------------------------------------
    #  SECTION 2 — COLLECTION PROGRESS
    # ---------------------------------------------------------

    ttk.Label(summary_frame, text="Collections").grid(
        row=row, column=0, sticky="w", padx=10, pady=5)
    row += 1

    # Battle Stamps
    battlestamps_label = ttk.Label(summary_frame, text="Battle Stamps:").grid(
        row=row, column=0, sticky="w", padx=25, pady=5
    )
    battlestamps_label = ttk.Label(
        summary_frame, textvariable=battle_progress_text)
    battlestamps_label.grid(
        row=row, column=1, sticky="w", padx=25, pady=5
    )
    Tooltip(battlestamps_label,
            "Shows how many battle stamps you have collected.\n"
            "Hover over names in the Battle Stamps tab for stamp images.")
    row += 1

    # Cards
    cards_label = ttk.Label(summary_frame, text="Cards:").grid(
        row=row, column=0, sticky="w", padx=25, pady=5)

    cards_label = ttk.Label(summary_frame, textvariable=cards_progress_text)
    cards_label.grid(
        row=row, column=1, sticky="w", padx=25, pady=5)
    Tooltip(cards_label, "Shows how many cards you have collected.\n"
            "Hover over names in the Cards tab for card images.")
    row += 1

    ttk.Label(summary_frame, text="Costumes:").grid(
        row=row, column=0, sticky="w", padx=25, pady=5)
    row += 1

    ttk.Label(summary_frame, text="Equipped Costumes:").grid(
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
            summary_frame, textvariable=saveio.AppState.costume_display_vars[i])
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
    map_label = ttk.Label(summary_frame, text="World:").grid(
        row=row, column=2, sticky="w", padx=25)
    map_label = ttk.Label(summary_frame, textvariable=saveio.AppState.selected_world,
                          width=33)
    map_label.grid(row=row, column=3, padx=25)
    Tooltip(map_label, "This is the world you are currently in.")
    row += 1

    positions = [
        ("Player Position:", saveio.AppState.player_position_vars),
        ("Camera Position:", saveio.AppState.camera_position_vars)
    ]

    for label_text, vars_list in positions:
        ttk.Label(summary_frame, text=label_text).grid(
            row=row, column=2, sticky="w", padx=25, pady=5
        )
        for i, axis in enumerate(["X", "Y", "Z"]):
            ttk.Label(summary_frame, text=f"{axis}:").grid(
                row=row + i, column=3, sticky="w", padx=25, pady=5
            )
            value_label = ttk.Label(
                summary_frame, textvariable=vars_list[i], width=15)
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
        ttk.Label(summary_frame, text=label_text).grid(
            row=row, column=2, sticky="w", padx=25, pady=5)
        ttk.Label(summary_frame, textvariable=var, width=33, anchor="w").grid(
            row=row, column=3, sticky="w", padx=25, pady=5)
        row += 1

    misc_stats = [
        ("Robot Ramp Jumps:", saveio.AppState.robotjumps_var),
        ("Monster Pail Bashes:", saveio.AppState.monsterbashes_var),
    ]
    row = 14
    for label_text, var in misc_stats:
        ttk.Label(summary_frame, text=label_text).grid(
            row=row, column=2, sticky="w", padx=25, pady=5)
        ttk.Label(summary_frame, textvariable=var, width=33, anchor="w").grid(
            row=row, column=3, sticky="w", padx=25, pady=5)
        row += 1

    # ---------- Stats & World Frame ----------
    stats_frame = frames["Stats & World"]
    ttk.Label(stats_frame, text="Stats").grid(
        row=row, column=0, sticky="w", padx=10, pady=5)
    row += 1

    ttk.Label(stats_frame, text="Level:").grid(
        row=row, column=0, sticky="w", padx=25, pady=5)
    level_dropdown = ttk.Combobox(
        stats_frame,
        textvariable=saveio.AppState.level_var,
        values=[str(i) for i in range(1, 11)],
        width=31,
        state="readonly",
    )
    level_dropdown.grid(row=row, column=1, sticky="w", padx=25, pady=5)

    frames["level_dropdown"] = level_dropdown

    for event in ("<<ComboboxSelected>>", "<FocusOut>", "<Return>"):
        level_dropdown.bind(event, saveio.update_xp_from_level)
    row += 1

    ttk.Label(stats_frame, text="XP:").grid(
        row=row, column=0, sticky="w", padx=25, pady=5)
    ttk.Entry(stats_frame, textvariable=saveio.AppState.xp_var, width=33).grid(
        row=row, column=1, padx=25, pady=5, sticky="w")
    row += 1

    ttk.Label(stats_frame, text="Candy:").grid(
        row=row, column=0, sticky="w", padx=25, pady=5)
    ttk.Entry(stats_frame, textvariable=saveio.AppState.candy_var, width=33).grid(
        row=row, column=1, padx=25, pady=5, sticky="w")
    row += 2

    ttk.Label(stats_frame, text="World, Location and Position").grid(
        row=row, column=0, padx=10, pady=5, sticky="w")
    row += 1
    ttk.Label(stats_frame, text="World:").grid(
        row=row, column=0, padx=25, pady=5, sticky="w")
    ttk.Combobox(stats_frame, textvariable=saveio.AppState.selected_world, values=list(
        WORLD_PATHS.keys()), width=31, state="readonly").grid(row=row, column=1, padx=25, pady=5, sticky="w")
    row += 1

    # Location dropdown variable
    location_var = tk.StringVar(value="")  # initially empty

    ttk.Label(stats_frame, text="Location:").grid(
        row=row, column=0, padx=25, pady=5, sticky="w")
    location_cb = ttk.Combobox(
        stats_frame, textvariable=location_var, values=[], width=31, state="readonly")
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
        stats_frame, "Player Position:", saveio.AppState.player_position_vars)
    player_position_frame2.grid(
        row=row, column=0, columnspan=2, sticky="w", padx=25, pady=5)
    row += 1

    camera_position_frame2 = create_vector_editor(
        stats_frame, "Camera Position:", saveio.AppState.camera_position_vars)
    camera_position_frame2.grid(
        row=row, column=0, columnspan=2, sticky="w", padx=25, pady=5)

    # ---------- Costumes Frame ----------
    costumes_frame = frames["Costumes"]
    row = 0

    ttk.Label(costumes_frame, text="Costumes").grid(
        row=row, column=0, padx=10, pady=5, sticky="w")
    # Card entries grid
    costumes_per_col = 5
    start_row = 0
    for i, name in enumerate(COSTUME_OPTIONS):
        col = (i // costumes_per_col)
        row = start_row + (i % costumes_per_col)

        ttk.Checkbutton(
            costumes_frame,
            text=name,
            width=15
        ).grid(row=row, column=col + 1, sticky="w", padx=10, pady=5)

    row += 6

    ttk.Label(costumes_frame, text="Costume Pieces").grid(
        row=row, column=0, padx=10, pady=5, sticky="w")
    row += 1

    ttk.Label(costumes_frame, text="Equipped Costumes").grid(
        row=row, column=0, padx=10, pady=5, sticky="w")

    for i, name in enumerate(NAMES):
        ttk.Label(costumes_frame, text=name).grid(
            row=row, column=1, padx=10, pady=5)

        ttk.Combobox(
            costumes_frame,
            textvariable=saveio.AppState.costume_vars[i],
            values=COSTUME_OPTIONS,
            width=15
        ).grid(row=row, column=2, sticky="w", padx=10, pady=5)
        row += 1

    # ---------- Quests ----------
    quests_frame = frames["Quests"]

    ttk.Label(quests_frame, text="Quests").grid(
        row=0, column=0, sticky="w", padx=10, pady=5
    )

    # === Scrollable Canvas ===
    canvas = tk.Canvas(quests_frame, highlightthickness=0)
    scrollbar = ttk.Scrollbar(
        quests_frame, orient="vertical", command=canvas.yview)

    scrollable = ttk.Frame(canvas)
    scrollable.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.grid(row=1, column=0, sticky="nsew")
    scrollbar.grid(row=1, column=1, sticky="ns")
    quests_frame.rowconfigure(1, weight=1)
    quests_frame.columnconfigure(0, weight=1)

    # === Mouse wheel support ===

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # === Toggle helper ===

    def toggle_frame(frame, label=None, title=None):
        if frame.winfo_viewable():
            frame.grid_remove()
            if label and title:
                label.config(text=f"▶ {title}")
        else:
            frame.grid()
            if label and title:
                label.config(text=f"▼ {title}")

    # === Build Quest Log ===
    row = 0

    for world, quests in QUESTS.items():
        # ----- World header -----
        world_lbl = ttk.Label(
            scrollable,
            text=f"▶ {world}",
            cursor="hand2",
            font=("Segoe UI", 10, "bold")
        )
        world_lbl.grid(row=row, column=0, sticky="w", padx=15, pady=4)
        row += 1

        world_frame = ttk.Frame(scrollable)
        world_frame.grid(row=row, column=0, sticky="w", padx=30)
        # collapsed by default # world_frame.grid_remove() to collapse
        world_frame.grid_remove()
        world_lbl.bind(
            "<Button-1>",
            lambda e, f=world_frame, l=world_lbl, t=world: toggle_frame(
                f, l, t)
        )
        row += 1
        qrow = 0

        for quest_name, data in quests.items():
            # ----- Quest header -----
            quest_lbl = ttk.Label(
                world_frame,
                text=f"▶ {quest_name}",
                cursor="hand2",
                font=("Segoe UI", 9, "bold")
            )
            quest_lbl.grid(row=qrow, column=0, sticky="w", padx=5, pady=2)

            quest_frame = ttk.Frame(world_frame)
            quest_frame.grid(row=qrow+1, column=0, sticky="w", padx=20)
            # collapsed by default  # quest_frame.grid_remove() to collapse
            quest_frame.grid_remove()
            quest_lbl.bind(
                "<Button-1>",
                lambda e, f=quest_frame, l=quest_lbl, t=quest_name: toggle_frame(
                    f, l, t)
            )
            qrow += 2

            # ----- Status -----
            status_var = tk.StringVar(value="❌ Not Started")
            # Quests Flags
            if "flags" in data:
                flags = data["flags"]

                def make_flag_updater(s=status_var, f=flags):
                    def inner(*_):
                        accomplished = AppState.quest_flags

                        started = f.get("started", [])
                        completed = f.get("completed", [])

                        if completed and all(flag in accomplished for flag in completed):
                            s.set("✅ Completed")
                        elif any(flag in accomplished for flag in started):
                            s.set("▶ In Progress")
                        else:
                            s.set("❌ Not Started")

                    AppState.quest_flags_var.trace_add("write", lambda *args: inner())
                    inner()

                make_flag_updater()

            ttk.Label(quest_frame, textvariable=status_var).grid(
                row=0, column=0, sticky="w", pady=(0, 2))

            # ----- Description -----
            ttk.Label(
                quest_frame,
                text=f"Description: {data.get('description') or 'N/A'}",
                wraplength=550
            ).grid(row=1, column=0, sticky="w")

            # ----- How to complete -----
            ttk.Label(
                quest_frame,
                text=f"How to complete: {data.get('how_to_complete') or 'N/A'}",
                wraplength=550
            ).grid(row=2, column=0, sticky="w", pady=(2, 2))

            # ----- Reward -----
            ttk.Label(
                quest_frame,
                text=f"Reward: {data.get('reward') or 'N/A'}",
                wraplength=550
            ).grid(row=3, column=0, sticky="w", pady=(2, 2))

    return notebook, frames
