# saveio.py
import re
import shutil
from datetime import datetime
from tkinter import filedialog, messagebox
import tkinter as tk
from constants import (
    XP_THRESHOLDS, WORLD_PATHS, CARD_PATTERN, CARD_NAMES,
    BATTLE_ITEM_PATTERN, BATTLE_ITEM_NAMES
)

class AppState:
    # storage
    save_header = b""
    save_text_data = ""
    loading_save = False
    original_candy_value = 0
    last_total_candy = 0

    # Tk variables (initialized via init_vars)
    save_path = None
    total_candy_var = None
    candy_var = None
    level_var = None
    xp_var = None
    robotjumps_var = None
    monsterbashes_var = None
    suburbsbobbing_var = None
    mallbobbing_var = None
    countrybobbing_var = None
    selected_world = None
    costume_vars = None
    player_position_vars = None
    camera_position_vars = None

    @classmethod
    def init_vars(cls, root):
        cls.save_path = tk.StringVar()
        cls.total_candy_var = tk.StringVar(value="0")
        cls.candy_var = tk.StringVar(value="0")
        cls.level_var = tk.StringVar(value="1")
        cls.xp_var = tk.StringVar(value="0")
        cls.robotjumps_var = tk.StringVar(value="0")
        cls.monsterbashes_var = tk.StringVar(value="0")
        cls.suburbsbobbing_var = tk.StringVar(value="0")
        cls.mallbobbing_var = tk.StringVar(value="0")
        cls.countrybobbing_var = tk.StringVar(value="0")
        cls.selected_world = tk.StringVar(value="")
        # default to empty costume slots (UI will set defaults)
        cls.costume_vars = [tk.StringVar(value="") for _ in range(3)]
        cls.player_position_vars = [tk.DoubleVar(value=0.0) for _ in range(3)]
        cls.camera_position_vars = [tk.DoubleVar(value=0.0) for _ in range(3)]

# ---------------- utility / parsing ----------------
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

def update_or_add_field(text, field_name, new_value):
    """
    Update or insert field into save text. Handles vector fields (PlayerPosition, CameraPosition) specially.
    """
    is_vector = field_name in ["PlayerPosition", "CameraPosition"]
    if is_vector and isinstance(new_value, (tuple, list)):
        value_str = f"<{new_value[0]},{new_value[1]},{new_value[2]}>"
        pattern = fr"{field_name}=<[-.\d]+,[-.\d]+,[-.\d]+>"
        replacement = f"{field_name}={value_str}"
    else:
        # numeric or string - ensure terminator semicolon
        if isinstance(new_value, str) and not new_value.endswith(";"):
            if ";" in new_value:
                value_str = new_value
            else:
                value_str = f"{new_value};"
        else:
            value_str = str(new_value)
            if not value_str.endswith(";"):
                value_str = value_str + ";"
        # pattern allows decimals too
        pattern = fr"{field_name}\s*=\s*-?\d+(?:\.\d+)?;"
        replacement = f"{field_name}={value_str}"

    if re.search(pattern, text):
        return re.sub(pattern, replacement, text)
    # insert before EquippedCostumes if possible, else append
    insert_point = text.find("EquippedCostumes=")
    insert_text = replacement if replacement.endswith("\n") else replacement + "\n"
    if insert_point != -1:
        return text[:insert_point] + insert_text + text[insert_point:]
    else:
        return text.strip() + "\n" + insert_text

