# ui.py
import os
import saveio
from saveio import AppState
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from map_editor import MapEditor
from constants import NAMES, COSTUME_OPTIONS, COSTUME_DISPLAY_NAMES, CARD_NAMES, CARD_IMAGES, BATTLE_ITEM_NAMES, BATTLE_STAMP_IMAGES, WORLD_PATHS, DEBUG_TELEPORTS, MAP_HOUSES, MAP_IMAGES, QUESTS, QUEST_FLAG_MAP
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARDS_DIR = os.path.join(BASE_DIR, "images", "cards")


# ---------- small widgets ----------

def toggle_frame(frame):
    if frame.winfo_viewable():
        frame.grid_remove()
    else:
        frame.grid()


class ImageTooltip:
    """
    Tooltip for showing images (cards or battle stamps) on hover.
    Automatically scales 64x64 stamps to 128x128 for better visibility.
    Keeps pixel art crisp using Image.NEAREST.
    """

    def __init__(self, widget, img_path, scale_stamps=True):
        self.widget = widget
        self.img_path = img_path
        self.scale_stamps = False  # set to "scale_stamps" to upscale 64x64 image
        self.tip_window = None
        self.photo = None

        widget.bind("<Enter>", self._show_tooltip)
        widget.bind("<Leave>", self._hide_tooltip)

    def _show_tooltip(self, event=None):
        if self.tip_window:
            return

        if not self.img_path or not os.path.isfile(self.img_path):
            return

        # Load image
        img = Image.open(self.img_path)
        w, h = img.size

        # If it's a small stamp and scaling is enabled, double it
        if self.scale_stamps and (w, h) == (64, 64):
            img = img.resize((w * 2, h * 2), Image.NEAREST)
        # Otherwise, keep original size (e.g., 128x128 cards)

        self.photo = ImageTk.PhotoImage(img)

        # Create tooltip window
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        x = self.widget.winfo_pointerx() + 10
        y = self.widget.winfo_pointery() + 10
        tw.wm_geometry(f"+{x}+{y}")

        # Display image
        lbl = tk.Label(tw, image=self.photo,
                       borderwidth=0, highlightthickness=0)
        lbl.pack()

    def _hide_tooltip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


