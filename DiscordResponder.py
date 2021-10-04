import math
import Clan
from Player import super_troop_list


# PLAYER

def player_info(player_obj):
    field_dict_list = []
    field_dict_list.append({
        'name': '**Exp Lvl**',
        'value': player_obj.xp_lvl,
        'inline': True
    })
    field_dict_list.append({
        'name': '**TH Lvl**',
        'value': player_obj.th_lvl,
        'inline': True
    })
    if player_obj.th_weapon_lvl:
        field_dict_list.append({
            'name': '**TH Weapon Lvl**',
            'value': player_obj.th_weapon_lvl,
            'inline': True
        })
    field_dict_list.append({
        'name': '**Trophies**',
        'value': player_obj.trophies,
        'inline': True
    })
    field_dict_list.append({
        'name': '**Best Trophies**',
        'value': player_obj.best_trophies,
        'inline': True
    })
    if player_obj.legend_trophies:
        field_dict_list.append({
            'name': '**Legend Trophies**',
            'value': player_obj.legend_trophies,
            'inline': True
        })
    if player_obj.best_legend_rank:
        field_dict_list.append({
            'name': '**Best Rank | Trophies**',
            'value': (f"{player_obj.best_legend_rank} | "
                      f"{player_obj.best_legend_trophies}"),
            'inline': True
        })
    if player_obj.current_legend_rank:
        field_dict_list.append({
            'name': '**Current Rank | Trophies**',
            'value': (f"{player_obj.current_legend_rank} | "
                      f"{player_obj.current_legend_trophies}"),
            'inline': True
        })
    if player_obj.previous_legend_rank:
        field_dict_list.append({
            'name': '**Previous Rank | Trophies**',
            'value': (f"{player_obj.previous_legend_rank} | "
                      f"{player_obj.previous_legend_trophies}"),
            'inline': True
        })

    field_dict_list.append({
        'name': '**War Stars**',
        'value': player_obj.war_stars,
        'inline': True
    })
    if player_obj.clan_tag:
        field_dict_list.append({
            'name': '**Clan**',
            'value': (f"[{player_obj.clan_name}]"
                      f"(https://link.clashofclans.com/"
                      f"en?action=OpenClanProfile&tag="
                      f"{player_obj.clan_tag[1:]})"),
            'inline': True
        })

        if player_obj.role == 'leader':
            role_name = 'Leader'
        elif player_obj.role == 'coLeader':
            role_name = 'Co-Leader'
        elif player_obj.role == 'admin':
            role_name = 'Elder'
        else:
            role_name = 'Member'
        field_dict_list.append({
            'name': '**Clan Role**',
            'value': role_name,
            'inline': True
        })
    else:
        field_dict_list.append({
            'name': '**Clan**',
            'value': f"{player_obj.name} is not in a clan",
            'inline': True
        })

    hero_title = ''
    hero_value = ''
    for hero in player_obj.heroes:
        if hero.name == 'Barbarian King':
            hero_title = 'BK'
            hero_value = f'{hero.lvl}'
        elif hero.name == 'Archer Queen':
            hero_title += ' | AQ'
            hero_value += f' | {hero.lvl}'
        elif hero.name == 'Grand Warden':
            hero_title += ' | GW'
            hero_value += f' | {hero.lvl}'
        elif hero.name == 'Royal Champion':
            hero_title += ' | RC'
            hero_value += f' | {hero.lvl}'
        else:
            break
    if hero_title != '':
        field_dict_list.append({
            'name': f'**{hero_title}**',
            'value': hero_value,
            'inline': True
        })

    pet_title = ''
    pet_value = ''
    for troop in player_obj.troops:
        if troop.name == 'L.A.S.S.I':
            pet_title = 'LA'
            pet_value = f'{troop.lvl}'
        elif troop.name == 'Mighty Yak':
            pet_title += ' | MY'
            pet_value += f' | {troop.lvl}'
        elif troop.name == 'Electro Owl':
            pet_title += ' | EO'
            pet_value += f' | {troop.lvl}'
        elif troop.name == 'Unicorn':
            pet_title += ' | UC'
            pet_value += f' | {troop.lvl}'
    if pet_title != '':
        field_dict_list.append({
            'name': f'**{pet_title}**',
            'value': pet_value,
            'inline': True
        })

    field_dict_list.append({
        'name': '**Link**',
        'value': (f"[{player_obj.name}]"
                  f"(https://link.clashofclans.com/"
                  f"en?action=OpenPlayerProfile&tag="
                  f"{player_obj.tag[1:]})"),
        'inline': True
    })
    return field_dict_list


