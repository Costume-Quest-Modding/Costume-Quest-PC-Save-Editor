# ui.py
from constants import THEMES, NAMES, COSTUME_OPTIONS, COSTUME_DISPLAY_NAMES, CARD_NAMES, CARD_IMAGES, BATTLE_ITEM_NAMES, BATTLE_STAMP_IMAGES, WORLD_PATHS, DEBUG_TELEPORTS
from PIL import Image, ImageTk
from saveio import AppState
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
import saveio
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARDS_DIR = os.path.join(BASE_DIR, "images", "cards")

# keep a module-level theme name
_current_theme_name = "light"


def current_theme():
    return THEMES[_current_theme_name]


def apply_theme(root, theme_name):
    global _current_theme_name
    _current_theme_name = theme_name
    theme = THEMES[theme_name]
    style = ttk.Style()
    style.theme_use(theme["style_theme"])

    style.configure("TNotebook", background=theme.get(
        "notebook_bg", theme["bg"]), borderwidth=0)
    style.configure("TNotebook.Tab",
                    background=theme["tab_bg"],
                    foreground=theme["tab_fg"],
                    padding=6)
    style.map("TNotebook.Tab",
              background=[("selected", theme["tab_selected_bg"])],
              foreground=[("selected", theme["tab_selected_fg"])])
    style.configure("TFrame", background=theme["bg"])
    style.configure("TLabel", background=theme["bg"], foreground=theme["fg"])
    style.configure("TEntry",
                    fieldbackground=theme["entry_bg"],
                    foreground=theme["entry_fg"],
                    background=theme["entry_bg"])
    root.configure(bg=theme["bg"])
    root.set_theme(theme["root_theme"])


def toggle_theme(root):
    apply_theme(root, "dark" if _current_theme_name == "light" else "light")

