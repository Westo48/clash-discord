import re
import datetime
from coc.errors import Maintenance, NotFound, PrivateWarLog, GatewayError
import Player
import Clan
import War
import CWLGroup
import CWLWar


th_lineup_dict = {
    14: 0,
    13: 0,
    12: 0,
    11: 0,
    10: 0,
    9: 0,
    8: 0,
    7: 0,
    6: 0,
    5: 0,
    4: 0,
    3: 0,
    2: 0,
    1: 0
}


# Player

async def get_player(player_tag, coc_client):
    try:
        player_obj = await coc_client.get_player(player_tag)

    except Maintenance:
        return None

    except NotFound:
        return None

    except GatewayError:
        return None

    return player_obj


def verify_token(api_key, player_tag, header):
    return Player.verify_token(api_key, player_tag, header)


def find_unit_name(unit_name, unit_list):
    """
        take in unit name and list of units
        odered list of unit objects from coc.py
        then returns the unit object provided by coc.py,
        returns None if not found
    """

    # formatting the name for P.E.K.K.A
    unit_name = re.sub('[.]', '', unit_name)
    for unit_obj in unit_list:
        # formatting the name for P.E.K.K.A
        formatted_unit_name = re.sub('[.]', '', unit_obj.name)
        if formatted_unit_name.lower() == unit_name.lower():
            return unit_obj
    return None


def find_hero(player_obj, hero_name):
    """
        finds a hero based on unformatted name given

        Args:
            player_obj (obj): coc.py player object
            hero_name (str): requested hero name

        Returns:
            hero: object of coc.py hero
            None: if hero is not found returns none
    """
    # search in heroes
    coc_hero_obj = find_unit_name(hero_name, player_obj.heroes)

    # hero is found based on name retun hero object
    if coc_hero_obj:
        return coc_hero_obj

    # hero was not found based on name
    return None


def find_pet(player_obj, pet_name):
    """
        finds a pet based on unformatted name given

        Args:
            player_obj (obj): coc.py player object
            pet_name (str): requested pet name

        Returns:
            pet: object of coc.py pet
            None: if pet is not found returns none
    """
    # search in pets
    coc_pet_obj = find_unit_name(pet_name, player_obj.hero_pets)

    # pet is found based on name retun pet object
    if coc_pet_obj:
        return coc_pet_obj

    # pet was not found based on name
    return None


def find_home_troop(player_obj, troop_name):
    """
        finds a home troop based on unformatted name given

        Args:
            player_obj (obj): coc.py player object
            troop_name (str): requested home troop name

        Returns:
            troop: object of coc.py troop
            None: if troop is not found returns none
    """
    # search in home troops
    coc_troop_obj = find_unit_name(troop_name, player_obj.home_troops)

    # troop is found based on name retun troop object
    if coc_troop_obj:
        return coc_troop_obj

    # troop was not found based on name
    return None


def find_siege(player_obj, siege_name):
    """
        finds a siege based on unformatted name given

        Args:
            player_obj (obj): coc.py player object
            siege_name (str): requested siege name

        Returns:
            siege: object of coc.py siege
            None: if siege is not found returns none
    """
    # search in sieges
    coc_siege_obj = find_unit_name(siege_name, player_obj.siege_machines)

    # siege is found based on name retun siege object
    if coc_siege_obj:
        return coc_siege_obj

    # siege was not found based on name
    return None


def find_super_troop(player_obj, troop_name):
    """
        finds a super troop based on unformatted name given

        Args:
            player_obj (obj): coc.py player object
            troop_name (str): requested super troop name

        Returns:
            super_troop: object of coc.py super troop
            None: if super troop is not found returns none
    """
    # search in super troops
    coc_troop_obj = find_unit_name(troop_name, player_obj.super_troops)

    # super troop is found based on name retun super troop object
    if coc_troop_obj:
        return coc_troop_obj

    # super troop was not found based on name
    return None