def unit_lvl(player_obj, unit_obj, unit_name):
    if not unit_obj:
        # unit not found response
        return {
            'name': f"could not find {unit_name}",
            'value': f"you either do not have it unlocked or it is misspelled"
        }

    if unit_obj.lvl == unit_obj.max_lvl:
        # unit is max lvl
        return {
            'name': f"{unit_obj.name} lvl {unit_obj.lvl}",
            'value': f"max lvl"
        }
    elif unit_obj.lvl == unit_obj.th_max:
        # unit is max for th, but not total max
        return {
            'name': f"{unit_obj.name} lvl {unit_obj.lvl}",
            'value': (
                f"TH {player_obj.th_lvl} max, "
                f"max {unit_obj.name} is {unit_obj.max_lvl}"
            )
        }
    else:
        # unit is not max for th nor is it total max
        if unit_obj.max_lvl == unit_obj.th_max:
            # unit max is the same as th max
            return {
                'name': f"{unit_obj.name} lvl {unit_obj.lvl}",
                'value': f"max {unit_obj.name} is {unit_obj.max_lvl}"
            }
        else:
            # unit max is not the same as th max
            return {
                'name': f"{unit_obj.name} lvl {unit_obj.lvl}",
                'value': (
                    f"TH {player_obj.th_lvl} max is {unit_obj.th_max}, "
                    f"max {unit_obj.name} is {unit_obj.max_lvl}"
                )
            }


def unit_lvl_all(player_obj):
    field_dict_list = []
    for field_dict in hero_lvl_all(player_obj):
        field_dict_list.append(field_dict)
    for field_dict in troop_lvl_all(player_obj):
        field_dict_list.append(field_dict)
    for field_dict in spell_lvl_all(player_obj):
        field_dict_list.append(field_dict)
    return field_dict_list


def hero_lvl_all(player_obj):
    field_dict_list = []
    for hero_obj in player_obj.heroes:
        if hero_obj.village == 'home':
            field_dict_list.append(unit_lvl(
                player_obj, hero_obj, hero_obj.name))
    return field_dict_list


def troop_lvl_all(player_obj):
    field_dict_list = []
    for troop_obj in player_obj.troops:
        if troop_obj.village == 'home':
            field_dict_list.append(unit_lvl(
                player_obj, troop_obj, troop_obj.name))
    return field_dict_list


def spell_lvl_all(player_obj):
    field_dict_list = []
    for spell_obj in player_obj.spells:
        if spell_obj.village == 'home':
            field_dict_list.append(unit_lvl(
                player_obj, spell_obj, spell_obj.name))
    return field_dict_list


def active_super_troops(player_obj, active_super_troops):
    if len(active_super_troops) == 0:
        return [{
            'name': "none",
            'value': f"{player_obj.name} does not have any active super troops"
        }]
    else:
        field_dict_list = []
        for super_troop in active_super_troops:
            field_dict_list.append({
                'name': super_troop.name,
                'value': f"is active"
            })
        return field_dict_list


# CLAN

def clan_info(clan_obj):
    field_dict_list = []

    field_dict_list.append({
        'name': "**Description**",
        'value': clan_obj.description,
        'inline': False
    })
    field_dict_list.append({
        'name': "**Members**",
        'value': len(clan_obj.members),
        'inline': True
    })
    field_dict_list.append({
        'name': "**Clan Lvl**",
        'value': clan_obj.clan_lvl,
        'inline': True
    })
    field_dict_list.append({
        'name': "**Clan War League**",
        'value': clan_obj.war_league_name,
        'inline': True
    })
    field_dict_list.append({
        'name': "**Total Points**",
        'value': clan_obj.clan_points,
        'inline': True
    })
    field_dict_list.append({
        'name': "**Link**",
        'value': (f"[{clan_obj.name}]"
                  f"(https://link.clashofclans.com/"
                  f"en?action=OpenClanProfile&tag="
                  f"{clan_obj.tag[1:]})"),
        'inline': True
    })

    return field_dict_list


