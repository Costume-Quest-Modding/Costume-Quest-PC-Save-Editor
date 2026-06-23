import re
from constants import XP_THRESHOLDS, WORLD_PATHS

def extract_save_data(text):
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
    return (
        total, candy, costumes, xp,
        robot_jumps, monster_bashes,
        suburbsbobbing, mallbobbing, countrybobbing,
        player_position, camera_position, world
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


def calculate_level_from_xp(xp):
    for lvl in sorted(XP_THRESHOLDS, reverse=True):
        if xp >= XP_THRESHOLDS[lvl]:
            return lvl
    return 1