import requests
import json
import re


class Player(object):
    """
    Player
        Instance Attributes
            tag (str): The player's tag
            name (str): The player's name
            th_lvl (int): The player's home town hall level
            th_weapon_lvl (int): The player's home town hall weapon level
                not available if player has TH 11 or lower
            xp_lvl (int): The player's experience level
            trophies (int): current trophy count
            best_trophies (int): max trophy amount
            war_stars (int): amount of war stars earned
            attack_wins (int): attack win count
                current season
            defense_wins (int): defense win count
                current season
            builder_hall_lvl (int): The player's builder hall level
                not available if player has not unlocked builder hall
            vs_trophies (int): current versus trophy count
            best_vs_trophies (int): max versus trophy amount
            vs_battle_wins (int): 
            role (str): The player's role in their clan
                not available if player is not in a clan
            donations (int): donations given
                current season
            donations_received (int): donations received
                current season
            clan_tag (str): tag of the clan the player is in
                not available if player is not in a clan
            clan_name (str): name of the clan the player is in
                not available if player is not in a clan
            clan_lvl (int): level of the clan the player is in
                not available if player is not in a clan
            clan_icons (dict): dict of clan icons
            league_id (int): ID of the league the player is in
                not available if player is not in a league
            league_name (str): name of the league the player is in
                not available if player is not in a league
            league_icons (dict): dict of league icons
            heroes (list): list of Hero objects
            troops (list): list of Troop objects
            spells (list): list of Spell objects
    """

    def __init__(
        self, tag, name, th_lvl, th_weapon_lvl, xp_lvl,
        trophies, best_trophies, war_stars, attack_wins, defense_wins,
        builder_hall_lvl, vs_trophies, best_vs_trophies, vs_battle_wins,
        role, donations, donations_received, clan_tag, clan_name, clan_lvl,
        clan_icons, league_id, league_name, league_icons,
        heroes, troops, spells
    ):
        self.tag = tag
        self.name = name
        self.th_lvl = th_lvl
        self.th_weapon_lvl = th_weapon_lvl
        self.xp_lvl = xp_lvl
        self.trophies = trophies
        self.best_trophies = best_trophies
        self.war_stars = war_stars
        self.attack_wins = attack_wins
        self.defense_wins = defense_wins
        self.builder_hall_lvl = builder_hall_lvl
        self.vs_trophies = vs_trophies
        self.best_vs_trophies = best_vs_trophies
        self.vs_battle_wins = vs_battle_wins
        self.role = role
        self.donations = donations
        self.donations_received = donations_received
        self.clan_tag = clan_tag
        self.clan_name = clan_name
        self.clan_lvl = clan_lvl
        self.clan_icons = clan_icons
        self.league_id = league_id
        self.league_name = league_name
        self.league_icons = league_icons
        self.heroes = heroes
        self.troops = troops
        self.spells = spells

    def find_unit(self, unit_name):
        """
            Take in a unit name and return the corresponding unit object.
            If no unit is found returns None.
        """

        # formatting the name from '-' to ' '
        unit_name = re.sub('[-]', ' ', unit_name)
        unit_name = re.sub('[.]', '', unit_name)
        for hero in self.heroes:
            if hero.name.lower() == unit_name.lower():
                return hero
        for troop in self.troops:
            # formatting for P.E.K.K.A.
            formatted_unit_name = re.sub('[.]', '', troop.name)
            if formatted_unit_name.lower() == unit_name.lower():
                return troop
        for spell in self.spells:
            if spell.name.lower() == unit_name.lower():
                return spell
        return None

    def find_hero(self, hero_name):
        """
            Take in a hero name and return the corresponding hero object.
            If no hero is found returns None.
        """

        # formatting the name from '-' to ' '
        hero_name = re.sub('[-]', ' ', hero_name)
        hero_name = re.sub('[.]', '', hero_name)
        for hero in self.heroes:
            if hero.name.lower() == hero_name.lower():
                return hero
        return None

    def find_troop(self, troop_name):
        """
            Take in a troop name and return the corresponding troop object.
            If no troop is found returns None.
        """

        # formatting the name from '-' to ' '
        troop_name = re.sub('[-]', ' ', troop_name)
        troop_name = re.sub('[.]', '', troop_name)
        for troop in self.troops:
            # formatting for P.E.K.K.A.
            formatted_troop_name = re.sub('[.]', '', troop.name)
            if formatted_troop_name.lower() == troop_name.lower():
                return troop
        return None

    def find_spell(self, spell_name):
        """
            Take in a spell name and return the corresponding spell object.
            If no spell is found returns None.
        """

        # formatting the name from '-' to ' '
        spell_name = re.sub('[-]', ' ', spell_name)
        spell_name = re.sub('[.]', '', spell_name)
        for spell in self.spells:
            if spell.name.lower() == spell_name.lower():
                return spell
        return None


class Hero(object):
    """
    Hero
        Instance Attributes
            name (str): The name of the hero
            lvl (int): The level of the Player's hero
            max_lvl (int): The max level of the hero
            th_max (int): Max hero level for the Player's town hall level
            village (str): Base the hero comes from
                'home' or 'builderBase'
    """

    def __init__(self, name, lvl, max_lvl, th_max, village):
        self.name = name
        self.lvl = lvl
        self.max_lvl = max_lvl
        self.th_max = th_max
        self.village = village


class Troop(object):
    """
    Troop
        Instance Attributes
            name (str): The name of the troop
            lvl (int): The level of the Player's troop
            max_lvl (int): The max level of the troop
            th_max (int): Max troop level for the Player's town hall level
            village (str): Base the troop comes from
                'home' or 'builderBase'
    """

    def __init__(self, name, lvl, max_lvl, th_max, village):
        self.name = name
        self.lvl = lvl
        self.max_lvl = max_lvl
        self.th_max = th_max
        self.village = village


class Spell(object):
    """
    Spell
        Instance Attributes
            name (str): The name of the spell
            lvl (int): The level of the Player's spell
            max_lvl (int): The max level of the spell
            th_max (int): Max spell level for the Player's town hall level
            village (str): Base the spell comes from
                'home' or 'builderBase'
    """

    def __init__(self, name, lvl, max_lvl, th_max, village):
        self.name = name
        self.lvl = lvl
        self.max_lvl = max_lvl
        self.th_max = th_max
        self.village = village


# todo make comments for inner workings of get method
# todo legends league stats
# ? include all troops whether they are unlocked or not
def get(tag, header):
    """Takes in a player's tag and returns a Player object"""

    player_json = json_response(tag, header)

    if 'reason' in player_json:
        None

    if 'townHallWeaponLevel' in player_json:
        th_weap_lvl = player_json['townHallWeaponLevel']
    else:
        th_weap_lvl = None

    if 'builderHallLevel' in player_json:
        bh_lvl = player_json['builderHallLevel']
        vs_trophies = player_json['versusTrophies']
        best_vs_trophies = player_json['bestVersusTrophies']
        vs_battle_wins = player_json['versusBattleWins']
    else:
        bh_lvl = None
        vs_trophies = None
        best_vs_trophies = None
        vs_battle_wins = None

    if 'clan' in player_json:
        role = player_json['role']
        clan_tag = player_json['clan']['tag']
        clan_name = player_json['clan']['name']
        clan_lvl = player_json['clan']['clanLevel']
        clan_icons = {
            'small': player_json['clan']['badgeUrls']['small'],
            'medium': player_json['clan']['badgeUrls']['medium'],
            'large': player_json['clan']['badgeUrls']['large']
        }
    else:
        role = None
        clan_tag = None
        clan_name = None
        clan_lvl = None
        clan_icons = None

    if 'league' in player_json:
        league_id = player_json['league']['id']
        league_name = player_json['league']['name']
        league_icons = {
            'tiny': player_json['league']['iconUrls']['tiny'],
            'small': player_json['league']['iconUrls']['small'],
            'medium': player_json['league']['iconUrls']['medium']
        }
    else:
        league_id = None
        league_name = None
        league_icons = None

    heroes = []
    for hero in player_json['heroes']:
        if hero['village'] == 'home':
            heroes.append(Hero(
                hero['name'], hero['level'], hero['maxLevel'],
                troop_dict[player_json['townHallLevel']
                           ]['hero'][hero['name']]['thMax'],
                hero['village'])
            )

    troops = []
    # siege machines are part of 'troops' in the player_json
    for troop in player_json['troops']:
        if (troop['village'] == 'home'
                and troop['name'] not in super_troop_list):
            troops.append(Troop(
                troop['name'], troop['level'], troop['maxLevel'],
                troop_dict[player_json['townHallLevel']
                           ]['troop'][troop['name']]['thMax'],
                troop['village'])
            )

    spells = []
    for spell in player_json['spells']:
        if spell['village'] == 'home':
            spells.append(Spell(
                spell['name'], spell['level'], spell['maxLevel'],
                troop_dict[player_json['townHallLevel']
                           ]['spell'][spell['name']]['thMax'],
                spell['village'])
            )

    return Player(
        tag, player_json['name'], player_json['townHallLevel'],
        th_weap_lvl, player_json['expLevel'], player_json['trophies'],
        player_json['bestTrophies'], player_json['warStars'],
        player_json['attackWins'], player_json['defenseWins'],
        bh_lvl, vs_trophies, best_vs_trophies, vs_battle_wins,
        role, player_json['donations'], player_json['donationsReceived'],
        clan_tag, clan_name, clan_lvl, clan_icons,
        league_id, league_name, league_icons, heroes, troops, spells
    )


