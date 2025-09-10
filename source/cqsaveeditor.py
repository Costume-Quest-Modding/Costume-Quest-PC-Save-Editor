import tkinter as tk
import re
import shutil
import os
import sys
from tkinter import filedialog, messagebox, ttk
from ttkthemes import ThemedTk
from datetime import datetime

# ==================== Constants ====================

XP_THRESHOLDS = {
    1: 0, 2: 2500, 3: 6000, 4: 12000, 5: 20000,
    6: 31000, 7: 45000, 8: 62000, 9: 82000, 10: 105000,
}

NAMES = ["Reynold/Wren", "Everett", "Lucy"]

WORLD_PATHS = {
    "Suburbs": "worlds/cq_suburbs/cq_suburbs.leveldata",
    "Autumn Haven Mall": "worlds/cq_mall_interior/cq_mall_interior",
    "Fall Valley": "worlds/cq_fallvalley/cq_fallvalley",
}

COSTUME_OPTIONS = [
    "Costume_Robot", "Costume_Knight", "Costume_StatueOfLiberty",
    "Costume_SpaceWarrior", "Costume_Ninja", "Costume_Unicorn",
    "Costume_Pumpkin", "Costume_Vampire", "Costume_FrenchFries",
    "Costume_BlackCat", "Costume_Grubbin"
]

CARD_PATTERN = re.compile(
    r'(TrickyTreatCard_(\d+)=InventoryItem\{[^}]*CurrentAmount=)(\d+)(;[^}]*\})'
)

# Example card names dictionary (fill with all 54)
CARD_NAMES = {
    1: "Raz-Ums",
    2: "Glop",
    3: "Wobblers",
    4: "Choconana",
    5: "Shimmerfizz",
    6: "Chunkwutter",
    7: "Candy Hair",
    8: "Moops",
    9: "Chocolate Carrot",
    10: "Fuds",
    11: "Sweet Tooth",
    12: "Jammie Jams",
    13: "Lollopops",
    14: "Fruity Foam",
    15: "Swedish Noses",
    16: "Box Cake",
    17: "Gooz",
    18: "Fee-Fi-Fo-Fudge",
    19: "Slime Beetles",
    20: "Sour Feet",
    21: "Fish Head",
    22: "Gummy Water",
    23: "Licorice Cables",
    24: "Cinnamon Brain",
    25: "Mossy Log",
    26: "Wood Chips",
    27: "Pizza Sundae",
    28: "Sweet Fat",
    29: "Pimples",
    30: "Frozen Butter",
    31: "Edible Hat",
    32: "Sludge",
    33: "Coffee Toffee Taffee",
    34: "Banana Beard",
    35: "Broccoli Wafers",
    36: "Gingerbread Ham",
    37: "Mice Crispy Treat",
    38: "Jaw Hurters",
    39: "Blobbles",
    40: "Barf Roll-Ups",
    41: "Chocolate Hamburger",
    42: "Clippingz",
    43: "Salmon Rings",
    44: "Street Chews",
    45: "Fried Popcorn",
    46: "Coconuts & Bolts",
    47: "Jelly Has-Beens",
    48: "Unicorn Pellets",
    49: "Misfortune Cookie",
    50: "Sugar Bucket",
    51: "Old Lady Fingers",
    52: "Boogie Pie",
    53: "Human Crackers",
    54: "Gloop"
}

THEMES = {
    "dark": {
        "root_theme": "black",
        "style_theme": "xpnative",
        "bg": "#1e1e1e",
        "fg": "#e0e0e0",
        "notebook_bg": "#2a2a2a",
        "menu_bg": "#2a2a2a",
        "menu_fg": "#dddddd",
        "menu_active_bg": "#444444",
        "menu_active_fg": "#80c0ff",
        "entry_bg": "#2a2a2a",
        "entry_fg": "#e0e0e0",
        "tab_bg": "#2a2a2a",
        "tab_fg": "#cccccc",
        "tab_selected_bg": "#444444",
        "tab_selected_fg": "#ffffff"
    },
    "light": {
        "bg": "#E3F2FD",
        "fg": "#0D47A1",
        "root_theme": "winxpblue",
        "style_theme": "xpnative",
        "notebook_bg": "#BBDEFB",
        "menu_bg": "#BBDEFB",
        "menu_fg": "#0D47A1",
        "menu_active_bg": "#90CAF9",
        "menu_active_fg": "#0D47A1",
        "entry_bg": "#FFFFFF",
        "entry_fg": "#0D47A1",
        "tab_bg": "#BBDEFB",
        "tab_fg": "#0D47A1",
        "tab_selected_bg": "#90CAF9",
        "tab_selected_fg": "#0D47A1",
    }
}


# === Battle Item Support ===
BATTLE_ITEM_PATTERN = re.compile(
    r'(BattleItem_(\w+)=InventoryItem\{[^}]*?CurrentAmount=)(\d+)(;[^}]*\})'
)

BATTLE_ITEM_NAMES = {
    "FangOfTheWolf": "Fang of the Wolf",
    "BlackCat": "Black Cat",
    "MovingTombstone": "Moving Tombstone",
    "Egg": "Egg",
    "DisembodiedHand": "Disembodied Hand",
    "PumpkinGuts": "Pumpkin Guts",
    "ScreamingSpider": "Screaming Spider",
    "BloodshotEyeballs": "Bloodshot Eyeballs",
    "ToiletPaper": "Toilet Paper",
    "OneEyedVampireBat": "One-Eyed Vampire Bat",
    "WitchesBrew": "Witch's Brew",
    "JawboneOfTheWolf": "Jawbone of the Wolf",
    "AlbinoBlackCat": "Albino Black Cat",
    "Banshee": "Banshee",
    "FlyingTombstone": "Flying Tombstone",
    "RottenEgg": "Rotten Egg",
    "SixFingeredHand": "Disembodied Six Fingered Hand",
    "MoldyPumpkinGuts": "Moldy Pumpkin Guts",
    "YodelingWidow": "Yodeling Black Widow",
    "TwoPlyToiletPaper": "2-Ply Toilet Paper",
    "HeadlessBanshee": "Headless Banshee",
    "VegetarianBrew": "Vegetarian Witch's Brew",
    "NoEyedVampireBat": "No-Eyed Vampire Bat",
    "BowlOfEyeballs": "Bowl of Bloodshot Eyeballs"
}

