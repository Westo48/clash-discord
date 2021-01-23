import math

import Player
import Clan
import War
import CWLGroup
import CWLWar


cwl_clan_lineup_dict = {
    'clan': {},
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
    2: 0
}


# Player

# returns player.name and troop.lvl
def response_troop_lvl(player_name, unit_name, clan_tag, header):
    player_tag = Clan.get(clan_tag, header).find_member(player_name)
    player = Player.get(player_tag, header)
    if not player:
        return (f'Could not find {player_name} in the clan.')
    unit = player.find_unit(unit_name)
    if not unit:
        return (f'Could not find {unit_name}. '
                f'You either do not have it unlocked or it is misspelled.')
    if unit.lvl == unit.max_lvl:
        return f'{player.name} has lvl {unit.lvl} {unit.name}, which is max.'
    elif unit.lvl == unit.th_max:
        return (f'{player.name} has lvl {unit.lvl} {unit.name}, '
                f'which is max for TH {player.th_lvl}, '
                f'max {unit.name} is {unit.max_lvl}.')
    else:
        return (f'{player.name} has lvl {unit.lvl} {unit.name}, '
                f'max for TH {player.th_lvl} is {unit.th_max}, '
                f'max {unit.name} is {unit.max_lvl}.')


# ? discontinue this function
# returns a list of all troops and their levels
def response_all_troop_level(player_name, clan_tag, header):
    clan = Clan.get(clan_tag, header)
    player_tag = clan.find_member(player_name)
    player = Player.get(player_tag, header)
    response_list = []
    response_list.append(f'{player.name} troops:')
    for troop in player.troops:
        if troop.village == 'home':
            if troop.lvl == troop.max_lvl:
                response_list.append(
                    f'{troop.name} is lvl {troop.lvl}, which is max.')
                response_list.append('__________')
            elif troop.lvl == troop.th_max:
                response_list.append(
                    f'{troop.name} is lvl {troop.lvl}, which is max for TH {player.th_lvl}, max {troop.name} is {troop.max_lvl}.')
                response_list.append('__________')
            else:
                response_list.append(
                    f'{troop.name} is lvl {troop.lvl}, max for TH {player.th_lvl} is lvl {troop.th_max}, max {troop.name} is {troop.max_lvl}.')
                response_list.append('__________')
    del response_list[-1]
    return response_list


# Clan

# returns a string response of members that can donate the best of that unit
# todo put this into the clan framework
def response_donation(unit_name, clan, header):
    """
        Takes in the unit name and clan tag, returns a list of players
        who can donate.

        Returns an empty list if nobody can donate requested unit.
        Returns None if hero has been requested.

        Args:
            unit_name (str): Name of requested unit.
            clan_tag (str): Tag of player's.
            header (dict): Json header

        Returns:
            list: List of players who can donate.
    """

    class Donor(object):
        def __init__(self, player, unit):
            self.player = player
            self.unit = unit

    # get a member list to make less overall responses
    members = []
    member_range = min([15, len(clan.members)])
    for i in range(0, member_range):
        member = Player.get(clan.members[i].tag, header)

        # checking if they have the specified unit
        unit = member.find_unit(unit_name)
        if unit:
            members.append(Donor(member, unit))

    # if nobody has the requested unit
    if len(members) == 0:
        return members

    # if hero has been requested return None
    if members[0].player.find_hero(unit_name):
        return None

    donor_max = max(member.unit.lvl for member in members)

    # list of those that can donate
    donators = []

    # checking to see if anyone can donate max
    if (donor_max + clan.donation_upgrade) >= members[0].unit.max_lvl:
        # go thru each member and return the donors that can donate max
        for member in members:
            # if the member can donate max unit
            if (member.unit.lvl+clan.donation_upgrade) >= member.unit.max_lvl:
                # adding the donor's name to the donator list
                donators.append(member)
        return donators

    # since nobody can donate max
    # ! this still needs to be tested
    else:
        for member in members:
            troop = member.find_troop(unit_name)
            if troop.lvl >= donor_max:
                donators.append(member)
        return donators


def response_player(player_name, clan_tag, header):
    "takes in the player name and returns player object"
    clan = Clan.get(clan_tag, header)
    player_tag = clan.find_member(player_name)
    if player_tag == "":
        return None
    return Player.get(player_tag, header)


# returns a string of the member's role
def response_member_role(player_name, clan_tag, header):
    clan = Clan.get(clan_tag, header)
    player_tag = clan.find_member(player_name)
    player = Player.get(player_tag, header)
    return player.role


# War