def find_spell(player_obj, spell_name):
    """
        finds a spell based on unformatted name given

        Args:
            player_obj (obj): coc.py player object
            spell_name (str): requested spell name

        Returns:
            spell: object of coc.py spell
            None: if spell is not found returns none
    """
    # search in spells
    coc_spell_obj = find_unit_name(spell_name, player_obj.spells)

    # spell is found based on name retun spell object
    if coc_spell_obj:
        return coc_spell_obj

    # spell was not found based on name
    return None


def find_builder_troop(player_obj, troop_name):
    """
        finds a builder troop based on unformatted name given

        Args:
            player_obj (obj): coc.py player object
            troop_name (str): requested builder troop name

        Returns:
            troop: object of coc.py troop
            None: if troop is not found returns none
    """
    # search in builder troops
    coc_troop_obj = find_unit_name(troop_name, player_obj.builder_troops)

    # troop is found based on name retun troop object
    if coc_troop_obj:
        return coc_troop_obj

    # troop was not found based on name
    return None


def find_unit(player_obj, unit_name):
    """
        finds a unit based on unformatted name given

        Args:
            player_obj (obj): coc.py player object
            unit_name (str): requested unit name

        Returns:
            coc_unit_obj: object of coc.py unit
            None: if unit is not found returns none
    """
    # search in heroes
    coc_unit_obj = find_hero(player_obj, unit_name)
    if coc_unit_obj:
        return coc_unit_obj

    # search in hero pets
    coc_unit_obj = find_pet(player_obj, unit_name)
    if coc_unit_obj:
        return coc_unit_obj

    # search in home troops
    coc_unit_obj = find_home_troop(player_obj, unit_name)
    if coc_unit_obj:
        return coc_unit_obj

    # search in sieges
    coc_unit_obj = find_siege(player_obj, unit_name)
    if coc_unit_obj:
        return coc_unit_obj

    # search in super troops
    coc_unit_obj = find_super_troop(player_obj, unit_name)
    if coc_unit_obj:
        return coc_unit_obj

    # search in spells
    coc_unit_obj = find_spell(player_obj, unit_name)
    if coc_unit_obj:
        return coc_unit_obj

    # search in builder troops
    coc_unit_obj = find_builder_troop(player_obj, unit_name)
    if coc_unit_obj:
        return coc_unit_obj

    # unit was not found
    return None


def player_active_super_troops(player_obj):
    """
        Returns a list of active super troops,
        if no active super troops are found it will return an empty list
    """
    active_super_troops = []
    for troop_obj in player_obj.troops:
        if troop_obj.is_active:
            active_super_troops.append(troop_obj)
    return active_super_troops


# Clan
# todo DOCSTRING
async def get_clan(clan_tag, coc_client):
    try:
        clan_obj = await coc_client.get_clan(clan_tag)

    except Maintenance:
        return None

    except NotFound:
        return None

    except GatewayError:
        return None

    return clan_obj


async def clan_lineup(clan_obj, coc_client):
    clan_lineup_dict = th_lineup_dict.copy()

    for member in clan_obj.members:
        player_obj = await coc_client.get_player(member.tag)
        clan_lineup_dict[player_obj.town_hall] += 1

    return clan_lineup_dict