# Get the directory where the script is located
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# ==================== Theme Functions ====================

current_theme_name = "light"

def apply_theme(theme_name):
    theme = THEMES[theme_name]
    style = ttk.Style()
    style.theme_use(theme["style_theme"])

    style.configure("TNotebook", background=theme.get("notebook_bg", theme["bg"]), borderwidth=0)
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
    style.configure("TCombobox",
                    fieldbackground=theme["entry_bg"],
                    foreground=theme["entry_fg"],
                    background=theme["entry_bg"])

    root.configure(bg=theme["bg"])
    root.set_theme(theme["root_theme"])
    create_menu()

def current_theme():
    return THEMES[current_theme_name]

root = ThemedTk(theme=current_theme()["root_theme"])

def apply_theme_styles():
    theme = current_theme()
    style = ttk.Style()
    style.theme_use(theme["style_theme"])
    style.configure("TNotebook",
                    background=theme["notebook_bg"],
                    borderwidth=0)
    style.configure("TNotebook.Tab",
                    background=theme["tab_bg"],
                    foreground=theme["tab_fg"])
    style.map("TNotebook.Tab",
              background=[("selected", theme["tab_selected_bg"])])
    style.configure("Custom.TFrame", background=theme["notebook_bg"])

def toggle_theme():
    global current_theme_name
    current_theme_name = "dark" if current_theme_name == "light" else "light"
    apply_theme_styles()
    root.set_theme(current_theme()["root_theme"])
    create_menu()

apply_theme_styles()

# ==================== Global State ====================

class AppState:
    save_header = b""
    save_text_data = ""
    dark_mode_enabled = True
    original_candy_value = 0
    last_total_candy = 0
    loading_save = False
    selected_world = None
    total_candy_var = None
    candy_var = None
    level_var = None
    xp_var = None
    robotjumps_var = None
    monsterbashes_var = None
    suburbsbobbing_var = None
    mallbobbing_var = None
    countrybobbing_var = None
    costume_vars = [None, None, None]
    player_position_vars = [tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar()]
    camera_position_vars = [tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar()]
    save_path = None

# ==================== Utility Functions ====================

def calculate_level_from_xp(xp):
    for lvl in sorted(XP_THRESHOLDS, reverse=True):
        if xp >= XP_THRESHOLDS[lvl]:
            return lvl
    return 1

def extract_int(pattern, text, default=0):
    match = re.search(pattern, text)
    return int(match.group(1)) if match else default

def extract_vector3(pattern, text):
    match = re.search(pattern, text)
    if match:
        return tuple(float(match.group(i)) for i in range(1, 4))
    return (0.0, 0.0, 0.0)

def parse_vector(text, key):
    match = re.search(rf"{key}=<([-.\d]+),([-.\d]+),([-.\d]+)>;", text)
    if match:
        return tuple(float(match.group(i)) for i in range(1, 4))
    return (0.0, 0.0, 0.0)

def parse_quaternion(text, key):
    match = re.search(rf"{key}=<([-.\d]+),([-.\d]+),([-.\d]+),([-.\d]+)>;", text)
    if match:
        return tuple(float(match.group(i)) for i in range(1, 5))
    return (0.0, 0.0, 0.0, 1.0)

def update_world_path_in_save(text_data, new_path):
    # Replace the Level=...; line with the new path
    new_text, count = re.subn(r'(Level=)[^;]+;', fr'\1{new_path};', text_data)
    if count == 0:
        # No match found, optionally insert it or handle error
        print("Warning: Level path not found in save file text.")
        return text_data
    return new_text

def update_or_add_field(text, field_name, new_value):
    is_vector = field_name in ["PlayerPosition", "CameraPosition"]
    if is_vector:
        value_str = f"<{new_value[0]},{new_value[1]},{new_value[2]}>"
        pattern = fr"{field_name}=<[-.\d]+,[-.\d]+,[-.\d]+>"
        replacement = f"{field_name}={value_str}"
    else:
        value_str = str(new_value)
        pattern = fr"{field_name}\s*=\s*-?\d+(?:\.\d+)?;"
        replacement = f"{field_name}={value_str};"

    if re.search(pattern, text):
        return re.sub(pattern, replacement, text)
    insert_point = text.find("EquippedCostumes=")
    insert_text = replacement + ("\n" if not replacement.endswith("\n") else "")
    return text[:insert_point] + insert_text + text[insert_point:] if insert_point != -1 else text.strip() + "\n" + insert_text

def populate_card_entries_from_save():
    # Load Battle Items
    for match in BATTLE_ITEM_PATTERN.finditer(AppState.save_text_data):
        item_key = match.group(2)
        current_amount = match.group(3)
        if hasattr(battle_stamps_frame, "entries") and item_key in battle_stamps_frame.entries:
            entry = battle_stamps_frame.entries[item_key]
            entry.delete(0, tk.END)
            entry.insert(0, current_amount)
    if hasattr(battle_stamps_frame, "entries"):
        update_battle_item_progress()
    for match in CARD_PATTERN.finditer(AppState.save_text_data):
        card_num = int(match.group(2))
        current_amount = match.group(3)
        if card_num in cards_frame.entries:
            cards_frame.entries[card_num].delete(0, tk.END)
            cards_frame.entries[card_num].insert(0, current_amount)