# returns a string of the war overview
def response_war_overview(clan_tag, time_zone, header):
    war = War.get(clan_tag, header)
    if war.state == 'preparation':
        time_string = war.string_date_time(time_zone)

        return f'{war.clan.name} is preparing for war with {war.opponent.name} with {time_string} left before war starts.'
    elif war.state == 'inWar':
        time_string = war.string_date_time(time_zone)
        scoreboard_string = war.string_scoreboard()

        return f'{war.clan.name} is in war with {war.opponent.name} with {time_string} left in war. {war.clan.name} is {scoreboard_string}.'
    elif war.state == 'warEnded':
        scoreboard_string = war.string_scoreboard()
        return f'War against {war.opponent.name} has ended. {war.clan.name} {scoreboard_string}.'
    else:
        return f'You are not in war.'


# returns a string of the time remaining in war response
def response_war_time(clan_tag, time_zone, header):
    war = War.get(clan_tag, header)
    if war.state == 'preparation':
        return f'{war.clan.name} is preparing for war with {war.string_date_time(time_zone)} left before war starts.'
    elif war.state == 'inWar':
        return f'{war.clan.name} is in war with {war.string_date_time(time_zone)} left in war.'
    elif war.state == 'warEnded':
        return f'The war with {war.opponent.name} has ended.'
    else:
        return 'You are not in war.'


# todo if nobody has attacked logic
# returns a string of the war no attack response
def response_war_no_attack(clan_tag, time_zone, header):
    war = War.get(clan_tag, header)

    if war.state == 'preparation':
        return f'{war.clan.name} is still preparing for war with {war.string_date_time(time_zone)} before war starts, nobody has attacked.'

    elif war.state == 'inWar':
        no_attack_list = war.no_attack()
        if len(no_attack_list) == 0:
            return f'All {war.team_size} {war.clan.name} war members attacked.'
        no_attack_string = ''
        for member in no_attack_list:
            no_attack_string += f'{member.name}, '
        # removes the last 2 characters ', ' of the string
        no_attack_string = no_attack_string[:-2]
        # singular
        if len(no_attack_list) == 1:
            no_attack_string += ' has not attacked'
        # plural
        else:
            no_attack_string += ' have not attacked'
        no_attack_string += f' with {war.string_date_time(time_zone)} left in war.'
        return no_attack_string

    elif war.state == 'warEnded':
        no_attack_list = war.no_attack()
        if len(no_attack_list) == 0:
            return f'All {war.team_size} {war.clan.name} war members attacked.'
        no_attack_string = ''
        for member in no_attack_list:
            no_attack_string += f'{member.name}, '
        # removes the last 2 characters ', ' of the string
        no_attack_string = no_attack_string[:-2]
        no_attack_string += ' did not attack.'
        return no_attack_string

    else:
        return 'You are not in war.'


def war_no_attack_members(clan_tag, time_zone, header):
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


# returns a list of all war members and their stars
def response_war_members_overview(clan_tag, time_zone, header):
    "returns a list of all war members and their stars"
    war = War.get(clan_tag, header)
    response_list = []

    if war.state == 'preparation':
        response_list.append(
            f'{war.clan.name} is still preparaing for war, nobody has attacked.')
    elif war.state == 'inWar':
        response_list.append(
            f'{war.clan.name} is in war with {war.opponent.name} with {war.string_date_time(time_zone)} left in war. {war.clan.name} is {war.string_scoreboard()}.')
        response_list.append('____________________')
        for member in war.clan.members:
            # no atk response
            if len(member.attacks) == 0:
                response_list.append(
                    f'{member.name} map pos {member.map_position} TH {member.th_lvl} has not attacked.')
            else:
                response_list.append(
                    f'{member.name} map pos {member.map_position} TH {member.th_lvl} has attacked {len(member.attacks)} {member.string_member_attack_times()} for a total of {member.stars} {member.string_member_stars()}')
            response_list.append('__________')

        del response_list[-1]
    elif war.state == 'warEnded':
        response_list.append(
            f'War against {war.opponent.name} has ended. {war.clan.name} {war.string_scoreboard()}.')
        response_list.append('____________________')
        for member in war.clan.members:
            # no atk response
            if len(member.attacks) == 0:
                response_list.append(
                    f'{member.name} map pos {member.map_position} TH {member.th_lvl} did not attacked.')
            else:
                response_list.append(
                    f'{member.name} map pos {member.map_position} TH {member.th_lvl} attacked {len(member.attacks)} {member.string_member_attack_times()} for a total of {member.stars} {member.string_member_stars()}.')
            response_list.append('__________')

        del response_list[-1]
    else:
        response_list.append('You are not in war.')

    return response_list


