# constants.py
import re
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARDS_DIR = os.path.join(BASE_DIR, "images", "cards")
STAMP_DIR = os.path.join(BASE_DIR, "images", "battle_stamps")

XP_THRESHOLDS = {
    1: 0, 2: 2500, 3: 6000, 4: 12000, 5: 20000,
    6: 31000, 7: 45000, 8: 62000, 9: 82000, 10: 105000,
    11: 130000, 12: 160000, 13: 200000, 14: 250000,
}

NAMES = ["Reynold/Wren", "Everett", "Lucy"]

MAP_IMAGES = {
    "Suburbs": os.path.join(BASE_DIR, "images", "maps", "suburbs.png"),
    "Autumn Haven Mall": os.path.join(BASE_DIR, "images", "maps", "mall.png"),
    "Fall Valley": os.path.join(BASE_DIR, "images", "maps", "fall_valley.png")
}

MAP_ICONS = {
    "house": os.path.join(BASE_DIR, "images", "mapicons", "house.png"),
    "monster_house": os.path.join(BASE_DIR, "images", "mapicons", "monster_house.png"),
    # add later, ideas include: shop, chest, npc's, hide and seek kids, bobbing for apples, etc.
}

QUEST_FLAG_MAP = {
    # Individual component quests
    "Door N Skeleton - First Door": ["DoorNSkeleton_FirstDoor"],
    "Door N Skeleton - Second Door": ["DoorNSkeleton_SecondDoor"],
    "Suburbs MQ1 - Car Wreck": ["Burbs_MQ1_CarWreck"],
    "L_010 - No Costume Started": ["L_010_NoCostumeStarted"],

    # Parent quests
    # Robot Repair
    "Robot Repair": {
        "started": [
            "DoorNSkeleton_FirstDoor",
            "DoorNSkeleton_SecondDoor",
            "Burbs_MQ1_CarWreck",
            "L_010_NoCostumeStarted"
        ],
        "completed": [
            "DoorNSkeleton_FirstDoor",
            "DoorNSkeleton_SecondDoor",
            "Burbs_MQ1_CarWreck",
            "L_010_NoCostumeStarted",
            "L_010_BashTutorialDone",
            "RobotPiece_TreasureChest1",
            "RobotPiece_TreasureChest2",
            "RobotPiece_TreasureChest3",
            "L_010_TreasureTutorialDone",
            "Burbs_MQ1_Ramp",
            "RobotRamp"
        ]
    }
}