def donation(clan_obj, donator_list, unit_name):
    if not donator_list:
        # unit is a hero
        return [{
            'name': f"{unit_name}",
            'value': "not a valid donatable unit"
        }]
    if len(donator_list) == 0:
        # nobody can donate unit
        return [{
            'name': f"{clan_obj.name}",
            'value': f"unable to donate {unit_name}"
        }]

    field_dict_list = []
    if ((donator_list[0].unit.lvl + clan_obj.donation_upgrade) >=
            donator_list[0].unit.max_lvl):
        # if donators can donate max
        value = (
            f"{donator_list[0].unit.name} "
            f"lvl {donator_list[0].unit.max_lvl}, "
            f"max"
        )
    else:
        value = (
            f"{donator_list[0].unit.name} "
            f"lvl {donator_list[0].unit.lvl + clan_obj.donation_upgrade} "
            f"max is {donator_list[0].unit.max_lvl}"
        )

    for donator in donator_list:
        field_dict_list.append({
            'name': f"{donator.player.name}",
            'value': value
        })

    return field_dict_list


def super_troop_search(clan_obj, donor_list, unit_name):
    if len(donor_list) == 0:
        return (f"Nobody in {clan_obj.name} "
                f"has {unit_name} activated.")

    message_string = ""
    for member in donor_list:
        message_string += f"{member.name}, "

    # cuts the last two characters from the string ', '
    message_string = message_string[:-2]
    if len(donor_list) == 1:
        message_string += f" has {unit_name} activated"
    else:
        message_string += f" have {unit_name} activated."

    return message_string


# WAR

# returns a string of the war overview
def war_overview(war_obj):
    if war_obj.state == "preparation":
        time_string = war_obj.string_date_time()

        return (
            f"{war_obj.clan.name} is preparing for war with "
            f"{war_obj.opponent.name} with {time_string} "
            f"left before war starts"
        )
    elif war_obj.state == "inWar":
        time_string = war_obj.string_date_time()
        scoreboard_string = war_obj.string_scoreboard()

        return (
            f"{war_obj.clan.name} is in war with {war_obj.opponent.name} "
            f"with {time_string} left in war, "
            f"{war_obj.clan.name} is {scoreboard_string}"
        )
    elif war_obj.state == "warEnded":
        scoreboard_string = war_obj.string_scoreboard()
        return (
            f"war against {war_obj.opponent.name} has ended, "
            f"{war_obj.clan.name} {scoreboard_string}"
        )
    else:
        return f"you are not in war"


def response_war_time(war_obj):
    if war_obj.state == "preparation":
        return f"{war_obj.clan.name} is preparing for war with {war_obj.string_date_time()} left before war starts"
    elif war_obj.state == "inWar":
        return f"{war_obj.clan.name} is in war with {war_obj.string_date_time()} left in war"
    elif war_obj.state == "warEnded":
        return f"The war with {war_obj.opponent.name} has ended"
    else:
        return "You are not in war"


# todo if nobody has attacked logic
# returns a string of the war no attack response
def response_war_no_attack(war_obj):
    if war_obj.state == "preparation":
        return (f"{war_obj.clan.name} is still preparing for war with "
                f"{war_obj.string_date_time()} before war starts, nobody has attacked")

    elif war_obj.state == "inWar":
        no_attack_list = war_obj.no_attack()
        if len(no_attack_list) == 0:
            return f"all {war_obj.team_size} {war_obj.clan.name} war members attacked"
        no_attack_string = ""
        for member in no_attack_list:
            no_attack_string += f"{member.name}, "
        # removes the last 2 characters ", " of the string
        no_attack_string = no_attack_string[:-2]
        # singular
        if len(no_attack_list) == 1:
            no_attack_string += " has not attacked"
        # plural
        else:
            no_attack_string += " have not attacked"
        no_attack_string += f" with {war_obj.string_date_time()} left in war"
        return no_attack_string

    elif war_obj.state == "warEnded":
        no_attack_list = war_obj.no_attack()
        if len(no_attack_list) == 0:
            return f"all {war_obj.team_size} {war_obj.clan.name} war members attacked"
        no_attack_string = ""
        for member in no_attack_list:
            no_attack_string += f"{member.name}, "
        # removes the last 2 characters ", " of the string
        no_attack_string = no_attack_string[:-2]
        no_attack_string += " did not attack"
        return no_attack_string

    else:
        return "you are not in war"


