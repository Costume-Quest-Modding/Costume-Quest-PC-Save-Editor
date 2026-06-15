# constants.py
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

QUESTS = {
    "Suburbs": {
        # World 1 Info Finished and Correct
        # Now adding Quest Flags
        "Robot Repair": {
            "questtype": "Main",
            "description": "Dorsilla ruined my costume! I need to rebuild it!",
            "how_to_complete": "\n- Open all 3 treasure coffins in the alley to rebuild the Robot costume.",
            "reward": "300 XP",

            "flags": {
                "started": [
                    "DoorNSkeleton_FirstDoor",
                    "DoorNSkeleton_SecondDoor",
                    "Burbs_MQ1_CarWreck",
                    "L_010_NoCostumeStarted"
                ],
                "completed": [
                    "DoorNSkeleton_FirstDoor", # First Door Completed
                    "DoorNSkeleton_SecondDoor", # Second Door Completed
                    "Burbs_MQ1_CarWreck",
                    "L_010_NoCostumeStarted",
                    "L_010_BashTutorialDone",
                    "RobotPiece_TreasureChest1", # Aluminum Foil
                    "RobotPiece_TreasureChest2", # 
                    "RobotPiece_TreasureChest3", # 
                    "L_010_TreasureTutorialDone",
                    "Burbs_MQ1_Ramp",
                    "RobotRamp"
                ]
            }
        },
        "Programmed for Protection": {
            "questtype": "Main",
            "description": "Bullies are oppressing the weak in Auburn Pines! They must be stopped!",
            "how_to_complete": "\n- Talk to Travis get the quest."
            "\n- Talk to Travis again to start the chase."
            "\n- Run away from him using the Robot's Boost ability.",
            "reward": "300 XP",

            "flags": {
                "started": [
                    "Burbs_MQ_02_Started" # Quest Started
                ],
                "completed": [
                    "Burbs_MQ_02_Started", # Quest Started
                    "Burbs_MQ_02_RaceInProgress", # Race in Progress
                    "Burbs_MQ_02_WinCutscene", # Win Cutscene
                    "BMQ2_RaceOver", # Race Finished
                    "L01_bAlreadyInteracted", 
                    "L01_bEverettJoinedParty"
                ]
            }
        },
        "Pie for the Putterpam": {
            "questtype": "Main",
            "description": "Mrs. Putterpam is in need of a pie ingredient.",
            "how_to_complete": "\n- Talk to Mrs. Putterpam to get the quest."
            "\n- Find her the missing ingredient (Cherries). (Must complete \"The Patriot's Party\" first.)"
            "\n- Talk to her to return the ingredient.",
            "reward": "300 XP"
        },
        "The Patriot's Party": {
            "questtype": "Main",
            "description": "Russell won't let us into his awesome party.",
            "how_to_complete": "\n- Talk to Russell to get the quest."
            "\n- Talk to 4 NPCs to build the Liberty Costume. (One has a Costume Pattern and 3 have Costume Pieces)"
            "\n- Talk again to Russell (as the Liberty Costume) to enter the party.",
            "reward": "300 XP",

            "flags": {
                "started": [
                    "Burbs_MQ_04_Started" # Quest Started
                ],
                "completed": [
                    "Burbs_MQ_04_Started", # Quest Started
                    "Burbs_MQ_04_Lackey1", # Lackey 1
                    "Burbs_MQ_04_Lackey2", # Lackey 2
                    "Burbs_MQ_04_Lackey3", # Lackey 3
                    "Suburbs_OpenedManholeB", # Manhole B Opened
                    "StatuePiece_TreasureChest1", # Liberty Costume Piece 1
                    "StatuePiece_TreasureChest2", # Liberty Costume Piece 2
                    "PatriotQuestRamp", # Ramp 1
                    "PatriotQuestRamp2", # Ramp 2
                    "BMQ4_bEverettHint" # Everett Hint for Liberty Costume
                ]
            }
        },
        "These Tombstones Aren't Styrofoam": {
            "questtype": "Main",
            "description": "Get through the cemetery and find Monster HQ!",
            "how_to_complete": "\n- Open the Monster Gate and enter the Cemetery to start the quest."
            "\n- Trigger the cutscene at the end of the Cemetery to finish the quest.",
            "reward": "300 XP"
        },
        "Suburbs Bobbing for Apples": {
            "questtype": "Side",
            "description": "Bob for Apples!",
            "how_to_complete": "\n- Complete 3 rounds of Apple Bobbing to finish the quest.",
            "reward": "\n- 20 Candy (Round 1)"
            "\n- 50 Candy (Round 2)"
            "\n- Sweet Tooth Creepy Treat Card (Round 3)",

            "flags": {
                "started": [
                    "Burbs_SQ_01_Started" # Quest Started
                ],
                "completed": [
                    "Burbs_SQ_01_Started", # Quest Started
                    "Burbs_SQ_01_Compl_1", # Round 1 Completed
                    "Burbs_SQ_01_Compl_2", # Round 2 Completed
                    "Burbs_SQ_01_Compl_3" # Round 3 Completed
                ]
            }
        },
        "Auburn Pines Hide 'n' Seek": {
            "questtype": "Side",
            "description": "Find all six kids hiding in Auburn Pines.",
            "how_to_complete": "\n- Find/Talk to all six kids playing hide and seek around Auburn Pines.",
            "reward": "\n- Candy Pail Upgrade: Tote Bag\n- 500 XP\n +3 AP"# The game actually gives 300XP for this quest, but for consistency with other Hide 'n Seek quests, it's set to 500XP here.
        },
        "This Card Is So Rare": {
            "questtype": "Side",
            "description": "Trade with a fellow Creepy Treat collector to get a rare card! ",
            "how_to_complete": "\n- Trade Scott your duplicate Glop Creepy Treat Card.",
            "reward": "\n- 200 XP\n- Choconana Creepy Treat Card"
        },
        "Suburbs Collect 'em All": {
            "questtype": "Side",
            "description": "Trade with a fellow Creepy Treat collector!",
            "how_to_complete": "\n- Trade Austin your duplicate Fruity Foam Creepy Treat Card.",
            "reward": "\n- 200 XP\n- Jelly Has-Beens Creepy Treat Card"
        }
    },
    "Autumn Haven Mall": {
        # World 2 Info NEEDS FINISHED AND VERIFIED
        "Tickets for Treats": {
            "questtype": "Main",
            "description": "Free the kids from their indentured gaming.",
            "how_to_complete": "\n- Talk to one of the kids playing games in the Arcade to get the quest."
            "\n- Talk to BoJonn or his assistant and defeat them to complete the quest.",
            "reward": "\n- Costume Material: Scarf\n- 300 XP"
        },
        "Earn Your Monster Slayer Badge": {
            "questtype": "Main",
            "description": "Prove you're a Monster Slayer by defeating enemies on the second floor of the Mall and collecting their MONSTER HORNS.",
            "how_to_complete": "\n- Talk to Pablo or Derek to trigger the quest."
            "\n- Defeat 3 enemies and collect their Monster Horns from Mall's second floor."
            "\n- Talk to Pablo or Derek again to complete the quest.",
            "reward": "\n- Access to 3rd Floor\n- Ninja Costume\n- 300 XP"
        },
        "The Mall-O-Rail is Broken": {
            "questtype": "Main",
            "description": "Help Sid fix the Mall-O-Rail.",
            "how_to_complete": "\n- Enter Light Mall and Talk to Sid to get the quest."
            "\n- Head to the Arcade and complete \"The Patriot's Party\" quest to access BoJonn 3.)"
            "\n- Take the Mall-O-Rail and Talk to Sid again to complete the quest.",
            "reward": "\n- Costume Material: Rope\n- 300 XP"
        },
        "The Dark Side of the Mall": {
            "questtype": "Main",
            "description": "The Light Side of the Mall awaits.",
            "how_to_complete": "\n- Head through the Dark Mall and collect the Costume Pattern from the Security Guard"
            "\n- Collect all 3 Costume Pieces from the 3 NPCs."
            "\n- Trigger the cutscene at the end of the Cemetery to finish the quest.",
            "reward": "300 XP"
        },
        "Extreme Costume Challenge!": {
            "questtype": "Side",
            "description": "If we win, we might get awesome prizes!",
            "how_to_complete": "\n- Talk to the Announcer to obtain the Quest. (Must have Lucy to trigger the quest and must havethe Liberty Costume to complete the quest.)"
            "\n- Find and Talk to all 3 Judges."
            "\n- Equip \"Robot\",  \"Knight\" and \"Statue of Liberty\" for the Contest and talk to the Announcer again to complete the quest.",
            "reward": "\n- Unicorn Costume Pattern\n- 300 XP"
        },
        "This Card Is Rarer": {
            "questtype": "Side",
            "description": "Trade with a fellow Creepy Treat collector to get a rare card!",
            "how_to_complete": "\n- Trade Carlos your duplicate Cinnamon Brain Creepy Treat Card.",
            "reward": "\n- 200 XP\n- Gummy Water Creepy Treat Card"
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
            "how_to_complete": "\n- Complete 3 rounds of Apple Bobbing to finish the quest.",
            "reward": "\n- 20 Candy (Round 1)"
            "\n- 50 Candy (Round 2)"
            "\n- Pizza Sundae Creepy Treat Card (Round 3)"
        },
        "Mall Hide 'n' Seek": {
            "questtype": "Side",
            "description": "Find all six kids hiding in Autumn Haven Mall.",
            "how_to_complete": "\n- Find/Talk to all six kids playing hide and seek around Autumn Haven Mall.",
            "reward": "\n- Candy Pail Upgrade: Pumpkin Pail\n 500 XP\n +5 AP",
            # The game actually gives 300XP for this quest, but for consistency with other Hide 'n Seek quests, it's set to 500XP here.
        }
    },
    "Fall Valley": {
        "The Original Costume Quest": {
            "questtype": "Main",
            "description": "Get our costumes back from the Repugians!",
            "how_to_complete": "\n- Head to Town and obtain the Fry Costume from Chip."
            "\n- Head back to the Repugians and use the Fry Costume to lure both of them into the barn."
            "\n- Open the Treasure Coffin nearby to retrieve your costumes."
            "\n- Lure 3 customers to Chip's Fry Stand while wearing the Fry Costume."
            "\n- Talk to Henry to enter the Carnival."
            "\n- Battle the Monsters near the Ferris Wheel."
            "\n- Use the Ninja Costume to sneak past Orzo."
            "\n- Use the Space Warrior Costume to get through the Darkness to finish the quest.",
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
            "how_to_complete": "\n- Enter the Maze area and talk to the Grubbin to get the quest and Grubbin Costume Pattern."
            "\n- Find the Grubbin Costume Pieces by talking to 3 NPCs in Maze."
            "\n- Head to the Repugian Guard blocking one of the Maze paths and while wearing the Grubbin Costume to finish the quest.",
            "reward": "300 XP"
        },
        "Fall Valley Hide 'n' Seek": {
            "questtype": "Side",
            "description": "Find all six kids hiding in Fall Valley.",
            "how_to_complete": "\n- Talk to six kids hiding around Fall Valley.",
            "reward": "\n- 500 XP\n- Candy Pail Upgrade: Bat Bucket."
            "\n\nNote: Completing this quest actually gives 300XP in-game, but for consistency with other Hide 'n Seek quests, it's set to 500XP here."
        },
        "Fall Valley Bobbing for Apples": {
            "questtype": "Side",
            "description": "Bob for Apples!",
            "how_to_complete": "\n- Complete 3 rounds of Apple Bobbing to finish the quest.",
            "reward": "\n- 20 Candy (Round 1)"
            "\n- 50 Candy (Round 2)"
            "\n- Sugar Bucket Creepy Treat Card (Round 3)"
        },
        "This Card Is The Rarest": {
            "questtype": "Side",
            "description": "Trade with a fellow Creepy Treat collector to get a rare card!",
            "how_to_complete": "\n- Trade Nathan your duplicate Street Chews Creepy Treat Card.",
            "reward": "\n- 200 XP\n- Mice Crispy Treat Creepy Treat Card"
        },
        "Fall Valley Collect 'em All": {
            "questtype": "Side",
            "description": "Trade with a fellow Creepy Treat collector!",
            "how_to_complete": "\n- Trade Rebecca your duplicate Unicorn Pellets Creepy Treat Card.",
            "reward": "\n- 200 XP\n- Jelly Has-Beens Creepy Treat Card"
        }
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