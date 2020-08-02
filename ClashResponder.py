import math

import Player
import Clan
import War
import CWLGroup
import CWLWar


# Player

# returns player.name and troop.lvl
def response_troop_lvl(player_name, troop_name, clan_tag, header):
    player_tag = Clan.get(clan_tag, header).find_member(player_name)
    player = Player.get(player_tag, header)
    troop = player.find_troop(troop_name)
    if troop.name == '':
        return "Couldn't find that troop, hero, or spell. You either do not have it unlocked or it is misspelled."
    if troop.lvl == troop.max_lvl:
        return f'{player.name} has lvl {troop.lvl} {troop.name}, which is max.'
    elif troop.lvl == troop.th_max:
        return f'{player.name} has lvl {troop.lvl} {troop.name}, which is max for TH {player.th_lvl}, max {troop.name} is {troop.max_lvl}.'
    else:
        return f'{player.name} has lvl {troop.lvl} {troop.name}, max for TH {player.th_lvl} is {troop.th_max}, max {troop.name} is {troop.max_lvl}.'


# returns a list of all troops and their levels
def response_all_troop_level(player_name, clan_tag, header):
    clan = Clan.get(clan_tag, header)
    player_tag = clan.find_member(player_name)
    player = Player.get(player_tag, header)
    response_list = []
    response_list.append(f'{player.name} troops:')
    for troop in player.troops:
        if troop.village == 'home':
            if troop.name != 'Super Barbarian' and troop.name != 'Super Wall Breaker' and troop.name != 'Super Giant' and troop.name != 'Sneaky Goblin':
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

# returns a string response of members that can donate the best of that troop
def response_donation(troop_name, clan_tag, header):
    # name formatting done at the class level
    clan = Clan.get(clan_tag, header)

    # get a member_list to make less responses
    members = []
    for i in range(0, 25):
        member = Player.get(clan.members[i].tag, header)

        if member.find_troop(troop_name).name != '':
            members.append(member)
    # list of those that can donate
    donators = []
    # list of troops to iterate through
    troops = []
    # get the list of troops from all the members
    for member in members:
        troop = member.find_troop(troop_name)
        if troop.name != '':
            troops.append(troop)

    # returns an empty list if there are no troops found (could be misspelled troop_name)
    if len(troops) == 0:
        return []
    donor_max = max(troop.lvl for troop in troops)

    donor_string = ''
    # checking to see if anyone can donate max
    if (donor_max + clan.donation_upgrade) >= troops[0].max_lvl:
        # go thru each member and return the donors that can donate max
        for member in members:
            troop = member.find_troop(troop_name)
            # adding the donor's name to the donor string
            if (troop.lvl + clan.donation_upgrade) >= troop.max_lvl:
                donators.append(member)
                donor_string += f'{member.name}, '
        # cuts the last two characters from the string ', '
        donor_string = donor_string[:-2]
        # singular
        if len(donators) == 1:
            return f'{donor_string} is able to donate max {troops[0].name} which is level {troops[0].max_lvl}.'
        # plural
        else:
            return f'{donor_string} are able to donate max {troops[0].name} which is level {troops[0].max_lvl}.'

    # since nobody can donate max
    else:
        for member in members:
            troop = member.find_troop(troop_name)
            if troop.lvl >= donor_max:
                donators.append(member)
                donor_string += f'{member.name}, '
        # cuts the last two characters from the string ', '
        donor_string = donor_string[:-2]
        # singular
        if len(donators) == 1:
            return f'{donor_string} is able to donate lvl {donor_max + clan.donation_upgrade} {troops[0].name}, max is lvl {troops[0].max_lvl}.'
        # plural
        else:
            return f'{donor_string} are able to donate lvl {donor_max + clan.donation_upgrade} {troops[0].name}, max is lvl {troops[0].max_lvl}.'


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


# returns a list of all war members and their stars
def response_war_members_overview(clan_tag, time_zone, header):
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

# CWL Group


# CWL War

# returns a string of the cwl war no attack response
def response_cwl_war_no_attack(clan_tag, time_zone, header):
    group = CWLGroup.get(clan_tag, header)
    war = group.find_current_war()

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
        return 'You are not in war.'


# returns a string of the current cwl war overview
def response_cwl_war_overview(clan_tag, time_zone, header):
    group = CWLGroup.get(clan_tag, header)
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
        return f'You are not in war.'


# returns a string of the time remaining in war response
def response_cwl_war_time(clan_tag, time_zone, header):
    group = CWLGroup.get(clan_tag, header)
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
        return 'You are not in war.'


# returns a list of cwl war attack string responses for all war members
def response_cwl_war_all_attacks(clan_tag, time_zone, header):
    group = CWLGroup.get(clan_tag, header)
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
        response_list.append('You are not in war.')
    return response_list


# returns CWL standing
def response_cwl_standing(clan_tag, header):
    class ScoredMember(object):
        def __init__(self, tag, name, war_count, score):
            self.tag = tag
            self.name = name
            self.war_count = war_count
            self.score = score
    # get the CWLGroup object
    cwl_group = CWLGroup.get(clan_tag, header)
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
                    avg_score = scored_member.score/scored_member.war_count
                    participation_multiplier = math.log(
                        scored_member.war_count, 7)
                    scored_member.score = avg_score*participation_multiplier

    sorted_cwl_war_members = sorted(
        cwl_war_members, key=lambda member: member.score, reverse=True)
    return_string_list = []
    for member in sorted_cwl_war_members:
        return_string_list.append(
            f'{member.name} has a score of {round(member.score, 3)}')
    return return_string_list


def th_multiplier(th_difference):
    if th_difference < -2:
        th_mult = 10
    elif th_difference == -2:
        th_mult = 35
    elif th_difference == -1:
        th_mult = 50
    elif th_difference == 0:
        th_mult = 100
    elif th_difference == 1:
        th_mult = 150
    elif th_difference == 2:
        th_mult = 165
    elif th_difference > 2:
        th_mult = 200
    else:
        th_mult = 100
    return th_mult