# returns a list of all war members and their stars
def war_members_overview(war_obj):
    "returns a list of all war members and their stars"
    response_list = []

    if war_obj.state == 'preparation':
        response_list.append(
            f'{war_obj.clan.name} is still preparaing for war, nobody has attacked')
    elif war_obj.state == 'inWar':
        response_list.append(
            f'{war_obj.clan.name} is in war with {war_obj.opponent.name} with {war_obj.string_date_time()} left in war, {war_obj.clan.name} is {war_obj.string_scoreboard()}.')
        response_list.append('____________________')
        for member in war_obj.clan.members:
            # no atk response
            if len(member.attacks) == 0:
                response_list.append(
                    f'{member.name} map pos {member.map_position} TH {member.th_lvl} has not attacked')
            else:
                response_list.append(
                    f'{member.name} map pos {member.map_position} TH {member.th_lvl} has attacked {len(member.attacks)} {member.string_member_attack_times()} for a total of {member.stars} {member.string_member_stars()}')
            response_list.append('__________')

        del response_list[-1]
    elif war_obj.state == 'warEnded':
        response_list.append(
            f'War against {war_obj.opponent.name} has ended. {war_obj.clan.name} {war_obj.string_scoreboard()}')
        response_list.append('____________________')
        for member in war_obj.clan.members:
            # no atk response
            if len(member.attacks) == 0:
                response_list.append(
                    f'{member.name} map pos {member.map_position} TH {member.th_lvl} did not attack')
            else:
                response_list.append(
                    f'{member.name} map pos {member.map_position} TH {member.th_lvl} attacked {len(member.attacks)} {member.string_member_attack_times()} for a total of {member.stars} {member.string_member_stars()}')
            response_list.append('__________')

        del response_list[-1]
    else:
        response_list.append('you are not in war')

    return response_list


# returns a list of war attack string responses for all war members
def war_all_attacks(war_obj):
    response_list = []

    if war_obj.state == 'preparation':
        response_list.append(
            f'{war_obj.clan.name} is still preparaing for war, nobody has attacked')
    elif war_obj.state == 'inWar':
        response_list.append(
            f'{war_obj.clan.name} is in war with {war_obj.opponent.name} with {war_obj.string_date_time()} left in war, {war_obj.clan.name} is {war_obj.string_scoreboard()}')
        response_list.append('____________________')
        for member in war_obj.clan.members:
            # no atk response
            if len(member.attacks) == 0:
                response_list.append(
                    f'{member.name} map pos {member.map_position} TH {member.th_lvl} has not attacked')
            else:
                response_list.append(
                    f'{member.name} map pos {member.map_position} TH {member.th_lvl} has attacked {len(member.attacks)} {member.string_member_attack_times()} for a total of {member.stars} {member.string_member_stars()}')
                for attack in member.attacks:
                    defender = war_obj.find_defender(attack.defender_tag)

                    if attack.stars == 0 or attack.stars == 3:
                        response_list.append(
                            f' - {attack.stars} {attack.string_attack_stars()} against {defender.name} map pos {defender.map_position} TH {defender.th_lvl}')
                    else:
                        response_list.append(
                            f' - {attack.stars} {attack.string_attack_stars()}, {round(attack.destruction_percent, 2)}% against {defender.name} map pos {defender.map_position} TH {defender.th_lvl}')

            response_list.append('__________')

        del response_list[-1]
    elif war_obj.state == 'warEnded':
        response_list.append(
            f'war against {war_obj.opponent.name} has ended, {war_obj.clan.name} {war_obj.string_scoreboard()}')
        response_list.append('____________________')
        for member in war_obj.clan.members:
            if len(member.attacks) == 0:
                response_list.append(
                    f'{member.name} map pos {member.map_position} TH {member.th_lvl} did not attack')
            else:

                response_list.append(
                    f'{member.name} map pos {member.map_position} TH {member.th_lvl} has attacked {len(member.attacks)} {member.string_member_attack_times()} for a total of {member.stars} {member.string_member_stars()}')
                for attack in member.attacks:
                    defender = war_obj.find_defender(attack.defender_tag)

                    if attack.stars == 0 or attack.stars == 3:
                        response_list.append(
                            f' - {attack.stars} {attack.string_attack_stars()} against {defender.name} map pos {defender.map_position} TH {defender.th_lvl}')
                    else:
                        response_list.append(
                            f' - {attack.stars} {attack.string_attack_stars()}, {round(attack.destruction_percent, 2)}% against {defender.name} map pos {defender.map_position} TH {defender.th_lvl}')

            response_list.append('__________')
        del response_list[-1]
    else:
        response_list.append('you are not in war')

    return response_list