# returns a list of war attack string responses for all war members
def response_war_all_attacks(clan_tag, time_zone, header):
    war = War.get(clan_tag, header)
    response_list = []

    if war.state == 'preparation':
        response_list.append(
            f'{war.clan.name} is still preparaing for war, nobody has attacked.')
    elif war.state == 'inWar':
        response_list.append(
            f'{war.clan.name} is in war with {war.opponent.name} with {war.string_date_time(time_zone)} left in war. {war.clan.name} is {war.string_scoreboard()}.')
        response_list.append('____________________')
        for member in war.clan.members:
            # no atk response
            if len(member.attacks) == 0:
                response_list.append(
                    f'{member.name} map pos {member.map_position} TH {member.th_lvl} has not attacked.')
            else:
                response_list.append(
                    f'{member.name} map pos {member.map_position} TH {member.th_lvl} has attacked {len(member.attacks)} {member.string_member_attack_times()} for a total of {member.stars} {member.string_member_stars()}')
                for attack in member.attacks:
                    defender = war.find_defender(attack.defender_tag)

                    if attack.stars == 0 or attack.stars == 3:
                        response_list.append(
                            f' - {attack.stars} {attack.string_attack_stars()} against {defender.name} map pos {defender.map_position} TH {defender.th_lvl}')
                    else:
                        response_list.append(
                            f' - {attack.stars} {attack.string_attack_stars()}, {round(attack.destruction_percent, 2)}% against {defender.name} map pos {defender.map_position} TH {defender.th_lvl}')

            response_list.append('__________')

        del response_list[-1]
    elif war.state == 'warEnded':
        response_list.append(
            f'War against {war.opponent.name} has ended. {war.clan.name} {war.string_scoreboard()}.')
        response_list.append('____________________')
        for member in war.clan.members:
            if len(member.attacks) == 0:
                response_list.append(
                    f'{member.name} map pos {member.map_position} TH {member.th_lvl} did not attack.')
            else:

                response_list.append(
                    f'{member.name} map pos {member.map_position} TH {member.th_lvl} has attacked {len(member.attacks)} {member.string_member_attack_times()} for a total of {member.stars} {member.string_member_stars()}.')
                for attack in member.attacks:
                    defender = war.find_defender(attack.defender_tag)

                    if attack.stars == 0 or attack.stars == 3:
                        response_list.append(
                            f' - {attack.stars} {attack.string_attack_stars()} against {defender.name} map pos {defender.map_position} TH {defender.th_lvl}')
                    else:
                        response_list.append(
                            f' - {attack.stars} {attack.string_attack_stars()}, {round(attack.destruction_percent, 2)}% against {defender.name} map pos {defender.map_position} TH {defender.th_lvl}')

            response_list.append('__________')
        del response_list[-1]
    else:
        response_list.append('You are not in war.')

    return response_list


def response_war_all_member_standing(clan_tag, time_zone, header):
    "returns a response list of member scores"
    war = War.get(clan_tag, header)
    return_list = []
    if war.state == 'preparation':
        return_list.append('War has not started, there is no score.')
        return return_list
    elif war.state == 'notInWar':
        return_list.append('You are not in war.')
        return return_list
    else:
        war_members = sorted(
            war.clan.members, key=lambda member: member.score, reverse=True)
        # razgriz has a score of
        for member in war_members:
            return_list.append(
                f'{member.name} has a score of {round(member.score, 3)}')
        return return_list


# todo update all for if not in CWL logic
# CWL Group

def response_cwl_lineup(cwl_group):
    if not cwl_group:
        return None
    clan_lineup = []
    for clan in cwl_group.clans:
        clan_lineup_dict = {
            'clan': {},
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
            2: 0
        }
        clan_lineup_dict['clan'] = clan
        for member in clan.members:
            clan_lineup_dict[member.th_lvl] += 1
        clan_lineup.append(clan_lineup_dict)
    return clan_lineup


# CWL War

