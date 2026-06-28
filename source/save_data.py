from dataclasses import dataclass
import re
import saveio
from constants import WORLD_PATHS, BATTLE_ITEM_NAMES, XP_THRESHOLDS

@dataclass(frozen=True)
class ParsedSaveData:
    total_candy: int
    current_candy: int
    equipped_costumes: list[str]
    experience_points: int
    robot_ramp_jumps: int
    monster_pail_bashes: int
    suburbs_bobbing_high_score: int
    mall_bobbing_high_score: int
    country_bobbing_high_score: int
    player_position: tuple[float, float, float]
    camera_position: tuple[float, float, float]
    world: str


def extract_save_data(text) -> ParsedSaveData:
    total = extract_int(r"TotalCandyAmount=(\d+);", text)
    candy_matches = list(re.finditer(r"CandyAmount\s*=\s*(\d+);", text))
    candy = int(candy_matches[-1].group(1)) if candy_matches else 0
    costume_match = re.search(r"EquippedCostumes=\[([^\]]*)\];", text)
    costumes = [c.strip().replace("Costume_", "")
    for c in costume_match.group(1).split(",")
    if c.strip()] if costume_match else []
    
    xp = extract_int(r"ExperiencePoints\s*=\s*(\d+);", text)
    robot_jumps = extract_int(r"RobotRampJumos=(\d+)", text)
    monster_bashes = extract_int(r"MonsterPailBashes=(\d+)", text)
    suburbsbobbing = extract_int(r"SuburbsBobbingHighScore=(\d+)", text)
    mallbobbing = extract_int(r"MallBobbingHighScore=(\d+)", text)
    countrybobbing = extract_int(r"CountryBobbingHighScore=(\d+)", text)
    player_position = extract_vector3(
        r"PlayerPosition=<([-.\d]+),([-.\d]+),([-.\d]+)>", text)
    camera_position = extract_vector3(
        r"CameraPosition=<([-.\d]+),([-.\d]+),([-.\d]+)>", text)

    match = re.search(r"Level=([^;]+);", text)
    world = next((k for k, v in WORLD_PATHS.items()
                 if v in match.group(1)), "Suburbs") if match else "Suburbs"
    return ParsedSaveData(
        total_candy=total,
        current_candy=candy,
        equipped_costumes=costumes,
        experience_points=xp,
        robot_ramp_jumps=robot_jumps,
        monster_pail_bashes=monster_bashes,
        suburbs_bobbing_high_score=suburbsbobbing,
        mall_bobbing_high_score=mallbobbing,
        country_bobbing_high_score=countrybobbing,
        player_position=player_position,
        camera_position=camera_position,
        world=world,
    )


def extract_int(pattern, text, default=0):
    match = re.search(pattern, text)
    return int(match.group(1)) if match else default


def extract_vector3(pattern, text):
    match = re.search(pattern, text)
    if match:
        return tuple(float(match.group(i)) for i in range(1, 4))
    return (0.0, 0.0, 0.0)


def extract_quests(text):
    """
    Returns a list of completed quest IDs from the QuestAccomplishments=[...] list.
    """
    match = re.search(r"QuestAccomplishments=\[([A-Za-z0-9_,]+)\];", text)
    if match:
        quests_str = match.group(1)
        # Split by comma and remove empty strings
        return [q.strip() for q in quests_str.split(",") if q.strip()]
    return []

# ---------------- helpers ----------------

def update_or_add_field(text, field_name, new_value):
    is_vector = field_name in ["PlayerPosition", "CameraPosition"]

    if is_vector and isinstance(new_value, (tuple, list)):
        value_str = f"<{new_value[0]},{new_value[1]},{new_value[2]}>"
        pattern = fr"{field_name}=<[-.\d]+,[-.\d]+,[-.\d]+>"
        replacement = f"{field_name}={value_str}"

    elif isinstance(new_value, (int, float)):
        value_str = str(new_value)
        if not value_str.endswith(";"):
            value_str += ";"
        pattern = fr"{field_name}\s*=\s*-?\d+(?:\.\d+)?;"
        replacement = f"{field_name}={value_str}"

    else:
        value_str = str(new_value)
        if not value_str.endswith(";"):
            value_str += ";"
        pattern = fr"{field_name}\s*=\s*.*?;"
        replacement = f"{field_name}={value_str}"

    if re.search(pattern, text):
        return re.sub(pattern, replacement, text, count=1)

    insert_point = text.find("EquippedCostumes=")
    insert_text = replacement + "\n"

    if insert_point != -1:
        return text[:insert_point] + insert_text + text[insert_point:]

    return text.strip() + "\n" + insert_text