# ==================== Save Data Handling ====================

def extract_save_data(text):
    total = extract_int(r"TotalCandyAmount=(\d+);", text)
    candy_matches = list(re.finditer(r"CandyAmount\s*=\s*(\d+);", text))
    candy = int(candy_matches[-1].group(1)) if candy_matches else 0
    costume_match = re.search(r"EquippedCostumes=\[([^\]]*)\];", text)
    costumes = [c.strip() for c in costume_match.group(1).split(",") if c.strip()] if costume_match else []
    xp = extract_int(r"ExperiencePoints\s*=\s*(\d+);", text)
    robot_jumps = extract_int(r"RobotRampJumos=(\d+)", text)
    monster_bashes = extract_int(r"MonsterPailBashes=(\d+)", text)
    suburbsbobbing = extract_int(r"SuburbsBobbingHighScore=(\d+)", text)
    mallbobbing = extract_int(r"MallBobbingHighScore=(\d+)", text)
    countrybobbing = extract_int(r"CountryBobbingHighScore=(\d+)", text)
    player_position = extract_vector3(r"PlayerPosition=<([-.\d]+),([-.\d]+),([-.\d]+)>", text)
    camera_position = extract_vector3(r"CameraPosition=<([-.\d]+),([-.\d]+),([-.\d]+)>", text)
    match = re.search(r"Level=([^;]+);", text)
    world = next((k for k, v in WORLD_PATHS.items() if v == match.group(1)), "Suburbs") if match else "Suburbs"
    return (
        total, candy, costumes, xp,
        robot_jumps, monster_bashes,
        suburbsbobbing, mallbobbing, countrybobbing,
        player_position, camera_position, world
    )

def open_save():
    file_path = filedialog.askopenfilename(title="Open Costume Quest Save File", filetypes=[("All Files", "*.*")])
    if not file_path:
        return

    with open(file_path, "rb") as f:
        binary_data = f.read()

    header = binary_data[:8]
    raw = binary_data[8:]

    start = raw.find(b"{Level=")
    end = raw.find(b"}", start)
    section = raw[start:end + 1].decode(errors="ignore") if start != -1 and end != -1 else ""
    path = section.split("=")[1].strip(";} ") if "=" in section else ""
    world = next((k for k, v in WORLD_PATHS.items() if v == path), "Suburbs")

    raw_text = raw.decode(errors="ignore")

    try:
        (
            total, candy, costumes, xp,
            robotjumps, monsterbashes,
            suburbsbobbing, mallbobbing, countrybobbing,
            player_pos, camera_pos, world
        ) = extract_save_data(raw_text)
    except Exception as e:
        messagebox.showerror("Load Error", f"Failed to parse save file:\n{e}")
        return

    AppState.loading_save = True

    AppState.total_candy_var.set(total)
    AppState.candy_var.set(str(candy))
    AppState.original_candy_value = candy
    AppState.xp_var.set(str(xp))
    AppState.level_var.set(str(calculate_level_from_xp(xp)))
    AppState.robotjumps_var.set(str(robotjumps))
    AppState.monsterbashes_var.set(str(monsterbashes))
    AppState.suburbsbobbing_var.set(str(suburbsbobbing))
    AppState.mallbobbing_var.set(str(mallbobbing))
    AppState.countrybobbing_var.set(str(countrybobbing))

    for i in range(3):
        AppState.costume_vars[i].set(costumes[i] if i < len(costumes) else "")
        AppState.player_position_vars[i].set(player_pos[i])
        AppState.camera_position_vars[i].set(camera_pos[i])

    AppState.selected_world.set(world)
    AppState.save_path.set(file_path)
    AppState.save_header = header
    AppState.save_text_data = raw_text
    AppState.loading_save = False

    populate_card_entries_from_save()

    # Load Battle Items
    for match in BATTLE_ITEM_PATTERN.finditer(AppState.save_text_data):
        item_key = match.group(2)
        current_amount = match.group(3)
        if hasattr(battle_stamps_frame, "entries") and item_key in battle_stamps_frame.entries:
            entry = battle_stamps_frame.entries[item_key]
            entry.delete(0, tk.END)
            entry.insert(0, current_amount)
    if hasattr(battle_stamps_frame, "entries"):
        update_battle_item_progress()


def update_save_data(
    text,
    new_level,
    xp,
    new_candy,
    new_total,
    new_world,
    player_pos,
    camera_pos,
    costumes,
    robotjumps,
    monsterbashes,
    suburbsbobbing,
    mallbobbing,
    countrybobbing
):
        text = update_or_add_field(text, "Level", new_level)
        text = update_or_add_field(text, "ExperiencePoints", xp)
        text = update_or_add_field(text, "CandyAmount", new_candy)
        text = update_or_add_field(text, "TotalCandyAmount", new_total)
        text = update_or_add_field(text, "World", new_world)
        text = update_or_add_field(text, "PlayerPosition", player_pos)
        text = update_or_add_field(text, "CameraPosition", camera_pos)
        costume_str = ",".join([c for c in costumes if c])
        text = re.sub(r"EquippedCostumes=\[[^\]]*\];", f"EquippedCostumes=[{costume_str}];", text)
        text = update_or_add_field(text, "RobotRampJumos", robotjumps)
        text = update_or_add_field(text, "MonsterPailBashes", monsterbashes)
        text = update_or_add_field(text, "SuburbsBobbingHighScore", suburbsbobbing)
        text = update_or_add_field(text, "MallBobbingHighScore", mallbobbing)
        text = update_or_add_field(text, "CountryBobbingHighScore", countrybobbing)
        return text

