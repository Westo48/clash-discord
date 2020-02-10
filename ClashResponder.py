from ClashFrame import *
from ClashResponderReferences import *

raz_tag = '#RGQ8RGU9'
heroes_tag = '#JJRJGVR0'
header = {
    'Accept': 'application/json',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjkyNWJjYzg1LWFhZDktNGM2NC05M2Y2LWM4MWEwZGVhOGUwNiIsImlhdCI6MTU3NDYyMjY3Nywic3ViIjoiZGV2ZWxvcGVyLzdjZmJkOWFjLTFlYzAtNDI3OS1jODM2LTU0YzMxN2FlZmE4NiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjEwOC4yMTEuOTUuMjU0Il0sInR5cGUiOiJjbGllbnQifV19.gdc-4-OEZzsYBLk8HfqZBH-idvlK1vX9nim91XEqLgwNAyarfZquxfkZDKPsswUGyiXRIFV7Am3RB7iWtd9T5w'
}


# todo make checks so that if someone types something in wrong it will at least not error out

# War

def war_response():
    war_object = war_overview(heroes_tag, header)

    if war_object.state == 'preparation':
        days, hours, minutes, seconds = date_time_calculator(war_object.start_time)
        return f'You are preparing for war with {war_object.opponent_name} with {date_time_string(days, hours, minutes, seconds)} left before war starts.'

    elif war_object.state == 'inWar':
        days, hours, minutes, seconds = date_time_calculator(war_object.end_time)
        return f'You are in war with {war_object.opponent_name} with {date_time_string(days, hours, minutes, seconds)} left in war. You are {scoreboard_string(war_object)}.'

    elif war_object.state == 'warEnded':
        return f'War against {war_object.opponent_name} has ended. You {scoreboard_string(war_object)}.'

    else:
        return 'You are not in war.'


def no_attack_response():
    no_attack_string = ''
    no_attack_list = []
    war_object = war_overview(heroes_tag, header)
    if war_object.state == 'preparation':
        return 'You are still preparing for war, nobody has attacked.'
    elif war_object.state == 'inWar':
        for member in war_object.clan_members:
            if len(member.attacks) == 0:
                no_attack_list.append(member)
        if len(no_attack_list) == 0:
            no_attack_string = f'All {war_object.team_size} war members have attacked.'
        else:
            days, hours, minutes, seconds = date_time_calculator(war_object.end_time)
            no_attack_string = f'You have {date_time_string(days, hours, minutes, seconds)} left in war. '
            for member in no_attack_list:
                no_attack_string += f'{member.name}, '
            # removes the last 2 characters (comma and space) of the string
            no_attack_string = no_attack_string[:-2]
            no_attack_string += ' has not attacked.'
    elif war_object.state == 'warEnded':
        for member in war_object.clan_members:
            if len(member.attacks) == 0:
                no_attack_list.append(member)
        if len(no_attack_list) == 0:
            no_attack_string = f'All {war_object.team_size} war members attacked.'
        else:
            for member in no_attack_list:
                no_attack_string += f'{member.name}, '
            # removes the last character (comma) of the string
            no_attack_string = no_attack_string[:-2]
            no_attack_string += ' did not attack.'
    else:
        no_attack_string = 'You are not in war.'

    return no_attack_string


def all_attacks_response():
    war_object = war_overview(heroes_tag, header)
    if war_object.state == 'preparation':
        return 'You are still preparing for war, nobody has attacked.'
    elif war_object.state == 'notInWar':
        return 'You are not in war.'
    else:
        return get_all_attacks(war_object)


# CWL

def cwl_war_response():
    cwl_group_object = cwl_group(heroes_tag, header)
    if cwl_group_object.state == 'warEnded':
        return 'Clan Wars have ended.'

    cwl_war_object = find_cwl_war(cwl_group_object, heroes_tag)

    if cwl_war_object.state == 'preparation':
        days, hours, minutes, seconds = date_time_calculator(cwl_war_object.start_time)
        return f'You are preparing for war with {cwl_war_object.opponent_name} with {date_time_string(days, hours, minutes, seconds)} left before war starts.'

    elif cwl_war_object.state == 'inWar':
        days, hours, minutes, seconds = date_time_calculator(cwl_war_object.end_time)
        return f'You are in war with {cwl_war_object.opponent_name} with {date_time_string(days, hours, minutes, seconds)} left in war. You are {scoreboard_string(cwl_war_object)}.'

    else:
        return 'You are not in war.'