QUESTS = {
    "Suburbs": {
        "Robot Repair": {
            "questtype": "Main",
            "description": "Dorsilla ruined my costume! I need to rebuild it!",
            "how_to_complete": "\nOpen all 3 treasure coffins in the alley to rebuild the Robot costume.",
            "reward": "300 XP"
        },
        "Programmed for Protection": {
            "questtype": "Main",
            "description": "Bullies are oppressing the weak in Auburn Pines! They must be stopped!",
            "how_to_complete": "\nTalk to Travis twice to get the quest."
            "\nRun away from him using the Robot's Boost ability.",
            "reward": "300 XP"
        },
        "Pie for the Putterpam": {
            "questtype": "Main",
            "description": "Mrs. Putterpam is in need of a pie ingredient.",
            "how_to_complete": "\nTalk to Mrs. Putterpam to get the quest."
            "\nFind her the missing ingredient (Cherries). (Must complete \"The Patriot's Party\" first.)"
            "\nReturn to her with the ingredient.",
            "reward": "300 XP"
        },
        "The Patriot's Party": {
            "questtype": "Main",
            "description": "Russell won't let us into his awesome party.",
            "how_to_complete": "\nTalk to Russell to get the quest."
            "\nTalk to 4 NPCs to build the Liberty Costume. (One has a Costume Pattern and 3 have Costume Pieces)"
            "\nTalk again to Russell (as the Liberty Costume) to enter the party.",
            "reward": "300 XP"
        },
        "These Tombstones Aren't Styrofoam": {
            "questtype": "Main",
            "description": "Get through the cemetery and find Monster HQ!",
            "how_to_complete": "\nOpen the Monster Gate and enter the Cemetery to start the quest."
            "\nTrigger the cutscene at the end of the Cemetery to finish the quest.",
            "reward": "300 XP"
        },
        "Suburbs Bobbing for Apples": {
            "questtype": "Side",
            "description": "Bob for Apples!",
            "how_to_complete": "\nComplete 3 rounds of Apple Bobbing to finish the quest.",
            "reward": "\n20 Candy (Round 1)"
            "\n50 Candy (Round 2)"
            "\nSweet Tooth Creepy Treat Card (Round 3)"
        },
        "Auburn Pines Hide 'n' Seek": {
            "questtype": "Side",
            "description": "Find all six kids hiding in Auburn Pines.",
            "how_to_complete": "\nTalk to six kids hiding around Auburn Pines."
            "\nUse the \"Map\" tab within this program if you need help locating any 6 of them.",
            "reward": "[TODO]"
        },
        "This Card Is So Rare": {
            "questtype": "Side",
            "description": "Trade with a fellow Creepy Treat collector to get a rare card! ",
            "how_to_complete": "Trade Scott your duplicate Glop Creepy Treat Card.",
            "reward": "200 XP\nChoconana Creepy Treat Card"
        },
        "Suburbs Collect 'em All": {
            "questtype": "Side",
            "description": "Trade with a fellow Creepy Treat collector!",
            "how_to_complete": "Trade Austin your duplicate Fruity Foam Creepy Treat Card.",
            "reward": "200 XP\nJelly Has-Beens Creepy Treat Card"
        }
    },
    "Autumn Haven Mall": {
        "Tickets for Treats": {
            "questtype": "Main",
            "description": "[TODO]",
            "how_to_complete": "[TODO]",
            "reward": "[TODO]"
        },
        "Earn Your Monster Slayer Badge": {
            "questtype": "Main",
            "description": "[TODO]",
            "how_to_complete": "[TODO]",
            "reward": "[TODO]"
        },
        "The Mall-O-Rail is Broken": {
            "questtype": "Main",
            "description": "[TODO]",
            "how_to_complete": "[TODO]",
            "reward": "[TODO]"
        },
        "The Dark Side of the Mall": {
            "questtype": "Main",
            "description": "[TODO]",
            "how_to_complete": "[TODO]",
            "reward": "[TODO]"
        },
        "Extreme Costume Challenge!": {
            "questtype": "Main",
            "description": "[TODO]",
            "how_to_complete": "[TODO]",
            "reward": "[TODO]"
        },
        "This Card Is Rarer": {
            "questtype": "Side",
            "description": "[TODO]",
            "how_to_complete": "[TODO]",
            "reward": "[TODO]"
        },
        "Mall Collect 'em All": {
            "questtype": "Side",
            "description": "[TODO]",
            "how_to_complete": "[TODO]",
            "reward": "[TODO]"
        },
        "Mall Bobbing for Apples": {
            "questtype": "Side",
            "description": "Bob for Apples!",
            "how_to_complete": "\nComplete 3 rounds of Apple Bobbing to finish the quest.",
            "reward": "\n20 Candy (Round 1)"
            "\n50 Candy (Round 2)"
            "\nPizza Sundae Creepy Treat Card (Round 3)"
        },
        "Mall Hide 'n' Seek": {
            "questtype": "Side",
            "description": "Find all six kids hiding in Autumn Haven Mall.",
            "how_to_complete": "\nTalk to six kids hiding around Autumn Haven Mall."
            "\nUse the \"Map\" tab within this program if you need help locating any 6 of them.",
            "reward": "500 XP\nCandy Pail Upgrade: Pumpkin Pail"
        }
    },
    "Fall Valley": {
        "The Original Costume Quest": {
            "questtype": "Main",
            "description": "Get our costumes back from the Repugians!",
            "how_to_complete": "\nHead to Town and obtain the Fry Costume from Chip."
            "\nHead back to the Repugians and use the Fry Costume to lure both of them into the barn."
            "\nOpen the Treasure Coffin nearby to retrieve your costumes."
            "\nLure 3 customers to Chip's Fry Stand while wearing the Fry Costume."
            "\nTalk to Henry to enter the Carnival."
            "\nBattle the Monsters near the Ferris Wheel."
            "\nUse the Ninja Costume to sneak past Orzo."
            "\nUse the Space Warrior Costume to get through the Darkness to finish the quest.",
            "reward": "300 XP"
        },
        "All's Fair That Ends Fare": {
            "questtype": "Main",
            "description": "Something fishy is afoot at the Carnival.",
            "how_to_complete": "[TODO]",
            "reward": "[TODO]"
        },
        "Children of the High Fructose Corn Syrup": {
            "questtype": "Main",
            "description": "[TODO]",
            "how_to_complete": "\nEnter the Maze area and talk to the Grubbin to get the quest and Grubbin Costume Pattern."
            "\nFind the Grubbin Costume Pieces by talking to 3 NPCs in Maze."
            "\nHead to the Repugian Guard blocking one of the Maze paths and while wearing the Grubbin Costume to finish the quest.",
            "reward": "300 XP"
        },
        "Fall Valley Hide 'n' Seek": {
            "questtype": "Side",
            "description": "Find all six kids hiding in Fall Valley.",
            "how_to_complete": "\nTalk to six kids hiding around Fall Valley."
            "\nUse the \"Map\" tab within this program if you need help locating any 6 of them.",
            "reward": "500 XP\nCandy Pail Upgrade: Bat Bucket."
            "\nNote: Completing this quest actually gives 300XP in-game, but for consistency with other Hide 'n Seek quests, it's set to 500XP here."
        },
        "Fall Valley Bobbing for Apples": {
            "questtype": "Side",
            "description": "Bob for Apples!",
            "how_to_complete": "\nComplete 3 rounds of Apple Bobbing to finish the quest.",
            "reward": "\n20 Candy (Round 1)"
            "\n50 Candy (Round 2)"
            "\nSugar Bucket Creepy Treat Card (Round 3)"
        },
        "This Card Is The Rarest": {
            "questtype": "Side",
            "description": "Trade with a fellow Creepy Treat collector to get a rare card!",
            "how_to_complete": "Trade Nathan your duplicate Street Chews Creepy Treat Card.",
            "reward": "200 XP\nMice Crispy Treat Creepy Treat Card"
        },
        "Fall Valley Collect 'em All": {
            "questtype": "Side",
            "description": "Trade with a fellow Creepy Treat collector!",
            "how_to_complete": "Trade Rebecca your duplicate Unicorn Pellets Creepy Treat Card.",
            "reward": "200 XP\nJelly Has-Beens Creepy Treat Card"
        }
    }
}