def save_changes():
    path = AppState.save_path.get()
    if not path:
        messagebox.showerror("Error", "No save file loaded.")
        return
    try:
        new_candy = int(AppState.candy_var.get())
        new_total = int(AppState.total_candy_var.get())
        AppState.original_candy_value = new_candy
        AppState.last_total_candy = new_total
        selected_costumes = [var.get().strip() for var in AppState.costume_vars if var.get().strip()]
        xp = int(AppState.xp_var.get())
        new_level = int(AppState.level_var.get())
        new_world = (AppState.selected_world.get())
        robotjumps = int(AppState.robotjumps_var.get())
        monsterbashes = int(AppState.monsterbashes_var.get())
        suburbsbobbing = int(AppState.suburbsbobbing_var.get())
        mallbobbing = int(AppState.mallbobbing_var.get())
        countrybobbing = int(AppState.countrybobbing_var.get())
        player_pos = tuple(var.get() for var in AppState.player_position_vars)
        camera_pos = tuple(var.get() for var in AppState.camera_position_vars)
        new_world_path = WORLD_PATHS.get(AppState.selected_world.get(), WORLD_PATHS["Suburbs"])
        updated_text = re.sub(r'(Level=)[^;]+;', r'\1' + new_world_path + ';', AppState.save_text_data)

        # Start from the current save data
        updated_text = AppState.save_text_data

        # Update card values using regex
        for card_num, entry in cards_frame.entries.items():
            val = entry.get().strip()
            if not val.isdigit():
                messagebox.showerror("Invalid input", f"Card {card_num} has invalid amount '{val}'")
                return
            pattern = re.compile(
                rf'(TrickyTreatCard_{card_num}=InventoryItem\{{[^}}]*CurrentAmount=)(\d+)(;[^}}]*\}})'
            )
            updated_text = pattern.sub(rf'\g<1>{val}\g<3>', updated_text, count=1)

        # Save Battle Items
        for item_key, entry in getattr(battle_stamps_frame, "entries", {}).items():
            val = entry.get().strip()
            if not val.isdigit():
                messagebox.showerror("Invalid input", f"{BATTLE_ITEM_NAMES[item_key]} has invalid amount '{val}'")
                return
            pattern = re.compile(
                rf'(BattleItem_{item_key}=InventoryItem\{{[^}}]*?CurrentAmount=)(\d+)(;[^}}]*\}})'
            )
            updated_text = pattern.sub(rf'\g<1>{val}\g<3>', updated_text, count=1)

        updated_text = update_save_data(
            updated_text,
            new_level,
            xp,
            new_candy,
            new_total,
            new_world,
            player_pos,
            camera_pos,
            selected_costumes,
            robotjumps,
            monsterbashes,
            suburbsbobbing,
            mallbobbing,
            countrybobbing
        )

        with open(path, "wb") as f:
            f.write(AppState.save_header)
            f.write(updated_text.encode("utf-8"))
        messagebox.showinfo("Success", "Save file updated!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save: {e}")

def save_as():
    if not AppState.save_text_data:
        messagebox.showerror("Error", "No save file loaded.")
        return
    path = filedialog.asksaveasfilename(
        title="Save As",
        defaultextension=".",
        filetypes=[("JSON File", "*.json"),
        ("Text File", "*.txt"),
        ("All Files", "*.*")]
    )
    if not path:
        return
    try:
        new_candy = int(AppState.candy_var.get())
        new_total = int(AppState.total_candy_var.get())
        AppState.original_candy_value = new_candy
        AppState.last_total_candy = new_total
        selected_costumes = [var.get().strip() for var in AppState.costume_vars if var.get().strip()]
        xp = int(AppState.xp_var.get())
        new_level = int(AppState.level_var.get())
        new_world = (AppState.selected_world.get())
        robotjumps = int(AppState.robotjumps_var.get())
        monsterbashes = int(AppState.monsterbashes_var.get())
        suburbsbobbing = int(AppState.suburbsbobbing_var.get())
        mallbobbing = int(AppState.mallbobbing_var.get())
        countrybobbing = int(AppState.countrybobbing_var.get())
        player_pos = tuple(var.get() for var in AppState.player_position_vars)
        camera_pos = tuple(var.get() for var in AppState.camera_position_vars)
        new_world_path = WORLD_PATHS.get(AppState.selected_world.get(), WORLD_PATHS["Suburbs"])
        updated_text = re.sub(r'(Level=)[^;]+;', r'\1' + new_world_path + ';', AppState.save_text_data)

        # Start from the current save data
        updated_text = AppState.save_text_data

        # Update card values using regex
        for card_num, entry in cards_frame.entries.items():
            val = entry.get().strip()
            if not val.isdigit():
                messagebox.showerror("Invalid input", f"Card {card_num} has invalid amount '{val}'")
                return
            pattern = re.compile(
                rf'(TrickyTreatCard_{card_num}=InventoryItem\{{[^}}]*CurrentAmount=)(\d+)(;[^}}]*\}})'
            )
            updated_text = pattern.sub(rf'\g<1>{val}\g<3>', updated_text, count=1)

        # Save Battle Items
        for item_key, entry in getattr(battle_stamps_frame, "entries", {}).items():
            val = entry.get().strip()
            if not val.isdigit():
                messagebox.showerror("Invalid input", f"{BATTLE_ITEM_NAMES[item_key]} has invalid amount '{val}'")
                return
            pattern = re.compile(
                rf'(BattleItem_{item_key}=InventoryItem\{{[^}}]*?CurrentAmount=)(\d+)(;[^}}]*\}})'
            )
            updated_text = pattern.sub(rf'\g<1>{val}\g<3>', updated_text, count=1)

        updated_text = update_save_data(
            updated_text,
            new_level,
            xp,
            new_candy,
            new_total,
            new_world,
            player_pos,
            camera_pos,
            selected_costumes,
            robotjumps,
            monsterbashes,
            suburbsbobbing,
            mallbobbing,
            countrybobbing
        )

        if path.endswith(".json"):
            data = {
                "Level": new_level,
                "ExperiencePoints": xp,
                "CandyAmount": new_candy,
                "TotalCandyAmount": new_total,
                "World": new_world,
                "PlayerPosition": player_pos,
                "CameraPosition": camera_pos,
                "EquippedCostumes": selected_costumes,
                "RobotRampJumps": robotjumps,
                "MonsterPailBashes": monsterbashes,
                "SuburbsBobbingHighScore": suburbsbobbing,
                "MallBobbingHighScore": mallbobbing,
                "CountryBobbingHighScore": countrybobbing
            }
            with open(path, "w", encoding="utf-8") as f:
                import json
                json.dump(data, f, indent=4)

        elif path.endswith(".txt"):
            data = [
                f"Level: {new_level}",
                f"Experience Points: {xp}",
                f"Current Candy Amount: {new_candy}",
                f"Total Candy Amount: {new_total}",
                f"World: {new_world}",
                f"Player Position: {player_pos}",
                f"Camera Position: {camera_pos}",
                f"Equipped Costumes: {', '.join(selected_costumes)}",
                f"Robot Ramp Jumps: {robotjumps}",
                f"Monster Pail Bashes: {monsterbashes}",
                f"Suburbs Bobbing High Score: {suburbsbobbing}",
                f"Mall Bobbing High Score: {mallbobbing}",
                f"Country Bobbing High Score: {countrybobbing}"
            ]
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(data))
        
        else:
            with open(path, "wb") as f:
                f.write(AppState.save_header)
                f.write(updated_text.encode("utf-8"))
        messagebox.showinfo("Saved", f"File successfully saved to:\n{path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save: {e}")