# returns a string response of members that can donate the best of that unit
# todo put this into the clan framework
async def donation(clan_obj, unit_name, coc_client):
    """
        Takes in the unit name and clan tag, returns a list of players
        who can donate.

        Returns an empty list if nobody can donate requested unit.
        Returns None if hero has been requested.

        Args:
            unit_name (str): Name of requested unit.
            clan_obj (obj): Clan object.
            coc_client (obj): coc.py client

        Returns:
            list: List of players who can donate.
    """

    class Donor(object):
        def __init__(self, player_obj, unit_obj):
            self.player_obj = player_obj
            self.unit_obj = unit_obj

    # get a member list to make less overall responses
    member_list = []
    for member in clan_obj.members:
        player_obj = await coc_client.get_player(member.tag)

        # checking if they have the specified unit
        unit_obj = find_unit(player_obj, unit_name)
        if unit_obj:
            member_list.append(Donor(player_obj, unit_obj))

    # if nobody has the requested unit
    if len(member_list) == 0:
        return member_list

    # if hero has been requested return None
    if find_hero(member_list[0].player_obj, member_list[0].unit_obj.name):
        return None

    # if pet has been requested return None
    if find_pet(member_list[0].player_obj, member_list[0].unit_obj.name):
        return None

    # if super troop has been requested return None
    if member_list[0].unit_obj.is_super_troop:
        return None

    # if builder has been requested return None
    if member_list[0].unit_obj.is_builder_base:
        return None

    donor_max = max(member.unit_obj.level for member in member_list)

    # list of those that can donate
    donor_list = []

    # setting donation_upgrade
    donation_upgrade = clan_donation_upgrade(clan_obj)

    # checking to see if anyone can donate max
    if (donor_max + donation_upgrade) >= member_list[0].unit_obj.max_level:
        # go thru each member and return the donors that can donate max
        for member in member_list:
            # if the member can donate max unit
            if ((member.unit_obj.level+donation_upgrade) >=
                    member.unit_obj.max_level):
                # adding the donor's name to the donator list
                donor_list.append(member)
        return donor_list

    # since nobody can donate max
    else:
        for member_obj in member_list:
            if member_obj.unit_obj.level >= donor_max:
                donor_list.append(member_obj)
        return donor_list


def clan_donation_upgrade(clan_obj):
    if clan_obj.level < 5:
        return 0
    elif clan_obj.level < 10:
        return 1
    else:
        return 2


async def active_super_troop_search(super_troop_obj, clan_obj, coc_client):
    """
        Takes in the unit name and clan object, returns a list of players
        who have super troop active.

        Returns an empty list if nobody has the super troop active.

        Args:
            super_troop_obj (obj): coc.py super troop object
            clan_obj (obj): coc.py clan object
            coc_client (obj): coc.py client

        Returns:
            list: list of players who can donate
    """

    donor_list = []
    # getting a list of members with the given super_troop activated
    for clan_member_obj in clan_obj.members:
        member_obj = await get_player(clan_member_obj.tag, coc_client)
        active_super_troop = member_obj.get_troop(super_troop_obj.name)
        if not active_super_troop:
            continue
        if active_super_troop.is_active:
            donor_list.append(member_obj)
    return donor_list


# returns a string of the member's role
def response_member_role(player_name, clan_tag, header):
    clan = Clan.get(clan_tag, header)
    player_tag = clan.find_member(player_name)
    player = Player.get(player_tag, header)
    return player.role


# War
# todo DOCSTRING
async def get_war(clan_tag, coc_client):
    try:
        war_obj = await coc_client.get_clan(clan_tag)

    except Maintenance:
        return None

    except NotFound:
        return None

    except PrivateWarLog:
        return None

    except GatewayError:
        return None

    return war_obj


def war_clan_lineup(war_clan_obj):
    clan_lineup_dict = th_lineup_dict.copy()

    for member in war_clan_obj.members:
        clan_lineup_dict[member.th_lvl] += 1

    return clan_lineup_dict


def war_no_attack(war_obj):
    """
        Returns a list of members that have missed an attack.
    """
    no_attack_members = []
    for member_obj in war_obj.clan.members:
        if len(member_obj.attacks) != war_obj.attacks_per_member:
            no_attack_members.append(member_obj)
    return no_attack_members


def war_no_attack_members(clan_tag, header):
    "returns a list of players that haven't attacked"
    war = War.get(clan_tag, header)

    if war.state == 'preparation':
        return []

    elif war.state == 'inWar':
        return war.no_attack()

    elif war.state == 'warEnded':
        return []

    else:
        return []


# todo update all for if not in CWL logic
# CWL Group