MAP_HOUSES = {
    # Houses are 15x15.
    "Suburbs": {
        "StartHouse01": {
            "coords": (140, 485, 155, 500),
            "name": "StartHouse01",
            "category": "House",
            "subtype": "Cutscene",
            "internal_name": "N/A",
            "description": "Reynold/Wren's House",
            "reward": "N/A"
        },
        "StartHouse02": {
            "coords": (160, 452, 175, 467),
            "name": "StartHouse02",
            "category": "House",
            "subtype": "Candy",
            "internal_name": "N/A",
            "description": "N/A",
            "reward": "100 Candy"
        },
        "StartHouse03": {
            "coords": (180, 442, 195, 457),
            "name": "StartHouse03",
            "category": "House",
            "subtype": "Cutscene",
            "internal_name": "N/A",
            "description": "Sibling Gets Kidnapped",
            "reward": "N/A"
        },
        "House01": {
            "coords": (310, 315, 325, 330),
            "name": "House01",
            "category": "House",
            "subtype": "Candy",
            "internal_name": "FriendlySuburbDoor15",
            "description": "N/A",
            "reward": "50 Candy"
        },
        "House02": {
            "coords": (320, 210, 335, 225),
            "name": "House02",
            "category": "House",
            "subtype": "Candy",
            "internal_name": "FriendlySuburbDoor18",
            "description": "N/A",
            "reward": "50 Candy"
        },
        "House03": {
            "coords": (405, 155, 420, 170),
            "name": "House03",
            "category": "House",
            "subtype": "Candy",
            "internal_name": "FriendlySuburbDoor19",
            "description": "N/A",
            "reward": "50 Candy"
        },
        "House04": {
            "coords": (405, 360, 420, 375),
            "name": "House04",
            "category": "House",
            "subtype": "Candy",
            "internal_name": "FriendlySuburbDoor12",
            "description": "N/A",
            "reward": "50 Candy"
        },
        "House05": {
            "coords": (450, 300, 465, 315),
            "name": "House05",
            "category": "House",
            "subtype": "Candy",
            "internal_name": "FriendlySuburbDoor14",
            "description": "N/A",
            "reward": "50 Candy"
        },
        "House06": {
            "coords": (508, 358, 523, 373),
            "name": "House06",
            "category": "House",
            "subtype": "Candy",
            "internal_name": "FriendlySuburbDoor7",
            "description": "N/A",
            "reward": "50 Candy"
        },
        "House07": {
            "coords": (630, 400, 645, 415),
            "name": "House07",
            "category": "House",
            "subtype": "Candy",
            "internal_name": "FriendlySuburbDoor27",
            "description": "N/A",
            "reward": "50 Candy"
        },
        "House08": {
            "coords": (680, 250, 695, 265),
            "name": "House08",
            "category": "House",
            "subtype": "Candy",
            "internal_name": "FriendlySuburbDoor22",
            "description": "N/A",
            "reward": "50 Candy"
        },
        "House09": {
            "coords": (585, 115, 600, 130),
            "name": "House09",
            "category": "House",
            "subtype": "Candy",
            "internal_name": "FriendlySuburbDoor24",
            "description": "N/A",
            "reward": "50 Candy"
        },
        "House10": {
            "coords": (480, 135, 495, 150),
            "name": "House10",
            "category": "House",
            "subtype": "Candy",
            "internal_name": "FriendlySuburbDoor28",
            "description": "N/A",
            "reward": "50 Candy"
        },
        "MonsterHouse01": {
            "coords": (255, 270, 270, 285),
            "name": "MonsterHouse01",
            "category": "House",
            "subtype": "Monster",
            "internal_name": "MonsterSuburbDoor1",
            "description": "N/A",
            "reward": "25 Candy"
        },
        "MonsterHouse02": {
            "coords": (370, 260, 385, 275),
            "name": "MonsterHouse02",
            "category": "House",
            "subtype": "Monster",
            "internal_name": "MonsterSuburbDoor2",
            "description": "N/A",
            "reward": "25 Candy"
        },
        "MonsterHouse03": {
            "coords": (580, 365, 595, 380),
            "name": "MonsterHouse03",
            "category": "House",
            "subtype": "Monster",
            "internal_name": "MonsterSuburbDoor3",
            "description": "N/A",
            "reward": "25 Candy"
        },
        "MonsterHouse04": {
            "coords": (475, 200, 490, 215),
            "name": "MonsterHouse04",
            "category": "House",
            "subtype": "Monster",
            "internal_name": "MonsterSuburbDoor4",
            "description": "N/A",
            "reward": "25 Candy"
        },
        "MonsterHouse05": {
            "coords": (685, 350, 700, 365),
            "name": "MonsterHouse05",
            "category": "House",
            "subtype": "Monster",
            "internal_name": "MonsterSuburbDoor5",
            "description": "N/A",
            "reward": "25 Candy"
        },
        "MonsterHouse06": {
            "coords": (520, 70, 535, 85),
            "name": "MonsterHouse06",
            "category": "House",
            "subtype": "Monster",
            "internal_name": "MonsterSuburbDoor6",
            "description": "N/A",
            "reward": "50 Candy"
        },
        "MonsterHouse07": {
            "coords": (650, 160, 665, 175),
            "name": "MonsterHouse07",
            "category": "House",
            "subtype": "Monster",
            "internal_name": "MonsterSuburbDoor7",
            "description": "N/A",
            "reward": "50 Candy"
        },
        "MonsterHouse08": {
            "coords": (458, 423, 473, 438),
            "name": "MonsterHouse08",
            "category": "House",
            "subtype": "Monster",
            "internal_name": "MonsterSuburbDoor8",
            "description": "N/A",
            "reward": "25 Candy"
        }
    },
    "Autumn Haven Mall": {
        "Kiosk_01": {
            "coords": (150, 150, 200, 200),
            "name": "1",
            "category": "2",
            "subtype": "3",
            "internal_name": "4",
            "description": "5",
            "reward": "6"
        },
        "Store_01": {
            "coords": (260, 140, 330, 210),
            "name": "1",
            "category": "2",
            "subtype": "3",
            "internal_name": "4",
            "description": "5",
            "reward": "6"
        },
        "Store_02": {
            "coords": (390, 100, 460, 170),
            "name": "1",
            "category": "2",
            "subtype": "3",
            "internal_name": "4",
            "description": "5",
            "reward": "6"
        }
    },
    "Fall Valley": {
        "Tent_01": {
            "coords": (80, 220, 140, 280),
            "name": "1",
                    "category": "2",
                    "subtype": "3",
                    "internal_name": "4",
                    "description": "5",
                    "reward": "6"
        },
        "Festival_Stand": {
            "coords": (200, 160, 250, 210),
            "name": "1",
            "category": "2",
            "subtype": "3",
            "internal_name": "4",
            "description": "5",
            "reward": "6"
        },
        "House_01": {
            "coords": (420, 120, 470, 170),
            "name": "1",
            "category": "2",
            "subtype": "3",
            "internal_name": "4",
            "description": "5",
            "reward": "6"
        }
    }
}