def backup_save():
    path = AppState.save_path.get()
    if not path:
        messagebox.showerror("Error", "No save file loaded.")
        return
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{path}_backup_{timestamp}"
        shutil.copy2(path, backup_path)
        messagebox.showinfo("Backup Created", f"Backup saved as:{backup_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create backup: {e}")

# ==================== GUI Building Functions ====================

def create_vector_editor(parent, label_text, variables, state="normal"):
    frame = ttk.Frame(parent)
    frame.columnconfigure(1, weight=1)  # Let column 1 (entries) expand if needed

    # Section label
    ttk.Label(frame, text=label_text).grid(row=0, column=0, sticky="w", padx=(10, 5))

    for i, (axis, var) in enumerate(zip(["X", "Y", "Z"], variables)):
        ttk.Label(frame, text=f"{axis}:").grid(row=i + 1, column=0, padx=10, pady=2, sticky="e")
        ttk.Entry(frame, textvariable=var, state=state).grid(row=i + 1, column=1, padx=5, pady=2, sticky="we")

    return frame

# ==================== Event Bindings ====================

def on_candy_change(*args):
    if AppState.loading_save:
        return
    try:
        new_candy = int(AppState.candy_var.get())
        delta = new_candy - AppState.original_candy_value
        total = int(AppState.total_candy_var.get()) + delta
        AppState.total_candy_var.set(str(total))
        total = max(0, total)
        AppState.total_candy_var.set(total)
        AppState.original_candy_value = new_candy
    except ValueError:
        pass

def update_xp_from_level(*args):
    try:
        level = int(AppState.level_var.get())
        xp = XP_THRESHOLDS.get(level, 0)
        AppState.xp_var.set(str(xp))
    except ValueError:
        AppState.level_var.set("")

def update_level_from_xp(*args):
    try:
        xp = int(AppState.xp_var.get())
        level = calculate_level_from_xp(xp)
        AppState.level_var.set(str(level))
    except ValueError:
        pass

def create_menu():
    theme = current_theme()

    def make_menu(parent):
        return tk.Menu(parent,
                       background=theme["menu_bg"],
                       foreground=theme["menu_fg"],
                       activebackground=theme["menu_active_bg"],
                       activeforeground=theme["menu_active_fg"],
                       tearoff=0)

    menu_bar = make_menu(root)

    # File menu
    file_menu = make_menu(menu_bar)
    file_menu.add_command(label="Open", command=open_save)
    file_menu.add_command(label="Save", command=save_changes)
    file_menu.add_command(label="Save As...", command=save_as)
    file_menu.add_command(label="Backup Save File", command=backup_save)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Options menu
    options_menu = make_menu(menu_bar)
    options_menu.add_command(label="Toggle Light/Dark Mode", command=toggle_theme)
    menu_bar.add_cascade(label="Options", menu=options_menu)

    # Help menu
    help_menu = make_menu(menu_bar)
    help_menu.add_command(
        label="How to Use",
        command=lambda: messagebox.showinfo(
            "How to Use",
            "Use the main tabs to navigate. Use the dropdown tabs/textboxes to edit save file information.\n\n"
            "'File Options'\n\n"
            "'Open' - Open existing save file.\n\n"
            "'Save' - Save changes to current save.\n\n"
            "'Save As... - Choose where to save your file. (Try saving as a .json or .txt)\n\n"
            "'Backup Save File' - Makes a backup of currently loaded save."
        )
    )
    help_menu.add_command(
        label="About",
        command=lambda: messagebox.showinfo(
            "About",
            "Costume Quest PC Save Editor\nVersion Beta 1.2 by DeathMaster001"
        )
    )
    menu_bar.add_cascade(label="Help", menu=help_menu)

    root.config(menu=menu_bar)