def war_all_member_standing(war_obj):
    "returns a response list of member scores"
    return_list = []
    if war_obj.state == 'preparation':
        return_list.append({
            'name': 'war has not started',
            'value': 'there is no score'
        })
        return return_list
    elif war_obj.state == 'notInWar':
        return_list.append({
            'name': 'you are not in war',
            'value': 'there is no score'
        })
        return return_list
    else:
        war_members = sorted(
            war_obj.clan.members, key=lambda member: member.score, reverse=True)
        # razgriz has a score of
        for member in war_members:
            return_list.append({
                'name': member.name,
                'value': f'{round(member.score, 3)}'
            })
        return return_list


# CWL GROUP

def cwl_lineup(cwl_lineup):
    message = (
        "```\n"
        "CWL Group Lineup\n"
        "14 | 13 | 12 | 11 | 10 | 9  | 8\n"
        "-------------------------------\n"
    )
    for clan_dict in cwl_lineup:
        lineup_message = f"{clan_dict['clan'].name}\n"
        for key in clan_dict:
            if key != 'clan' and key > 6:
                if key >= 8:
                    lineup_message += f"{clan_dict[key]}"
                    # if it is a double digit number
                    if clan_dict[key] >= 10:
                        lineup_message += " | "
                    # if it is a single digit number add an extra space
                    else:
                        lineup_message += "  | "
        # removes the last 4 characters '  | ' of the string
        lineup_message = lineup_message[:-4]
        lineup_message += "\n\n"
        message += lineup_message
    message += "```"
    return message


# returns each member's CWL standing
def cwl_clan_standing(cwl_group, clan_tag, header):
    class ScoredMember(object):
        def __init__(self, tag, name, war_count, score):
            self.tag = tag
            self.name = name
            self.war_count = war_count
            self.score = score

    if not cwl_group:
        return ['you are not in CWL']

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
def cwl_member_standing(player_obj, cwl_group, clan_tag, header):
    if not cwl_group:
        return 'you are not in CWL'

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
        if member.tag == player_obj.tag:
            found = True
            break
    if not found:
        return 'Could not find {player.name} in the CWL group.'

    for war in cwl_wars:
        for war_member in war.clan.members:
            if war_member.tag == player_obj.tag:
                member_round_scores.append(war_member.score)
                break

    if len(member_round_scores) == 0:
        return_string = f'{player_obj.name} did not participate in any wars.'

    elif len(member_round_scores) == 1:
        return_string = f'{player_obj.name} was in 1 war and had a score of {round(member_round_scores[0], 3)} for that war.'

    else:
        total_score = 0
        for round_score in member_round_scores:
            total_score += round_score
        avg_score = total_score / len(member_round_scores)
        participation_multiplier = math.log(len(member_round_scores), 7)
        member_score = avg_score * participation_multiplier

        return_string = f"{player_obj.name} was in {len(member_round_scores)} wars with an overall score of {round(member_score, 3)}. {player_obj.name}'s scores are: "
        for cwl_round_score in member_round_scores:
            return_string += f'{round(cwl_round_score, 3)}, '
        # removes the last 2 characters ', ' of the string
        return_string = return_string[:-2]
        return_string += '.'

    return return_string