DEBUG_TELEPORTS = {
    "Suburbs": {
        "Reynold & Wren's House": (-25.5, 3.3, 33.3),
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
    },
    "Repugia": {
        "Spawn (New Game)": (-90.9, 53.3, -0.4)
    }
}

WORLD_PATHS = {
    # Base Game Worlds
    "Suburbs": "worlds/cq_suburbs/cq_suburbs",
    "Autumn Haven Mall": "worlds/cq_mall_interior/cq_mall_interior",
    "Fall Valley": "worlds/cq_fallvalley/cq_fallvalley",
    # DLC Worlds
    "Repugia": "worlds/cq_repugia/cq_repugia"
}

COSTUME_OPTIONS = [
    "Costume_Robot", "Costume_Knight", "Costume_StatueOfLiberty",
    "Costume_SpaceWarrior", "Costume_Ninja", "Costume_Unicorn",
    "Costume_Pumpkin", "Costume_Vampire", "Costume_FrenchFries",
    "Costume_BlackCat", "Costume_Grubbin"
]

COSTUME_DISPLAY_NAMES = {
    "Costume_Robot": "Robot",
    "Costume_Knight": "Knight",
    "Costume_StatueOfLiberty": "Statue of Liberty",
    "Costume_SpaceWarrior": "Space Warrior",
    "Costume_Ninja": "Ninja",
    "Costume_Unicorn": "Unicorn",
    "Costume_Pumpkin": "Pumpkin",
    "Costume_Vampire": "Vampire",
    "Costume_FrenchFries": "French Fries",
    "Costume_BlackCat": "Black Cat",
    "Costume_Grubbin": "Grubbin"
}