dark_mode_enabled = False  # Assuming you start in dark mode with theme="black"

# ==================== App Initialization ====================

# Initialize the UI
root.title("Costume Quest PC Save Editor")
root.geometry("800x600")
root.minsize(800, 600)

# Initialize AppState Tkinter variables now that root exists
AppState.save_path = tk.StringVar()
AppState.total_candy_var = tk.StringVar(value="0")
AppState.candy_var = tk.StringVar(value="0")
AppState.level_var = tk.StringVar(value="1")
AppState.xp_var = tk.StringVar(value="0")
AppState.robotjumps_var = tk.StringVar(value="0")
AppState.monsterbashes_var = tk.StringVar(value="0")
AppState.suburbsbobbing_var = tk.StringVar(value="0")
AppState.mallbobbing_var = tk.StringVar(value="0")
AppState.countrybobbing_var = tk.StringVar(value="0")
AppState.selected_world = tk.StringVar(value="")
AppState.costume_vars = [tk.StringVar(value=opt) for opt in COSTUME_OPTIONS[:3]]
AppState.player_position_vars = [tk.DoubleVar(value=0.0) for _ in range(3)]
AppState.camera_position_vars = [tk.DoubleVar(value=0.0) for _ in range(3)]

# Trace callbacks
AppState.candy_var.trace_add("write", on_candy_change)
AppState.xp_var.trace_add("write", update_level_from_xp)

# Remaining globals
save_header = []
save_text_data = []

# Notebook and frames
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

frames = {
    "Summary": ttk.Frame(notebook),
    "Stats": ttk.Frame(notebook),
    "World/Location": ttk.Frame(notebook),
    "Battle Stamps": ttk.Frame(notebook),
    "Cards": ttk.Frame(notebook),
    "Costumes": ttk.Frame(notebook),
    "Quests": ttk.Frame(notebook),
    "100% Tracker": ttk.Frame(notebook),
}

for name, frame in frames.items():
    notebook.add(frame, text=name)

# Helper to create label + widget in grid
def grid_label_widget(frame, row, label_text, widget, label_padx=25, widget_padx=25, sticky="w", label_col=0, widget_col=1, pady=5):
    ttk.Label(frame, text=label_text).grid(row=row, column=label_col, sticky=sticky, padx=label_padx, pady=pady)
    widget.grid(row=row, column=widget_col, sticky=sticky, padx=widget_padx, pady=pady)

# --- Summary Frame ---
summary_frame = frames["Summary"]
row = 0
ttk.Label(summary_frame, text="Main Stats").grid(row=row, column=0, sticky="w", padx=10, pady=5)
ttk.Label(summary_frame, text="Misc. Stats").grid(row=row, column=2, sticky="w", padx=10, pady=5)
row += 1

# Summary Level
level_label = ttk.Label(summary_frame, textvariable=AppState.level_var)
grid_label_widget(summary_frame, row, "Level:", level_label)
row += 1

# Summary XP
xp_entry = ttk.Label(summary_frame, textvariable=AppState.xp_var)
xp_entry.bind("<FocusOut>", update_level_from_xp)
grid_label_widget(summary_frame, row, "Experience Points (XP):", xp_entry)
row += 1

# Summary CurrentCandy
candy_entry = ttk.Label(summary_frame, textvariable=AppState.candy_var, width=33)
grid_label_widget(summary_frame, row, "Current Candy:", candy_entry)
row += 1
total_candy_entry = ttk.Label(summary_frame, textvariable=AppState.total_candy_var, width=33)
grid_label_widget(summary_frame, row, "Total Candy:", total_candy_entry)
row += 1

# Summary Misc. Stats
misc_stats = [
    ("Robot Ramp Jumps:", AppState.robotjumps_var),
    ("Monster Pail Bashes:", AppState.monsterbashes_var),
    ("Suburbs Bobbing High Score:", AppState.suburbsbobbing_var),
    ("Autumn Haven Mall Bobbing High Score:", AppState.mallbobbing_var),
    ("Fall Valley Bobbing High Score:", AppState.countrybobbing_var)
]
row = 1
for label_text, var in misc_stats:
    ttk.Label(summary_frame, text=label_text).grid(row=row, column=2, sticky="w", padx=25, pady=5)
    ttk.Label(summary_frame, textvariable=var, width=25, anchor="w").grid(row=row, column=3, sticky="w", padx=25, pady=5)
    row += 1

# Summary World/Location Stats
row = 5
ttk.Label(summary_frame, text="World/Location Stats").grid(row=row, column=0, sticky="w", padx=10, pady=5)
row += 1

grid_label_widget(
    summary_frame, row, "World:",
    ttk.Label(summary_frame, textvariable=AppState.selected_world, width=30, state="readonly"),
    label_padx=25, widget_padx=25
)
row += 1

# Vector editors
player_position_frame = create_vector_editor(summary_frame, "Player Position:", AppState.player_position_vars)
player_position_frame.grid(row=row, column=0, columnspan=2, sticky="w", padx=25, pady=5)
row += 1

camera_position_frame = create_vector_editor(summary_frame, "Camera Position:", AppState.camera_position_vars)
camera_position_frame.grid(row=row, column=0, columnspan=2, sticky="w", padx=25, pady=5)
row += 1

ttk.Label(summary_frame, text="Costumes:").grid(row=row, column=0, sticky="w", padx=25, pady=5)
row += 1
ttk.Label(summary_frame, text="Equipped Costumes:").grid(row=row, column=0, padx=35, pady=5)

start_row = 10  # or whatever row you want to begin on