def json_response(tag, header):
    tag = tag[1:]
    url = f'https://api.clashofclans.com/v1/players/%23{tag}'
    return requests.get(url, headers=header).json()


super_troop_list = [
    'Super Barbarian', 'Super Archer', 'Super Giant', 'Sneaky Goblin',
    'Super Wall Breaker', 'Super Wizard', 'Inferno Dragon', 'Super Minion',
    'Super Valkyrie', 'Super Witch', 'Ice Hound'
]

troop_dict = {
    1: {
        'hero': {
            'Barbarian King': {
                'name': 'Barbarian King', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Archer Queen': {
                'name': 'Archer Queen', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Grand Warden': {
                'name': 'Grand Warden', 'thMax': 0, 'type': 'Elixir'
            },
            'Royal Champion': {
                'name': 'Royal Champion', 'thMax': 0, 'type': 'Dark Elixir'
            }
        },
        'troop': {
            'Barbarian': {
                'name': 'Barbarian', 'thMax': 1, 'type': 'Elixir'
            },
            'Archer': {
                'name': 'Archer', 'thMax': 1, 'type': 'Elixir'
            },
            'Giant': {
                'name': 'Giant', 'thMax': 1, 'type': 'Elixir'
            },
            'Goblin': {
                'name': 'Goblin', 'thMax': 0, 'type': 'Elixir'
            },
            'Wall Breaker': {
                'name': 'Wall Breaker', 'thMax': 0, 'type': 'Elixir'
            },
            'Balloon': {
                'name': 'Balloon', 'thMax': 0, 'type': 'Elixir'
            },
            'Wizard': {
                'name': 'Wizard', 'thMax': 0, 'type': 'Elixir'
            },
            'Healer': {
                'name': 'Healer', 'thMax': 0, 'type': 'Elixir'
            },
            'Dragon': {
                'name': 'Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'P.E.K.K.A': {
                'name': 'P.E.K.K.A', 'thMax': 0, 'type': 'Elixir'
            },
            'Baby Dragon': {
                'name': 'Baby Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Miner': {
                'name': 'Miner', 'thMax': 0, 'type': 'Elixir'
            },
            'Electro Dragon': {
                'name': 'Electro Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Yeti': {
                'name': 'Yeti', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Barbarian': {
                'name': 'Super Barbarian', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Archer': {
                'name': 'Super Archer', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Wall Breaker': {
                'name': 'Super Wall Breaker', 'thMax': 0, 'type': 'Elixir'
            },
            'Sneaky Goblin': {
                'name': 'Sneaky Goblin', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Giant': {
                'name': 'Super Giant', 'thMax': 0, 'type': 'Elixir'
            },
            'Inferno Dragon': {
                'name': 'Inferno Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Valkyrie': {
                'name': 'Super Valkyrie', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Super Witch': {
                'name': 'Super Witch', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Minion': {
                'name': 'Minion', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Hog Rider': {
                'name': 'Hog Rider', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Valkyrie': {
                'name': 'Valkyrie', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Golem': {
                'name': 'Golem', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Witch': {
                'name': 'Witch', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Lava Hound': {
                'name': 'Lava Hound', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Bowler': {
                'name': 'Bowler', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Ice Golem': {
                'name': 'Ice Golem', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Headhunter': {
                'name': 'Headhunter', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Wall Wrecker': {
                'name': 'Wall Wrecker', 'thMax': 0, 'type': 'Gold'
            },
            'Battle Blimp': {
                'name': 'Battle Blimp', 'thMax': 0, 'type': 'Gold'
            },
            'Stone Slammer': {
                'name': 'Stone Slammer', 'thMax': 0, 'type': 'Gold'
            },
            'Siege Barracks': {
                'name': 'Siege Barracks', 'thMax': 0, 'type': 'Gold'
            },
            'Log Launcher': {
                'name': 'Log Launcher', 'thMax': 0, 'type': 'Gold'
            }
        },
        'spell': {
            'Lightning Spell': {
                'name': 'Lightning Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Healing Spell': {
                'name': 'Healing Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Rage Spell': {
                'name': 'Rage Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Jump Spell': {
                'name': 'Jump Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Freeze Spell': {
                'name': 'Freeze Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Clone Spell': {
                'name': 'Clone Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Invisibility Spell': {
                'name': 'Invisibility Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Poison Spell': {
                'name': 'Poison Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Earthquake Spell': {
                'name': 'Earthquake Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Haste Spell': {
                'name': 'Haste Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Skeleton Spell': {
                'name': 'Skeleton Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Bat Spell': {
                'name': 'Bat Spell', 'thMax': 0, 'type': 'Dark Elixir'
            }
        }
    },
    2: {
        'hero': {
            'Barbarian King': {
                'name': 'Barbarian King', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Archer Queen': {
                'name': 'Archer Queen', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Grand Warden': {
                'name': 'Grand Warden', 'thMax': 0, 'type': 'Elixir'
            },
            'Royal Champion': {
                'name': 'Royal Champion', 'thMax': 0, 'type': 'Dark Elixir'
            }
        },
        'troop': {
            'Barbarian': {
                'name': 'Barbarian', 'thMax': 1, 'type': 'Elixir'
            },
            'Archer': {
                'name': 'Archer', 'thMax': 1, 'type': 'Elixir'
            },
            'Giant': {
                'name': 'Giant', 'thMax': 1, 'type': 'Elixir'
            },
            'Goblin': {
                'name': 'Goblin', 'thMax': 1, 'type': 'Elixir'
            },
            'Wall Breaker': {
                'name': 'Wall Breaker', 'thMax': 0, 'type': 'Elixir'
            },
            'Balloon': {
                'name': 'Balloon', 'thMax': 0, 'type': 'Elixir'
            },
            'Wizard': {
                'name': 'Wizard', 'thMax': 0, 'type': 'Elixir'
            },
            'Healer': {
                'name': 'Healer', 'thMax': 0, 'type': 'Elixir'
            },
            'Dragon': {
                'name': 'Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'P.E.K.K.A': {
                'name': 'P.E.K.K.A', 'thMax': 0, 'type': 'Elixir'
            },
            'Baby Dragon': {
                'name': 'Baby Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Miner': {
                'name': 'Miner', 'thMax': 0, 'type': 'Elixir'
            },
            'Electro Dragon': {
                'name': 'Electro Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Yeti': {
                'name': 'Yeti', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Barbarian': {
                'name': 'Super Barbarian', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Archer': {
                'name': 'Super Archer', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Wall Breaker': {
                'name': 'Super Wall Breaker', 'thMax': 0, 'type': 'Elixir'
            },
            'Sneaky Goblin': {
                'name': 'Sneaky Goblin', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Giant': {
                'name': 'Super Giant', 'thMax': 0, 'type': 'Elixir'
            },
            'Inferno Dragon': {
                'name': 'Inferno Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Valkyrie': {
                'name': 'Super Valkyrie', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Super Witch': {
                'name': 'Super Witch', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Minion': {
                'name': 'Minion', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Hog Rider': {
                'name': 'Hog Rider', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Valkyrie': {
                'name': 'Valkyrie', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Golem': {
                'name': 'Golem', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Witch': {
                'name': 'Witch', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Lava Hound': {
                'name': 'Lava Hound', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Bowler': {
                'name': 'Bowler', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Ice Golem': {
                'name': 'Ice Golem', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Headhunter': {
                'name': 'Headhunter', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Wall Wrecker': {
                'name': 'Wall Wrecker', 'thMax': 0, 'type': 'Gold'
            },
            'Battle Blimp': {
                'name': 'Battle Blimp', 'thMax': 0, 'type': 'Gold'
            },
            'Stone Slammer': {
                'name': 'Stone Slammer', 'thMax': 0, 'type': 'Gold'
            },
            'Siege Barracks': {
                'name': 'Siege Barracks', 'thMax': 0, 'type': 'Gold'
            },
            'Log Launcher': {
                'name': 'Log Launcher', 'thMax': 0, 'type': 'Gold'
            }
        },
        'spell': {
            'Lightning Spell': {
                'name': 'Lightning Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Healing Spell': {
                'name': 'Healing Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Rage Spell': {
                'name': 'Rage Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Jump Spell': {
                'name': 'Jump Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Freeze Spell': {
                'name': 'Freeze Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Clone Spell': {
                'name': 'Clone Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Invisibility Spell': {
                'name': 'Invisibility Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Poison Spell': {
                'name': 'Poison Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Earthquake Spell': {
                'name': 'Earthquake Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Haste Spell': {
                'name': 'Haste Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Skeleton Spell': {
                'name': 'Skeleton Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Bat Spell': {
                'name': 'Bat Spell', 'thMax': 0, 'type': 'Dark Elixir'
            }
        }
    },
    3: {
        'hero': {
            'Barbarian King': {
                'name': 'Barbarian King', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Archer Queen': {
                'name': 'Archer Queen', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Grand Warden': {
                'name': 'Grand Warden', 'thMax': 0, 'type': 'Elixir'
            },
            'Royal Champion': {
                'name': 'Royal Champion', 'thMax': 0, 'type': 'Dark Elixir'
            }
        },
        'troop': {
            'Barbarian': {
                'name': 'Barbarian', 'thMax': 2, 'type': 'Elixir'
            },
            'Archer': {
                'name': 'Archer', 'thMax': 2, 'type': 'Elixir'
            },
            'Giant': {
                'name': 'Giant', 'thMax': 1, 'type': 'Elixir'
            },
            'Goblin': {
                'name': 'Goblin', 'thMax': 2, 'type': 'Elixir'
            },
            'Wall Breaker': {
                'name': 'Wall Breaker', 'thMax': 1, 'type': 'Elixir'
            },
            'Balloon': {
                'name': 'Balloon', 'thMax': 0, 'type': 'Elixir'
            },
            'Wizard': {
                'name': 'Wizard', 'thMax': 0, 'type': 'Elixir'
            },
            'Healer': {
                'name': 'Healer', 'thMax': 0, 'type': 'Elixir'
            },
            'Dragon': {
                'name': 'Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'P.E.K.K.A': {
                'name': 'P.E.K.K.A', 'thMax': 0, 'type': 'Elixir'
            },
            'Baby Dragon': {
                'name': 'Baby Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Miner': {
                'name': 'Miner', 'thMax': 0, 'type': 'Elixir'
            },
            'Electro Dragon': {
                'name': 'Electro Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Yeti': {
                'name': 'Yeti', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Barbarian': {
                'name': 'Super Barbarian', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Archer': {
                'name': 'Super Archer', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Wall Breaker': {
                'name': 'Super Wall Breaker', 'thMax': 0, 'type': 'Elixir'
            },
            'Sneaky Goblin': {
                'name': 'Sneaky Goblin', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Giant': {
                'name': 'Super Giant', 'thMax': 0, 'type': 'Elixir'
            },
            'Inferno Dragon': {
                'name': 'Inferno Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Valkyrie': {
                'name': 'Super Valkyrie', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Super Witch': {
                'name': 'Super Witch', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Minion': {
                'name': 'Minion', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Hog Rider': {
                'name': 'Hog Rider', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Valkyrie': {
                'name': 'Valkyrie', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Golem': {
                'name': 'Golem', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Witch': {
                'name': 'Witch', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Lava Hound': {
                'name': 'Lava Hound', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Bowler': {
                'name': 'Bowler', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Ice Golem': {
                'name': 'Ice Golem', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Headhunter': {
                'name': 'Headhunter', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Wall Wrecker': {
                'name': 'Wall Wrecker', 'thMax': 0, 'type': 'Gold'
            },
            'Battle Blimp': {
                'name': 'Battle Blimp', 'thMax': 0, 'type': 'Gold'
            },
            'Stone Slammer': {
                'name': 'Stone Slammer', 'thMax': 0, 'type': 'Gold'
            },
            'Siege Barracks': {
                'name': 'Siege Barracks', 'thMax': 0, 'type': 'Gold'
            },
            'Log Launcher': {
                'name': 'Log Launcher', 'thMax': 0, 'type': 'Gold'
            }
        },
        'spell': {
            'Lightning Spell': {
                'name': 'Lightning Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Healing Spell': {
                'name': 'Healing Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Rage Spell': {
                'name': 'Rage Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Jump Spell': {
                'name': 'Jump Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Freeze Spell': {
                'name': 'Freeze Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Clone Spell': {
                'name': 'Clone Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Invisibility Spell': {
                'name': 'Invisibility Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Poison Spell': {
                'name': 'Poison Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Earthquake Spell': {
                'name': 'Earthquake Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Haste Spell': {
                'name': 'Haste Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Skeleton Spell': {
                'name': 'Skeleton Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Bat Spell': {
                'name': 'Bat Spell', 'thMax': 0, 'type': 'Dark Elixir'
            }
        }
    },
    4: {
        'hero': {
            'Barbarian King': {
                'name': 'Barbarian King', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Archer Queen': {
                'name': 'Archer Queen', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Grand Warden': {
                'name': 'Grand Warden', 'thMax': 0, 'type': 'Elixir'
            },
            'Royal Champion': {
                'name': 'Royal Champion', 'thMax': 0, 'type': 'Dark Elixir'
            }
        },
        'troop': {
            'Barbarian': {
                'name': 'Barbarian', 'thMax': 2, 'type': 'Elixir'
            },
            'Archer': {
                'name': 'Archer', 'thMax': 2, 'type': 'Elixir'
            },
            'Giant': {
                'name': 'Giant', 'thMax': 2, 'type': 'Elixir'
            },
            'Goblin': {
                'name': 'Goblin', 'thMax': 2, 'type': 'Elixir'
            },
            'Wall Breaker': {
                'name': 'Wall Breaker', 'thMax': 2, 'type': 'Elixir'
            },
            'Balloon': {
                'name': 'Balloon', 'thMax': 2, 'type': 'Elixir'
            },
            'Wizard': {
                'name': 'Wizard', 'thMax': 0, 'type': 'Elixir'
            },
            'Healer': {
                'name': 'Healer', 'thMax': 0, 'type': 'Elixir'
            },
            'Dragon': {
                'name': 'Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'P.E.K.K.A': {
                'name': 'P.E.K.K.A', 'thMax': 0, 'type': 'Elixir'
            },
            'Baby Dragon': {
                'name': 'Baby Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Miner': {
                'name': 'Miner', 'thMax': 0, 'type': 'Elixir'
            },
            'Electro Dragon': {
                'name': 'Electro Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Yeti': {
                'name': 'Yeti', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Barbarian': {
                'name': 'Super Barbarian', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Archer': {
                'name': 'Super Archer', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Wall Breaker': {
                'name': 'Super Wall Breaker', 'thMax': 0, 'type': 'Elixir'
            },
            'Sneaky Goblin': {
                'name': 'Sneaky Goblin', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Giant': {
                'name': 'Super Giant', 'thMax': 0, 'type': 'Elixir'
            },
            'Inferno Dragon': {
                'name': 'Inferno Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Valkyrie': {
                'name': 'Super Valkyrie', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Super Witch': {
                'name': 'Super Witch', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Minion': {
                'name': 'Minion', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Hog Rider': {
                'name': 'Hog Rider', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Valkyrie': {
                'name': 'Valkyrie', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Golem': {
                'name': 'Golem', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Witch': {
                'name': 'Witch', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Lava Hound': {
                'name': 'Lava Hound', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Bowler': {
                'name': 'Bowler', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Ice Golem': {
                'name': 'Ice Golem', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Headhunter': {
                'name': 'Headhunter', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Wall Wrecker': {
                'name': 'Wall Wrecker', 'thMax': 0, 'type': 'Gold'
            },
            'Battle Blimp': {
                'name': 'Battle Blimp', 'thMax': 0, 'type': 'Gold'
            },
            'Stone Slammer': {
                'name': 'Stone Slammer', 'thMax': 0, 'type': 'Gold'
            },
            'Siege Barracks': {
                'name': 'Siege Barracks', 'thMax': 0, 'type': 'Gold'
            },
            'Log Launcher': {
                'name': 'Log Launcher', 'thMax': 0, 'type': 'Gold'
            }
        },
        'spell': {
            'Lightning Spell': {
                'name': 'Lightning Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Healing Spell': {
                'name': 'Healing Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Rage Spell': {
                'name': 'Rage Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Jump Spell': {
                'name': 'Jump Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Freeze Spell': {
                'name': 'Freeze Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Clone Spell': {
                'name': 'Clone Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Invisibility Spell': {
                'name': 'Invisibility Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Poison Spell': {
                'name': 'Poison Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Earthquake Spell': {
                'name': 'Earthquake Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Haste Spell': {
                'name': 'Haste Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Skeleton Spell': {
                'name': 'Skeleton Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Bat Spell': {
                'name': 'Bat Spell', 'thMax': 0, 'type': 'Dark Elixir'
            }
        }
    },
    5: {
        'hero': {
            'Barbarian King': {
                'name': 'Barbarian King', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Archer Queen': {
                'name': 'Archer Queen', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Grand Warden': {
                'name': 'Grand Warden', 'thMax': 0, 'type': 'Elixir'
            },
            'Royal Champion': {
                'name': 'Royal Champion', 'thMax': 0, 'type': 'Dark Elixir'
            }
        },
        'troop': {
            'Barbarian': {
                'name': 'Barbarian', 'thMax': 3, 'type': 'Elixir'
            },
            'Archer': {
                'name': 'Archer', 'thMax': 3, 'type': 'Elixir'
            },
            'Giant': {
                'name': 'Giant', 'thMax': 2, 'type': 'Elixir'
            },
            'Goblin': {
                'name': 'Goblin', 'thMax': 3, 'type': 'Elixir'
            },
            'Wall Breaker': {
                'name': 'Wall Breaker', 'thMax': 2, 'type': 'Elixir'
            },
            'Balloon': {
                'name': 'Balloon', 'thMax': 2, 'type': 'Elixir'
            },
            'Wizard': {
                'name': 'Wizard', 'thMax': 2, 'type': 'Elixir'
            },
            'Healer': {
                'name': 'Healer', 'thMax': 0, 'type': 'Elixir'
            },
            'Dragon': {
                'name': 'Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'P.E.K.K.A': {
                'name': 'P.E.K.K.A', 'thMax': 0, 'type': 'Elixir'
            },
            'Baby Dragon': {
                'name': 'Baby Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Miner': {
                'name': 'Miner', 'thMax': 0, 'type': 'Elixir'
            },
            'Electro Dragon': {
                'name': 'Electro Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Yeti': {
                'name': 'Yeti', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Barbarian': {
                'name': 'Super Barbarian', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Archer': {
                'name': 'Super Archer', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Wall Breaker': {
                'name': 'Super Wall Breaker', 'thMax': 0, 'type': 'Elixir'
            },
            'Sneaky Goblin': {
                'name': 'Sneaky Goblin', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Giant': {
                'name': 'Super Giant', 'thMax': 0, 'type': 'Elixir'
            },
            'Inferno Dragon': {
                'name': 'Inferno Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Valkyrie': {
                'name': 'Super Valkyrie', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Super Witch': {
                'name': 'Super Witch', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Minion': {
                'name': 'Minion', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Hog Rider': {
                'name': 'Hog Rider', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Valkyrie': {
                'name': 'Valkyrie', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Golem': {
                'name': 'Golem', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Witch': {
                'name': 'Witch', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Lava Hound': {
                'name': 'Lava Hound', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Bowler': {
                'name': 'Bowler', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Ice Golem': {
                'name': 'Ice Golem', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Headhunter': {
                'name': 'Headhunter', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Wall Wrecker': {
                'name': 'Wall Wrecker', 'thMax': 0, 'type': 'Gold'
            },
            'Battle Blimp': {
                'name': 'Battle Blimp', 'thMax': 0, 'type': 'Gold'
            },
            'Stone Slammer': {
                'name': 'Stone Slammer', 'thMax': 0, 'type': 'Gold'
            },
            'Siege Barracks': {
                'name': 'Siege Barracks', 'thMax': 0, 'type': 'Gold'
            },
            'Log Launcher': {
                'name': 'Log Launcher', 'thMax': 0, 'type': 'Gold'
            }
        },
        'spell': {
            'Lightning Spell': {
                'name': 'Lightning Spell', 'thMax': 4, 'type': 'Elixir'
            },
            'Healing Spell': {
                'name': 'Healing Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Rage Spell': {
                'name': 'Rage Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Jump Spell': {
                'name': 'Jump Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Freeze Spell': {
                'name': 'Freeze Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Clone Spell': {
                'name': 'Clone Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Invisibility Spell': {
                'name': 'Invisibility Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Poison Spell': {
                'name': 'Poison Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Earthquake Spell': {
                'name': 'Earthquake Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Haste Spell': {
                'name': 'Haste Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Skeleton Spell': {
                'name': 'Skeleton Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Bat Spell': {
                'name': 'Bat Spell', 'thMax': 0, 'type': 'Dark Elixir'
            }
        }
    },
    6: {
        'hero': {
            'Barbarian King': {
                'name': 'Barbarian King', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Archer Queen': {
                'name': 'Archer Queen', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Grand Warden': {
                'name': 'Grand Warden', 'thMax': 0, 'type': 'Elixir'
            },
            'Royal Champion': {
                'name': 'Royal Champion', 'thMax': 0, 'type': 'Dark Elixir'
            }
        },
        'troop': {
            'Barbarian': {
                'name': 'Barbarian', 'thMax': 3, 'type': 'Elixir'
            },
            'Archer': {
                'name': 'Archer', 'thMax': 3, 'type': 'Elixir'
            },
            'Giant': {
                'name': 'Giant', 'thMax': 3, 'type': 'Elixir'
            },
            'Goblin': {
                'name': 'Goblin', 'thMax': 3, 'type': 'Elixir'
            },
            'Wall Breaker': {
                'name': 'Wall Breaker', 'thMax': 3, 'type': 'Elixir'
            },
            'Balloon': {
                'name': 'Balloon', 'thMax': 3, 'type': 'Elixir'
            },
            'Wizard': {
                'name': 'Wizard', 'thMax': 3, 'type': 'Elixir'
            },
            'Healer': {
                'name': 'Healer', 'thMax': 1, 'type': 'Elixir'
            },
            'Dragon': {
                'name': 'Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'P.E.K.K.A': {
                'name': 'P.E.K.K.A', 'thMax': 0, 'type': 'Elixir'
            },
            'Baby Dragon': {
                'name': 'Baby Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Miner': {
                'name': 'Miner', 'thMax': 0, 'type': 'Elixir'
            },
            'Electro Dragon': {
                'name': 'Electro Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Yeti': {
                'name': 'Yeti', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Barbarian': {
                'name': 'Super Barbarian', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Archer': {
                'name': 'Super Archer', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Wall Breaker': {
                'name': 'Super Wall Breaker', 'thMax': 0, 'type': 'Elixir'
            },
            'Sneaky Goblin': {
                'name': 'Sneaky Goblin', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Giant': {
                'name': 'Super Giant', 'thMax': 0, 'type': 'Elixir'
            },
            'Inferno Dragon': {
                'name': 'Inferno Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Valkyrie': {
                'name': 'Super Valkyrie', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Super Witch': {
                'name': 'Super Witch', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Minion': {
                'name': 'Minion', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Hog Rider': {
                'name': 'Hog Rider', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Valkyrie': {
                'name': 'Valkyrie', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Golem': {
                'name': 'Golem', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Witch': {
                'name': 'Witch', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Lava Hound': {
                'name': 'Lava Hound', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Bowler': {
                'name': 'Bowler', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Ice Golem': {
                'name': 'Ice Golem', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Headhunter': {
                'name': 'Headhunter', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Wall Wrecker': {
                'name': 'Wall Wrecker', 'thMax': 0, 'type': 'Gold'
            },
            'Battle Blimp': {
                'name': 'Battle Blimp', 'thMax': 0, 'type': 'Gold'
            },
            'Stone Slammer': {
                'name': 'Stone Slammer', 'thMax': 0, 'type': 'Gold'
            },
            'Siege Barracks': {
                'name': 'Siege Barracks', 'thMax': 0, 'type': 'Gold'
            },
            'Log Launcher': {
                'name': 'Log Launcher', 'thMax': 0, 'type': 'Gold'
            }
        },
        'spell': {
            'Lightning Spell': {
                'name': 'Lightning Spell', 'thMax': 4, 'type': 'Elixir'
            },
            'Healing Spell': {
                'name': 'Healing Spell', 'thMax': 3, 'type': 'Elixir'
            },
            'Rage Spell': {
                'name': 'Rage Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Jump Spell': {
                'name': 'Jump Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Freeze Spell': {
                'name': 'Freeze Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Clone Spell': {
                'name': 'Clone Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Invisibility Spell': {
                'name': 'Invisibility Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Poison Spell': {
                'name': 'Poison Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Earthquake Spell': {
                'name': 'Earthquake Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Haste Spell': {
                'name': 'Haste Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Skeleton Spell': {
                'name': 'Skeleton Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Bat Spell': {
                'name': 'Bat Spell', 'thMax': 0, 'type': 'Dark Elixir'
            }
        }
    },
    7: {
        'hero': {
            'Barbarian King': {
                'name': 'Barbarian King', 'thMax': 5, 'type': 'Dark Elixir'
            },
            'Archer Queen': {
                'name': 'Archer Queen', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Grand Warden': {
                'name': 'Grand Warden', 'thMax': 0, 'type': 'Elixir'
            },
            'Royal Champion': {
                'name': 'Royal Champion', 'thMax': 0, 'type': 'Dark Elixir'
            }
        },
        'troop': {
            'Barbarian': {
                'name': 'Barbarian', 'thMax': 4, 'type': 'Elixir'
            },
            'Archer': {
                'name': 'Archer', 'thMax': 4, 'type': 'Elixir'
            },
            'Giant': {
                'name': 'Giant', 'thMax': 4, 'type': 'Elixir'
            },
            'Goblin': {
                'name': 'Goblin', 'thMax': 4, 'type': 'Elixir'
            },
            'Wall Breaker': {
                'name': 'Wall Breaker', 'thMax': 4, 'type': 'Elixir'
            },
            'Balloon': {
                'name': 'Balloon', 'thMax': 4, 'type': 'Elixir'
            },
            'Wizard': {
                'name': 'Wizard', 'thMax': 4, 'type': 'Elixir'
            },
            'Healer': {
                'name': 'Healer', 'thMax': 2, 'type': 'Elixir'
            },
            'Dragon': {
                'name': 'Dragon', 'thMax': 2, 'type': 'Elixir'
            },
            'P.E.K.K.A': {
                'name': 'P.E.K.K.A', 'thMax': 0, 'type': 'Elixir'
            },
            'Baby Dragon': {
                'name': 'Baby Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Miner': {
                'name': 'Miner', 'thMax': 0, 'type': 'Elixir'
            },
            'Electro Dragon': {
                'name': 'Electro Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Yeti': {
                'name': 'Yeti', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Barbarian': {
                'name': 'Super Barbarian', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Archer': {
                'name': 'Super Archer', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Wall Breaker': {
                'name': 'Super Wall Breaker', 'thMax': 0, 'type': 'Elixir'
            },
            'Sneaky Goblin': {
                'name': 'Sneaky Goblin', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Giant': {
                'name': 'Super Giant', 'thMax': 0, 'type': 'Elixir'
            },
            'Inferno Dragon': {
                'name': 'Inferno Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Valkyrie': {
                'name': 'Super Valkyrie', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Super Witch': {
                'name': 'Super Witch', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Minion': {
                'name': 'Minion', 'thMax': 2, 'type': 'Dark Elixir'
            },
            'Hog Rider': {
                'name': 'Hog Rider', 'thMax': 2, 'type': 'Dark Elixir'
            },
            'Valkyrie': {
                'name': 'Valkyrie', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Golem': {
                'name': 'Golem', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Witch': {
                'name': 'Witch', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Lava Hound': {
                'name': 'Lava Hound', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Bowler': {
                'name': 'Bowler', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Ice Golem': {
                'name': 'Ice Golem', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Headhunter': {
                'name': 'Headhunter', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Wall Wrecker': {
                'name': 'Wall Wrecker', 'thMax': 0, 'type': 'Gold'
            },
            'Battle Blimp': {
                'name': 'Battle Blimp', 'thMax': 0, 'type': 'Gold'
            },
            'Stone Slammer': {
                'name': 'Stone Slammer', 'thMax': 0, 'type': 'Gold'
            },
            'Siege Barracks': {
                'name': 'Siege Barracks', 'thMax': 0, 'type': 'Gold'
            },
            'Log Launcher': {
                'name': 'Log Launcher', 'thMax': 0, 'type': 'Gold'
            }
        },
        'spell': {
            'Lightning Spell': {
                'name': 'Lightning Spell', 'thMax': 4, 'type': 'Elixir'
            },
            'Healing Spell': {
                'name': 'Healing Spell', 'thMax': 4, 'type': 'Elixir'
            },
            'Rage Spell': {
                'name': 'Rage Spell', 'thMax': 4, 'type': 'Elixir'
            },
            'Jump Spell': {
                'name': 'Jump Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Freeze Spell': {
                'name': 'Freeze Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Clone Spell': {
                'name': 'Clone Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Invisibility Spell': {
                'name': 'Invisibility Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Poison Spell': {
                'name': 'Poison Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Earthquake Spell': {
                'name': 'Earthquake Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Haste Spell': {
                'name': 'Haste Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Skeleton Spell': {
                'name': 'Skeleton Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Bat Spell': {
                'name': 'Bat Spell', 'thMax': 0, 'type': 'Dark Elixir'
            }
        }
    },
    8: {
        'hero': {
            'Barbarian King': {
                'name': 'Barbarian King', 'thMax': 10, 'type': 'Dark Elixir'
            },
            'Archer Queen': {
                'name': 'Archer Queen', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Grand Warden': {
                'name': 'Grand Warden', 'thMax': 0, 'type': 'Elixir'
            },
            'Royal Champion': {
                'name': 'Royal Champion', 'thMax': 0, 'type': 'Dark Elixir'
            }
        },
        'troop': {
            'Barbarian': {
                'name': 'Barbarian', 'thMax': 5, 'type': 'Elixir'
            },
            'Archer': {
                'name': 'Archer', 'thMax': 5, 'type': 'Elixir'
            },
            'Giant': {
                'name': 'Giant', 'thMax': 5, 'type': 'Elixir'
            },
            'Goblin': {
                'name': 'Goblin', 'thMax': 5, 'type': 'Elixir'
            },
            'Wall Breaker': {
                'name': 'Wall Breaker', 'thMax': 5, 'type': 'Elixir'
            },
            'Balloon': {
                'name': 'Balloon', 'thMax': 5, 'type': 'Elixir'
            },
            'Wizard': {
                'name': 'Wizard', 'thMax': 5, 'type': 'Elixir'
            },
            'Healer': {
                'name': 'Healer', 'thMax': 3, 'type': 'Elixir'
            },
            'Dragon': {
                'name': 'Dragon', 'thMax': 3, 'type': 'Elixir'
            },
            'P.E.K.K.A': {
                'name': 'P.E.K.K.A', 'thMax': 3, 'type': 'Elixir'
            },
            'Baby Dragon': {
                'name': 'Baby Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Miner': {
                'name': 'Miner', 'thMax': 0, 'type': 'Elixir'
            },
            'Electro Dragon': {
                'name': 'Electro Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Yeti': {
                'name': 'Yeti', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Barbarian': {
                'name': 'Super Barbarian', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Archer': {
                'name': 'Super Archer', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Wall Breaker': {
                'name': 'Super Wall Breaker', 'thMax': 0, 'type': 'Elixir'
            },
            'Sneaky Goblin': {
                'name': 'Sneaky Goblin', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Giant': {
                'name': 'Super Giant', 'thMax': 0, 'type': 'Elixir'
            },
            'Inferno Dragon': {
                'name': 'Inferno Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Valkyrie': {
                'name': 'Super Valkyrie', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Super Witch': {
                'name': 'Super Witch', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Minion': {
                'name': 'Minion', 'thMax': 4, 'type': 'Dark Elixir'
            },
            'Hog Rider': {
                'name': 'Hog Rider', 'thMax': 4, 'type': 'Dark Elixir'
            },
            'Valkyrie': {
                'name': 'Valkyrie', 'thMax': 2, 'type': 'Dark Elixir'
            },
            'Golem': {
                'name': 'Golem', 'thMax': 2, 'type': 'Dark Elixir'
            },
            'Witch': {
                'name': 'Witch', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Lava Hound': {
                'name': 'Lava Hound', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Bowler': {
                'name': 'Bowler', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Ice Golem': {
                'name': 'Ice Golem', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Headhunter': {
                'name': 'Headhunter', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Wall Wrecker': {
                'name': 'Wall Wrecker', 'thMax': 0, 'type': 'Gold'
            },
            'Battle Blimp': {
                'name': 'Battle Blimp', 'thMax': 0, 'type': 'Gold'
            },
            'Stone Slammer': {
                'name': 'Stone Slammer', 'thMax': 0, 'type': 'Gold'
            },
            'Siege Barracks': {
                'name': 'Siege Barracks', 'thMax': 0, 'type': 'Gold'
            },
            'Log Launcher': {
                'name': 'Log Launcher', 'thMax': 0, 'type': 'Gold'
            }
        },
        'spell': {
            'Lightning Spell': {
                'name': 'Lightning Spell', 'thMax': 5, 'type': 'Elixir'
            },
            'Healing Spell': {
                'name': 'Healing Spell', 'thMax': 5, 'type': 'Elixir'
            },
            'Rage Spell': {
                'name': 'Rage Spell', 'thMax': 5, 'type': 'Elixir'
            },
            'Jump Spell': {
                'name': 'Jump Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Freeze Spell': {
                'name': 'Freeze Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Clone Spell': {
                'name': 'Clone Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Invisibility Spell': {
                'name': 'Invisibility Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Poison Spell': {
                'name': 'Poison Spell', 'thMax': 2, 'type': 'Dark Elixir'
            },
            'Earthquake Spell': {
                'name': 'Earthquake Spell', 'thMax': 2, 'type': 'Dark Elixir'
            },
            'Haste Spell': {
                'name': 'Haste Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Skeleton Spell': {
                'name': 'Skeleton Spell', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Bat Spell': {
                'name': 'Bat Spell', 'thMax': 0, 'type': 'Dark Elixir'
            }
        }
    },
    9: {
        'hero': {
            'Barbarian King': {
                'name': 'Barbarian King', 'thMax': 30, 'type': 'Dark Elixir'
            },
            'Archer Queen': {
                'name': 'Archer Queen', 'thMax': 30, 'type': 'Dark Elixir'
            },
            'Grand Warden': {
                'name': 'Grand Warden', 'thMax': 0, 'type': 'Elixir'
            },
            'Royal Champion': {
                'name': 'Royal Champion', 'thMax': 0, 'type': 'Dark Elixir'
            }
        },
        'troop': {
            'Barbarian': {
                'name': 'Barbarian', 'thMax': 6, 'type': 'Elixir'
            },
            'Archer': {
                'name': 'Archer', 'thMax': 6, 'type': 'Elixir'
            },
            'Giant': {
                'name': 'Giant', 'thMax': 6, 'type': 'Elixir'
            },
            'Goblin': {
                'name': 'Goblin', 'thMax': 6, 'type': 'Elixir'
            },
            'Wall Breaker': {
                'name': 'Wall Breaker', 'thMax': 5, 'type': 'Elixir'
            },
            'Balloon': {
                'name': 'Balloon', 'thMax': 6, 'type': 'Elixir'
            },
            'Wizard': {
                'name': 'Wizard', 'thMax': 6, 'type': 'Elixir'
            },
            'Healer': {
                'name': 'Healer', 'thMax': 4, 'type': 'Elixir'
            },
            'Dragon': {
                'name': 'Dragon', 'thMax': 4, 'type': 'Elixir'
            },
            'P.E.K.K.A': {
                'name': 'P.E.K.K.A', 'thMax': 4, 'type': 'Elixir'
            },
            'Baby Dragon': {
                'name': 'Baby Dragon', 'thMax': 2, 'type': 'Elixir'
            },
            'Miner': {
                'name': 'Miner', 'thMax': 0, 'type': 'Elixir'
            },
            'Electro Dragon': {
                'name': 'Electro Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Yeti': {
                'name': 'Yeti', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Barbarian': {
                'name': 'Super Barbarian', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Archer': {
                'name': 'Super Archer', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Wall Breaker': {
                'name': 'Super Wall Breaker', 'thMax': 0, 'type': 'Elixir'
            },
            'Sneaky Goblin': {
                'name': 'Sneaky Goblin', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Giant': {
                'name': 'Super Giant', 'thMax': 0, 'type': 'Elixir'
            },
            'Inferno Dragon': {
                'name': 'Inferno Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Valkyrie': {
                'name': 'Super Valkyrie', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Super Witch': {
                'name': 'Super Witch', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Minion': {
                'name': 'Minion', 'thMax': 5, 'type': 'Dark Elixir'
            },
            'Hog Rider': {
                'name': 'Hog Rider', 'thMax': 5, 'type': 'Dark Elixir'
            },
            'Valkyrie': {
                'name': 'Valkyrie', 'thMax': 4, 'type': 'Dark Elixir'
            },
            'Golem': {
                'name': 'Golem', 'thMax': 4, 'type': 'Dark Elixir'
            },
            'Witch': {
                'name': 'Witch', 'thMax': 2, 'type': 'Dark Elixir'
            },
            'Lava Hound': {
                'name': 'Lava Hound', 'thMax': 2, 'type': 'Dark Elixir'
            },
            'Bowler': {
                'name': 'Bowler', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Ice Golem': {
                'name': 'Ice Golem', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Headhunter': {
                'name': 'Headhunter', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Wall Wrecker': {
                'name': 'Wall Wrecker', 'thMax': 0, 'type': 'Gold'
            },
            'Battle Blimp': {
                'name': 'Battle Blimp', 'thMax': 0, 'type': 'Gold'
            },
            'Stone Slammer': {
                'name': 'Stone Slammer', 'thMax': 0, 'type': 'Gold'
            },
            'Siege Barracks': {
                'name': 'Siege Barracks', 'thMax': 0, 'type': 'Gold'
            },
            'Log Launcher': {
                'name': 'Log Launcher', 'thMax': 0, 'type': 'Gold'
            }
        },
        'spell': {
            'Lightning Spell': {
                'name': 'Lightning Spell', 'thMax': 6, 'type': 'Elixir'
            },
            'Healing Spell': {
                'name': 'Healing Spell', 'thMax': 6, 'type': 'Elixir'
            },
            'Rage Spell': {
                'name': 'Rage Spell', 'thMax': 5, 'type': 'Elixir'
            },
            'Jump Spell': {
                'name': 'Jump Spell', 'thMax': 2, 'type': 'Elixir'
            },
            'Freeze Spell': {
                'name': 'Freeze Spell', 'thMax': 1, 'type': 'Elixir'
            },
            'Clone Spell': {
                'name': 'Clone Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Invisibility Spell': {
                'name': 'Invisibility Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Poison Spell': {
                'name': 'Poison Spell', 'thMax': 3, 'type': 'Dark Elixir'
            },
            'Earthquake Spell': {
                'name': 'Earthquake Spell', 'thMax': 3, 'type': 'Dark Elixir'
            },
            'Haste Spell': {
                'name': 'Haste Spell', 'thMax': 2, 'type': 'Dark Elixir'
            },
            'Skeleton Spell': {
                'name': 'Skeleton Spell', 'thMax': 1, 'type': 'Dark Elixir'
            },
            'Bat Spell': {
                'name': 'Bat Spell', 'thMax': 0, 'type': 'Dark Elixir'
            }
        }
    },
    10: {
        'hero': {
            'Barbarian King': {
                'name': 'Barbarian King', 'thMax': 40, 'type': 'Dark Elixir'
            },
            'Archer Queen': {
                'name': 'Archer Queen', 'thMax': 40, 'type': 'Dark Elixir'
            },
            'Grand Warden': {
                'name': 'Grand Warden', 'thMax': 0, 'type': 'Elixir'
            },
            'Royal Champion': {
                'name': 'Royal Champion', 'thMax': 0, 'type': 'Dark Elixir'
            }
        },
        'troop': {
            'Barbarian': {
                'name': 'Barbarian', 'thMax': 7, 'type': 'Elixir'
            },
            'Archer': {
                'name': 'Archer', 'thMax': 7, 'type': 'Elixir'
            },
            'Giant': {
                'name': 'Giant', 'thMax': 7, 'type': 'Elixir'
            },
            'Goblin': {
                'name': 'Goblin', 'thMax': 7, 'type': 'Elixir'
            },
            'Wall Breaker': {
                'name': 'Wall Breaker', 'thMax': 6, 'type': 'Elixir'
            },
            'Balloon': {
                'name': 'Balloon', 'thMax': 6, 'type': 'Elixir'
            },
            'Wizard': {
                'name': 'Wizard', 'thMax': 7, 'type': 'Elixir'
            },
            'Healer': {
                'name': 'Healer', 'thMax': 4, 'type': 'Elixir'
            },
            'Dragon': {
                'name': 'Dragon', 'thMax': 5, 'type': 'Elixir'
            },
            'P.E.K.K.A': {
                'name': 'P.E.K.K.A', 'thMax': 6, 'type': 'Elixir'
            },
            'Baby Dragon': {
                'name': 'Baby Dragon', 'thMax': 4, 'type': 'Elixir'
            },
            'Miner': {
                'name': 'Miner', 'thMax': 3, 'type': 'Elixir'
            },
            'Electro Dragon': {
                'name': 'Electro Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Yeti': {
                'name': 'Yeti', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Barbarian': {
                'name': 'Super Barbarian', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Archer': {
                'name': 'Super Archer', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Wall Breaker': {
                'name': 'Super Wall Breaker', 'thMax': 0, 'type': 'Elixir'
            },
            'Sneaky Goblin': {
                'name': 'Sneaky Goblin', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Giant': {
                'name': 'Super Giant', 'thMax': 0, 'type': 'Elixir'
            },
            'Inferno Dragon': {
                'name': 'Inferno Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Valkyrie': {
                'name': 'Super Valkyrie', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Super Witch': {
                'name': 'Super Witch', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Minion': {
                'name': 'Minion', 'thMax': 6, 'type': 'Dark Elixir'
            },
            'Hog Rider': {
                'name': 'Hog Rider', 'thMax': 6, 'type': 'Dark Elixir'
            },
            'Valkyrie': {
                'name': 'Valkyrie', 'thMax': 5, 'type': 'Dark Elixir'
            },
            'Golem': {
                'name': 'Golem', 'thMax': 5, 'type': 'Dark Elixir'
            },
            'Witch': {
                'name': 'Witch', 'thMax': 3, 'type': 'Dark Elixir'
            },
            'Lava Hound': {
                'name': 'Lava Hound', 'thMax': 3, 'type': 'Dark Elixir'
            },
            'Bowler': {
                'name': 'Bowler', 'thMax': 2, 'type': 'Dark Elixir'
            },
            'Ice Golem': {
                'name': 'Ice Golem', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Headhunter': {
                'name': 'Headhunter', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Wall Wrecker': {
                'name': 'Wall Wrecker', 'thMax': 0, 'type': 'Gold'
            },
            'Battle Blimp': {
                'name': 'Battle Blimp', 'thMax': 0, 'type': 'Gold'
            },
            'Stone Slammer': {
                'name': 'Stone Slammer', 'thMax': 0, 'type': 'Gold'
            },
            'Siege Barracks': {
                'name': 'Siege Barracks', 'thMax': 0, 'type': 'Gold'
            },
            'Log Launcher': {
                'name': 'Log Launcher', 'thMax': 0, 'type': 'Gold'
            }
        },
        'spell': {
            'Lightning Spell': {
                'name': 'Lightning Spell', 'thMax': 7, 'type': 'Elixir'
            },
            'Healing Spell': {
                'name': 'Healing Spell', 'thMax': 7, 'type': 'Elixir'
            },
            'Rage Spell': {
                'name': 'Rage Spell', 'thMax': 5, 'type': 'Elixir'
            },
            'Jump Spell': {
                'name': 'Jump Spell', 'thMax': 3, 'type': 'Elixir'
            },
            'Freeze Spell': {
                'name': 'Freeze Spell', 'thMax': 5, 'type': 'Elixir'
            },
            'Clone Spell': {
                'name': 'Clone Spell', 'thMax': 3, 'type': 'Elixir'
            },
            'Invisibility Spell': {
                'name': 'Invisibility Spell', 'thMax': 0, 'type': 'Elixir'
            },
            'Poison Spell': {
                'name': 'Poison Spell', 'thMax': 4, 'type': 'Dark Elixir'
            },
            'Earthquake Spell': {
                'name': 'Earthquake Spell', 'thMax': 4, 'type': 'Dark Elixir'
            },
            'Haste Spell': {
                'name': 'Haste Spell', 'thMax': 4, 'type': 'Dark Elixir'
            },
            'Skeleton Spell': {
                'name': 'Skeleton Spell', 'thMax': 3, 'type': 'Dark Elixir'
            },
            'Bat Spell': {
                'name': 'Bat Spell', 'thMax': 3, 'type': 'Dark Elixir'
            }
        }
    },
    11: {
        'hero': {
            'Barbarian King': {
                'name': 'Barbarian King', 'thMax': 50, 'type': 'Dark Elixir'
            },
            'Archer Queen': {
                'name': 'Archer Queen', 'thMax': 50, 'type': 'Dark Elixir'
            },
            'Grand Warden': {
                'name': 'Grand Warden', 'thMax': 20, 'type': 'Elixir'
            },
            'Royal Champion': {
                'name': 'Royal Champion', 'thMax': 0, 'type': 'Dark Elixir'
            }
        },
        'troop': {
            'Barbarian': {
                'name': 'Barbarian', 'thMax': 8, 'type': 'Elixir'
            },
            'Archer': {
                'name': 'Archer', 'thMax': 8, 'type': 'Elixir'
            },
            'Giant': {
                'name': 'Giant', 'thMax': 8, 'type': 'Elixir'
            },
            'Goblin': {
                'name': 'Goblin', 'thMax': 7, 'type': 'Elixir'
            },
            'Wall Breaker': {
                'name': 'Wall Breaker', 'thMax': 7, 'type': 'Elixir'
            },
            'Balloon': {
                'name': 'Balloon', 'thMax': 7, 'type': 'Elixir'
            },
            'Wizard': {
                'name': 'Wizard', 'thMax': 8, 'type': 'Elixir'
            },
            'Healer': {
                'name': 'Healer', 'thMax': 5, 'type': 'Elixir'
            },
            'Dragon': {
                'name': 'Dragon', 'thMax': 6, 'type': 'Elixir'
            },
            'P.E.K.K.A': {
                'name': 'P.E.K.K.A', 'thMax': 7, 'type': 'Elixir'
            },
            'Baby Dragon': {
                'name': 'Baby Dragon', 'thMax': 5, 'type': 'Elixir'
            },
            'Miner': {
                'name': 'Miner', 'thMax': 5, 'type': 'Elixir'
            },
            'Electro Dragon': {
                'name': 'Electro Dragon', 'thMax': 2, 'type': 'Elixir'
            },
            'Yeti': {
                'name': 'Yeti', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Barbarian': {
                'name': 'Super Barbarian', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Archer': {
                'name': 'Super Archer', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Wall Breaker': {
                'name': 'Super Wall Breaker', 'thMax': 0, 'type': 'Elixir'
            },
            'Sneaky Goblin': {
                'name': 'Sneaky Goblin', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Giant': {
                'name': 'Super Giant', 'thMax': 0, 'type': 'Elixir'
            },
            'Inferno Dragon': {
                'name': 'Inferno Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Valkyrie': {
                'name': 'Super Valkyrie', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Super Witch': {
                'name': 'Super Witch', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Minion': {
                'name': 'Minion', 'thMax': 7, 'type': 'Dark Elixir'
            },
            'Hog Rider': {
                'name': 'Hog Rider', 'thMax': 7, 'type': 'Dark Elixir'
            },
            'Valkyrie': {
                'name': 'Valkyrie', 'thMax': 6, 'type': 'Dark Elixir'
            },
            'Golem': {
                'name': 'Golem', 'thMax': 7, 'type': 'Dark Elixir'
            },
            'Witch': {
                'name': 'Witch', 'thMax': 4, 'type': 'Dark Elixir'
            },
            'Lava Hound': {
                'name': 'Lava Hound', 'thMax': 4, 'type': 'Dark Elixir'
            },
            'Bowler': {
                'name': 'Bowler', 'thMax': 3, 'type': 'Dark Elixir'
            },
            'Ice Golem': {
                'name': 'Ice Golem', 'thMax': 3, 'type': 'Dark Elixir'
            },
            'Headhunter': {
                'name': 'Headhunter', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Wall Wrecker': {
                'name': 'Wall Wrecker', 'thMax': 0, 'type': 'Gold'
            },
            'Battle Blimp': {
                'name': 'Battle Blimp', 'thMax': 0, 'type': 'Gold'
            },
            'Stone Slammer': {
                'name': 'Stone Slammer', 'thMax': 0, 'type': 'Gold'
            },
            'Siege Barracks': {
                'name': 'Siege Barracks', 'thMax': 0, 'type': 'Gold'
            },
            'Log Launcher': {
                'name': 'Log Launcher', 'thMax': 0, 'type': 'Gold'
            }
        },
        'spell': {
            'Lightning Spell': {
                'name': 'Lightning Spell', 'thMax': 8, 'type': 'Elixir'
            },
            'Healing Spell': {
                'name': 'Healing Spell', 'thMax': 7, 'type': 'Elixir'
            },
            'Rage Spell': {
                'name': 'Rage Spell', 'thMax': 5, 'type': 'Elixir'
            },
            'Jump Spell': {
                'name': 'Jump Spell', 'thMax': 3, 'type': 'Elixir'
            },
            'Freeze Spell': {
                'name': 'Freeze Spell', 'thMax': 6, 'type': 'Elixir'
            },
            'Clone Spell': {
                'name': 'Clone Spell', 'thMax': 5, 'type': 'Elixir'
            },
            'Invisibility Spell': {
                'name': 'Invisibility Spell', 'thMax': 2, 'type': 'Elixir'
            },
            'Poison Spell': {
                'name': 'Poison Spell', 'thMax': 5, 'type': 'Dark Elixir'
            },
            'Earthquake Spell': {
                'name': 'Earthquake Spell', 'thMax': 5, 'type': 'Dark Elixir'
            },
            'Haste Spell': {
                'name': 'Haste Spell', 'thMax': 5, 'type': 'Dark Elixir'
            },
            'Skeleton Spell': {
                'name': 'Skeleton Spell', 'thMax': 4, 'type': 'Dark Elixir'
            },
            'Bat Spell': {
                'name': 'Bat Spell', 'thMax': 4, 'type': 'Dark Elixir'
            }
        }
    },
    12: {
        'hero': {
            'Barbarian King': {
                'name': 'Barbarian King', 'thMax': 65, 'type': 'Dark Elixir'
            },
            'Archer Queen': {
                'name': 'Archer Queen', 'thMax': 65, 'type': 'Dark Elixir'
            },
            'Grand Warden': {
                'name': 'Grand Warden', 'thMax': 40, 'type': 'Elixir'
            },
            'Royal Champion': {
                'name': 'Royal Champion', 'thMax': 0, 'type': 'Dark Elixir'
            }
        },
        'troop': {
            'Barbarian': {
                'name': 'Barbarian', 'thMax': 8, 'type': 'Elixir'
            },
            'Archer': {
                'name': 'Archer', 'thMax': 9, 'type': 'Elixir'
            },
            'Giant': {
                'name': 'Giant', 'thMax': 9, 'type': 'Elixir'
            },
            'Goblin': {
                'name': 'Goblin', 'thMax': 7, 'type': 'Elixir'
            },
            'Wall Breaker': {
                'name': 'Wall Breaker', 'thMax': 8, 'type': 'Elixir'
            },
            'Balloon': {
                'name': 'Balloon', 'thMax': 8, 'type': 'Elixir'
            },
            'Wizard': {
                'name': 'Wizard', 'thMax': 9, 'type': 'Elixir'
            },
            'Healer': {
                'name': 'Healer', 'thMax': 5, 'type': 'Elixir'
            },
            'Dragon': {
                'name': 'Dragon', 'thMax': 7, 'type': 'Elixir'
            },
            'P.E.K.K.A': {
                'name': 'P.E.K.K.A', 'thMax': 8, 'type': 'Elixir'
            },
            'Baby Dragon': {
                'name': 'Baby Dragon', 'thMax': 6, 'type': 'Elixir'
            },
            'Miner': {
                'name': 'Miner', 'thMax': 6, 'type': 'Elixir'
            },
            'Electro Dragon': {
                'name': 'Electro Dragon', 'thMax': 3, 'type': 'Elixir'
            },
            'Yeti': {
                'name': 'Yeti', 'thMax': 2, 'type': 'Elixir'
            },
            'Super Barbarian': {
                'name': 'Super Barbarian', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Archer': {
                'name': 'Super Archer', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Wall Breaker': {
                'name': 'Super Wall Breaker', 'thMax': 0, 'type': 'Elixir'
            },
            'Sneaky Goblin': {
                'name': 'Sneaky Goblin', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Giant': {
                'name': 'Super Giant', 'thMax': 0, 'type': 'Elixir'
            },
            'Inferno Dragon': {
                'name': 'Inferno Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Valkyrie': {
                'name': 'Super Valkyrie', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Super Witch': {
                'name': 'Super Witch', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Minion': {
                'name': 'Minion', 'thMax': 8, 'type': 'Dark Elixir'
            },
            'Hog Rider': {
                'name': 'Hog Rider', 'thMax': 9, 'type': 'Dark Elixir'
            },
            'Valkyrie': {
                'name': 'Valkyrie', 'thMax': 7, 'type': 'Dark Elixir'
            },
            'Golem': {
                'name': 'Golem', 'thMax': 9, 'type': 'Dark Elixir'
            },
            'Witch': {
                'name': 'Witch', 'thMax': 5, 'type': 'Dark Elixir'
            },
            'Lava Hound': {
                'name': 'Lava Hound', 'thMax': 5, 'type': 'Dark Elixir'
            },
            'Bowler': {
                'name': 'Bowler', 'thMax': 4, 'type': 'Dark Elixir'
            },
            'Ice Golem': {
                'name': 'Ice Golem', 'thMax': 5, 'type': 'Dark Elixir'
            },
            'Headhunter': {
                'name': 'Headhunter', 'thMax': 2, 'type': 'Dark Elixir'
            },
            'Wall Wrecker': {
                'name': 'Wall Wrecker', 'thMax': 3, 'type': 'Gold'
            },
            'Battle Blimp': {
                'name': 'Battle Blimp', 'thMax': 3, 'type': 'Gold'
            },
            'Stone Slammer': {
                'name': 'Stone Slammer', 'thMax': 3, 'type': 'Gold'
            },
            'Siege Barracks': {
                'name': 'Siege Barracks', 'thMax': 0, 'type': 'Gold'
            },
            'Log Launcher': {
                'name': 'Log Launcher', 'thMax': 0, 'type': 'Gold'
            }
        },
        'spell': {
            'Lightning Spell': {
                'name': 'Lightning Spell', 'thMax': 9, 'type': 'Elixir'
            },
            'Healing Spell': {
                'name': 'Healing Spell', 'thMax': 7, 'type': 'Elixir'
            },
            'Rage Spell': {
                'name': 'Rage Spell', 'thMax': 6, 'type': 'Elixir'
            },
            'Jump Spell': {
                'name': 'Jump Spell', 'thMax': 3, 'type': 'Elixir'
            },
            'Freeze Spell': {
                'name': 'Freeze Spell', 'thMax': 7, 'type': 'Elixir'
            },
            'Clone Spell': {
                'name': 'Clone Spell', 'thMax': 5, 'type': 'Elixir'
            },
            'Invisibility Spell': {
                'name': 'Invisibility Spell', 'thMax': 3, 'type': 'Elixir'
            },
            'Poison Spell': {
                'name': 'Poison Spell', 'thMax': 6, 'type': 'Dark Elixir'
            },
            'Earthquake Spell': {
                'name': 'Earthquake Spell', 'thMax': 5, 'type': 'Dark Elixir'
            },
            'Haste Spell': {
                'name': 'Haste Spell', 'thMax': 5, 'type': 'Dark Elixir'
            },
            'Skeleton Spell': {
                'name': 'Skeleton Spell', 'thMax': 6, 'type': 'Dark Elixir'
            },
            'Bat Spell': {
                'name': 'Bat Spell', 'thMax': 5, 'type': 'Dark Elixir'
            }
        }
    },
    13: {
        'hero': {
            'Barbarian King': {
                'name': 'Barbarian King', 'thMax': 75, 'type': 'Dark Elixir'
            },
            'Archer Queen': {
                'name': 'Archer Queen', 'thMax': 75, 'type': 'Dark Elixir'
            },
            'Grand Warden': {
                'name': 'Grand Warden', 'thMax': 50, 'type': 'Elixir'
            },
            'Royal Champion': {
                'name': 'Royal Champion', 'thMax': 25, 'type': 'Dark Elixir'
            }
        },
        'troop': {
            'Barbarian': {
                'name': 'Barbarian', 'thMax': 9, 'type': 'Elixir'
            },
            'Archer': {
                'name': 'Archer', 'thMax': 9, 'type': 'Elixir'
            },
            'Giant': {
                'name': 'Giant', 'thMax': 10, 'type': 'Elixir'
            },
            'Goblin': {
                'name': 'Goblin', 'thMax': 8, 'type': 'Elixir'
            },
            'Wall Breaker': {
                'name': 'Wall Breaker', 'thMax': 9, 'type': 'Elixir'
            },
            'Balloon': {
                'name': 'Balloon', 'thMax': 9, 'type': 'Elixir'
            },
            'Wizard': {
                'name': 'Wizard', 'thMax': 10, 'type': 'Elixir'
            },
            'Healer': {
                'name': 'Healer', 'thMax': 6, 'type': 'Elixir'
            },
            'Dragon': {
                'name': 'Dragon', 'thMax': 8, 'type': 'Elixir'
            },
            'P.E.K.K.A': {
                'name': 'P.E.K.K.A', 'thMax': 9, 'type': 'Elixir'
            },
            'Baby Dragon': {
                'name': 'Baby Dragon', 'thMax': 7, 'type': 'Elixir'
            },
            'Miner': {
                'name': 'Miner', 'thMax': 7, 'type': 'Elixir'
            },
            'Electro Dragon': {
                'name': 'Electro Dragon', 'thMax': 4, 'type': 'Elixir'
            },
            'Yeti': {
                'name': 'Yeti', 'thMax': 3, 'type': 'Elixir'
            },
            'Super Barbarian': {
                'name': 'Super Barbarian', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Archer': {
                'name': 'Super Archer', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Wall Breaker': {
                'name': 'Super Wall Breaker', 'thMax': 0, 'type': 'Elixir'
            },
            'Sneaky Goblin': {
                'name': 'Sneaky Goblin', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Giant': {
                'name': 'Super Giant', 'thMax': 0, 'type': 'Elixir'
            },
            'Inferno Dragon': {
                'name': 'Inferno Dragon', 'thMax': 0, 'type': 'Elixir'
            },
            'Super Valkyrie': {
                'name': 'Super Valkyrie', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Super Witch': {
                'name': 'Super Witch', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Minion': {
                'name': 'Minion', 'thMax': 9, 'type': 'Dark Elixir'
            },
            'Hog Rider': {
                'name': 'Hog Rider', 'thMax': 10, 'type': 'Dark Elixir'
            },
            'Valkyrie': {
                'name': 'Valkyrie', 'thMax': 8, 'type': 'Dark Elixir'
            },
            'Golem': {
                'name': 'Golem', 'thMax': 10, 'type': 'Dark Elixir'
            },
            'Witch': {
                'name': 'Witch', 'thMax': 5, 'type': 'Dark Elixir'
            },
            'Lava Hound': {
                'name': 'Lava Hound', 'thMax': 6, 'type': 'Dark Elixir'
            },
            'Bowler': {
                'name': 'Bowler', 'thMax': 5, 'type': 'Dark Elixir'
            },
            'Ice Golem': {
                'name': 'Ice Golem', 'thMax': 5, 'type': 'Dark Elixir'
            },
            'Headhunter': {
                'name': 'Headhunter', 'thMax': 3, 'type': 'Dark Elixir'
            },
            'Wall Wrecker': {
                'name': 'Wall Wrecker', 'thMax': 4, 'type': 'Gold'
            },
            'Battle Blimp': {
                'name': 'Battle Blimp', 'thMax': 4, 'type': 'Gold'
            },
            'Stone Slammer': {
                'name': 'Stone Slammer', 'thMax': 4, 'type': 'Gold'
            },
            'Siege Barracks': {
                'name': 'Siege Barracks', 'thMax': 4, 'type': 'Gold'
            },
            'Log Launcher': {
                'name': 'Log Launcher', 'thMax': 4, 'type': 'Gold'
            }

        },
        'spell': {
            'Lightning Spell': {
                'name': 'Lightning Spell', 'thMax': 9, 'type': 'Elixir'
            },
            'Healing Spell': {
                'name': 'Healing Spell', 'thMax': 8, 'type': 'Elixir'
            },
            'Rage Spell': {
                'name': 'Rage Spell', 'thMax': 6, 'type': 'Elixir'
            },
            'Jump Spell': {
                'name': 'Jump Spell', 'thMax': 4, 'type': 'Elixir'
            },
            'Freeze Spell': {
                'name': 'Freeze Spell', 'thMax': 7, 'type': 'Elixir'
            },
            'Clone Spell': {
                'name': 'Clone Spell', 'thMax': 6, 'type': 'Elixir'
            },
            'Invisibility Spell': {
                'name': 'Invisibility Spell', 'thMax': 4, 'type': 'Elixir'
            },
            'Poison Spell': {
                'name': 'Poison Spell', 'thMax': 7, 'type': 'Dark Elixir'
            },
            'Earthquake Spell': {
                'name': 'Earthquake Spell', 'thMax': 5, 'type': 'Dark Elixir'
            },
            'Haste Spell': {
                'name': 'Haste Spell', 'thMax': 5, 'type': 'Dark Elixir'
            },
            'Skeleton Spell': {
                'name': 'Skeleton Spell', 'thMax': 7, 'type': 'Dark Elixir'
            },
            'Bat Spell': {
                'name': 'Bat Spell', 'thMax': 5, 'type': 'Dark Elixir'
            }
        }
    }
}