def update_save_data(
    text,
    new_level,
    xp,
    new_candy,
    new_total,
    new_world_path,
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
    text = update_or_add_field(text, "World", new_world_path)
    text = update_or_add_field(text, "PlayerPosition", player_pos)
    text = update_or_add_field(text, "CameraPosition", camera_pos)
    costume_str = ",".join([c for c in costumes if c])
    # replace full EquippedCostumes block if present
    text = re.sub(r"EquippedCostumes=\[[^\]]*\];", f"EquippedCostumes=[{costume_str}];", text)
    text = update_or_add_field(text, "RobotRampJumos", robotjumps)
    text = update_or_add_field(text, "MonsterPailBashes", monsterbashes)
    text = update_or_add_field(text, "SuburbsBobbingHighScore", suburbsbobbing)
    text = update_or_add_field(text, "MallBobbingHighScore", mallbobbing)
    text = update_or_add_field(text, "CountryBobbingHighScore", countrybobbing)
    return text

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
    world = None
    if match:
        path = match.group(1)
        world = next((k for k, v in WORLD_PATHS.items() if v == path), "Suburbs")
    else:
        world = "Suburbs"
    return (
        total, candy, costumes, xp,
        robot_jumps, monster_bashes,
        suburbsbobbing, mallbobbing, countrybobbing,
        player_position, camera_position, world
    )

# ---------------- file operations (UI calls these) ----------------
def open_save_dialog():
    """Open file dialog, read file, parse and populate AppState variables.
       Returns True on success, False otherwise."""
    path = filedialog.askopenfilename(title="Open Costume Quest Save File", filetypes=[("All Files", "*.*")])
    if not path:
        return False
    try:
        with open(path, "rb") as f:
            binary_data = f.read()
        header = binary_data[:8]
        raw = binary_data[8:]
        # try to find {Level=...} section for path detection
        start = raw.find(b"{Level=")
        end = raw.find(b"}", start)
        section = raw[start:end + 1].decode(errors="ignore") if start != -1 and end != -1 else ""
        # decode whole raw text
        raw_text = raw.decode(errors="ignore")

        # parse
        (
            total, candy, costumes, xp,
            robotjumps, monsterbashes,
            suburbsbobbing, mallbobbing, countrybobbing,
            player_pos, camera_pos, world
        ) = extract_save_data(raw_text)
    except Exception as e:
        messagebox.showerror("Load Error", f"Failed to parse save file:\n{e}")
        return False

    # set state
    AppState.loading_save = True
    AppState.total_candy_var.set(str(total))
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
    AppState.save_path.set(path)
    AppState.save_header = header
    AppState.save_text_data = raw_text
    AppState.loading_save = False
    return True

def populate_entries_from_state(cards_entries, battle_entries):
    """Given UI entry widget maps, fill them from AppState.save_text_data"""
    if not AppState.save_text_data:
        return
    # battle items
    for match in BATTLE_ITEM_PATTERN.finditer(AppState.save_text_data):
        item_key = match.group(2)
        current_amount = match.group(3)
        if item_key in battle_entries:
            entry = battle_entries[item_key]
            entry.delete(0, tk.END)
            entry.insert(0, current_amount)
    # creepytreat cards
    for match in CARD_PATTERN.finditer(AppState.save_text_data):
        card_num = int(match.group(2))
        current_amount = match.group(3)
        if card_num in cards_entries:
            cards_entries[card_num].delete(0, tk.END)
            cards_entries[card_num].insert(0, current_amount)

def _replace_card_values_in_text(text, cards_entries):
    updated = text
    for card_num, entry in cards_entries.items():
        val = entry.get().strip()
        if not val.isdigit():
            raise ValueError(f"Card {card_num} has invalid amount '{val}'")
        pattern = re.compile(
            rf'(TrickyTreatCard_{card_num}=InventoryItem\{{[^}}]*CurrentAmount=)(\d+)(;[^}}]*\}})'
        )
        updated = pattern.sub(rf'\g<1>{val}\g<3>', updated, count=1)
    return updated

def _replace_battle_values_in_text(text, battle_entries):
    updated = text
    for item_key, entry in battle_entries.items():
        val = entry.get().strip()
        if not val.isdigit():
            raise ValueError(f"{BATTLE_ITEM_NAMES.get(item_key, item_key)} has invalid amount '{val}'")
        pattern = re.compile(
            rf'(BattleItem_{item_key}=InventoryItem\{{[^}}]*?CurrentAmount=)(\d+)(;[^}}]*\}})'
        )
        updated = pattern.sub(rf'\g<1>{val}\g<3>', updated, count=1)
    return updated

def save_changes(cards_entries, battle_entries):
    """Write changes back to loaded save file path."""
    path = AppState.save_path.get()
    if not path:
        messagebox.showerror("Error", "No save file loaded.")
        return False
    try:
        new_candy = int(AppState.candy_var.get())
        new_total = int(AppState.total_candy_var.get())
        AppState.original_candy_value = new_candy
        AppState.last_total_candy = new_total
        selected_costumes = [var.get().strip() for var in AppState.costume_vars if var.get().strip()]
        xp = int(AppState.xp_var.get())
        new_level = int(AppState.level_var.get())
        new_world_path = WORLD_PATHS.get(AppState.selected_world.get(), WORLD_PATHS["Suburbs"])
        robotjumps = int(AppState.robotjumps_var.get())
        monsterbashes = int(AppState.monsterbashes_var.get())
        suburbsbobbing = int(AppState.suburbsbobbing_var.get())
        mallbobbing = int(AppState.mallbobbing_var.get())
        countrybobbing = int(AppState.countrybobbing_var.get())

        player_pos = tuple(var.get() for var in AppState.player_position_vars)
        camera_pos = tuple(var.get() for var in AppState.camera_position_vars)

        updated_text = AppState.save_text_data

        # Update card values and battle items first
        updated_text = _replace_card_values_in_text(updated_text, cards_entries)
        updated_text = _replace_battle_values_in_text(updated_text, battle_entries)

        # Now update general fields
        updated_text = update_save_data(
            updated_text,
            new_level,
            xp,
            new_candy,
            new_total,
            new_world_path,
            player_pos,
            camera_pos,
            selected_costumes,
            robotjumps,
            monsterbashes,
            suburbsbobbing,
            mallbobbing,
            countrybobbing
        )

        # write file (preserve header)
        with open(path, "wb") as f:
            f.write(AppState.save_header)
            f.write(updated_text.encode("utf-8"))
        # update in-memory copy
        AppState.save_text_data = updated_text
        messagebox.showinfo("Success", "Save file updated!")
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save: {e}")
        return False

def save_as(cards_entries, battle_entries):
    if not AppState.save_text_data:
        messagebox.showerror("Error", "No save file loaded.")
        return False
    path = filedialog.asksaveasfilename(
        title="Save As",
        defaultextension=".",
        filetypes=[("JSON File", "*.json"), ("Text File", "*.txt"), ("All Files", "*.*")]
    )
    if not path:
        return False
    try:
        # Build updated_text the same way as save_changes
        updated_text = AppState.save_text_data
        updated_text = _replace_card_values_in_text(updated_text, cards_entries)
        updated_text = _replace_battle_values_in_text(updated_text, battle_entries)

        new_candy = int(AppState.candy_var.get())
        new_total = int(AppState.total_candy_var.get())
        selected_costumes = [var.get().strip() for var in AppState.costume_vars if var.get().strip()]
        xp = int(AppState.xp_var.get())
        new_level = int(AppState.level_var.get())
        new_world_path = WORLD_PATHS.get(AppState.selected_world.get(), WORLD_PATHS["Suburbs"])
        robotjumps = int(AppState.robotjumps_var.get())
        monsterbashes = int(AppState.monsterbashes_var.get())
        suburbsbobbing = int(AppState.suburbsbobbing_var.get())
        mallbobbing = int(AppState.mallbobbing_var.get())
        countrybobbing = int(AppState.countrybobbing_var.get())
        player_pos = tuple(var.get() for var in AppState.player_position_vars)
        camera_pos = tuple(var.get() for var in AppState.camera_position_vars)

        updated_text = update_save_data(
            updated_text,
            new_level,
            xp,
            new_candy,
            new_total,
            new_world_path,
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
            import json
            data = {
                "Level": new_level,
                "ExperiencePoints": xp,
                "CandyAmount": new_candy,
                "TotalCandyAmount": new_total,
                "World": new_world_path,
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
                json.dump(data, f, indent=4)
        elif path.endswith(".txt"):
            data = [
                f"Level: {new_level}",
                f"Experience Points: {xp}",
                f"Current Candy Amount: {new_candy}",
                f"Total Candy Amount: {new_total}",
                f"World: {new_world_path}",
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
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save: {e}")
        return False

def backup_save():
    path = AppState.save_path.get()
    if not path:
        messagebox.showerror("Error", "No save file loaded.")
        return False
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{path}_backup_{timestamp}"
        shutil.copy2(path, backup_path)
        messagebox.showinfo("Backup Created", f"Backup saved as:{backup_path}")
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create backup: {e}")
        return False