def cwl_no_attack_response():
    cwl_group_object = cwl_group(heroes_tag, header)
    if cwl_group_object.state == 'warEnded':
        return 'Clan Wars have ended.'
    elif cwl_group_object.state == 'notInWar':
        return 'You are not in war.'

    no_attack_string = ''
    no_attack_list = []
    cwl_war_object = find_cwl_war(cwl_group_object, heroes_tag)
    if cwl_war_object.state == 'preparation':
        return 'You are still preparing for war, nobody has attacked.'
    elif cwl_war_object.state == 'inWar':
        for member in cwl_war_object.clan_members:
            if len(member.attacks) == 0 and member.map_position <= 15:
                no_attack_list.append(member)
        if len(no_attack_list) == 0:
            no_attack_string = f'All {cwl_war_object.team_size} war members have attacked.'
        else:
            days, hours, minutes, seconds = date_time_calculator(cwl_war_object.end_time)
            no_attack_string = f'You have {date_time_string(days, hours, minutes, seconds)} left in war. '
            for member in no_attack_list:
                no_attack_string += f'{member.name}, '
            # removes the last 2 characters (comma and space) of the string
            no_attack_string = no_attack_string[:-2]
            no_attack_string += ' have not attacked.'
    else:
        no_attack_string = 'You are not in war.'

    return no_attack_string


def cwl_all_attacks_response():
    cwl_group_object = cwl_group(heroes_tag, header)
    if cwl_group_object.state == 'warEnded':
        return 'Clan Wars have ended.'
    elif cwl_group_object.state == 'notInWar':
        return 'You are not in war.'

    cwl_war_object = find_cwl_war(cwl_group_object, heroes_tag)
    if cwl_war_object.state == 'preparation':
        return 'You are still preparing for war, nobody has attacked.'
    else:
        return get_all_cwl_attacks(cwl_war_object)


# takes in CWLGroup class object and returns War class object
def find_cwl_war(cwl_group_object, clan_tag):
    for cwl_round in cwl_group_object.rounds:
        if not cwl_round[0] == '#0':
            # checking if the specified round is inWar or in preparation
            cwl_war_json = json_response(cwl_round[0], 'cwlWar', header)
            if cwl_war_json['state'] == 'inWar' or cwl_war_json['state'] == 'preparation':
                # check each war in the current round for clan_tag in 'clan' or 'opponent'
                for cwl_war in cwl_round:
                    current_cwl_war = cwl_war_overview(clan_tag, cwl_war, header)
                    # todo shouldn't need opponent tag checked since the war_overview changes the clan tag to the actual clan
                    if current_cwl_war.clan_tag == clan_tag or current_cwl_war.opponent_tag == clan_tag:
                        return current_cwl_war
    # todo set return up if nothing is found just in case
    for cwl_war in cwl_group_object.rounds[-1]:
        if not cwl_war[0] == '#0':
            current_cwl_war = cwl_war_overview(clan_tag, cwl_war, header)
            # todo shouldn't need opponent tag checked since the war_overview changes the clan tag to the actual clan
            if current_cwl_war.clan_tag == clan_tag or current_cwl_war.opponent_tag == clan_tag:
                return current_cwl_war


# Player

def troop_level_response(player_name, troop_name):
    player_name = re.sub('[-]', ' ', player_name)
    player_tag = find_member(clan(heroes_tag, header), player_name)
    player_object = player(player_tag, header)
    troop_object = find_troop(player_object, troop_name)
    if troop_object.lvl == troop_object.max_lvl:
        return f'{player_object.player_name} has lvl {troop_object.lvl} {troop_object.name}, which is max.'
    else:
        return f'{player_object.player_name} has lvl {troop_object.lvl} {troop_object.name}, max is lvl {troop_object.max_lvl}'