# returns a string of the cwl war no attack response
def response_cwl_war_no_attack(clan_tag, time_zone, header):
    group = CWLGroup.get(clan_tag, header)

    if not group:
        return 'You are not in CWL.'

    war = group.find_current_war(clan_tag, header)

    if war.state == 'preparation':
        return f'{war.clan.name} is still preparing for war with {war.string_date_time(time_zone)} before war starts, nobody has attacked.'

    elif war.state == 'inWar':
        no_attack_list = war.no_attack()
        if len(no_attack_list) == 0:
            return f'All {war.team_size} {war.clan.name} war members attacked.'
        no_attack_string = ''
        for member in no_attack_list:
            no_attack_string += f'{member.name}, '
        # removes the last 2 characters ', ' of the string
        no_attack_string = no_attack_string[:-2]
        # singular
        if len(no_attack_list) == 1:
            no_attack_string += ' has not attacked.'
        # plural
        else:
            no_attack_string += ' have not attacked.'
        return no_attack_string

    elif war.state == 'warEnded':
        no_attack_list = war.no_attack()
        if len(no_attack_list) == 0:
            return f'All {war.team_size} {war.clan.name} war members attacked.'
        no_attack_string = ''
        for member in no_attack_list:
            no_attack_string += f'{member.name}, '
        # removes the last 2 characters ', ' of the string
        no_attack_string = no_attack_string[:-2]
        no_attack_string += ' did not attack.'
        return no_attack_string

    else:
        return 'You are not in CWL.'


# returns a string of the current cwl war overview
def response_cwl_war_overview(clan_tag, time_zone, header):
    group = CWLGroup.get(clan_tag, header)

    if not group:
        return 'You are not in CWL.'

    war = group.find_current_war(clan_tag, header)
    if war.state == 'preparation':
        time_string = war.string_date_time(time_zone)
        return f'{war.clan.name} is preparing for war with {war.opponent.name} with {time_string} left before war starts.'
    elif war.state == 'inWar':
        time_string = war.string_date_time(time_zone)
        scoreboard_string = war.string_scoreboard()
        return f'{war.clan.name} is in war with {war.opponent.name} with {time_string} left in war. {war.clan.name} is {scoreboard_string}.'
    elif war.state == 'warEnded':
        scoreboard_string = war.string_scoreboard()
        return f'War against {war.opponent.name} has ended. You {scoreboard_string}.'
    else:
        return 'You are not in CWL.'


# returns a string of the time remaining in war response
def response_cwl_war_time(clan_tag, time_zone, header):
    group = CWLGroup.get(clan_tag, header)

    if not group:
        return 'You are not in CWL.'

    war = group.find_current_war(clan_tag, header)

    if war.state == 'preparation':
        time_string = war.string_date_time(time_zone)
        return f'{war.clan.name} is preparing for war with {time_string} left before war starts.'
    elif war.state == 'inWar':
        time_string = war.string_date_time(time_zone)
        return f'{war.clan.name} is preparing for war with {time_string} left in war.'
    elif war.state == 'warEnded':
        return f'The war with {war.opponent.name} has ended.'
    else:
        return 'You are not in CWL.'


# returns a list of cwl war attack string responses for all war members
def response_cwl_war_all_attacks(clan_tag, time_zone, header):
    group = CWLGroup.get(clan_tag, header)

    if not group:
        return ['You are not in CWL.']

    war = group.find_current_war(clan_tag, header)
    response_list = []
    if war.state == 'preparation':
        response_list.append(
            f'{war.clan.name} is still preparaing for war, nobody has attacked.')
    elif war.state == 'inWar':
        response_list.append(
            f'{war.clan.name} is in war with {war.opponent.name} with {war.string_date_time(time_zone)} left in war. {war.clan.name} is {war.string_scoreboard()}.')
        response_list.append('____________________')
        for member in war.clan.members:
            if len(member.attacks) == 0:
                response_list.append(
                    f'{member.name} map pos {member.map_position} TH {member.th_lvl} has not attacked.')
            else:

                response_list.append(
                    f'{member.name} map pos {member.map_position} TH {member.th_lvl} has attacked {len(member.attacks)} {member.string_member_attack_times()} for a total of {member.stars} {member.string_member_stars()}')
                for attack in member.attacks:
                    defender = war.find_defender(attack.defender_tag)

                    if attack.stars == 0 or attack.stars == 3:
                        response_list.append(
                            f' - {attack.stars} {attack.string_attack_stars()} against {defender.name} map pos {defender.map_position} TH {defender.th}')
                    else:
                        response_list.append(
                            f' - {attack.stars} {attack.string_attack_stars()}, {round(attack.destruction_percent, 2)}% against {defender.name} map pos {defender.map_position} TH {defender.th}')

            response_list.append('__________')
        del response_list[-1]
    elif war.stat == 'warEnded':
        response_list.append(
            f'War against {war.opponent.name} has ended. {war.clan.name} {war.string_scoreboard()}.')
        response_list.append('____________________')
        for member in war.clan.members:
            if len(member.attacks) == 0:
                response_list.append(
                    f'{member.name} map pos {member.map_position} TH {member.th_lvl} did not attack.')
            else:

                response_list.append(
                    f'{member.name} map pos {member.map_position} TH {member.th_lvl} has attacked {len(member.attacks)} {member.string_member_attack_times()} for a total of {member.stars} {member.string_member_stars()}')
                for attack in member.attacks:
                    defender = war.find_defender(attack.defender_tag)

                    if attack.stars == 0 or attack.stars == 3:
                        response_list.append(
                            f' - {attack.stars} {attack.string_attack_stars()} against {defender.name} map pos {defender.map_position} TH {defender.th}')
                    else:
                        response_list.append(
                            f' - {attack.stars} {attack.string_attack_stars()}, {round(attack.destruction_percent, 2)}% against {defender.name} map pos {defender.map_position} TH {defender.th}')

            response_list.append('__________')
        del response_list[-1]
    else:
        response_list.append('You are not in CWL.')
    return response_list