def update_save_data(
    text,
    selected_world,
    new_level,
    xp,
    new_candy,
    new_total,
    player_pos,
    camera_pos,
    costumes,
    robotjumps,
    monsterbashes,
    suburbsbobbing,
    mallbobbing,
    countrybobbing
):
    text = update_or_add_field(text, "Level", get_level_path_from_selected_world(selected_world))
    text = update_or_add_field(text, "ExperiencePoints", xp)
    text = saveio.update_current_candy(text, new_candy)
    text = update_or_add_field(text, "TotalCandyAmount", new_total)
    text = update_or_add_field(text, "PlayerPosition", player_pos)
    text = update_or_add_field(text, "CameraPosition", camera_pos)

    costume_str = ",".join(
        f"Costume_{c}" if not c.startswith("Costume_") else c
        for c in costumes if c
    )
    text = re.sub(
        r"EquippedCostumes=\[[^\]]*\];",
        f"EquippedCostumes=[{costume_str}];",
        text
    )

    text = update_or_add_field(text, "RobotRampJumos", robotjumps)
    text = update_or_add_field(text, "MonsterPailBashes", monsterbashes)
    text = update_or_add_field(text, "SuburbsBobbingHighScore", suburbsbobbing)
    text = update_or_add_field(text, "MallBobbingHighScore", mallbobbing)
    text = update_or_add_field(text, "CountryBobbingHighScore", countrybobbing)

    return text


# ---------------- inventory replacements ----------------

def replace_cards(text, cards_entries):
    updated = text
    for card_num, entry in cards_entries.items():
        val = entry.get().strip()
        if not val.isdigit():
            raise ValueError(f"Card {card_num} invalid value {val}")

        pattern = re.compile(
            rf'(TrickyTreatCard_{card_num}=InventoryItem\{{[^}}]*CurrentAmount=)(\d+)(;[^}}]*\}})'
        )
        updated = pattern.sub(rf'\g<1>{val}\g<3>', updated, count=1)
    return updated


def replace_battle(text, battle_entries):
    updated = text
    for item_key, entry in battle_entries.items():
        val = entry.get().strip()
        if not val.isdigit():
            raise ValueError(
                f"{BATTLE_ITEM_NAMES.get(item_key, item_key)} invalid value {val}"
            )

        pattern = re.compile(
            rf'(BattleItem_{item_key}=InventoryItem\{{[^}}]*?CurrentAmount=)(\d+)(;[^}}]*\}})'
        )
        updated = pattern.sub(rf'\g<1>{val}\g<3>', updated, count=1)

    return updated


def replace_quests(text, quest_flags):
    quest_str = ",".join(quest_flags)

    if re.search(r"QuestAccomplishments=\[.*?\];", text):
        return re.sub(
            r"QuestAccomplishments=\[.*?\];",
            f"QuestAccomplishments=[{quest_str}];",
            text
        )

    insert_point = text.find("EquippedCostumes=")
    insert_text = f"QuestAccomplishments=[{quest_str}];\n"

    if insert_point != -1:
        return text[:insert_point] + insert_text + text[insert_point:]

    return text.strip() + "\n" + insert_text

def calculate_level_from_xp(xp):
    for lvl in sorted(XP_THRESHOLDS, reverse=True):
        if xp >= XP_THRESHOLDS[lvl]:
            return lvl
    return 1

def get_level_path_from_selected_world(selected_world):
    #world_name = AppState.selected_world.get()
    return WORLD_PATHS.get(selected_world, WORLD_PATHS["Suburbs"])