# Create a StringVar for each label
AppState.costume_display_vars = [tk.StringVar() for _ in NAMES]

for i, name in enumerate(NAMES):
    AppState.costume_vars[i].set(COSTUME_OPTIONS[i])
    AppState.costume_display_vars[i].set(f"{name}: {AppState.costume_vars[i].get()}")

    # Create label bound to the combined StringVar
    ttk.Label(summary_frame, textvariable=AppState.costume_display_vars[i]).grid(
        row=start_row + i, column=1, padx=10, pady=5, sticky="w"
    )

    # Correct closure capture using a default argument in lambda
    def update_label(index=i, n=name):
        AppState.costume_display_vars[index].set(f"{n}: {AppState.costume_vars[index].get()}")

    AppState.costume_vars[i].trace_add("write", lambda *args, idx=i, name=name: AppState.costume_display_vars[idx].set(f"{name}: {AppState.costume_vars[idx].get()}"))


# ==================== Stats Frame lol ====================
stats_frame = frames["Stats"]
ttk.Label(stats_frame, text="Main Stats").grid(row=row, column=0, sticky="w", padx=10, pady=5)
row += 1

# Level dropdown
level_dropdown = ttk.Combobox(stats_frame, textvariable=AppState.level_var, values=[""] + [str(i) for i in range(1, 11)], width=30, state="readonly")
for event in ("<<ComboboxSelected>>", "<FocusOut>", "<Return>"):
    level_dropdown.bind(event, update_xp_from_level)
grid_label_widget(stats_frame, row, "Level:", level_dropdown)
row += 1

# XP entry
xp_entry = ttk.Entry(stats_frame, textvariable=AppState.xp_var, width=33)
xp_entry.bind("<FocusOut>", update_level_from_xp)
grid_label_widget(stats_frame, row, "Experience Points (XP):", xp_entry)
row += 1

# Candy entry
candy_entry = ttk.Entry(stats_frame, textvariable=AppState.candy_var, width=33)
grid_label_widget(stats_frame, row, "Current Candy:", candy_entry)
row += 1

# Misc stats data: label text and associated variables
misc_stats = [
    ("Total Candy:", AppState.total_candy_var),
    ("Robot Ramp Jumps:", AppState.robotjumps_var),
    ("Monster Pail Bashes:", AppState.monsterbashes_var),
    ("Suburbs Bobbing High Score:", AppState.suburbsbobbing_var),
    ("Autumn Haven Mall Bobbing High Score:", AppState.mallbobbing_var),
    ("Fall Valley Bobbing High Score:", AppState.countrybobbing_var),
]

# --- World/Location Frame ---
world_frame = frames["World/Location"]
row = 0

grid_label_widget(
    world_frame, row, "World:",
    ttk.Combobox(world_frame, textvariable=AppState.selected_world, values=list(WORLD_PATHS.keys()), width=30, state="readonly"),
    label_padx=10, widget_padx=10
)
row += 1

# Vector editors
player_position_frame = create_vector_editor(world_frame, "Player Position:", AppState.player_position_vars)
player_position_frame.grid(row=row, column=0, columnspan=2, sticky="w", padx=25, pady=5)
row += 1

camera_position_frame = create_vector_editor(world_frame, "Camera Position:", AppState.camera_position_vars)
camera_position_frame.grid(row=row, column=0, columnspan=2, sticky="w", padx=25, pady=5)

# --- Costumes Frame ---
costumes_frame = frames["Costumes"]
ttk.Label(costumes_frame, text="Equipped Costumes:").grid(row=0, column=0, padx=10, pady=5)

for i, name in enumerate(NAMES):
    AppState.costume_vars[i].set(COSTUME_OPTIONS[i])
    ttk.Label(costumes_frame, text=name).grid(row=i, column=1, padx=10, pady=5)
    ttk.Combobox(costumes_frame, textvariable=AppState.costume_vars[i], values=COSTUME_OPTIONS, width=30).grid(row=i, column=2, sticky="w", padx=10, pady=5)


# --- Cards Frame ---
cards_frame = frames["Cards"]
row += 1

cards_frame.entries = {}
cards_per_col = 18

for i in range(54):
    card_num = i + 1
    col = i // cards_per_col * 2
    row = (i % cards_per_col) + 1

    card_name = CARD_NAMES.get(card_num, f"Card {card_num}")

    label = ttk.Label(cards_frame, text=f"{card_name}")
    label.grid(row=row, column=col, sticky='e', padx=5, pady=2)

    entry = tk.Entry(cards_frame, width=8)
    entry.grid(row=row, column=col + 1, sticky='w', padx=5, pady=2)

    cards_frame.entries[card_num] = entry


# --- Battle Items Frame ---
battle_stamps_frame = frames["Battle Stamps"]

battle_stamps_frame.entries = {}
battle_stamps_frame.progress_var = tk.DoubleVar()
battle_stamps_frame.toggle_all_var = tk.IntVar()

def update_battle_item_progress():
    total = len(battle_stamps_frame.entries)
    collected = sum(1 for entry in battle_stamps_frame.entries.values()
                    if entry.get().strip().isdigit() and int(entry.get().strip()) > 0)
    percentage = (collected / total) * 100 if total > 0 else 0
    battle_stamps_frame.progress_var.set(percentage)
    progress_label.config(text=f"Collected: {collected} / {total} ({percentage:.0f}%)")

def toggle_all_battle_items():
    val = "1" if battle_stamps_frame.toggle_all_var.get() else "0"
    for entry in battle_stamps_frame.entries.values():
        entry.delete(0, tk.END)
        entry.insert(0, val)
    update_battle_item_progress()