# CWL WAR


def cwl_war_overview(war_obj):
    '''returns a string of the current cwl war overview'''
    if war_obj.state == 'preparation':
        time_string = war_obj.string_date_time()
        return f'{war_obj.clan.name} is preparing for war with {war_obj.opponent.name} with {time_string} left before war starts'
    elif war_obj.state == 'inWar':
        time_string = war_obj.string_date_time()
        scoreboard_string = war_obj.string_scoreboard()
        return f'{war_obj.clan.name} is in war with {war_obj.opponent.name} with {time_string} left in war, {war_obj.clan.name} is {scoreboard_string}'
    elif war_obj.state == 'warEnded':
        scoreboard_string = war_obj.string_scoreboard()
        return f'war against {war_obj.opponent.name} has ended, {war_obj.clan.name} {scoreboard_string}'
    else:
        return 'you are not in CWL'


def cwl_war_time(war_obj):
    '''returns a string of the time remaining in war response'''
    if war_obj.state == 'preparation':
        time_string = war_obj.string_date_time()
        return f'{war_obj.clan.name} is preparing for war with {time_string} left before war starts'
    elif war_obj.state == 'inWar':
        time_string = war_obj.string_date_time()
        return f'{war_obj.clan.name} is preparing for war with {time_string} left in war'
    elif war_obj.state == 'warEnded':
        return f'the war with {war_obj.opponent.name} has ended'
    else:
        return 'you are not in CWL'


def cwl_war_no_attack(war_obj):
    '''returns a string of the cwl war no attack response'''
    if war_obj.state == 'preparation':
        return f'{war_obj.clan.name} is still preparing for war with {war_obj.string_date_time()} before war starts, nobody has attacked'

    elif war_obj.state == 'inWar':
        no_attack_list = war_obj.no_attack()
        if len(no_attack_list) == 0:
            return f'All {war_obj.team_size} {war_obj.clan.name} war members attacked'
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

    elif war_obj.state == 'warEnded':
        no_attack_list = war_obj.no_attack()
        if len(no_attack_list) == 0:
            return f'All {war_obj.team_size} {war_obj.clan.name} war members attacked'
        no_attack_string = ''
        for member in no_attack_list:
            no_attack_string += f'{member.name}, '
        # removes the last 2 characters ', ' of the string
        no_attack_string = no_attack_string[:-2]
        no_attack_string += ' did not attack'
        return no_attack_string

    else:
        return 'you are not in CWL'


# returns a list of cwl war attack string responses for all war members
def cwl_war_all_attacks(war_obj):
    response_list = []
    if war_obj.state == 'preparation':
        response_list.append(
            f'{war_obj.clan.name} is still preparaing for war, nobody has attacked')
    elif war_obj.state == 'inWar':
        response_list.append(
            f'{war_obj.clan.name} is in war with {war_obj.opponent.name} with {war_obj.string_date_time()} left in war, {war_obj.clan.name} is {war_obj.string_scoreboard()}')
        response_list.append('____________________')
        for member in war_obj.clan.members:
            if len(member.attacks) == 0:
                response_list.append(
                    f'{member.name} map pos {member.map_position} TH {member.th_lvl} has not attacked')
            else:

                response_list.append(
                    f'{member.name} map pos {member.map_position} TH {member.th_lvl} has attacked {len(member.attacks)} {member.string_member_attack_times()} for a total of {member.stars} {member.string_member_stars()}')
                for attack in member.attacks:
                    defender = war_obj.find_defender(attack.defender_tag)

                    if attack.stars == 0 or attack.stars == 3:
                        response_list.append(
                            f' - {attack.stars} {attack.string_attack_stars()} against {defender.name} map pos {defender.map_position} TH {defender.th_lvl}')
                    else:
                        response_list.append(
                            f' - {attack.stars} {attack.string_attack_stars()}, {round(attack.destruction_percent, 2)}% against {defender.name} map pos {defender.map_position} TH {defender.th_lvl}')

            response_list.append('__________')
        del response_list[-1]
    elif war_obj.stat == 'warEnded':
        response_list.append(
            f'war against {war_obj.opponent.name} has ended, {war_obj.clan.name} {war_obj.string_scoreboard()}')
        response_list.append('____________________')
        for member in war_obj.clan.members:
            if len(member.attacks) == 0:
                response_list.append(
                    f'{member.name} map pos {member.map_position} TH {member.th_lvl} did not attack')
            else:

                response_list.append(
                    f'{member.name} map pos {member.map_position} TH {member.th_lvl} has attacked {len(member.attacks)} {member.string_member_attack_times()} for a total of {member.stars} {member.string_member_stars()}')
                for attack in member.attacks:
                    defender = war_obj.find_defender(attack.defender_tag)

                    if attack.stars == 0 or attack.stars == 3:
                        response_list.append(
                            f' - {attack.stars} {attack.string_attack_stars()} against {defender.name} map pos {defender.map_position} TH {defender.th}')
                    else:
                        response_list.append(
                            f' - {attack.stars} {attack.string_attack_stars()}, {round(attack.destruction_percent, 2)}% against {defender.name} map pos {defender.map_position} TH {defender.th}')

            response_list.append('__________')
        del response_list[-1]
    else:
        response_list.append('you are not in CWL')
    return response_list


