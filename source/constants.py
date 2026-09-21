import re
import os
import sys

BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
CARDS_DIR = os.path.join(BASE_DIR, "images", "cards")
STAMP_DIR = os.path.join(BASE_DIR, "images", "battle_stamps")

NAMES = ["Reynold/Wren", "Everett", "Lucy"]

XP_THRESHOLDS = {
    1: 0, 2: 2500, 3: 6000, 4: 12000, 5: 20000,
    6: 31000, 7: 45000, 8: 62000, 9: 82000, 10: 105000
}

#Costume Pattern/Pieces
COSTUME_PIECES = {
    "Robot": {
        "CostumePattern_Robot": "Robot Pattern",
        "CostumePiece_Wheelies": "Roller Skate Shoes",
        "CostumePiece_CardboardBox": "Cardboard Box",
        "CostumePiece_AluminumFoil": "Aluminum Foil"
    },
    "Knight": {
        "CostumePattern_": "",
        "CostumePiece_": "",
        "CostumePiece_": "",
        "CostumePiece_": "",
    },
    "Statue of Liberty": {
        "CostumePattern_StatueOfLiberty": "Statue of Liberty Pattern",
        "CostumePiece_Sheet": "Sheet",
        "CostumePiece_Cardboard": "Cardboard",
        "CostumePiece_FeatherDuster": "Feather Duster",
    },
    "Space Warrior": {
        "CostumePattern_SpaceWarrior": "Space Warrior Pattern",
        "CostumePiece_SafetyVisor": "Safety Visor",
        "CostumePiece_EmptySodaBottle": "Empty Soda Bottle",
        "CostumePiece_SnowBoots": "Snow Boots",
    },
    "Ninja": {
        "CostumePattern_Ninja": "Ninja Pattern",
        "CostumePiece_SweatPants": "Sweat Pants",
        "CostumePiece_Scarf": "Scarf",
        "CostumePiece_Rope": "Rope",
    },
    "Unicorn": {
        "CostumePattern_Unicorn": "Unicorn Pattern",
        "CostumePiece_Fabric": "Fabric",
        "CostumePiece_Glitter": "Glitter",
        "CostumePiece_Yarn": "Yarn",
    },
    "Pumpkin": {
        "CostumePattern_Pumpkin": "Pumpkin Pattern",
        "CostumePiece_PaperMache": "Paper Mache",
        "CostumePiece_OrangePaint": "Paint",
        "CostumePiece_Leaves": "Leaves",
    },
    "Vampire": {
        "CostumePattern_Vampire": "Vampire Pattern",
        "CostumePiece_BlackCloth": "Black Cloth",
        "CostumePiece_ScaryFangs": "Scary Fangs",
        "CostumePiece_WhiteMakeup": "White Makeup",
    },
    "French Fries": {
        "CostumePattern_": "",
        "CostumePiece_": "",
        "CostumePiece_": "",
        "CostumePiece_": "",
    },
    "Black Cat": {
        "CostumePattern_": "",
        "CostumePiece_": "",
        "CostumePiece_": "",
        "CostumePiece_": "",
    },
    "Grubbin": {
        "CostumePattern_Grubbin": "Grubbin Pattern",
        "CostumePiece_BurlapSack": "Burlap Sack",
        "CostumePiece_DirtySocks": "Dirty Socks",
        "CostumePiece_GrubbinMask": "Grubbin Mask",
    }
}

DEBUG_TELEPORTS = {
    "Suburbs": {
        "Reynold & Wren's House": (-25.5, 3.3, 33.3),
        "Everett/Knight Costume": (11.3,2.9,22.2),
        "Bobbing for Apples": (126.0, 4.0, 60.0),
        "First Storm Drain": (117.0, 3.5, 161.0),
        "Second Storm Drain": (157.0, 3.5, -5.0),
        "Cemetery/Scarecrow": (67.0, 9.0, -77.0)
    },
    "Autumn Haven Mall": {
        "Mall Entrance": (-103.5, 55.5, 119.5),
        "Central Station": (153.1, 39.4, -185.6),
        "Mall (Second Floor)": (194.0, 38.5, -140.0),
        "Mall (Third Floor)": (117.5, 45.0, -147.0)
    },
    "Fall Valley": {
        "Vine Cage": (-22.5, 37.5, 117.3),
        "Fry Stand": (-49.0, 2.5, -32.0),
        "Carnival": (-8.0, 6.3, 62.0),
        "Scarecrow": (33.0, 6.0, 41.0),
        "Maze (Center)": (106.5, 3.5, 38.0),
        "Maze (End)": (60.0, 5.0, 93.5),
        "Dorsilla/Big Bones": (-12.0, 36.0, 122.0)
    }
}

WORLD_PATHS = {
    "Suburbs": "worlds/cq_suburbs/cq_suburbs",
    "Autumn Haven Mall": "worlds/cq_mall_interior/cq_mall_interior",
    "Fall Valley": "worlds/cq_fallvalley/cq_fallvalley"
}

COSTUME_OPTIONS = [
    # Base Game Costumes
    "Robot", "Knight", "Statue Of Liberty",
    "Space Warrior", "Ninja", "Unicorn",
    "Pumpkin", "Vampire", "French Fries",
    "Black Cat", "Grubbin"
]

COSTUME_DISPLAY_NAMES = {
    # Base Game Costumes
    "Costume_Robot": "Robot",
    "Costume_Knight": "Knight",
    "Costume_StatueOfLiberty": "Statue Of Liberty",
    "Costume_SpaceWarrior": "Space Warrior",
    "Costume_Ninja": "Ninja",
    "Costume_Unicorn": "Unicorn",
    "Costume_Pumpkin": "Pumpkin",
    "Costume_Vampire": "Vampire",
    "Costume_FrenchFries": "French Fries",
    "Costume_BlackCat": "Black Cat",
    "Costume_Grubbin": "Grubbin"
}

CARD_NAMES = {
    # Base Game Cards
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

CARD_IMAGES = {
    num: os.path.join(CARDS_DIR, f"trickcard_{num:03}.png")
    for num in CARD_NAMES.keys()
}

CARD_PATTERN = re.compile(
    r'(TrickyTreatCard_(\d+)=InventoryItem\{[^}]*CurrentAmount=)(\d+)(;[^}]*\})'
)

BATTLE_ITEM_NAMES = {
    # Base Game Stamps
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

BATTLE_STAMP_IMAGES = {
    key: os.path.join(STAMP_DIR, f"stamp_{i+1:03}.png")
    for i, key in enumerate(BATTLE_ITEM_NAMES.keys())
}

BATTLE_ITEM_PATTERN = re.compile(
    r'(BattleItem_(\w+)=InventoryItem\{[^}]*?CurrentAmount=)(\d+)(;[^}]*\})'
)