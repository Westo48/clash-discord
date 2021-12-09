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
            war_preference (bool): in (true) or out (false) for war
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
            super_troops (list): list of SuperTroop objects
    """

    def __init__(
        self, tag, name, th_lvl, th_weapon_lvl, xp_lvl,
        trophies, best_trophies, war_stars, attack_wins, defense_wins,
        builder_hall_lvl, vs_trophies, best_vs_trophies, vs_battle_wins,
        role, war_preference, donations, donations_received,
        clan_tag, clan_name, clan_lvl,
        clan_icons, league_id, league_name, league_icons,
        legend_trophies, previous_legend_rank, previous_legend_trophies,
        best_legend_rank, best_legend_trophies,
        current_legend_rank, current_legend_trophies,
        heroes, troops, spells, super_troops
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
        self.war_preference = war_preference
        self.donations = donations
        self.donations_received = donations_received
        self.clan_tag = clan_tag
        self.clan_name = clan_name
        self.clan_lvl = clan_lvl
        self.clan_icons = clan_icons
        self.league_id = league_id
        self.league_name = league_name
        self.league_icons = league_icons
        self.legend_trophies = legend_trophies
        self.previous_legend_rank = previous_legend_rank
        self.previous_legend_trophies = previous_legend_trophies
        self.best_legend_rank = best_legend_rank
        self.best_legend_trophies = best_legend_trophies
        self.current_legend_rank = current_legend_rank
        self.current_legend_trophies = current_legend_trophies
        self.heroes = heroes
        self.troops = troops
        self.spells = spells
        self.super_troops = super_troops

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

    def find_super_troop(self, super_troop_name):
        """
            Take in a super troop name and return
                the corresponding super troop object.
            If no super troop is found returns None.
        """

        # formatting the name from '-' to ' '
        super_troop_name = re.sub('[-]', ' ', super_troop_name)
        super_troop_name = re.sub('[.]', '', super_troop_name)
        for super_troop in self.super_troops:
            if super_troop.name.lower() == super_troop_name.lower():
                return super_troop
        return None

    def find_active_super_troops(self):
        """
            Returns a list of active super troops,
            if no active super troops are found it will return an empty list
        """
        active_super_troops = []
        for super_troop in self.super_troops:
            if super_troop.is_active:
                active_super_troops.append(super_troop)
        return active_super_troops


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


class SuperTroop(object):
    """
    SuperTroop
        Instance Attributes
            name (str): The name of the troop
            lvl (int): The level of the Player's troop
            max_lvl (int): The max level of the troop
            village (str): Base the troop comes from
                'home' or 'builderBase'
            is_active (bool): Whether the super troop is currently active

    """

    def __init__(self, name, lvl, max_lvl, village, is_active):
        self.name = name
        self.lvl = lvl
        self.max_lvl = max_lvl
        self.village = village
        self.is_active = is_active


# todo make comments for inner workings of get method
# todo legends league stats
# ? include all troops whether they are unlocked or not
def get(tag, header):
    """
        Takes in a player's tag and returns a Player object
        Returns None if player is not found
    """

    player_json = json_response(tag, header)

    if 'reason' in player_json:
        return None

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
        if player_json['warPreference'] == 'in':
            war_preference = True
        else:
            war_preference = False
    else:
        role = None
        clan_tag = None
        clan_name = None
        clan_lvl = None
        clan_icons = None
        war_preference = False

    if 'league' in player_json:
        league_id = player_json['league']['id']
        league_name = player_json['league']['name']
        league_icons = {
            'tiny': player_json['league']['iconUrls']['tiny'],
            'small': player_json['league']['iconUrls']['small'],
            'medium': player_json['league']['iconUrls']['medium']
        }
    else:
        league_id = 29000000
        league_name = "Unranked"
        league_icons = {
            "tiny": (
                "https://api-assets.clashofclans.com/leagues/"
                "36/e--YMyIexEQQhE4imLoJcwhYn6Uy8KqlgyY3_kFV6t4.png"
            ),
            'small': (
                "https://api-assets.clashofclans.com/leagues/"
                "72/e--YMyIexEQQhE4imLoJcwhYn6Uy8KqlgyY3_kFV6t4.png"
            )
        }

    if 'legendStatistics' in player_json:
        legend_trophies = player_json['legendStatistics']['legendTrophies']

        if 'previousSeason' in player_json['legendStatistics']:
            previous_legend_rank = player_json['legendStatistics']['previousSeason']['rank']
            previous_legend_trophies = player_json['legendStatistics']['previousSeason']['trophies']
        else:
            previous_legend_rank = None
            previous_legend_trophies = None

        best_legend_rank = player_json['legendStatistics']['bestSeason']['rank']
        best_legend_trophies = player_json['legendStatistics']['bestSeason']['trophies']

        if 'rank' in player_json['legendStatistics']['currentSeason']:
            current_legend_rank = player_json['legendStatistics']['currentSeason']['rank']
            current_legend_trophies = player_json['legendStatistics']['currentSeason']['trophies']
        else:
            current_legend_rank = None
            current_legend_trophies = None

    else:
        legend_trophies = None
        previous_legend_rank = None
        previous_legend_trophies = None
        best_legend_rank = None
        best_legend_trophies = None
        current_legend_rank = None
        current_legend_trophies = None

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
    super_troops = []
    # siege machines are part of 'troops' in the player_json
    # pets are part of 'troops' in the player_json
    for troop in player_json['troops']:
        if troop['village'] == 'home':
            if troop['name'] not in super_troop_list:
                troops.append(Troop(
                    troop['name'], troop['level'], troop['maxLevel'],
                    troop_dict[player_json['townHallLevel']
                               ]['troop'][troop['name']]['thMax'],
                    troop['village'])
                )
            else:
                is_active = False
                if 'superTroopIsActive' in troop:
                    is_active = True
                super_troops.append(SuperTroop(
                    troop['name'], troop['level'], troop['maxLevel'],
                    troop['village'], is_active)
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
        player_json['tag'], player_json['name'], player_json['townHallLevel'],
        th_weap_lvl, player_json['expLevel'], player_json['trophies'],
        player_json['bestTrophies'], player_json['warStars'],
        player_json['attackWins'], player_json['defenseWins'],
        bh_lvl, vs_trophies, best_vs_trophies, vs_battle_wins,
        role, war_preference,
        player_json['donations'], player_json['donationsReceived'],
        clan_tag, clan_name, clan_lvl, clan_icons,
        league_id, league_name, league_icons,
        legend_trophies, previous_legend_rank, previous_legend_trophies,
        best_legend_rank, best_legend_trophies,
        current_legend_rank, current_legend_trophies,
        heroes, troops, spells, super_troops
    )


def json_response(tag, header):
    # format the tag for http use
    tag = tag.replace("#", "")

    url = f'https://api.clashofclans.com/v1/players/%23{tag}'
    return requests.get(url, headers=header).json()


def verify_token(api_key, tag, header):
    """
        verifies player api key with coc server

        Returns True if correctly verified and False if not verified
    """
    # format the tag for http use
    tag = tag.replace("#", "")

    body = {'token': api_key}
    url = f'https://api.clashofclans.com/v1/players/%23{tag}/verifytoken'
    payload = requests.post(url, headers=header, json=body).json()
    # if verified by coc
    if payload['status'] == 'ok':
        return True
    # if not verified by coc
    else:
        return False


super_troop_list = [
    'Super Barbarian', 'Super Archer', 'Super Giant', 'Sneaky Goblin',
    'Super Wall Breaker', 'Super Wizard', 'Inferno Dragon', 'Super Minion',
    'Super Valkyrie', 'Super Witch', 'Ice Hound', 'Rocket Balloon',
    'Super Bowler', 'Super Dragon'
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
            'Dragon Rider': {
                'name': 'Dragon Rider', 'thMax': 0, 'type': 'Elixir'
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
            },
            'Flame Flinger': {
                'name': 'Flame Flinger', 'thMax': 0, 'type': 'Gold'
            },
            'L.A.S.S.I': {
                'name': 'L.A.S.S.I', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Mighty Yak': {
                'name': 'Mighty Yak', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Electro Owl': {
                'name': 'Electro Owl', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Unicorn': {
                'name': 'Unicorn', 'thMax': 0, 'type': 'Dark Elixir'
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
            'Dragon Rider': {
                'name': 'Dragon Rider', 'thMax': 0, 'type': 'Elixir'
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
            },
            'Flame Flinger': {
                'name': 'Flame Flinger', 'thMax': 0, 'type': 'Gold'
            },
            'L.A.S.S.I': {
                'name': 'L.A.S.S.I', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Mighty Yak': {
                'name': 'Mighty Yak', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Electro Owl': {
                'name': 'Electro Owl', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Unicorn': {
                'name': 'Unicorn', 'thMax': 0, 'type': 'Dark Elixir'
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
            'Dragon Rider': {
                'name': 'Dragon Rider', 'thMax': 0, 'type': 'Elixir'
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
            },
            'Flame Flinger': {
                'name': 'Flame Flinger', 'thMax': 0, 'type': 'Gold'
            },
            'L.A.S.S.I': {
                'name': 'L.A.S.S.I', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Mighty Yak': {
                'name': 'Mighty Yak', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Electro Owl': {
                'name': 'Electro Owl', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Unicorn': {
                'name': 'Unicorn', 'thMax': 0, 'type': 'Dark Elixir'
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
            'Dragon Rider': {
                'name': 'Dragon Rider', 'thMax': 0, 'type': 'Elixir'
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
            },
            'Flame Flinger': {
                'name': 'Flame Flinger', 'thMax': 0, 'type': 'Gold'
            },
            'L.A.S.S.I': {
                'name': 'L.A.S.S.I', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Mighty Yak': {
                'name': 'Mighty Yak', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Electro Owl': {
                'name': 'Electro Owl', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Unicorn': {
                'name': 'Unicorn', 'thMax': 0, 'type': 'Dark Elixir'
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
            'Dragon Rider': {
                'name': 'Dragon Rider', 'thMax': 0, 'type': 'Elixir'
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
            },
            'Flame Flinger': {
                'name': 'Flame Flinger', 'thMax': 0, 'type': 'Gold'
            },
            'L.A.S.S.I': {
                'name': 'L.A.S.S.I', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Mighty Yak': {
                'name': 'Mighty Yak', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Electro Owl': {
                'name': 'Electro Owl', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Unicorn': {
                'name': 'Unicorn', 'thMax': 0, 'type': 'Dark Elixir'
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
            'Dragon Rider': {
                'name': 'Dragon Rider', 'thMax': 0, 'type': 'Elixir'
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
            },
            'Flame Flinger': {
                'name': 'Flame Flinger', 'thMax': 0, 'type': 'Gold'
            },
            'L.A.S.S.I': {
                'name': 'L.A.S.S.I', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Mighty Yak': {
                'name': 'Mighty Yak', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Electro Owl': {
                'name': 'Electro Owl', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Unicorn': {
                'name': 'Unicorn', 'thMax': 0, 'type': 'Dark Elixir'
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
            'Dragon Rider': {
                'name': 'Dragon Rider', 'thMax': 0, 'type': 'Elixir'
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
            },
            'Flame Flinger': {
                'name': 'Flame Flinger', 'thMax': 0, 'type': 'Gold'
            },
            'L.A.S.S.I': {
                'name': 'L.A.S.S.I', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Mighty Yak': {
                'name': 'Mighty Yak', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Electro Owl': {
                'name': 'Electro Owl', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Unicorn': {
                'name': 'Unicorn', 'thMax': 0, 'type': 'Dark Elixir'
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
            'Dragon Rider': {
                'name': 'Dragon Rider', 'thMax': 0, 'type': 'Elixir'
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
            },
            'Flame Flinger': {
                'name': 'Flame Flinger', 'thMax': 0, 'type': 'Gold'
            },
            'L.A.S.S.I': {
                'name': 'L.A.S.S.I', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Mighty Yak': {
                'name': 'Mighty Yak', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Electro Owl': {
                'name': 'Electro Owl', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Unicorn': {
                'name': 'Unicorn', 'thMax': 0, 'type': 'Dark Elixir'
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
            'Dragon Rider': {
                'name': 'Dragon Rider', 'thMax': 0, 'type': 'Elixir'
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
            },
            'Flame Flinger': {
                'name': 'Flame Flinger', 'thMax': 0, 'type': 'Gold'
            },
            'L.A.S.S.I': {
                'name': 'L.A.S.S.I', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Mighty Yak': {
                'name': 'Mighty Yak', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Electro Owl': {
                'name': 'Electro Owl', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Unicorn': {
                'name': 'Unicorn', 'thMax': 0, 'type': 'Dark Elixir'
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
            'Dragon Rider': {
                'name': 'Dragon Rider', 'thMax': 0, 'type': 'Elixir'
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
            },
            'Flame Flinger': {
                'name': 'Flame Flinger', 'thMax': 0, 'type': 'Gold'
            },
            'L.A.S.S.I': {
                'name': 'L.A.S.S.I', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Mighty Yak': {
                'name': 'Mighty Yak', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Electro Owl': {
                'name': 'Electro Owl', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Unicorn': {
                'name': 'Unicorn', 'thMax': 0, 'type': 'Dark Elixir'
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
            'Dragon Rider': {
                'name': 'Dragon Rider', 'thMax': 0, 'type': 'Elixir'
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
            },
            'Flame Flinger': {
                'name': 'Flame Flinger', 'thMax': 0, 'type': 'Gold'
            },
            'L.A.S.S.I': {
                'name': 'L.A.S.S.I', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Mighty Yak': {
                'name': 'Mighty Yak', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Electro Owl': {
                'name': 'Electro Owl', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Unicorn': {
                'name': 'Unicorn', 'thMax': 0, 'type': 'Dark Elixir'
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
            'Dragon Rider': {
                'name': 'Dragon Rider', 'thMax': 0, 'type': 'Elixir'
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
            },
            'Flame Flinger': {
                'name': 'Flame Flinger', 'thMax': 0, 'type': 'Gold'
            },
            'L.A.S.S.I': {
                'name': 'L.A.S.S.I', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Mighty Yak': {
                'name': 'Mighty Yak', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Electro Owl': {
                'name': 'Electro Owl', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Unicorn': {
                'name': 'Unicorn', 'thMax': 0, 'type': 'Dark Elixir'
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
            'Dragon Rider': {
                'name': 'Dragon Rider', 'thMax': 0, 'type': 'Elixir'
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
            },
            'Flame Flinger': {
                'name': 'Flame Flinger', 'thMax': 0, 'type': 'Gold'
            },
            'L.A.S.S.I': {
                'name': 'L.A.S.S.I', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Mighty Yak': {
                'name': 'Mighty Yak', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Electro Owl': {
                'name': 'Electro Owl', 'thMax': 0, 'type': 'Dark Elixir'
            },
            'Unicorn': {
                'name': 'Unicorn', 'thMax': 0, 'type': 'Dark Elixir'
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
    },
    14: {
        'hero': {
            'Barbarian King': {
                'name': 'Barbarian King', 'thMax': 80, 'type': 'Dark Elixir'
            },
            'Archer Queen': {
                'name': 'Archer Queen', 'thMax': 80, 'type': 'Dark Elixir'
            },
            'Grand Warden': {
                'name': 'Grand Warden', 'thMax': 55, 'type': 'Elixir'
            },
            'Royal Champion': {
                'name': 'Royal Champion', 'thMax': 30, 'type': 'Dark Elixir'
            }
        },
        'troop': {
            'Barbarian': {
                'name': 'Barbarian', 'thMax': 10, 'type': 'Elixir'
            },
            'Archer': {
                'name': 'Archer', 'thMax': 10, 'type': 'Elixir'
            },
            'Giant': {
                'name': 'Giant', 'thMax': 10, 'type': 'Elixir'
            },
            'Goblin': {
                'name': 'Goblin', 'thMax': 8, 'type': 'Elixir'
            },
            'Wall Breaker': {
                'name': 'Wall Breaker', 'thMax': 10, 'type': 'Elixir'
            },
            'Balloon': {
                'name': 'Balloon', 'thMax': 10, 'type': 'Elixir'
            },
            'Wizard': {
                'name': 'Wizard', 'thMax': 10, 'type': 'Elixir'
            },
            'Healer': {
                'name': 'Healer', 'thMax': 7, 'type': 'Elixir'
            },
            'Dragon': {
                'name': 'Dragon', 'thMax': 9, 'type': 'Elixir'
            },
            'P.E.K.K.A': {
                'name': 'P.E.K.K.A', 'thMax': 9, 'type': 'Elixir'
            },
            'Baby Dragon': {
                'name': 'Baby Dragon', 'thMax': 8, 'type': 'Elixir'
            },
            'Miner': {
                'name': 'Miner', 'thMax': 8, 'type': 'Elixir'
            },
            'Electro Dragon': {
                'name': 'Electro Dragon', 'thMax': 5, 'type': 'Elixir'
            },
            'Yeti': {
                'name': 'Yeti', 'thMax': 4, 'type': 'Elixir'
            },
            'Dragon Rider': {
                'name': 'Dragon Rider', 'thMax': 3, 'type': 'Elixir'
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
                'name': 'Minion', 'thMax': 10, 'type': 'Dark Elixir'
            },
            'Hog Rider': {
                'name': 'Hog Rider', 'thMax': 11, 'type': 'Dark Elixir'
            },
            'Valkyrie': {
                'name': 'Valkyrie', 'thMax': 9, 'type': 'Dark Elixir'
            },
            'Golem': {
                'name': 'Golem', 'thMax': 11, 'type': 'Dark Elixir'
            },
            'Witch': {
                'name': 'Witch', 'thMax': 5, 'type': 'Dark Elixir'
            },
            'Lava Hound': {
                'name': 'Lava Hound', 'thMax': 6, 'type': 'Dark Elixir'
            },
            'Bowler': {
                'name': 'Bowler', 'thMax': 6, 'type': 'Dark Elixir'
            },
            'Ice Golem': {
                'name': 'Ice Golem', 'thMax': 6, 'type': 'Dark Elixir'
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
            },
            'Flame Flinger': {
                'name': 'Flame Flinger', 'thMax': 0, 'type': 'Gold'
            },
            'L.A.S.S.I': {
                'name': 'L.A.S.S.I', 'thMax': 10, 'type': 'Dark Elixir'
            },
            'Mighty Yak': {
                'name': 'Mighty Yak', 'thMax': 10, 'type': 'Dark Elixir'
            },
            'Electro Owl': {
                'name': 'Electro Owl', 'thMax': 10, 'type': 'Dark Elixir'
            },
            'Unicorn': {
                'name': 'Unicorn', 'thMax': 10, 'type': 'Dark Elixir'
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
                'name': 'Clone Spell', 'thMax': 7, 'type': 'Elixir'
            },
            'Invisibility Spell': {
                'name': 'Invisibility Spell', 'thMax': 4, 'type': 'Elixir'
            },
            'Poison Spell': {
                'name': 'Poison Spell', 'thMax': 8, 'type': 'Dark Elixir'
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
