import re

from coc.errors import Maintenance, NotFound, PrivateWarLog
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


def super_troop_unit_name(unit_name):
    for super_troop in Player.super_troop_list:
        if unit_name.lower() == super_troop.lower():
            return super_troop
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
def get_clan(clan_tag, header):
    return Clan.get(clan_tag, header)


def clan_lineup(clan_obj, header):
    clan_lineup_dict = th_lineup_dict.copy()

    for member in clan_obj.members:
        player_obj = get_player(member.tag, header)
        clan_lineup_dict[player_obj.th_lvl] += 1

    return clan_lineup_dict


# returns a string response of members that can donate the best of that unit
# todo put this into the clan framework
def donation(unit_name, clan, header):
    """
        Takes in the unit name and clan tag, returns a list of players
        who can donate.

        Returns an empty list if nobody can donate requested unit.
        Returns None if hero has been requested.

        Args:
            unit_name (str): Name of requested unit.
            clan (obj): Clan object.
            header (dict): Json header

        Returns:
            list: List of players who can donate.
    """

    class Donor(object):
        def __init__(self, player, unit):
            self.player = player
            self.unit = unit

    # get a member list to make less overall responses
    member_list = []
    for member in clan.members:
        player = Player.get(member.tag, header)

        # checking if they have the specified unit
        unit = player.find_unit(unit_name)
        if unit:
            member_list.append(Donor(player, unit))

    # if nobody has the requested unit
    if len(member_list) == 0:
        return member_list

    # if hero has been requested return None
    if member_list[0].player.find_hero(unit_name):
        return None

    donor_max = max(member.unit.lvl for member in member_list)

    # list of those that can donate
    donators = []

    # checking to see if anyone can donate max
    if (donor_max + clan.donation_upgrade) >= member_list[0].unit.max_lvl:
        # go thru each member and return the donors that can donate max
        for member in member_list:
            # if the member can donate max unit
            if (member.unit.lvl+clan.donation_upgrade) >= member.unit.max_lvl:
                # adding the donor's name to the donator list
                donators.append(member)
        return donators

    # since nobody can donate max
    # ! this still needs to be tested
    else:
        for member in member_list:
            troop = member.find_troop(unit_name)
            if troop.lvl >= donor_max:
                donators.append(member)
        return donators


def active_super_troop_search(unit_name, clan, header):
    """
        Takes in the unit name and clan object, returns a list of players
        who have super troop active.

        Returns an empty list if nobody has the super troop active.

        Args:
            unit_name (str): Name of requested unit.
            clan (obj): Clan object.
            header (dict): Json header

        Returns:
            list: List of players who can donate.
    """

    donor_list = []
    # getting a list of members with the given super_troop activated
    for member in clan.members:
        player = Player.get(member.tag, header)
        active_super_troops = player.find_active_super_troops()
        for super_troop in active_super_troops:
            # if the member has the requested active super troop add to list
            if super_troop.name == unit_name:
                donor_list.append(member)
                break
    return donor_list


# returns a string of the member's role
def response_member_role(player_name, clan_tag, header):
    clan = Clan.get(clan_tag, header)
    player_tag = clan.find_member(player_name)
    player = Player.get(player_tag, header)
    return player.role


# War
# todo DOCSTRING
def get_war(clan_tag, header):
    return War.get(clan_tag, header)


def war_clan_lineup(war_clan_obj):
    clan_lineup_dict = th_lineup_dict.copy()

    for member in war_clan_obj.members:
        clan_lineup_dict[member.th_lvl] += 1

    return clan_lineup_dict


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