CARD_PATTERN = re.compile(
    r'(TrickyTreatCard_(\d+)=InventoryItem\{[^}]*CurrentAmount=)(\d+)(;[^}]*\})'
)

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
    54: "Gloop",
    # DLC Cards below here
    55: "Nutty Dumdums",
    56: "Strawberry Smackdown",
    57: "Cuttin' Candy",
    58: "Cake Cod",
    59: "Dietetic Marzipan",
    60: "Fansy Dollups",
    61: "Bubble Onions",
    62: "Glazed Butter Cubes",
    63: "Wikkids",
    64: "Dreamy Dipz",
    65: "Rainbow Whipz",
    66: "KLORKS!",
    67: "Caramold",
    68: "Sweet Wet Wheat",
    69: "Maple Crusties",
    70: "2-Headed Toddlers",
    71: "Red Hot Foam",
    72: "Wiggly Woozers"
}

CARD_IMAGES = {
    num: os.path.join(CARDS_DIR, f"trickcard_{num:03}.png")
    for num in CARD_NAMES.keys()
}

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


BATTLE_STAMP_IMAGES = {
    key: os.path.join(STAMP_DIR, f"stamp_{i+1:03}.png")
    for i, key in enumerate(BATTLE_ITEM_NAMES.keys())
}

# Helper for icon path if needed when packaged
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