def embed_message(
    Embed,
    color,
    icon_url,
    title,
    bot_prefix,
    bot_user_name,
    thumbnail,
    field_list,
    image_url,
    author_display_name,
    author_avatar_url
):
    embed_list = []
    embed = Embed(
        colour=color,
        title=title
    )

    embed.set_author(
        icon_url=icon_url,
        name=f"[{bot_prefix}] {bot_user_name}"
    )
    if thumbnail:
        embed.set_thumbnail(
            url=thumbnail['medium'])
    else:
        embed.set_thumbnail(
            url=("https://api-assets.clashofclans.com/leagues/72/e--"
                 "YMyIexEQQhE4imLoJcwhYn6Uy8KqlgyY3_kFV6t4.png"))

    if image_url:
        embed.set_image(
            url=image_url)

    for field in field_list:
        if field_list.index(field) > 25:
            # discord will not accept more than 25 fields
            del field_list[:25]
            embed_list.append(
                embed_message(
                    Embed=Embed,
                    color=color,
                    icon_url=icon_url,
                    title=title,
                    bot_prefix=bot_prefix,
                    bot_user_name=bot_user_name,
                    thumbnail=thumbnail,
                    field_list=field_list,
                    image_url=image_url,
                    author_display_name=author_display_name,
                    author_avatar_url=author_avatar_url
                )[0])
        if 'inline' in field:
            embed.add_field(
                name=field['name'],
                value=field['value'],
                inline=field['inline']
            )
        else:
            embed.add_field(
                name=field['name'],
                value=field['value']
            )

    embed.set_footer(
        text=author_display_name,
        icon_url=author_avatar_url
    )

    embed_list.append(embed)

    embed_list.reverse()

    return embed_list


# DISCORD


def role_add_remove_list(needed_role_list, current_role_list):
    """
        Takes in list of needed and current role id's and
        returns add and remove lists of discord role id's

        Args:
            list
                needed_role_list (int): list of needed discord's role id
            list
                needed_role_list (int): list of current discord's role id

        Returns:
            add_roles_list: list of role id's to add to discord user
            remove_roles_list: list of role id's to remove from discord user
    """

    # add_list
    add_list = []
    for needed_role in needed_role_list:
        if needed_role not in current_role_list:
            # needed and not currently set
            # add to add list
            add_list.append(needed_role)

    # remove_list
    remove_list = []
    for current_role in current_role_list:
        if current_role not in needed_role_list:
            # currently set and not needed
            # add to remove list
            remove_list.append(current_role)

    return add_list, remove_list