def all_troop_level_response(player_name):
    player_name = re.sub('[-]', ' ', player_name)
    player_tag = find_member(clan(heroes_tag, header), player_name)
    player_object = player(player_tag, header)
    troop_response = [f'{player_object.player_name} troop levels:', '---------------------']
    for troop in player_object.troops:
        if troop.village == 'home':
            if troop.lvl == troop.max_lvl:
                troop_response.append(f'{troop.name} is max which is level {troop.lvl}.')
            else:
                troop_response.append(f'{troop.name} is level {troop.lvl}, max is level {troop.max_lvl}.')
            troop_response.append(f'---------------------')
    for hero in player_object.heroes:
        if hero.village == 'home':
            if hero.lvl == hero.max_lvl:
                troop_response.append(f'{hero.name} is max which is level {hero.lvl}.')
            else:
                troop_response.append(f'{hero.name} is level {hero.lvl}, max is level {hero.max_lvl}.')
            troop_response.append(f'---------------------')
    for spell in player_object.spells:
        if spell.village == 'home':
            if spell.lvl == spell.max_lvl:
                troop_response.append(f'{spell.name} is max which is level {spell.lvl}.')
            else:
                troop_response.append(f'{spell.name} is level {spell.lvl}, max is level {spell.max_lvl}.')
            troop_response.append(f'---------------------')
    # possibly remove trailing '--------------------'
    return troop_response


def member_role_response(player_name):
    player_name = re.sub('[-]', ' ', player_name)
    player_tag = find_member(clan(heroes_tag, header), player_name)
    player_object = player(player_tag, header)
    return player_object.role


def donation_response(player_name, troop_name):
    player_name = re.sub('[-]', ' ', player_name)
    clan_object = clan(heroes_tag, header)
    player_tag = find_member(clan_object, player_name)
    player_object = player(player_tag, header)
    troop_object = find_troop(player_object, troop_name)
    if troop_object.max_lvl <= (troop_object.lvl + 2):
        return f'{player_object.player_name} can donate max {troop_object.name} which is level {troop_object.max_lvl}'
    else:
        donor_member_list = []
        donor_troop_list = []
        donor_list = []
        donor_string = ''
        for i in range(0, 10):
            member_object = player(clan_object.members[i].tag, header)
            member_troop_object = find_troop(member_object, troop_object.name)
            donor_member_list.append(member_object)
            donor_troop_list.append(member_troop_object)
        troop_max = max(troop.lvl for troop in donor_troop_list)
        for member in donor_member_list:
            if find_troop(member, troop_object.name).lvl == troop_max:
                donor_list.append(member)
        if len(donor_list) == 1:
            if troop_object.max_lvl <= (troop_max + 2):
                return f'{donor_list[0].player_name} can donate max {troop_object.name} which is level {troop_object.max_lvl}.'
            else:
                return f'{donor_list[0].player_name} can donate level {troop_max + 2} {troop_object.name}, max is level {troop_object.max_lvl}.'
        for donor in donor_list:
            donor_string +=f'{donor.player_name}, '
        donor_string = donor_string[:-2]
        if troop_object.max_lvl <= (troop_max + 2):
            return f'{donor_string} are able to donate max {troop_object.name} which is level {troop_object.max_lvl}.'
        else:
            return f'{donor_string} are able to donate level {troop_max + 2} {troop_object.name}, max is level {troop_object.max_lvl}.'


# ? may or may not use this due to file being needed
def war_weight(THlvl, amount):
    # ! change this to Weston user for importing to desktop comp
    with open(r'C:\Users\Weston\PycharmProjects\ClashDiscord\Troop_Data.json') as troop_file:
        troop_data = json.load(troop_file)

    storage_num = int(troop_data['th'][f'{THlvl}']['storage'][0]['thMax'])
    weight = (storage_num + 1) * int(amount)
    return weight


# all_war_members_response
