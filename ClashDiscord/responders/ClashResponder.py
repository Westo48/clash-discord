import re
import datetime
import math
from coc.errors import Maintenance, NotFound, PrivateWarLog, GatewayError

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


async def verify_token(api_key, player_tag, coc_client):
    try:
        player_obj = await coc_client.verify_player_token(player_tag, api_key)

    except Maintenance:
        return None

    except NotFound:
        return None

    except GatewayError:
        return None

    return player_obj


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


def home_unit_names(coc):
    """
        returns a list of all home unit names

        Args:
            coc (obj): coc.py object

        Returns:
            home_unit_names: list of all unit names
    """
    return (
        coc.HERO_ORDER +
        coc.HERO_PETS_ORDER +
        coc.HOME_TROOP_ORDER +
        coc.SPELL_ORDER
    )


def hero_units(coc_client):
    """
        returns a list of all hero units

        Args:
            coc_client (obj): coc.py client

        Returns:
            hero_units: list of all units
    """
    return coc_client._hero_holder.items


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


# War

async def get_war(clan_tag, coc_client):
    try:
        war_obj = await coc_client.get_current_war(clan_tag)

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
        clan_lineup_dict[member.town_hall] += 1

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


# CWL Group

async def get_cwl_group(clan_tag, coc_client):
    try:
        cwl_group = await coc_client.get_league_group(clan_tag)

    except Maintenance:
        return None

    except NotFound:
        return None

    except GatewayError:
        return None

    return cwl_group


def cwl_clan_lineup(cwl_group_clan):
    clan_lineup_dict = th_lineup_dict.copy()
    for member in cwl_group_clan.members:
        clan_lineup_dict[member.town_hall] += 1
    return clan_lineup_dict


def cwl_member_score(cwl_wars, cwl_member):
    class ScoredCWLMember(object):
        """
            ScoredWarMember
                Instance Attributes
                    tag (str): WarMember's player tag
                    name (str): WarMember's player name
                    participated_wars (int): rounds participated
                    round_scores (list[int]): scores for each round
                    score (int): WarMember's war score
        """

        def __init__(self, tag, name, participated_wars, round_scores, score):
            self.tag = tag
            self.name = name
            self.participated_wars = participated_wars
            self.round_scores = round_scores
            self.score = score

    scored_member = ScoredCWLMember(cwl_member.tag, cwl_member.name, 0, [], 0)
    # for each war getting that war score and war count
    for war in cwl_wars:
        # do not include wars that are not even in preparation
        if war.war_tag == "#0":
            continue

        # do not include wars that are not over
        if war.state != "warEnded":
            continue

        round_score = 0
        for war_member in war.clan.members:
            if war_member.tag == cwl_member.tag:
                scored_member.participated_wars += 1
                round_score = member_score(war_member, war).score
                break

        scored_member.round_scores.append(round_score)

    # return without operating if member did not participate
    if scored_member.participated_wars == 0:
        return scored_member

    score_sum = 0
    for round_score in scored_member.round_scores:
        score_sum += round_score

    avg_score = score_sum / scored_member.participated_wars
    participation_multiplier = math.log(
        scored_member.participated_wars, len(cwl_wars))
    scored_member.score = avg_score * participation_multiplier
    return scored_member


# CWL War


# UTILS

def member_score(war_member, war_obj):
    class ScoredWarMember(object):
        """
            ScoredWarMember
                Instance Attributes
                    tag (str): WarMember's player tag
                    name (str): WarMember's player name
                    score (int): WarMember's war score
        """

        def __init__(self, tag, name, score):
            self.tag = tag
            self.name = name
            self.score = score

    # each missed attack should be -100
    if war_obj.is_cwl:
        attacks_per_member = 1
    else:
        attacks_per_member = 2
    # reactivate below code when coc.py returns correct attacks_per_member
    # member_score = war_obj.attacks_per_member*(-100)
    member_score = attacks_per_member*(-100)
    for attack in war_member.attacks:
        # add 100 since the member attacked
        member_score += 100

        scored_attack = attack_score(attack, war_member, war_obj)

        member_score += scored_attack.score
    member_score = member_score/attacks_per_member
    # reactivate below code when coc.py returns correct attacks_per_member
    # member_score = member_score/war_obj.attacks_per_member
    return ScoredWarMember(war_member.tag, war_member.name, member_score)


def attack_score(attack, war_member, war_obj):
    class ScoredWarAttack(object):
        """
            ScoredWarAttack
                Instance Attributes
                    stars (str): WarMemberAttack's stars earned
                    destruction (str): WarMemberAttack's destruction earned
                    score (int): WarMemberAttack's attack score
        """

        def __init__(self, stars, destruction, score):
            self.stars = stars
            self.destruction = destruction
            self.score = score

    star_score = attack.stars/3
    des_score = attack.destruction/100
    defender = find_defender(war_obj.opponent, attack.defender_tag)
    th_difference = defender.town_hall-war_member.town_hall
    attack_score = (((star_score*.75)+(des_score*.25))
                    * th_multiplier(th_difference))

    return ScoredWarAttack(attack.stars, attack.destruction, attack_score)


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