def role_switch(player, user_roles, client_clans):
    """
        takes in player role and list of discord user roles,
        returns new and old role
    """

    add_roles = []
    remove_roles = []

    if player is None:

        has_community = False
        # remove all listed roles (clan, member, and uninitiated)
        # give community role
        for role in user_roles:
            # checking for clan roles
            for clan in client_clans:
                if role.name == clan.name:
                    remove_roles.append(role.name)

            # checking for member roles
            if role.name == 'leader':
                remove_roles.append('leader')
            if role.name == 'co-leader':
                remove_roles.append('co-leader')
            if role.name == 'elder':
                remove_roles.append('elder')
            if role.name == 'member':
                remove_roles.append('member')
            if role.name == 'uninitiated':
                remove_roles.append('uninitiated')
            if role.name == 'community':
                has_community = True

        # add community role if community is not False
        if not has_community:
            add_roles.append('community')

        return add_roles, remove_roles

    # checking if the user's clan roles need changing
    old_clan = None
    for role in user_roles:
        for clan in client_clans:
            if role.name == clan.name:
                old_clan = role.name
                break
    new_clan = player.clan_name

    # add the roles to the lists if the clans are not the same
    if old_clan != new_clan:
        # if there is an old clan role then add it to the list
        if old_clan:
            remove_roles.append(old_clan)
        add_roles.append(new_clan)

    # checking if the user's member roles need changing
    new_role = None
    if player.role == 'leader':
        new_role = 'leader'
    elif player.role == 'coLeader':
        new_role = 'co-leader'
    elif player.role == 'admin':
        new_role = 'elder'
    elif player.role == 'member':
        new_role = 'member'
    else:
        new_role = 'uninitiated'

    old_role = None
    for role in user_roles:
        if role.name == 'leader':
            old_role = 'leader'
        if role.name == 'co-leader':
            old_role = 'co-leader'
        if role.name == 'elder':
            old_role = 'elder'
        if role.name == 'member':
            old_role = 'member'
        if role.name == 'uninitiated':
            old_role = 'uninitiated'
        if role.name == 'community':
            remove_roles.append(role.name)

    # add the roles to the lists if the member roles are not the same
    if old_role != new_role:
        # if there is an old clan member role then add it to the list
        if old_role:
            remove_roles.append(old_role)
        add_roles.append(new_role)

    return add_roles, remove_roles


def active_super_troop_role_switch(player, user_roles, active_super_troops):
    """
        takes in list of discord user roles and active super troops,
        returns new and old roles for active super troops
    """

    add_roles = []
    remove_roles = []

    # checking if the user's active super troop roles need changing
    old_super_troop_roles = []
    for role in user_roles:
        for super_troop in super_troop_list:
            if role.name == super_troop:
                old_super_troop_roles.append(role)

    for super_troop in active_super_troops:
        add_roles.append(super_troop.name)

    for old_role in old_super_troop_roles:
        remove_roles.append(old_role.name)

    return add_roles, remove_roles


# todo needs testing
# ? may not need
def client_roles_check(client_roles, user_roles):
    """
        Checks if a user has any of the client_roles and returns True or False
    """
    for value in client_roles:
        if value.is_clash_role:
            for role in user_roles:
                if role.name == value.name:
                    return True
    return False


def role_check(client_role, user_roles):
    """
        Returns True if user has requested role, False if not
    """
    for role in user_roles:
        if role.name == client_role:
            return True
    return False


def nickname_available(nickname, user_list):
    """
        returns a bool
        checks if anyone in the guild has the given display_name
    """
    for user in user_list:
        if nickname == user.display_name:
            return False
    return True


# todo change ctx to channel_list
def channel_changer(ctx, send_id):
    for channel in ctx.guild.channels:
        if channel.id == send_id:
            return channel
    return ctx.channel


def find_user_clan(player_name, client_clans, user_roles, header):
    """
        Returns a client clan if one is found
    """
    for client_clan in client_clans:
        for role in user_roles:

            # if the clan is found
            if client_clan.name == role.name:
                clan = Clan.get(client_clan.tag, header)

                # search the clan members for the given player
                player_tag = clan.find_member(player_name)
                if player_tag:
                    return client_clan
    return None


def player_name_string(display_name):
    if '|' in display_name:
        display_name_chars = ''
        for char in display_name:
            if char == '|':
                break
            else:
                display_name_chars += char
        display_name = display_name_chars
        if display_name[-1] == ' ':
            display_name = display_name[:-1]
    return display_name


def find_channel_member(user_name, channel_members):
    """
        Takes in a user's name and returns the discord member object.
    """
    for member in channel_members:
        if user_name == player_name_string(member.display_name):
            return member
    return ''