def get_cwl_group(clan_tag, header):
    return CWLGroup.get(clan_tag, header)


def cwl_clan_lineup(cwl_group_clan):
    clan_lineup_dict = th_lineup_dict.copy()
    for member in cwl_group_clan.members:
        clan_lineup_dict[member.th_lvl] += 1
    return clan_lineup_dict


# CWL War


# UTILS

def string_date_time(war_obj):
    """
        returns a string of the remaining time,
        if warEnded or notInWar, then variables will be None
    """
    if (war_obj.state == 'warEnded'
            or war_obj.state == 'notInWar'):
        return None

    if war_obj.state == "preparation":
        time_final = war_obj.start_time
    else:
        time_final = war_obj.end_time
    days, hours, minutes, seconds = date_time_calculator(
        time_final)
    return_string = ''
    if days > 0:
        if days == 1:
            days_text = 'day'
        else:
            days_text = 'days'
        return_string += f'{days} {days_text}, '

    if hours > 0:
        if hours == 1:
            hour_text = 'hour'
        else:
            hour_text = 'hours'
        return_string += f'{hours} {hour_text}, '

    if minutes > 0:
        if minutes == 1:
            minute_text = 'minute'
        else:
            minute_text = 'minutes'
        return_string += f'{minutes} {minute_text}, '

    if seconds > 0:
        if seconds == 1:
            second_text = 'second'
        else:
            second_text = 'seconds'
        return_string += f'{seconds} {second_text}, '

    # removing the ', ' from the end of the string
    return_string = return_string[:-2]

    return return_string


def date_time_calculator(time_final):
    """
        calculates the difference between now and final time
    """
    difference = time_final.time-time_final.now

    days = difference.days
    seconds = difference.seconds
    minutes = int(seconds % 3600 / 60)
    hours = int(seconds / 3600)
    remaining_seconds = (seconds - hours * 3600 - minutes * 60)

    return days, hours, minutes, remaining_seconds


def string_scoreboard(war_obj):
    """
        Returns a string of the war score.
    """
    if (war_obj.state == 'preparation'
            or war_obj.state == 'notInWar'):
        return None

    star_difference = (war_obj.clan.stars - war_obj.opponent.stars)
    destruction_difference = (war_obj.clan.destruction
                              - war_obj.opponent.destruction)
    # singular or plural
    if abs(star_difference) == 1:
        star_string = "star"
    else:
        star_string = "stars"

    # there is a star difference
    if star_difference != 0:
        return f"{war_obj.status} by {abs(star_difference)} {star_string}"
    # there is a destruction difference
    elif destruction_difference != 0:
        return (
            f"{war_obj.status} by "
            f"{round(abs(destruction_difference), 2)} "
            f"destruction percentage."
        )
    # tied score
    else:
        return "tied"


def find_defender(war_clan_obj, defender_tag):
    """
        Takes in a defender tag and returns 
        a WarMember object. 
        If it is not found then it will return None.
    """
    for defender_member_obj in war_clan_obj.members:
        if defender_tag == defender_member_obj.tag:
            return defender_member_obj
    return None


def string_attack_times(member_attack_list):
    """
        Returns 'time' or 'times' based on the number of attacks.
    """
    if len(member_attack_list) == 1:
        return 'time'
    else:
        return 'times'


def string_member_stars(war_star_count):
    """
        returns 'star' or 'stars' based on the number of stars
    """
    if war_star_count == 1:
        return 'star'
    else:
        return 'stars'


def th_multiplier(th_difference):
    """
        TH multiplier matrix.
    """
    if th_difference < -2:
        th_mult = 35
    elif th_difference == -2:
        th_mult = 50
    elif th_difference == -1:
        th_mult = 80
    elif th_difference == 0:
        th_mult = 100
    elif th_difference == 1:
        th_mult = 140
    elif th_difference == 2:
        th_mult = 155
    elif th_difference > 2:
        th_mult = 200
    else:
        th_mult = 100
    return th_mult