# Create UI
toggle_cb = ttk.Checkbutton(battle_stamps_frame, text="Toggle All", variable=battle_stamps_frame.toggle_all_var,
                           command=toggle_all_battle_items)
toggle_cb.grid(row=0, column=0, columnspan=4, pady=10)

items_per_col = 9
for i, (key, name) in enumerate(BATTLE_ITEM_NAMES.items()):
    col = (i // items_per_col) * 2
    row = (i % items_per_col) + 1
    ttk.Label(battle_stamps_frame, text=name).grid(row=row, column=col, sticky='e', padx=5, pady=2)
    entry = tk.Entry(battle_stamps_frame, width=8)
    entry.grid(row=row, column=col + 1, sticky='w', padx=5, pady=2)
    entry.bind("<KeyRelease>", lambda e: update_battle_item_progress())
    battle_stamps_frame.entries[key] = entry

progress_bar = ttk.Progressbar(battle_stamps_frame, variable=battle_stamps_frame.progress_var, maximum=100, length=200)
progress_bar.grid(row=21, column=0, columnspan=2, padx=10, pady=10, sticky="w")

progress_label = ttk.Label(battle_stamps_frame, text="Collected: 0 / 0 (0%)")
progress_label.grid(row=21, column=2, columnspan=4, sticky="w")

# --- 100% Tracker Frame ---
hundotracker_frame = frames["100% Tracker"]
row = 0
ttk.Label(hundotracker_frame, text="").grid(row=row, column=0, sticky="w", padx=10, pady=5)
row += 1
ttk.Label(hundotracker_frame, text="Apple Bobbing:").grid(row=row, column=0, sticky="w", padx=10, pady=5)
row += 1

# Misc stats data
misc_stats = [
    ("Suburbs High Score:", AppState.suburbsbobbing_var),
    ("Autumn Haven Mall High Score:", AppState.mallbobbing_var),
    ("Fall Valley High Score:", AppState.countrybobbing_var),
]

# Thresholds per world
bobbing_thresholds = {
    "Suburbs High Score:": 30,
    "Autumn Haven Mall High Score:": 35,
    "Fall Valley High Score:": 40,
}

# Separate dictionary just for Apple Bobbing
hundotracker_frame.applebobbing_entries = {}

# Progress bar setup
hundotracker_frame.progress_var = tk.DoubleVar()

applebobbingprogress = ttk.Label(hundotracker_frame, text="Completed: 0 / 0 (0%)")
applebobbingprogress.grid(row=row, column=0, columnspan=4, padx=10, pady=10, sticky="w")

applebobbingprogressbar = ttk.Progressbar(hundotracker_frame, variable=hundotracker_frame.progress_var, maximum=100, length=200)
applebobbingprogressbar.grid(row=row, column=1, columnspan=2, padx=10, pady=10, sticky="w")
row += 1

# Define the progress update function first
def update_applebobbing_progress():
    total = len(hundotracker_frame.applebobbing_entries)
    collected = sum(1 for var, threshold in hundotracker_frame.applebobbing_entries.values()
                    if int(var.get() or 0) >= threshold)
    percentage = (collected / total) * 100 if total > 0 else 0
    hundotracker_frame.progress_var.set(percentage)
    applebobbingprogress.config(text=f"Completed: {collected} / {total} ({percentage:.0f}%)")

# Now create the Apple Bobbing entries
for label_text, var in misc_stats:
    # Score label
    ttk.Label(hundotracker_frame, text=label_text).grid(row=row, column=0, sticky="w", padx=25, pady=5)
    ttk.Label(hundotracker_frame, textvariable=var, relief="sunken", width=10, anchor="w").grid(row=row, column=1, sticky="w", padx=25, pady=5)

    # Completed/incomplete status
    def make_status_var(v=var, threshold=bobbing_thresholds[label_text]):
        s = tk.StringVar()
        def update_status(*_):
            score = int(v.get() or 0)
            s.set("✅ Completed" if score >= threshold else "❌ Incomplete")
            update_applebobbing_progress()  # update progress dynamically
        v.trace_add("write", update_status)
        update_status()
        return s

    status_var = make_status_var()
    ttk.Label(hundotracker_frame, textvariable=status_var).grid(row=row, column=2, sticky="w", padx=10, pady=5)

    # Store variable + threshold in the Apple Bobbing dict
    hundotracker_frame.applebobbing_entries[label_text] = (var, bobbing_thresholds[label_text])

    row += 1

# Initial update
update_applebobbing_progress()

# Remaining categories
ttk.Label(hundotracker_frame, text="Battle Stamps").grid(row=row, column=0, sticky="w", padx=10, pady=5)
row += 1
ttk.Label(hundotracker_frame, text="Costumes").grid(row=row, column=0, sticky="w", padx=10, pady=5)
row += 1
ttk.Label(hundotracker_frame, text="Creepy Treat Cards").grid(row=row, column=0, sticky="w", padx=10, pady=5)
row += 1
ttk.Label(hundotracker_frame, text="Level").grid(row=row, column=0, sticky="w", padx=10, pady=5)
row += 1
ttk.Label(hundotracker_frame, text="Quests").grid(row=row, column=0, sticky="w", padx=10, pady=5)

# --- WIP Tabs ---
for tab in ("Quests",):
    frame = frames[tab]
    ttk.Label(frame, text="Not implemented yet.", anchor="center", justify="center").pack(expand=True, fill='both')

# Menu, icon, mainloop
create_menu()

# checking if the script is running from a pyinstaller generated exe or from loose script files

if getattr(sys, 'frozen', False):
    icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
else:
    icon_path = os.path.join(BASE_DIR, 'icon.ico')

root.iconbitmap(icon_path)
apply_theme("dark" if dark_mode_enabled else "light")
root.mainloop()