class BattleStampsTab(ttk.Frame):
    def __init__(self, parent, progress_text_var=None):
        super().__init__(parent)
        self.entries = {}
        self.progress_var = tk.DoubleVar()
        self.toggle_all_var = tk.IntVar()
        self.progress_text = progress_text_var
        self.missing_stamps_var = tk.StringVar(value="All")

        self._build_ui()
        self.update_progress()
        self.update_missing_stamps()

    def _build_ui(self):
        # Header row
        ttk.Label(self, text="Battle Stamps:").grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )
        ttk.Checkbutton(
            self, text="Toggle All", variable=self.toggle_all_var,
            command=self.toggle_all_stamps
        ).grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self, textvariable=self.progress_text).grid(
            row=0, column=2, padx=10, pady=5, sticky="w"
        )
        ttk.Progressbar(self, variable=self.progress_var, maximum=100, length=150).grid(
            row=0, column=3, padx=10, pady=5, sticky="w"
        )

        # Stamp entries grid
        items_per_col = 9
        start_row = 1
        for i, (stamp_num, name) in enumerate(BATTLE_ITEM_NAMES.items()):
            row = start_row + (i % items_per_col)
            col = (i // items_per_col) * 2

            lbl = ttk.Label(self, text=name)
            lbl.grid(row=row, column=col, sticky='e', padx=5, pady=2)

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
        self.progress_var.set(percent)
        if self.progress_text:
            self.progress_text.set(
                f"Collected: {collected} / {total} ({percent:.0f}%)")

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


class CardsTab(ttk.Frame):
    def __init__(self, parent, progress_text_var=None):
        super().__init__(parent)
        self.entries = {}
        self.progress_var = tk.DoubleVar()
        self.toggle_all_var = tk.IntVar()
        self.progress_text = progress_text_var
        self.missing_cards_var = tk.StringVar(value="All")

        self._build_ui()
        self.update_progress()
        self.update_missing_cards()

    def _build_ui(self):
        # Header row
        ttk.Label(self, text="Creepy Treat Cards:").grid(
            row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Checkbutton(self, text="Toggle All", variable=self.toggle_all_var,
                        command=self.toggle_all_cards).grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(self, textvariable=self.progress_text).grid(
            row=0, column=2, padx=10, pady=5, sticky="w")
        ttk.Progressbar(self, variable=self.progress_var, maximum=100, length=150).grid(
            row=0, column=3, padx=10, pady=5, sticky="w")

        # Card entries grid
        cards_per_col = 18
        start_row = 1
        for i in range(54):
            card_num = i + 1
            col = (i // cards_per_col) * 2
            row = start_row + (i % cards_per_col)
            card_name = CARD_NAMES.get(card_num, f"Card {card_num}")

            lbl = ttk.Label(self, text=card_name)
            lbl.grid(row=row, column=col, sticky='e', padx=5, pady=2)

            # Image tooltip
            img_path = CARD_IMAGES.get(card_num)
            if img_path and os.path.isfile(img_path):
                self._attach_image_tooltip(lbl, img_path)

            entry = tk.Entry(self, width=8)
            entry.grid(row=row, column=col + 1, sticky='w', padx=5, pady=2)
            entry.bind("<KeyRelease>", lambda e: [
                       self.update_progress(), self.update_missing_cards()])
            self.entries[card_num] = entry

        # Missing cards section
        last_row = start_row + cards_per_col * \
            ((54 + cards_per_col - 1) // cards_per_col)
        missing_frame = ttk.Frame(self)
        missing_frame.grid(row=last_row, column=0, columnspan=10, sticky="ew")
        missing_frame.columnconfigure(1, weight=1)

        ttk.Label(missing_frame, text="Missing Cards:").grid(
            row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(missing_frame, textvariable=self.missing_cards_var, anchor="w", wraplength=400).grid(
            row=0, column=1, sticky="ew", padx=10, pady=5
        )

        # Auto-wrap
        self.bind("<Configure>", self._update_wrap)

    def _attach_image_tooltip(self, widget, img_path):
        """Attach an image tooltip (like your ImageTooltip)"""
        ImageTooltip(widget, img_path)

    def _update_wrap(self, event=None):
        width = self.winfo_width()
        if width > 150:
            self.children.get('!frame').children.get(
                '!label2').config(wraplength=width - 150)

    def update_progress(self):
        total = len(self.entries)
        collected = sum(1 for e in self.entries.values() if e.get(
        ).strip().isdigit() and int(e.get().strip()) > 0)
        percent = (collected / total) * 100 if total > 0 else 0
        self.progress_var.set(percent)
        self.progress_text.set(
            f"Collected: {collected} / {total} ({percent:.0f}%)")

    def update_missing_cards(self):
        missing = [CARD_NAMES.get(num, f"Card {num}") for num, e in self.entries.items(
        ) if not e.get().strip() or e.get().strip() == "0"]
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


# ---------- Vector editor ----------


def create_vector_editor(parent, label_text, variables, state="normal"):
    frame = ttk.Frame(parent)
    frame.columnconfigure(1, weight=1)
    ttk.Label(frame, text=label_text).grid(row=0, column=0, sticky="w")
    for i, (axis, var) in enumerate(zip(["X", "Y", "Z"], variables)):
        ttk.Label(frame, text=f"{axis}:").grid(
            row=i + 1, column=1, padx=10, pady=2)
        if state == "readonly":  # use label instead of entry
            ttk.Label(frame, textvariable=var).grid(
                row=i + 1, column=2, padx=10, pady=2, sticky="w")
        else:  # normal editable entry
            ttk.Entry(frame, textvariable=var, state=state).grid(
                row=i + 1, column=2, padx=10, pady=2, sticky="w")
    return frame


# ---------- UI builder ----------


def create_menu(root, frames_refs):
    def make_menu(parent):
        return tk.Menu(parent, tearoff=0)

    menu_bar = make_menu(root)

    file_menu = make_menu(menu_bar)
    file_menu.add_command(
        label="Open", command=lambda: _open_and_fill(root, frames_refs))
    file_menu.add_command(label="Save", command=lambda: saveio.save_changes(
        frames_refs["Cards"].entries, frames_refs["Battle Stamps"].entries))
    file_menu.add_command(label="Save As...", command=lambda: saveio.save_as(
        frames_refs["Cards"].entries, frames_refs["Battle Stamps"].entries))
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
            " - Use the main tabs to access different sections (Summary, Stats, Cards, etc.).\n"
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
            "Costume Quest PC Save Editor - Alpha Version 1.1\n"
            "Made by: DeathMaster001\n\n"
            "This program allows you to view and edit Costume Quest PC save files. Use responsibly!"
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


def create_tabs(root):
    notebook = ttk.Notebook(root)
    frames = {
        "Summary": ttk.Frame(notebook),
        "Stats & World": ttk.Frame(notebook),
        "Battle Stamps": ttk.Frame(notebook),
        "Costumes": ttk.Frame(notebook),
        "Map": ttk.Frame(notebook),
        "Quests": ttk.Frame(notebook),
    }

    # Create CardsTab instance
    cards_progress_text = tk.StringVar(value="Collected: 0 / 0 (0%)")
    cards_frame = CardsTab(notebook, progress_text_var=cards_progress_text)
    frames["Cards"] = cards_frame

    battle_progress_text = tk.StringVar(value="Collected: 0 / 0 (0%)")
    battlestamps_frame = BattleStampsTab(
        notebook, progress_text_var=battle_progress_text)
    frames["Battle Stamps"] = battlestamps_frame

    # Add tabs in the desired order
    notebook.add(frames["Summary"], text="Summary")
    notebook.add(frames["Stats & World"], text="Stats & World")
    notebook.add(frames["Battle Stamps"], text="Battle Stamps")
    notebook.add(frames["Cards"], text="Cards")
    notebook.add(frames["Costumes"], text="Costumes")
    notebook.add(frames["Map"], text="Map")
    notebook.add(frames["Quests"], text="Quests")

    # ---------- Summary Frame ----------
    summary_frame = frames["Summary"]
    row = 0
    ttk.Label(summary_frame, text="Save Info").grid(
        row=row, column=0, sticky="w", padx=10, pady=5)
    row += 2
    ttk.Label(summary_frame, text="Player Info").grid(
        row=2, column=0, sticky="w", padx=10, pady=5)
    ttk.Label(summary_frame, text="World & Position").grid(
        row=0, column=2, sticky="w", padx=10, pady=5)
    ttk.Label(summary_frame, text="Apple Bobbing High Scores").grid(
        row=8, column=2, sticky="w", padx=10, pady=5)
    ttk.Label(summary_frame, text="Misc. Stats").grid(
        row=12, column=2, sticky="w", padx=10, pady=5)
    row += 1
    # ---------------------------------------------------------
    #  SECTION 1 — Save Info
    # ---------------------------------------------------------

    ttk.Label(summary_frame, text="Save File Type:").grid(
        row=1, column=0, sticky="w", padx=25)
    ttk.Label(summary_frame, textvariable=saveio.AppState.dlc_var,
              width=33).grid(row=1, column=1, padx=25, pady=5)

    # ---------------------------------------------------------
    #  SECTION 2 — Player Info
    # ---------------------------------------------------------

    ttk.Label(summary_frame, text="Level:").grid(
        row=row, column=0, sticky="w", padx=25)
    ttk.Label(summary_frame, textvariable=saveio.AppState.level_var,
              width=33).grid(row=row, column=1, padx=25, pady=5)
    row += 1

    ttk.Label(summary_frame, text="XP:").grid(
        row=row, column=0, sticky="w", padx=25, pady=5)
    ttk.Label(summary_frame, textvariable=saveio.AppState.xp_var,
              width=33).grid(row=row, column=1, padx=25, pady=5)
    row += 1

    ttk.Label(summary_frame, text="Candy:").grid(
        row=row, column=0, sticky="w", padx=25)
    ttk.Label(summary_frame, textvariable=saveio.AppState.candy_var,
              width=33).grid(row=row, column=1, padx=25, pady=5)
    row += 1

    ttk.Label(summary_frame, text="Total Candy:").grid(
        row=row, column=0, sticky="w", padx=25)
    ttk.Label(summary_frame, textvariable=saveio.AppState.total_candy_var,
              width=33).grid(row=row, column=1, padx=25, pady=5)
    row += 1

    # ---------------------------------------------------------
    #  SECTION 3 — COLLECTION PROGRESS
    # ---------------------------------------------------------

    ttk.Label(summary_frame, text="Collections").grid(
        row=row, column=0, sticky="w", padx=10, pady=5)
    row += 1

    # Battle Stamps
    ttk.Label(summary_frame, text="Battle Stamps:").grid(
        row=row, column=0, sticky="w", padx=25, pady=5
    )
    ttk.Label(summary_frame, textvariable=battle_progress_text).grid(
        row=row, column=1, sticky="w", padx=25, pady=5
    )
    row += 1

    # Cards
    ttk.Label(summary_frame, text="Cards:").grid(
        row=row, column=0, sticky="w", padx=25, pady=5)

    ttk.Label(summary_frame, textvariable=cards_progress_text).grid(
        row=row, column=1, sticky="w", padx=25, pady=5)
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
        ttk.Label(summary_frame, textvariable=saveio.AppState.costume_display_vars[i]).grid(
            row=row, column=1, padx=25, pady=5, sticky="w"
        )
        saveio.AppState.costume_vars[i].trace_add(
            "write",
            lambda *args, idx=i, nm=name: saveio.AppState.costume_display_vars[idx].set(
                f"{nm}: {COSTUME_DISPLAY_NAMES.get(saveio.AppState.costume_vars[idx].get(), saveio.AppState.costume_vars[idx].get())}"
            ),
        )
        row += 1

    # ---------------------------------------------------------
    #  SECTION 4 — WORLD & POSITION
    # ---------------------------------------------------------
    row = 1
    ttk.Label(summary_frame, text="Current Map:").grid(
        row=row, column=2, sticky="w", padx=25)
    ttk.Label(summary_frame, textvariable=saveio.AppState.selected_world,
              width=33).grid(row=row, column=3, padx=25)
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
            ttk.Label(summary_frame, textvariable=vars_list[i], width=15).grid(
                row=row + i, column=3, sticky="w", padx=40, pady=5
            )
        row += 3  # move row counter past this block

    # ---------------------------------------------------------
    #  SECTION 5 — MISC. STATS
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
    row = 13
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
        values=[""] + [str(i) for i in range(1, 15)],
        width=31,
        state="readonly",
    )
    level_dropdown.grid(row=row, column=1, sticky="w", padx=25, pady=5)
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
    ttk.Label(costumes_frame, text="Equipped Costumes").grid(
        row=0, column=0, padx=10, pady=5)
    for i, name in enumerate(NAMES):
        ttk.Label(costumes_frame, text=name).grid(
            row=i, column=1, padx=10, pady=5)
        ttk.Combobox(costumes_frame, textvariable=saveio.AppState.costume_vars[i], values=COSTUME_OPTIONS, width=30).grid(
            row=i, column=2, sticky="w", padx=10, pady=5)

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
    bobbing_map = {
        "Suburbs Bobbing for Apples": (saveio.AppState.suburbsbobbing_var, 30),
        "Mall Bobbing for Apples": (saveio.AppState.mallbobbing_var, 35),
        "Fall Valley Bobbing for Apples": (saveio.AppState.countrybobbing_var, 40),
    }

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
            status_var = tk.StringVar(value="❌ Incomplete")
            # Bobbing quests
            if quest_name in bobbing_map:
                bobbing_var, threshold = bobbing_map[quest_name]

                def make_bobbing_updater(v=bobbing_var, s=status_var, t=threshold):
                    def inner(*_):
                        score = int(v.get() or 0)
                        s.set("✅ Completed" if score >= t else "❌ Incomplete")
                    v.trace_add("write", lambda *args: inner())
                    inner()
                make_bobbing_updater()
            # QUEST_FLAG_MAP quests
            elif quest_name in QUEST_FLAG_MAP:
                flags = QUEST_FLAG_MAP[quest_name]

                def make_flag_updater(s=status_var, f=flags):
                    def inner(*_):
                        accomplished = AppState.quest_flags
                        # Check for special started/completed dict
                        if isinstance(f, dict):
                            if any(flag in accomplished for flag in f["started"]):
                                s.set("▶ In Progress")
                            if all(flag in accomplished for flag in f.get("completed", [])) and f.get("completed"):
                                s.set("✅ Completed")
                            elif not any(flag in accomplished for flag in f["started"]):
                                s.set("❌ Not Started")
                        else:
                            if all(flag in accomplished for flag in f):
                                s.set("✅ Completed")
                            elif any(flag in accomplished for flag in f):
                                s.set("▶ In Progress")
                            else:
                                s.set("❌ Not Started")
                    AppState.quest_flags_var.trace_add(
                        "write", lambda *args: inner())
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

    checkbox_vars = {}  # quest_id -> IntVar

    for qid in AppState.quest_flags:
        var = tk.IntVar(value=1)  # 1 = completed
        checkbox = tk.Checkbutton(scrollable, text=qid, variable=var)
        # use grid inside scrollable
        checkbox.grid(sticky="w", padx=10, pady=2)
        checkbox_vars[qid] = var

    # ---------- Map Tab ----------
    map_frame = frames["Map"]

    # Pick the default world and map path
    default_world = "Suburbs"
    map_path = MAP_IMAGES.get(default_world)

    # Create the MapEditor inside the Map tab
    map_editor = MapEditor(
        map_frame,
        initial_world="Suburbs",
        max_size=(800, 575)
    )
    map_editor.pack(fill="both", expand=True)

    # Keep a reference in frames dict if needed
    frames["MapEditor"] = map_editor

    return notebook, frames
