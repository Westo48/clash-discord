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

def get_player(player_tag, header):
    return Player.get(player_tag, header)


def verify_token(api_key, player_tag, header):
    return Player.verify_token(api_key, player_tag, header)

# returns player.name and troop.lvl


def find_unit(player_obj, unit_name):
    unit_obj = player_obj.find_unit(unit_name)
    if unit_obj:
        # unit was found
        return unit_obj
    if not unit_obj:
        # unit was not found
        return None


def super_troop_unit_name(unit_name):
    for super_troop in Player.super_troop_list:
        if unit_name.lower() == super_troop.lower():
            return super_troop
    return None


# Clan
# todo DOCSTRING
def get_clan(clan_tag, header):
    return Clan.get(clan_tag, header)


def clan_lineup(clan_obj, header):
    clan_lineup_dict = th_lineup_dict

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


def war_clan_lineup(war_clan_obj, header):
    clan_lineup_dict = th_lineup_dict

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
    clan_lineup_dict = th_lineup_dict
    for member in cwl_group_clan.members:
        clan_lineup_dict[member.th_lvl] += 1
    return clan_lineup


# CWL War