# returns each member's CWL standing
def response_cwl_clan_standing(clan_tag, header):
    class ScoredMember(object):
        def __init__(self, tag, name, war_count, score):
            self.tag = tag
            self.name = name
            self.war_count = war_count
            self.score = score
    # get the CWLGroup object
    cwl_group = CWLGroup.get(clan_tag, header)

    if not cwl_group:
        return ['You are not in CWL.']

    # get a list of all CWLWar objects
    cwl_wars = []
    for i in range(0, len(cwl_group.rounds)):
        cwl_war = cwl_group.find_specified_war(clan_tag, i, header)
        cwl_wars.append(cwl_war)
    # get a list of all CWLWarMembers their scores
    cwl_war_members = []
    # find your clan
    for clan in cwl_group.clans:
        if clan.tag == clan_tag:
            # for each member in the CWLWarClan
            for member in clan.members:
                scored_member = ScoredMember(member.tag, member.name, 0, 0)
                # for each war getting that war score and war count
                for war in cwl_wars:
                    for war_member in war.clan.members:
                        if war_member.tag == member.tag:
                            scored_member.war_count += 1
                            scored_member.score += war_member.score
                            break
                if scored_member.war_count != 0:
                    avg_score = scored_member.score / scored_member.war_count
                    participation_multiplier = math.log(
                        scored_member.war_count, 7)
                    scored_member.score = avg_score * participation_multiplier
                cwl_war_members.append(scored_member)

    sorted_cwl_war_members = sorted(
        cwl_war_members, key=lambda member: member.score, reverse=True)
    return_string_list = []
    for member in sorted_cwl_war_members:
        return_string_list.append(
            f'{member.name} has a score of {round(member.score, 3)}')
    return return_string_list


# returns each specified member's CWL War score
def response_cwl_member_standing(player_name, clan_tag, header):
    # find the player from the clan
    clan = Clan.get(clan_tag, header)
    player_tag = clan.find_member(player_name)
    # returns a response if they provided an incorrect player name
    if player_tag == '':
        return f'Could not find {player_name}'
    player = Player.get(player_tag, header)

    # get the CWLGroup object
    cwl_group = CWLGroup.get(clan_tag, header)

    if not cwl_group:
        return 'You are not in CWL.'

    # get a list of all CWLWar objects
    cwl_wars = []
    for i in range(0, len(cwl_group.rounds)):
        cwl_war = cwl_group.find_specified_war(clan_tag, i, header)
        cwl_wars.append(cwl_war)
    member_round_scores = []
    # find your clan
    found = False
    for clan in cwl_group.clans:
        if clan.tag == clan_tag:
            cwl_group_clan = clan
            found = True
            break
    if not found:
        return 'Could not find your clan based on the clan tag provided'

    found = False
    for member in cwl_group_clan.members:
        if member.tag == player.tag:
            found = True
            break
    if not found:
        return 'Could not find {player.name} in the CWL group.'

    for war in cwl_wars:
        for war_member in war.clan.members:
            if war_member.tag == player.tag:
                member_round_scores.append(war_member.score)
                break

    if len(member_round_scores) == 0:
        return_string = f'{player.name} did not participate in any wars.'

    elif len(member_round_scores) == 1:
        return_string = f'{player.name} was in 1 war and had a score of {round(member_round_scores[0], 3)} for that war.'

    else:
        total_score = 0
        for round_score in member_round_scores:
            total_score += round_score
        avg_score = total_score / len(member_round_scores)
        participation_multiplier = math.log(len(member_round_scores), 7)
        member_score = avg_score * participation_multiplier

        return_string = f"{player.name} was in {len(member_round_scores)} wars with an overall score of {round(member_score, 3)}. {player.name}'s scores are: "
        for cwl_round_score in member_round_scores:
            return_string += f'{round(cwl_round_score, 3)}, '
        # removes the last 2 characters ', ' of the string
        return_string = return_string[:-2]
        return_string += '.'

    return return_string
