class ClashDiscord_Category(object):
    """
        ClashDiscord_Category: object for client command categories

            Instance Attributes
                name (str): category name
                brief (str): formatted brief category name
                description (str): category description
                emoji (str): emoji for category
    """

    def __init__(self, name, brief, description, emoji):
        self.name = name
        self.brief = brief
        self.description = description
        self.emoji = emoji


class ClashDiscord_Emoji(object):
    """
        ClashDiscord_Emoji: object for client emoji's

            Instance Attributes
                display_name (str): 
                    emoji name to display if emoji is not found or usable
                discord_id (int): id for emoji in discord
                discord_name (str): formatted discord name emoji name
                coc_name (str): formatted coc.py name
                # description (str): description for emoji
    """

    def __init__(self, display_name, discord_id, discord_name, coc_name):
        self.display_name = display_name
        self.discord_id = discord_id
        self.discord_name = discord_name
        self.coc_name = coc_name


class ClashDiscord_Data(object):
    """
        ClashDiscord_Data: object for ClashDiscord client data

            Instance Attributes
                version (str): client version
                author (str): author of ClashDiscord
                description (str): description of ClashDiscord
                prefix (str): prefix for command calls
                embed_color (int): color integer for embed commands
                back_emoji (str): emoji for back button
                bot_categories (list): list of Bot_Category objects
                emojis (list[obj]): list of emoji objects
    """

    version = '2.3.0'
    author = "Razgriz#7805"
    description = ("Clash of Clans discord bot for discord member management "
                   "and various clash related info")
    prefix = '/'
    embed_color = 1752220
    back_emoji = '◀️'
    bot_categories = [
        ClashDiscord_Category(
            'Super User', 'superuser',
            'ClashDiscord client based commands for super user', '🧠'),
        ClashDiscord_Category(
            'Client', 'client', 'ClashDiscord client based commands', '🤖'),
        ClashDiscord_Category(
            'Discord', 'discord', 'Discord based commands', '💻'),
        ClashDiscord_Category(
            'Announce', 'announce', 'Announce based commands', '📣'),
        ClashDiscord_Category(
            'Player', 'player', 'Player based commands', '😎'),
        ClashDiscord_Category(
            'Clan', 'clan', 'Clan based commands', '🏠'),
        ClashDiscord_Category(
            'War', 'war', 'War based commands', '⚔️'),
        ClashDiscord_Category(
            'CWL', 'cwl', 'CWL based commands', '🔱')
    ]

    emojis = [
        ClashDiscord_Emoji(
            display_name="Barbarian",
            discord_id=929203422287253545,
            discord_name="troop_barbarian",
            coc_name="Barbarian"
        ),
        ClashDiscord_Emoji(
            display_name="Archer",
            discord_id=929203434937258034,
            discord_name="troop_archer",
            coc_name="Archer"
        ),
        ClashDiscord_Emoji(
            display_name="Giant",
            discord_id=929203478407041024,
            discord_name="troop_giant",
            coc_name="Giant"
        ),
        ClashDiscord_Emoji(
            display_name="Goblin",
            discord_id=929203487311560715,
            discord_name="troop_goblin",
            coc_name="Goblin"
        ),
        ClashDiscord_Emoji(
            display_name="Wall Breaker",
            discord_id=929203526511497308,
            discord_name="troop_wall_breaker",
            coc_name="Wall Breaker"
        ),
        ClashDiscord_Emoji(
            display_name="Balloon",
            discord_id=929203556391731250,
            discord_name="troop_balloon",
            coc_name="Balloon"
        ),
        ClashDiscord_Emoji(
            display_name="Wizard",
            discord_id=929203596111777832,
            discord_name="troop_wizard",
            coc_name="Wizard"
        ),
        ClashDiscord_Emoji(
            display_name="Healer",
            discord_id=929203616982630411,
            discord_name="troop_healer",
            coc_name="Healer"
        ),
        ClashDiscord_Emoji(
            display_name="Dragon",
            discord_id=929203638340038656,
            discord_name="troop_dragon",
            coc_name="Dragon"
        ),
        ClashDiscord_Emoji(
            display_name="P.E.K.K.A",
            discord_id=929203711073452072,
            discord_name="troop_pekka",
            coc_name="P.E.K.K.A"
        ),
        ClashDiscord_Emoji(
            display_name="Baby Dragon",
            discord_id=929203723010453614,
            discord_name="troop_baby_dragon",
            coc_name="Baby Dragon"
        ),
        ClashDiscord_Emoji(
            display_name="Miner",
            discord_id=929203735819845702,
            discord_name="troop_miner",
            coc_name="Miner"
        ),
        ClashDiscord_Emoji(
            display_name="Electro Dragon",
            discord_id=929203753746321408,
            discord_name="troop_electro_dragon",
            coc_name="Electro Dragon"
        ),
        ClashDiscord_Emoji(
            display_name="Yeti",
            discord_id=929203806804250644,
            discord_name="troop_yeti",
            coc_name="Yeti"
        ),
        ClashDiscord_Emoji(
            display_name="Dragon Rider",
            discord_id=929203816522481664,
            discord_name="troop_dragon_rider",
            coc_name="Dragon Rider"
        ),
        ClashDiscord_Emoji(
            display_name="Minion",
            discord_id=929203826051932160,
            discord_name="troop_minion",
            coc_name="Minion"
        ),
        ClashDiscord_Emoji(
            display_name="Hog Rider",
            discord_id=929203832272093214,
            discord_name="troop_hog_rider",
            coc_name="Hog Rider"
        ),
        ClashDiscord_Emoji(
            display_name="Valkyrie",
            discord_id=929203892980437023,
            discord_name="troop_valkyrie",
            coc_name="Valkyrie"
        ),
        ClashDiscord_Emoji(
            display_name="Golem",
            discord_id=929203899791978556,
            discord_name="troop_golem",
            coc_name="Golem"
        ),
        ClashDiscord_Emoji(
            display_name="Witch",
            discord_id=929203904707694643,
            discord_name="troop_witch",
            coc_name="Witch"
        ),
        ClashDiscord_Emoji(
            display_name="Lava Hound",
            discord_id=929203914170048552,
            discord_name="troop_lava_hound",
            coc_name="Lava Hound"
        ),
        ClashDiscord_Emoji(
            display_name="Bowler",
            discord_id=929203933937803335,
            discord_name="troop_bowler",
            coc_name="Bowler"
        ),
        ClashDiscord_Emoji(
            display_name="Ice Golem",
            discord_id=929204012354527292,
            discord_name="troop_ice_golem",
            coc_name="Ice Golem"
        ),
        ClashDiscord_Emoji(
            display_name="Headhunter",
            discord_id=929204070525308938,
            discord_name="troop_headhunter",
            coc_name="Headhunter"
        ),
        ClashDiscord_Emoji(
            display_name="Barbarian King",
            discord_id=929205073056260208,
            discord_name="hero_barbarian_king",
            coc_name="Barbarian King"
        ),
        ClashDiscord_Emoji(
            display_name="Archer Queen",
            discord_id=929205087753097276,
            discord_name="hero_archer_queen",
            coc_name="Archer Queen"
        ),
        ClashDiscord_Emoji(
            display_name="Grand Warden",
            discord_id=929217798515884032,
            discord_name="hero_grand_warden",
            coc_name="Grand Warden"
        ),
        ClashDiscord_Emoji(
            display_name="Royal Champion",
            discord_id=929217810897469480,
            discord_name="hero_royal_champion",
            coc_name="Royal Champion"
        ),
        ClashDiscord_Emoji(
            display_name="Wall Wrecker",
            discord_id=929207865057636362,
            discord_name="siege_wall_wrecker",
            coc_name="Wall Wrecker"
        ),
        ClashDiscord_Emoji(
            display_name="Battle Blimp",
            discord_id=929207889577533470,
            discord_name="siege_battle_blimp",
            coc_name="Battle Blimp"
        ),
        ClashDiscord_Emoji(
            display_name="Stone Slammer",
            discord_id=929207909890523148,
            discord_name="siege_stone_slammer",
            coc_name="Stone Slammer"
        ),
        ClashDiscord_Emoji(
            display_name="Siege Barracks",
            discord_id=929207924130209842,
            discord_name="siege_siege_barracks",
            coc_name="Siege Barracks"
        ),
        ClashDiscord_Emoji(
            display_name="Log Launcher",
            discord_id=929207939431034900,
            discord_name="siege_log_launcher",
            coc_name="Log Launcher"
        ),
        ClashDiscord_Emoji(
            display_name="Flame Flinger",
            discord_id=929207944338370571,
            discord_name="siege_flame_flinger",
            coc_name="Flame Flinger"
        ),
        ClashDiscord_Emoji(
            display_name="Lightning Spell",
            discord_id=929206569990766673,
            discord_name="spell_lightning_spell",
            coc_name="Lightning Spell"
        ),
        ClashDiscord_Emoji(
            display_name="Healing Spell",
            discord_id=929206597006278726,
            discord_name="spell_healing_spell",
            coc_name="Healing Spell"
        ),
        ClashDiscord_Emoji(
            display_name="Rage Spell",
            discord_id=929206604400832572,
            discord_name="spell_rage_spell",
            coc_name="Rage Spell"
        ),
        ClashDiscord_Emoji(
            display_name="Jump Spell",
            discord_id=929206607496241172,
            discord_name="spell_jump_spell",
            coc_name="Jump Spell"
        ),
        ClashDiscord_Emoji(
            display_name="Freeze Spell",
            discord_id=929206628950106153,
            discord_name="spell_freeze_spell",
            coc_name="Freeze Spell"
        ),
        ClashDiscord_Emoji(
            display_name="Clone Spell",
            discord_id=929206634964742185,
            discord_name="spell_clone_spell",
            coc_name="Clone Spell"
        ),
        ClashDiscord_Emoji(
            display_name="Invisibility Spell",
            discord_id=929206647602151424,
            discord_name="spell_invisibility_spell",
            coc_name="Invisibility Spell"
        ),
        ClashDiscord_Emoji(
            display_name="Poison Spell",
            discord_id=929206713830232084,
            discord_name="spell_poison_spell",
            coc_name="Poison Spell"
        ),
        ClashDiscord_Emoji(
            display_name="Earthquake Spell",
            discord_id=929206716900462603,
            discord_name="spell_earthquake_spell",
            coc_name="Earthquake Spell"
        ),
        ClashDiscord_Emoji(
            display_name="Haste Spell",
            discord_id=929206720998289448,
            discord_name="spell_haste_spell",
            coc_name="Haste Spell"
        ),
        ClashDiscord_Emoji(
            display_name="Skeleton Spell",
            discord_id=929206724328574996,
            discord_name="spell_skeleton_spell",
            coc_name="Skeleton Spell"
        ),
        ClashDiscord_Emoji(
            display_name="Bat Spell",
            discord_id=929206728434794586,
            discord_name="spell_bat_spell",
            coc_name="Bat Spell"
        ),
        ClashDiscord_Emoji(
            display_name="L.A.S.S.I",
            discord_id=929208654085890078,
            discord_name="pet_lassi",
            coc_name="L.A.S.S.I"
        ),
        ClashDiscord_Emoji(
            display_name="Electro Owl",
            discord_id=929208673371316285,
            discord_name="pet_electro_owl",
            coc_name="Electro Owl"
        ),
        ClashDiscord_Emoji(
            display_name="Mighty Yak",
            discord_id=929208680870707210,
            discord_name="pet_mighty_yak",
            coc_name="Mighty Yak"
        ),
        ClashDiscord_Emoji(
            display_name="Unicorn",
            discord_id=929208683190161439,
            discord_name="pet_unicorn",
            coc_name="Unicorn"
        ),
        ClashDiscord_Emoji(
            display_name="Town Hall 1",
            discord_id=929208930847043664,
            discord_name="th_1",
            coc_name="Town Hall 1"
        ),
        ClashDiscord_Emoji(
            display_name="Town Hall 3",
            discord_id=929208984446070785,
            discord_name="th_3",
            coc_name="Town Hall 3"
        ),
        ClashDiscord_Emoji(
            display_name="Town Hall 4",
            discord_id=929208991492493342,
            discord_name="th_4",
            coc_name="Town Hall 4"
        ),
        ClashDiscord_Emoji(
            display_name="Town Hall 5",
            discord_id=929208996454334464,
            discord_name="th_5",
            coc_name="Town Hall 5"
        ),
        ClashDiscord_Emoji(
            display_name="Town Hall 6",
            discord_id=929208999902064680,
            discord_name="th_6",
            coc_name="Town Hall 6"
        ),
        ClashDiscord_Emoji(
            display_name="Town Hall 7",
            discord_id=929209004582907944,
            discord_name="th_7",
            coc_name="Town Hall 7"
        ),
        ClashDiscord_Emoji(
            display_name="Town Hall 8",
            discord_id=929209007875432459,
            discord_name="th_8",
            coc_name="Town Hall 8"
        ),
        ClashDiscord_Emoji(
            display_name="Town Hall 9",
            discord_id=929209044827246633,
            discord_name="th_9",
            coc_name="Town Hall 9"
        ),
        ClashDiscord_Emoji(
            display_name="Town Hall 10",
            discord_id=929209052490268673,
            discord_name="th_10",
            coc_name="Town Hall 10"
        ),
        ClashDiscord_Emoji(
            display_name="Town Hall 11",
            discord_id=929209057896726560,
            discord_name="th_11",
            coc_name="Town Hall 11"
        ),
        ClashDiscord_Emoji(
            display_name="Town Hall 12",
            discord_id=929209059587010630,
            discord_name="th_12",
            coc_name="Town Hall 12"
        ),
        ClashDiscord_Emoji(
            display_name="Town Hall 13",
            discord_id=929415676165259294,
            discord_name="th_13",
            coc_name="Town Hall 13"
        ),
        ClashDiscord_Emoji(
            display_name="Town Hall 14",
            discord_id=929415746314969118,
            discord_name="th_14",
            coc_name="Town Hall 14"
        ),
        ClashDiscord_Emoji(
            display_name="Clan Wars",
            discord_id=929210758749892629,
            discord_name="label_clan_wars",
            coc_name="Clan Wars"
        ),
        ClashDiscord_Emoji(
            display_name="Clan War League",
            discord_id=929214029451378779,
            discord_name="label_clan_war_league",
            coc_name="Clan War League"
        ),
        ClashDiscord_Emoji(
            display_name="Trophy Pushing",
            discord_id=929214033872171009,
            discord_name="label_trophy_pushing",
            coc_name="Trophy Pushing"
        ),
        ClashDiscord_Emoji(
            display_name="Friendly Wars",
            discord_id=929214050334830612,
            discord_name="label_friendly_wars",
            coc_name="Friendly Wars"
        ),
        ClashDiscord_Emoji(
            display_name="Clan Games",
            discord_id=929214073793568798,
            discord_name="label_clan_games",
            coc_name="Clan Games"
        ),
        ClashDiscord_Emoji(
            display_name="Builder Base",
            discord_id=929214076532445214,
            discord_name="label_builder_base",
            coc_name="Builder Base"
        ),
        ClashDiscord_Emoji(
            display_name="Base Designing",
            discord_id=929214078482808843,
            discord_name="label_base_designing",
            coc_name="Base Designing"
        ),
        ClashDiscord_Emoji(
            display_name="Farming",
            discord_id=929214100909727815,
            discord_name="label_farming",
            coc_name="Farming"
        ),
        ClashDiscord_Emoji(
            display_name="Active Donator",
            discord_id=929214135936368651,
            discord_name="label_active_donator",
            coc_name="Active Donator"
        ),
        ClashDiscord_Emoji(
            display_name="Active Daily",
            discord_id=929214147063861298,
            discord_name="label_active_daily",
            coc_name="Active Daily"
        ),
        ClashDiscord_Emoji(
            display_name="Hungry Learner",
            discord_id=929214187652128798,
            discord_name="label_hungry_learner",
            coc_name="Hungry Learner"
        ),
        ClashDiscord_Emoji(
            display_name="Friendly",
            discord_id=929214194925056081,
            discord_name="label_friendly",
            coc_name="Friendly"
        ),
        ClashDiscord_Emoji(
            display_name="Talkative",
            discord_id=929214253519482890,
            discord_name="label_talkative",
            coc_name="Talkative"
        ),
        ClashDiscord_Emoji(
            display_name="Teacher",
            discord_id=929214256115761242,
            discord_name="label_teacher",
            coc_name="Teacher"
        ),
        ClashDiscord_Emoji(
            display_name="Competitive",
            discord_id=929214262595973201,
            discord_name="label_competitive",
            coc_name="Competitive"
        ),
        ClashDiscord_Emoji(
            display_name="Veteran",
            discord_id=929214315515482112,
            discord_name="label_veteran",
            coc_name="Veteran"
        ),
        ClashDiscord_Emoji(
            display_name="Newbie",
            discord_id=929214320422834176,
            discord_name="label_newbie",
            coc_name="Newbie"
        ),
        ClashDiscord_Emoji(
            display_name="Super Barbarian",
            discord_id=929220408413147146,
            discord_name="super_troop_super_barbarian",
            coc_name="Super Barbarian"
        ),
        ClashDiscord_Emoji(
            display_name="Super Archer",
            discord_id=929220516009639988,
            discord_name="super_troop_super_archer",
            coc_name="Super Archer"
        ),
        ClashDiscord_Emoji(
            display_name="Super Giant",
            discord_id=929220523353833582,
            discord_name="super_troop_super_giant",
            coc_name="Super Giant"
        ),
        ClashDiscord_Emoji(
            display_name="Sneaky Goblin",
            discord_id=929220531620827137,
            discord_name="super_troop_sneaky_goblin",
            coc_name="Sneaky Goblin"
        ),
        ClashDiscord_Emoji(
            display_name="Super Wall Breaker",
            discord_id=929220538956644372,
            discord_name="super_troop_super_wall_breaker",
            coc_name="Super Wall Breaker"
        ),
        ClashDiscord_Emoji(
            display_name="Rocket Balloon",
            discord_id=929220553573793802,
            discord_name="super_troop_rocket_balloon",
            coc_name="Rocket Balloon"
        ),
        ClashDiscord_Emoji(
            display_name="Super Wizard",
            discord_id=929220564281856070,
            discord_name="super_troop_super_wizard",
            coc_name="Super Wizard"
        ),
        ClashDiscord_Emoji(
            display_name="Super Dragon",
            discord_id=929220578320220170,
            discord_name="super_troop_super_dragon",
            coc_name="Super Dragon"
        ),
        ClashDiscord_Emoji(
            display_name="Inferno Dragon",
            discord_id=929220595701383208,
            discord_name="super_troop_inferno_dragon",
            coc_name="Inferno Dragon"
        ),
        ClashDiscord_Emoji(
            display_name="Super Minion",
            discord_id=929220904016302100,
            discord_name="super_troop_super_minion",
            coc_name="Super Minion"
        ),
        ClashDiscord_Emoji(
            display_name="Super Valkyrie",
            discord_id=929220914283966465,
            discord_name="super_troop_super_valkyrie",
            coc_name="Super Valkyrie"
        ),
        ClashDiscord_Emoji(
            display_name="Super Witch",
            discord_id=929220920462151691,
            discord_name="super_troop_super_witch",
            coc_name="Super Witch"
        ),
        ClashDiscord_Emoji(
            display_name="Ice Hound",
            discord_id=929220925298192394,
            discord_name="super_troop_ice_hound",
            coc_name="Ice Hound"
        ),
        ClashDiscord_Emoji(
            display_name="Super Bowler",
            discord_id=929220939969867776,
            discord_name="super_troop_super_bowler",
            coc_name="Super Bowler"
        ),
        ClashDiscord_Emoji(
            display_name="In",
            discord_id=929407005536428102,
            discord_name="icon_green_tick",
            # coc.py player.war_opted_in: True
            coc_name="war_opted_in=True"
        ),
        ClashDiscord_Emoji(
            display_name="Out",
            discord_id=929407018022871100,
            discord_name="icon_red_tick",
            # coc.py player.war_opted_in: False
            coc_name="war_opted_in=False"
        ),
        ClashDiscord_Emoji(
            display_name="Grey Tick",
            discord_id=929423833998438464,
            discord_name="icon_grey_tick",
            coc_name="Grey Tick"
        ),
        ClashDiscord_Emoji(
            display_name="Donations",
            discord_id=929407021235728404,
            discord_name="icon_donations",
            coc_name="donations"
        ),
        ClashDiscord_Emoji(
            display_name="Received",
            discord_id=929407028638662756,
            discord_name="icon_received",
            coc_name="received"
        ),
        ClashDiscord_Emoji(
            display_name="Exp Level",
            discord_id=929407046435102751,
            discord_name="icon_exp",
            coc_name="Exp Level"
        ),
        ClashDiscord_Emoji(
            display_name="Trophy",
            discord_id=930106600960720946,
            discord_name="icon_trophy",
            coc_name="Trophy"
        ),
        ClashDiscord_Emoji(
            display_name="Legend Trophy",
            discord_id=930107837051461682,
            discord_name="icon_legend_trophy",
            coc_name="Legend Trophy"
        ),
        ClashDiscord_Emoji(
            display_name="Shield",
            discord_id=929407832191811615,
            discord_name="icon_shield",
            coc_name="Shield"
        ),
        ClashDiscord_Emoji(
            display_name="White Star",
            discord_id=930149728455364608,
            discord_name="icon_white_star",
            coc_name="Player Star"
        ),
        ClashDiscord_Emoji(
            display_name="War Star",
            discord_id=930307229872181289,
            discord_name="icon_war_star",
            coc_name="War Star"
        ),
        ClashDiscord_Emoji(
            display_name="Clan Exp",
            discord_id=930307258775130202,
            discord_name="icon_clan_exp",
            coc_name="Clan Exp"
        ),
        ClashDiscord_Emoji(
            display_name="Gold",
            discord_id=929407562967818243,
            discord_name="resource_gold",
            coc_name="Gold"
        ),
        ClashDiscord_Emoji(
            display_name="Elixir",
            discord_id=929407572514062386,
            discord_name="resource_elixir",
            coc_name="Elixir"
        ),
        ClashDiscord_Emoji(
            display_name="Dark Elixir",
            discord_id=929407581561167932,
            discord_name="resource_dark_elixir",
            coc_name="Dark Elixir"
        ),
        ClashDiscord_Emoji(
            display_name="Gem",
            discord_id=929407596211863662,
            discord_name="resource_gem",
            coc_name="Gem"
        ),
        ClashDiscord_Emoji(
            display_name="Super Troop",
            discord_id=929408127143645184,
            discord_name="resource_super_troop",
            coc_name="Super Troop"
        ),
        ClashDiscord_Emoji(
            display_name="Unranked",
            discord_id=929410336673644576,
            discord_name="league_unranked",
            coc_name="Unranked"
        ),
        ClashDiscord_Emoji(
            display_name="Bronze League",
            discord_id=929410363827568661,
            discord_name="league_bronze",
            coc_name="Bronze League"
        ),
        ClashDiscord_Emoji(
            display_name="Bronze League III",
            discord_id=929410570128588871,
            discord_name="league_bronze_3",
            coc_name="Bronze League III"
        ),
        ClashDiscord_Emoji(
            display_name="Bronze League II",
            discord_id=929410572762628136,
            discord_name="league_bronze_2",
            coc_name="Bronze League II"
        ),
        ClashDiscord_Emoji(
            display_name="Bronze League I",
            discord_id=929410574532616223,
            discord_name="league_bronze_1",
            coc_name="Bronze League I"
        ),
        ClashDiscord_Emoji(
            display_name="Silver League",
            discord_id=929410616035278889,
            discord_name="league_silver",
            coc_name="Silver League"
        ),
        ClashDiscord_Emoji(
            display_name="Silver League III",
            discord_id=929410619818541096,
            discord_name="league_silver_3",
            coc_name="Silver League III"
        ),
        ClashDiscord_Emoji(
            display_name="Silver League II",
            discord_id=929410621945036811,
            discord_name="league_silver_2",
            coc_name="Silver League II"
        ),
        ClashDiscord_Emoji(
            display_name="Silver League I",
            discord_id=929410624671346798,
            discord_name="league_silver_1",
            coc_name="Silver League I"
        ),
        ClashDiscord_Emoji(
            display_name="Gold League",
            discord_id=929410650676006942,
            discord_name="league_gold",
            coc_name="Gold League"
        ),
        ClashDiscord_Emoji(
            display_name="Gold League III",
            discord_id=929410654354432121,
            discord_name="league_gold_3",
            coc_name="Gold League III"
        ),
        ClashDiscord_Emoji(
            display_name="Gold League II",
            discord_id=929410657743421550,
            discord_name="league_gold_2",
            coc_name="Gold League II"
        ),
        ClashDiscord_Emoji(
            display_name="Gold League I",
            discord_id=929410659907698689,
            discord_name="league_gold_1",
            coc_name="Gold League I"
        ),
        ClashDiscord_Emoji(
            display_name="Crystal League",
            discord_id=929410748201975889,
            discord_name="league_crystal",
            coc_name="Crystal League"
        ),
        ClashDiscord_Emoji(
            display_name="Crystal League III",
            discord_id=929410752979300383,
            discord_name="league_crystal_3",
            coc_name="Crystal League III"
        ),
        ClashDiscord_Emoji(
            display_name="Crystal League II",
            discord_id=929410755101601812,
            discord_name="league_crystal_2",
            coc_name="Crystal League II"
        ),
        ClashDiscord_Emoji(
            display_name="Crystal League I",
            discord_id=929410757618200627,
            discord_name="league_crystal_1",
            coc_name="Crystal League I"
        ),
        ClashDiscord_Emoji(
            display_name="Master League",
            discord_id=929410790409252905,
            discord_name="league_master",
            coc_name="Master League"
        ),
        ClashDiscord_Emoji(
            display_name="Master League III",
            discord_id=929410796377755779,
            discord_name="league_master_3",
            coc_name="Master League III"
        ),
        ClashDiscord_Emoji(
            display_name="Master League II",
            discord_id=929410806129496124,
            discord_name="league_master_2",
            coc_name="Master League II"
        ),
        ClashDiscord_Emoji(
            display_name="Master League I",
            discord_id=929410808679628871,
            discord_name="league_master_1",
            coc_name="Master League I"
        ),
        ClashDiscord_Emoji(
            display_name="Champion League",
            discord_id=929410867353755650,
            discord_name="league_champion",
            coc_name="Champion League"
        ),
        ClashDiscord_Emoji(
            display_name="Champion League III",
            discord_id=929410871355121694,
            discord_name="league_champion_3",
            coc_name="Champion League III"
        ),
        ClashDiscord_Emoji(
            display_name="Champion League II",
            discord_id=929410874194673774,
            discord_name="league_champion_2",
            coc_name="Champion League II"
        ),
        ClashDiscord_Emoji(
            display_name="Champion League I",
            discord_id=929410876916781116,
            discord_name="league_champion_1",
            coc_name="Champion League I"
        ),
        ClashDiscord_Emoji(
            display_name="Titan League",
            discord_id=929411044261109792,
            discord_name="league_titan",
            coc_name="Titan League"
        ),
        ClashDiscord_Emoji(
            display_name="Titan League III",
            discord_id=929411051466924092,
            discord_name="league_titan_3",
            coc_name="Titan League III"
        ),
        ClashDiscord_Emoji(
            display_name="Titan League II",
            discord_id=929411056432975884,
            discord_name="league_titan_2",
            coc_name="Titan League II"
        ),
        ClashDiscord_Emoji(
            display_name="Titan League I",
            discord_id=929411064351817769,
            discord_name="league_titan_1",
            coc_name="Titan League I"
        ),
        ClashDiscord_Emoji(
            display_name="Legend League",
            discord_id=929411096325021756,
            discord_name="league_legend",
            coc_name="Legend League"
        ),
        ClashDiscord_Emoji(
            display_name="Silver I",
            discord_id=929421151116066956,
            discord_name="clan_war_league_silver_1",
            # coc.py name is "Silver League I"
            # "Clan War" added for differentiation between league types
            coc_name="Clan War Silver League I"
        ),
        ClashDiscord_Emoji(
            display_name="Silver II",
            discord_id=929421153410383872,
            discord_name="clan_war_league_silver_2",
            # coc.py name is "Silver League II"
            # "Clan War" added for differentiation between league types
            coc_name="Clan War Silver League II"
        ),
        ClashDiscord_Emoji(
            display_name="Silver III",
            discord_id=929421156803551243,
            discord_name="clan_war_league_silver_3",
            # coc.py name is "Silver League III"
            # "Clan War" added for differentiation between league types
            coc_name="Clan War Silver League III"
        ),
        ClashDiscord_Emoji(
            display_name="Gold I",
            discord_id=929421174562230282,
            discord_name="clan_war_league_gold_1",
            # coc.py name is "Gold League I"
            # "Clan War" added for differentiation between league types
            coc_name="Clan War Gold League I"
        ),
        ClashDiscord_Emoji(
            display_name="Gold II",
            discord_id=929421176537747487,
            discord_name="clan_war_league_gold_2",
            # coc.py name is "Gold League II"
            # "Clan War" added for differentiation between league types
            coc_name="Clan War Gold League II"
        ),
        ClashDiscord_Emoji(
            display_name="Gold III",
            discord_id=929421180027404288,
            discord_name="clan_war_league_gold_3",
            # coc.py name is "Gold League III"
            # "Clan War" added for differentiation between league types
            coc_name="Clan War Gold League III"
        ),
        ClashDiscord_Emoji(
            display_name="Crystal I",
            discord_id=929421207034556486,
            discord_name="clan_war_league_crystal_1",
            # coc.py name is "Crystal League I"
            # "Clan War" added for differentiation between league types
            coc_name="Clan War Crystal League I"
        ),
        ClashDiscord_Emoji(
            display_name="Crystal II",
            discord_id=929421209823760395,
            discord_name="clan_war_league_crystal_2",
            # coc.py name is "Crystal League II"
            # "Clan War" added for differentiation between league types
            coc_name="Clan War Crystal League II"
        ),
        ClashDiscord_Emoji(
            display_name="Crystal III",
            discord_id=929421212839465020,
            discord_name="clan_war_league_crystal_3",
            # coc.py name is "Crystal League III"
            # "Clan War" added for differentiation between league types
            coc_name="Clan War Crystal League III"
        ),
        ClashDiscord_Emoji(
            display_name="Master I",
            discord_id=929421248482643979,
            discord_name="clan_war_league_master_1",
            # coc.py name is "Master League I"
            # "Clan War" added for differentiation between league types
            coc_name="Clan War Master League I"
        ),
        ClashDiscord_Emoji(
            display_name="Master II",
            discord_id=929421251355754517,
            discord_name="clan_war_league_master_2",
            # coc.py name is "Master League II"
            # "Clan War" added for differentiation between league types
            coc_name="Clan War Master League II"
        ),
        ClashDiscord_Emoji(
            display_name="Master III",
            discord_id=929421253658415114,
            discord_name="clan_war_league_master_3",
            # coc.py name is "Master League III"
            # "Clan War" added for differentiation between league types
            coc_name="Clan War Master League III"
        ),
        ClashDiscord_Emoji(
            display_name="Champion I",
            discord_id=929421274512490496,
            discord_name="clan_war_league_champion_1",
            # coc.py name is "Champion League I"
            # "Clan War" added for differentiation between league types
            coc_name="Clan War Champion League I"
        ),
        ClashDiscord_Emoji(
            display_name="Champion II",
            discord_id=929421277750517770,
            discord_name="clan_war_league_champion_2",
            # coc.py name is "Champion League II"
            # "Clan War" added for differentiation between league types
            coc_name="Clan War Champion League II"
        ),
        ClashDiscord_Emoji(
            display_name="Champion III",
            discord_id=929421280602619994,
            discord_name="clan_war_league_champion_3",
            # coc.py name is "Champion League III"
            # "Clan War" added for differentiation between league types
            coc_name="Clan War Champion League III"
        ),
    ]