# ---------- small widgets ----------


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        try:
            x, y, cx, cy = self.widget.bbox("insert")
            x += self.widget.winfo_rootx() + 20
            y += self.widget.winfo_rooty() + 10
        except Exception:
            x = self.widget.winfo_rootx() + 20
            y = self.widget.winfo_rooty() + 10
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None


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
    theme = THEMES[_current_theme_name]

    def make_menu(parent):
        return tk.Menu(parent,
                       background=theme["menu_bg"],
                       foreground=theme["menu_fg"],
                       activebackground=theme["menu_active_bg"],
                       activeforeground=theme["menu_active_fg"],
                       tearoff=0)

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

    options_menu = make_menu(menu_bar)
    options_menu.add_command(
        label="Toggle Light/Dark Mode", command=lambda: toggle_theme(root))
    menu_bar.add_cascade(label="Options", menu=options_menu)

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
            "Options Menu:\n"
            " - Toggle Light/Dark Mode: Switches editor themes.\n\n"
            "Tips:\n"
            " - Hover over labels for more info (tooltips).\n"
            " - Ensure you save changes before closing the editor."
        )
    )
    help_menu.add_command(
        label="About",
        command=lambda: messagebox.showinfo(
            "About",
            "Costume Quest PC Save Editor - Alpha Version\n"
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
        "Cards": ttk.Frame(notebook),
        "Costumes": ttk.Frame(notebook),
        "Quests": ttk.Frame(notebook),
    }
    for name, frame in frames.items():
        notebook.add(frame, text=name)

    # ---------- Summary Frame ----------
    summary_frame = frames["Summary"]
    row = 0
    ttk.Label(summary_frame, text="Player Info").grid(
        row=row, column=0, sticky="w", padx=10, pady=5)
    ttk.Label(summary_frame, text="World & Position").grid(
        row=row, column=2, sticky="w", padx=10, pady=5)
    ttk.Label(summary_frame, text="Apple Bobbing High Scores").grid(
        row=8, column=2, sticky="w", padx=10, pady=5)
    ttk.Label(summary_frame, text="Misc. Stats").grid(
        row=12, column=2, sticky="w", padx=10, pady=5)
    row += 1
    # ---------------------------------------------------------
    #  SECTION 1 — Player Info
    # ---------------------------------------------------------

    ttk.Label(summary_frame, text="Player Level:").grid(
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
    #  SECTION 2 — COLLECTION PROGRESS
    # ---------------------------------------------------------

    ttk.Label(summary_frame, text="Collections").grid(
        row=row, column=0, sticky="w", padx=10, pady=5)
    row += 1

    # Battle Stamps
    battle_progress_text = tk.StringVar(value="Collected: 0 / 0 (0%)")
    ttk.Label(summary_frame, text="Battle Stamps:").grid(
        row=row, column=0, sticky="w", padx=25, pady=5
    )
    ttk.Label(summary_frame, textvariable=battle_progress_text).grid(
        row=row, column=1, sticky="w", padx=25, pady=5
    )
    row += 1

    # Cards
    cards_progress_text = tk.StringVar(value="Collected: 0 / 0 (0%)")
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
    #  SECTION 3 — WORLD & POSITION
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

    ttk.Label(stats_frame, text="Experience Points (XP):").grid(
        row=row, column=0, sticky="w", padx=25, pady=5)
    ttk.Entry(stats_frame, textvariable=saveio.AppState.xp_var, width=33).grid(
        row=row, column=1, padx=25, pady=5, sticky="w")
    row += 1

    ttk.Label(stats_frame, text="Current Candy:").grid(
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

    # ---------- Cards frame ----------
    cards_frame = frames["Cards"]
    cards_frame.entries = {}
    cards_frame.progress_var = tk.DoubleVar()
    cards_frame.toggle_all_var = tk.IntVar()
    cards_frame.progress_text = cards_progress_text  # link to Summary tab

    def update_cards_progress():
        total = len(cards_frame.entries)
        collected = sum(1 for e in cards_frame.entries.values(
        ) if e.get().strip().isdigit() and int(e.get().strip()) > 0)
        percentage = (collected / total) * 100 if total > 0 else 0
        cards_frame.progress_var.set(percentage)
        cards_frame.progress_text.set(
            f"Collected: {collected} / {total} ({percentage:.0f}%)")

    def toggle_all_cards():
        val = "1" if cards_frame.toggle_all_var.get() else "0"
        for entry in cards_frame.entries.values():
            entry.delete(0, tk.END)
            entry.insert(0, val)
        update_cards_progress()

    # --- Header row ---
    ttk.Label(cards_frame, text="Creepy Treat Cards:").grid(
        row=0, column=0, padx=10, pady=5, sticky="w")
    ttk.Checkbutton(cards_frame, text="Toggle All", variable=cards_frame.toggle_all_var,
                    command=toggle_all_cards).grid(row=0, column=1, padx=10, pady=5)
    cards_frame.progress_label = ttk.Label(
        cards_frame, textvariable=cards_frame.progress_text)
    cards_frame.progress_label.grid(
        row=0, column=2, padx=10, pady=5, sticky="w")
    cards_frame.progress = ttk.Progressbar(
        cards_frame, variable=cards_frame.progress_var, maximum=100, length=150)
    cards_frame.progress.grid(row=0, column=3, padx=10, pady=5, sticky="w")

    # --- Card entries below ---
    cards_per_col = 18
    start_row = 1
    for i in range(54):
        card_num = i + 1
        col = (i // cards_per_col) * 2
        row = start_row + (i % cards_per_col)
        card_name = CARD_NAMES.get(card_num, f"Card {card_num}")

        lbl = ttk.Label(cards_frame, text=card_name)
        lbl.grid(row=row, column=col, sticky='e', padx=5, pady=2)

        # Attach image tooltip (if image exists)
        img_path = CARD_IMAGES.get(card_num)
        if os.path.isfile(img_path):
            ImageTooltip(lbl, img_path)

        # create entry
        entry = tk.Entry(cards_frame, width=8)
        entry.grid(row=row, column=col + 1, sticky='w', padx=5, pady=2)
        entry.bind("<KeyRelease>", lambda e: update_cards_progress())
        cards_frame.entries[card_num] = entry

    cards_frame.update_progress = update_cards_progress
    cards_frame.update_progress()

    # ---------- Battle Stamps ----------
    battle_frame = frames["Battle Stamps"]
    battle_frame.entries = {}
    battle_frame.progress_var = tk.DoubleVar()
    battle_frame.toggle_all_var = tk.IntVar()
    battle_frame.progress_text = battle_progress_text  # link to Summary tab

    def update_battle_item_progress():
        total = len(battle_frame.entries)
        collected = sum(1 for e in battle_frame.entries.values(
        ) if e.get().strip().isdigit() and int(e.get().strip()) > 0)
        percentage = (collected / total) * 100 if total else 0
        battle_frame.progress_var.set(percentage)
        battle_frame.progress_text.set(
            f"Collected: {collected} / {total} ({percentage:.0f}%)")

    def toggle_all_battle_items():
        val = "1" if battle_frame.toggle_all_var.get() else "0"
        for e in battle_frame.entries.values():
            e.delete(0, tk.END)
            e.insert(0, val)
        update_battle_item_progress()

    # --- Header row ---
    ttk.Label(battle_frame, text="Battle Stamps:").grid(
        row=0, column=0, padx=10, pady=5, sticky="w")
    ttk.Checkbutton(battle_frame, text="Toggle All", variable=battle_frame.toggle_all_var,
                    command=toggle_all_battle_items).grid(row=0, column=1, padx=10, pady=5)
    battle_frame.progress_label = ttk.Label(
        battle_frame, textvariable=battle_frame.progress_text)
    battle_frame.progress_label.grid(
        row=0, column=2, padx=10, pady=5, sticky="w")
    battle_frame.progress = ttk.Progressbar(
        battle_frame, variable=battle_frame.progress_var, maximum=100, length=150)
    battle_frame.progress.grid(row=0, column=3, padx=10, pady=5, sticky="w")

    # --- Battle stamp entries ---
    items_per_col = 9
    start_row = 1
    for i, (key, name) in enumerate(BATTLE_ITEM_NAMES.items()):
        row = start_row + (i % items_per_col)
        col = (i // items_per_col) * 2

        lbl = ttk.Label(battle_frame, text=name)
        lbl.grid(row=row, column=col, sticky="e", padx=5, pady=2)

        # Attach image tooltip (if image exists)
        img_path = BATTLE_STAMP_IMAGES.get(key)
        if img_path and os.path.isfile(img_path):
            ImageTooltip(lbl, img_path)

        # create entry
        entry = tk.Entry(battle_frame, width=8)
        entry.grid(row=row, column=col+1, sticky="w", padx=5, pady=2)
        entry.bind("<KeyRelease>", lambda e: update_battle_item_progress())
        battle_frame.entries[key] = entry

    battle_frame.update_progress = update_battle_item_progress
    battle_frame.update_progress()

    # ---------- Quests ----------
    quests_frame = frames["Quests"]
    ttk.Label(quests_frame, text="Quests").grid(
        row=0, column=0, sticky="w", padx=10, pady=5
    )
    quest_label = ttk.Label(quests_frame, text="Apple Bobbing Quests")
    quest_label.grid(row=1, column=0, sticky="w", padx=25, pady=5)
    ToolTip(quest_label, "Complete 3 rounds per location of Apple Bobbing to finish the quest.\nFirst 2 rounds give Candy, 3rd gives a Creepy Treat Card.")

    bobbing_data = [
        ("Suburbs High Score:", saveio.AppState.suburbsbobbing_var, 30),
        ("Autumn Haven Mall High Score:", saveio.AppState.mallbobbing_var, 35),
        ("Fall Valley High Score:", saveio.AppState.countrybobbing_var, 40),
    ]

    quests_frame.progress_var = tk.DoubleVar()
    progress_label = ttk.Label(quests_frame, text="Completed: 0 / 0 (0%)")
    progress_label.grid(row=3, column=0, sticky="w", padx=40, pady=5)
    progress_bar = ttk.Progressbar(
        quests_frame, variable=quests_frame.progress_var, maximum=100, length=200)
    progress_bar.grid(row=3, column=1, sticky="w", padx=40, pady=5)

    def update_quest_progress():
        total = len(bobbing_data)
        completed = 0
        for label_text, var, threshold in bobbing_data:
            score = int(var.get() or 0)
            if score >= threshold:
                completed += 1
        percent = (completed / total) * 100 if total > 0 else 0
        quests_frame.progress_var.set(percent)
        progress_label.config(
            text=f"Completed: {completed} / {total} ({percent:.0f}%)")

    r = 4
    for name, var, threshold in bobbing_data:
        ttk.Label(quests_frame, text=name.replace(" High Score:", "")).grid(
            row=r, column=0, sticky="w", padx=40, pady=5)
        status = tk.StringVar()

        def make_updater(v=var, s=status, t=threshold):
            def inner(*_):
                score = int(v.get() or 0)
                s.set("✅ Completed" if score >= t else "❌ Incomplete")
                update_quest_progress()
            v.trace_add("write", inner)
            inner()
        make_updater()

        ttk.Label(quests_frame, textvariable=status).grid(
            row=r, column=1, sticky="w", padx=10, pady=5)
        r += 1

    return notebook, frames
