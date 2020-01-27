import requests
from datetime import datetime, timedelta
import json
import re
import os


class WarMember:
    def __init__(self, map_pos, th, name, tag, has_attacked, attacks, stars, attack1_tag, attack1_stars,
                 attack1_destruction, attack2_tag, attack2_stars, attack2_destruction):
        self.map_pos = map_pos
        self.th = th
        self.name = name
        self.tag = tag
        self.has_attacked = has_attacked
        self.attacks = attacks
        self.stars = stars
        self.attack1_tag = attack1_tag
        self.attack1_stars = attack1_stars
        self.attack1_destruction = attack1_destruction
        self.attack2_tag = attack2_tag
        self.attack2_stars = attack2_stars
        self.attack2_destruction = attack2_destruction

    def get(self, param):
        pass


class PlayerTroop:
    def __init__(self, player_tag, player_name, troop_name, troop_display_name, player_troop_lvl, player_th, max_for_th, max_for_troop):
        self.player_tag = player_tag
        self.player_name = player_name
        self.troop_name = troop_name
        self.troop_display_name = troop_display_name
        self.player_troop_lvl = player_troop_lvl
        self.player_th = player_th
        self.max_for_th = max_for_th
        self.max_for_troop = max_for_troop

    def get(self, param):
        pass


RazgrizTag = 'RGQ8RGU9'
TheMightyHeroesTag = 'JJRJGVR0'
fullClanTag = '#JJRJGVR0'
header = {
    'Accept': 'application/json',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjkyNWJjYzg1LWFhZDktNGM2NC05M2Y2LWM4MWEwZGVhOGUwNiIsImlhdCI6MTU3NDYyMjY3Nywic3ViIjoiZGV2ZWxvcGVyLzdjZmJkOWFjLTFlYzAtNDI3OS1jODM2LTU0YzMxN2FlZmE4NiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjEwOC4yMTEuOTUuMjU0Il0sInR5cGUiOiJjbGllbnQifV19.gdc-4-OEZzsYBLk8HfqZBH-idvlK1vX9nim91XEqLgwNAyarfZquxfkZDKPsswUGyiXRIFV7Am3RB7iWtd9T5w'
}


# Clan War League calls

# todo make this an overview of the entire cwl, not just the current war
# ! cwl_overview is not quite finished
def cwl_overview(clan_tag):
    cwl_group_json = json_response(clan_tag, 'cwlGroup')
    cwl_state = cwl_group_json['state']
    clan_stars = 0
    ended_rounds = 0
    clan_wins = 0
    clan_losses = 0
    clan_ties = 0
    round_list = get_cwl_rounds(cwl_group_json)
    for cwl_round in round_list:
        if not cwl_round[0] == '#0':
            # checking if the specified round is not in preparation
            cwl_war_json = json_response(cwl_round[0][1:], 'cwlWar')
            if not cwl_war_json['state'] == 'preparation':
                # check each war in the current round for TheMightyHeroes in 'clan' or 'opponent'
                for cwl_war in cwl_round:
                    curr_war_json = json_response(cwl_war[1:], 'cwlWar')
                    # if this is the war that TheMightyHeroes are in or were in...
                    if curr_war_json['clan']['tag'] == fullClanTag or curr_war_json['opponent']['tag'] == fullClanTag:
                        # sets the clan and opponent accordingly (clan or opp status = 'clan' or 'opponent')
                        clan_status, opp_status = clan_opp_status(curr_war_json)
                        clan_stars += curr_war_json[clan_status]['stars']
                        # showing how many rounds have ended
                        # keeping score for win/lose/tie only run this if clan is not currently in war (do not add current war to win/lose/tie)
                        if not curr_war_json['state'] == 'inWar':
                            ended_rounds += 1
                            win_lose_tie = calculate_win_lose(curr_war_json, clan_status, opp_status)
                            if win_lose_tie == 'won!':
                                clan_wins += 1
                            elif win_lose_tie == 'lost.':
                                clan_losses += 1
                            else:
                                clan_ties += 1

    return f'Out of {ended_rounds} rounds you have won {clan_wins}, lost {clan_losses}, and tied {clan_ties} rounds. TheMightyHeroes have earned {clan_stars} stars.'


def cwl_war_time(clan_tag):
    cwl_group_json = json_response(clan_tag, 'cwlGroup')
    cwl_war_tag = get_curr_cwl_war(cwl_group_json)
    cwl_war_json = json_response(cwl_war_tag[1:], 'cwlWar')
    return war_time(cwl_war_json)


def cwl_curr_war_overview(clan_tag):
    # this returns the tag for getting json info
    cwl_war_tag = get_curr_cwl_war(clan_tag)
    cwl_war_json = json_response(cwl_war_tag[1:], 'cwlWar')
    clan_status, opp_status = clan_opp_status(cwl_war_json)

    return war_overview(cwl_war_json)


# war calls

def curr_war_time(clan_tag):
    curr_war_json = json_response(clan_tag, 'currentwar')
    return war_time(curr_war_json)


def curr_war_overview(clan_tag):
    war_json = json_response(clan_tag, 'currentwar')

    return war_overview(war_json)


def curr_no_atk(clan_tag):
    war_json = json_response(clan_tag, 'currentwar')
    return no_atk(war_json)


def curr_long_war_overview(clan_tag):
    war_json = json_response(clan_tag, 'currentwar')
    long_war_overview(war_json)


def all_attack_stars(clan_tag):
    war_json = json_response(clan_tag, 'currentwar')

    if check_war_state(war_json) == 'preparation':
        war_start_time = time_string_changer(war_json['startTime'])
        return f'{date_time_calculator(war_start_time)} until the war starts.'

    elif check_war_state(war_json) == 'inWar':
        clan_status, opp_status = clan_opp_status(war_json)
        return_line = []

        # gets war member data
        sorted_war_members = get_war_member_info(war_json, clan_status)

        return_line.append(f'{war_overview(war_json)}')

        for obj in sorted_war_members:

            if obj.has_attacked:
                if obj.attacks > 1:
                    attacks_text = 'attacks'
                else:
                    attacks_text = 'attack'

                if obj.stars == 1:
                    star_text = 'star'

                else:
                    star_text = 'stars'

                return_line.append(
                    f'{obj.name} is a th {obj.th} position {obj.map_pos} and has made {obj.attacks} {attacks_text} for {obj.stars} {star_text}')

            else:
                return_line.append(f'{obj.name} is a th {obj.th} position {obj.map_pos} has NOT made an attack')

            return_line.append(f'---------')

        del return_line[-1]
        return return_line

    elif check_war_state(war_json) == 'warEnded':
        clan_status, opp_status = clan_opp_status(war_json)
        return_line = []

        # gets war member data
        sorted_war_members = get_war_member_info(war_json, clan_status)

        return_line.append(f'{war_overview(war_json)}')
        for obj in sorted_war_members:

            if obj.has_attacked:
                if obj.attacks > 1:
                    attacks_text = 'attacks'
                else:
                    attacks_text = 'attack'

                if obj.stars == 1:
                    star_text = 'star'

                else:
                    star_text = 'stars'

                return_line.append(
                    f'{obj.name} is a th {obj.th} position {obj.map_pos} and made {obj.attacks} {attacks_text} for {obj.stars} {star_text}')

            else:
                return_line.append(f'{obj.name} is a th {obj.th} position {obj.map_pos} and did NOT made an attack')

            return_line.append(f'---------')

        del return_line[-1]
        return return_line

    elif check_war_state(war_json) == 'notInWar':

        return f'Currently searching for war'

    else:
        return 'Well... something went wrong'


def all_attacks(clan_tag):
    war_json = json_response(clan_tag, 'currentwar')

    if check_war_state(war_json) == 'preparation':
        war_start_time = time_string_changer(war_json['startTime'])
        return f'{date_time_calculator(war_start_time)} until the war starts.'

    elif check_war_state(war_json) == 'inWar':
        clan_status, opp_status = clan_opp_status(war_json)
        return_line = []

        # gets war member data
        sorted_war_members = get_war_member_info(war_json, clan_status)

        return_line.append(f'{war_overview(war_json)}')

        for obj in sorted_war_members:

            if obj.has_attacked:
                if obj.attacks > 1:
                    attacks_text = 'attacks'
                else:
                    attacks_text = 'attack'

                if obj.stars == 1:
                    star_text = 'star'

                else:
                    star_text = 'stars'

                return_line.append(
                    f'{obj.name} is a th {obj.th} position {obj.map_pos} and has made {obj.attacks} {attacks_text} for {obj.stars} {star_text}')

                for i in range(obj.attacks):
                    return_line.append(get_each_attack(i, war_json, obj))

            else:
                return_line.append(f'{obj.name} is a th {obj.th} position {obj.map_pos} has NOT made an attack')

            return_line.append(f'---------')

        return return_line

    elif check_war_state(war_json) == 'warEnded':
        return_line = []

        # gets war member data
        clan_status, opp_status = clan_opp_status(war_json)
        sorted_war_members = get_war_member_info(war_json, clan_status)

        return_line.append(f'{war_overview(war_json)}')
        for obj in sorted_war_members:

            if obj.has_attacked:
                if obj.attacks > 1:
                    attacks_text = 'attacks'
                else:
                    attacks_text = 'attack'

                if obj.stars == 1:
                    star_text = 'star'

                else:
                    star_text = 'stars'

                return_line.append(
                    f'{obj.name} is a th {obj.th} position {obj.map_pos} and made {obj.attacks} {attacks_text} for {obj.stars} {star_text}')

                for i in range(obj.attacks):
                    return_line.append(get_each_attack(i, war_json, obj))

            else:
                return_line.append(f'{obj.name} is a th {obj.th} position {obj.map_pos} and did NOT made an attack')

            return_line.append(f'---------')

        return return_line

    elif check_war_state(war_json) == 'notInWar':

        return f'Currently searching for war'

    else:
        return 'Well... something went wrong'


# player calls

# todo change this to return values that can be used by donation_checker
def user_troop_levels(player_name, troop_name):
    player = get_user_troop_level(player_name, troop_name)

    return f'{player.player_name}\'s {player.troop_display_name} is lvl {player.player_troop_lvl}, max for TH {player.player_th} is {player.max_for_th}'


def donation_checker(player_name, troop_name):
    player = get_user_troop_level(player_name, troop_name)
    # if they can donate the max for that specific troop then send it through that they can donate the max
    if player.max_for_troop <= (player.player_troop_lvl + 2):
        return f'{player.player_name} can donate max {player.troop_name} which is lvl {player.max_for_troop}'

    clan_members_json = json_response(TheMightyHeroesTag, 'members')
    member_name_list = []
    player_troop_list = []
    donor_list = []
    donor_string = ''
    for i in range(0, 10):
        member_name = clan_members_json['items'][i]['name']
        member_name_list.append(member_name)
    # filling the player troop list with the PlayerTroop objects
    for member in member_name_list:
        player_troop_list.append(get_user_troop_level(member, troop_name))

    troop_max = max(member.player_troop_lvl for member in player_troop_list)
    # set each member that can donate into the donor_list
    for member in player_troop_list:
        if member.player_troop_lvl >= troop_max:
            donor_list.append(member)

    if len(donor_list) == 1:
        if player.max_for_troop <= (troop_max + 2):
            return f'{donor_list[0].player_name} can donate max {donor_list[0].troop_display_name} which is level {min(troop_max + 2, player.max_for_troop)} '
        return f'{donor_list[0].player_name} can donate level {min(troop_max + 2, player.max_for_troop)} {donor_list[0].troop_display_name}'

    for donor in donor_list:
        donor_string += f'{donor.player_name}, '

    donor_string = donor_string[:-2]
    if player.max_for_troop <= (troop_max + 2):
        return f'{donor_string} are able to donate max {player.troop_display_name} which is level {min(troop_max + 2, player.max_for_troop)}'

    return f'{donor_string} are able to donate level {min(troop_max + 2, player.max_for_troop)} {player.troop_display_name}'


def war_weight(THlvl, amount):
    # ! change this to Weston user for importing to desktop comp
    with open(r'C:\Users\westo\Documents\My Documents\Software Development\Python\ClashDiscord\Troop_Data.json') as troop_file:
        troop_data = json.load(troop_file)
    
    storage_num = int(troop_data['th'][f'{THlvl}']['storage'][0]['thMax'])
    weight = (storage_num + 1) * int(amount)
    return weight


# show every given troop, the max for their TH, and the absolute max
# maybe not absolute max
def all_user_levels(player_name):
    with open(r'C:\Users\Weston\PycharmProjects\ClashDiscord\Troop_Data.json') as troop_file:
        troop_json = json.load(troop_file)

    player_name = re.sub('[-]', ' ', player_name)
    members_json = json_response(TheMightyHeroesTag, 'members')
    player_tag = ''

    return_line = []

    # getting the player tag in the list of members in the clan
    for mem in members_json['items']:
        if mem['name'].lower() == player_name.lower():
            player_name = mem['name']
            player_tag = mem['tag']

    if player_tag == '':
        return 'something went wrong with the player tag'

    player_tag = player_tag[1:]
    player_json = json_response(player_tag, 'players')
    player_th = player_json['townHallLevel']

    return_line.append(f'{player_name} is a TH {player_th}')
    return_line.append('---------')

    for player_hero in player_json['heroes']:
        if player_hero['village'] == 'home':
            hero_th_max = 'error, breakpoint: hero_th_max'
            hero_name = player_hero['name']
            hero_lvl = player_hero['level']
            for troop_hero in troop_json['th'][f'{player_th}']['hero']:
                if troop_hero['name'] == player_hero['name']:
                    hero_th_max = troop_hero['thMax']
            hero_max = player_hero['maxLevel']
            return_line.append(
                f'{player_name}\'s {hero_name} is lvl {hero_lvl}, max for TH {player_th} is lvl {hero_th_max}.')
            return_line.append('---------')

    for player_troop in player_json['troops']:
        if player_troop['village'] == 'home':
            troop_th_max = 'error, breakpoint: troop_th_max'
            troop_name = player_troop['name']
            formatted_troop_name = re.sub('[.]', '', troop_name)
            troop_lvl = player_troop['level']
            for troop_troop in troop_json['th'][f'{player_th}']['troop']:
                if troop_troop['name'].lower() == formatted_troop_name.lower():
                    troop_th_max = troop_troop['thMax']
            troop_max = player_troop['maxLevel']
            return_line.append(
                f'{player_name}\'s {troop_name} is lvl {troop_lvl}, max for TH {player_th} is lvl {troop_th_max}.')
            return_line.append('---------')

    for player_spell in player_json['spells']:
        spell_name = re.sub(' Spell', '', player_spell['name'])
        spell_th_max = 'error, breakpoint: spell_th_max'
        spell_lvl = player_spell['level']
        for troop_spell in troop_json['th'][f'{player_th}']['spell']:
            if troop_spell['name'] == spell_name:
                spell_th_max = troop_spell['thMax']
        spell_max = player_spell['maxLevel']
        return_line.append(f'{player_name}\'s {player_spell["name"]} is lvl {spell_lvl}, max for TH {player_th} is lvl {spell_th_max}.')
        return_line.append('---------')

    del return_line[-1]
    return return_line


def get_user(user_tag):
    # return user profile info
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + user_tag, headers=header)
    user_json = response.json()
    print(user_json['name'])


# clan calls

def get_clan(clan_tag):
    clan_json = json_response(clan_tag, 'clans')
    return clan_json['name'] + ' is level ' + str(clan_json['clanLevel'])


def search_clans():
    # search for a clan
    response = requests.get('https://api.clashofclans.com/v1/clans?name=test', headers=header)
    clan_json = response.json()
    for clan in clan_json['items']:
        print(clan['name'] + ' is level ' + str(clan['clanLevel']))


# references

def get_user_troop_level(player_name, troop_name):
    with open(r'C:\Users\westo\Documents\My Documents\Software Development\Python\ClashDiscord\Troop_Data.json') as troop_file:
        troop_data = json.load(troop_file)

    player_name = re.sub('[-]', ' ', player_name)
    members_json = json_response(TheMightyHeroesTag, 'members')
    player_tag = ''
    max_for_th = ''
    player_troop_lvl = ''
    max_for_troop = ''

    # getting the player tag in the list of members in the clan
    for mem in members_json['items']:
        if mem['name'].lower() == player_name.lower():
            player_name = mem['name']
            player_tag = mem['tag']

    if player_tag == '':
        return 'something went wrong with the player tag'

    player_tag = player_tag[1:]
    player_json = json_response(player_tag, 'players')
    player_th = player_json['townHallLevel']
    troop_display_name = ''
    found = False

    if not found:
        for troop in player_json['troops']:
            if troop['name'].lower() == troop_name.lower():
                player_troop_lvl = troop['level']
                troop_display_name = troop['name']
                max_for_troop = troop['maxLevel']
                found = True
                break

    if not found:
        for hero in player_json['heroes']:
            if hero['name'].lower() == troop_name.lower():
                player_troop_lvl = hero['level']
                troop_display_name = hero['name']
                max_for_troop = hero['maxLevel']
                found = True
                break

    if not found:
        for spell in player_json['spells']:
            full_spell_name = f'{troop_name} Spell'
            if spell['name'].lower() == full_spell_name.lower():
                player_troop_lvl = spell['level']
                troop_display_name = spell['name']
                max_for_troop = spell['maxLevel']
                found = True
                break

    for item in troop_data['th'][f'{player_th}']:
        for sub_item in troop_data['th'][f'{player_th}'][item]:
            if sub_item['name'].lower() == troop_name.lower():
                troop_name = sub_item['name']
                max_for_th = sub_item['thMax']

    if player_troop_lvl == '':
        return 'something went wrong getting the player\'s troop lvl'

    if max_for_th == '':
        return 'something went wrong getting the troop'

    player = PlayerTroop(player_tag, player_name, troop_name, troop_display_name, player_troop_lvl, player_th, max_for_th, max_for_troop)

    return player

    # return f'{player_name}\'s {troop_display_name} is lvl {player_troop_lvl}, max for TH {player_th} is {max_for_th}'


def war_overview(war_json):
    if check_war_state(war_json) == 'preparation':
        clan_status, opp_status = clan_opp_status(war_json)
        opponent_name = war_json[opp_status]['name']
        war_start_time = time_string_changer(war_json['startTime'])

        return f'You are preparing for war with {opponent_name} with {date_time_calculator(war_start_time)} left before war starts.'

    elif check_war_state(war_json) == 'inWar':
        clan_status, opp_status = clan_opp_status(war_json)
        opponent_name = war_json[opp_status]['name']
        war_end_time = time_string_changer(war_json['endTime'])

        # winning or losing will say 'winning/losing by x stars' or 'tied'
        # possibly show destruction win as well 'you have the same number of stars, but you/opponent has more destruction'
        scoreboard = score_calculator(war_json, clan_status, opp_status)
        return f'You are in war against {opponent_name} with {date_time_calculator(war_end_time)} left in war. You are {scoreboard}.'

    elif check_war_state(war_json) == 'warEnded':
        clan_status, opp_status = clan_opp_status(war_json)
        opponent_name = war_json[opp_status]['name']

        # win lose will say 'won/lost by x stars' or 'lost by x% destruction'
        scoreboard = score_calculator(war_json, clan_status, opp_status)
        return f'The war against {opponent_name} has ended, you {scoreboard}.'

    elif check_war_state(war_json) == 'notInWar':

        return f'Currently searching for war'

    else:
        return f'Something went wrong. Breakpoint: war_overview'


def war_time(war_json):

    if check_war_state(war_json) == 'preparation':
        war_start_time = time_string_changer(war_json['startTime'])
        return f'{date_time_calculator(war_start_time)} until the war starts.'

    elif check_war_state(war_json) == 'inWar':
        war_end_time = time_string_changer(war_json['endTime'])
        return f'{date_time_calculator(war_end_time)} until the war ends.'

    elif check_war_state(war_json) == 'warEnded':
        return f'The war has ended'

    elif check_war_state(war_json) == 'notInWar':

        return f'Currently searching for war or in Clan War League'

    else:
        return 'Well something went wrong, better let someone know'


def score_calculator(war_json, clan_status, opp_status):

    if check_war_state(war_json) == 'preparation':
        scoreboard_string = f'You are preparing for war, no score to show'

    elif check_war_state(war_json) == 'inWar':
        clan_stars = war_json[clan_status]['stars']
        clan_destruction = war_json[clan_status]['destructionPercentage']
        opp_stars = war_json[opp_status]['stars']
        opp_destruction = war_json[opp_status]['destructionPercentage']

        if clan_stars > opp_stars:
            score_diff = clan_stars - opp_stars
            scoreboard_string = f'winning by {score_diff} star(s)'

        elif clan_stars < opp_stars:
            score_diff = opp_stars - clan_stars
            scoreboard_string = f'losing by {score_diff} star(s)'

        elif clan_stars == opp_stars:
            scoreboard_string = 'stars are tied, '

            if clan_destruction > opp_destruction:
                score_diff = clan_destruction - opp_destruction
                scoreboard_string = f'winning by {score_diff} destruction percent'

            elif clan_destruction < opp_destruction:
                score_diff = clan_destruction - opp_destruction
                scoreboard_string = f'losing by {score_diff} destruction percent'

            elif clan_destruction == opp_destruction:
                scoreboard_string += 'destruction is tied'

            else:
                scoreboard_string = f'something went wrong. Breakpoint: clan_destruction'

        else:
            scoreboard_string = f'something went wrong. Breakpoint: clan_stars'

    elif check_war_state(war_json) == 'warEnded':
        clan_stars = war_json[clan_status]['stars']
        clan_destruction = war_json[clan_status]['destructionPercentage']
        opp_stars = war_json[opp_status]['stars']
        opp_destruction = war_json[opp_status]['destructionPercentage']

        if clan_stars > opp_stars:
            score_diff = clan_stars - opp_stars
            scoreboard_string = f'won by {score_diff} star(s)'

        elif clan_stars < opp_stars:
            score_diff = opp_stars - clan_stars
            scoreboard_string = f'lost by {score_diff} star(s)'

        elif clan_stars == opp_stars:
            scoreboard_string = 'stars were tied, '

            if clan_destruction > opp_destruction:
                score_diff = clan_destruction - opp_destruction
                scoreboard_string += f'won by {score_diff} destruction percent'

            elif clan_destruction < opp_destruction:
                score_diff = clan_destruction - opp_destruction
                scoreboard_string += f'lost by {score_diff} destruction percent'

            elif clan_destruction == opp_destruction:
                scoreboard_string += 'destruction was tied'

            else:
                scoreboard_string = f'something went wrong. Breakpoint: warEnded/clan_destruction'

        else:
            scoreboard_string = f'something went wrong. Breakpoint: warEnded/clan_stars'

    elif check_war_state(war_json) == 'notInWar':

        return f'Currently searching for war'

    else:
        return f'Something went wrong. Breakpoint: score_calculator'

    return scoreboard_string


def calculate_win_lose(war_json, clan_status, opp_status):
    clan_stars = war_json[clan_status]['stars']
    clan_destruction = war_json[clan_status]['destructionPercentage']
    opponent_stars = war_json[opp_status]['stars']
    opponent_destruction = war_json[opp_status]['destructionPercentage']
    if clan_stars > opponent_stars:
        return 'won!'
    elif clan_stars < opponent_stars:
        return 'lost.'
    else:
        if clan_destruction > opponent_destruction:
            return 'won!'
        elif clan_destruction < opponent_destruction:
            return 'lost.'
        else:
            return 'tied.'


# returns the sorted war member data
def get_war_member_info(json_data, clan_status):
    war_members = []

    # gets the info for war members
    for member in json_data[clan_status]['members']:
        star_points = 0
        number_of_attacks = 0
        member_attack1_tag = ''
        member_attack1_stars = 0
        member_attack1_destruction = 0
        member_attack2_tag = ''
        member_attack2_stars = 0
        member_attack2_destruction = 0
        if 'attacks' in member:
            attacked = True
            for points in member['attacks']:
                star_points += points['stars']
                number_of_attacks += 1
                if number_of_attacks == 1:
                    member_attack1_tag = points['defenderTag']
                    member_attack1_stars = points['stars']
                    member_attack1_destruction = ['destructionPercentage']

                elif number_of_attacks == 2:
                    member_attack2_tag = points['defenderTag']
                    member_attack2_stars = points['stars']
                    member_attack2_destruction = ['destructionPercentage']

                else:
                    print('something went wrong, breakpoint: getting attack information from all attacks method')

        else:
            attacked = False

        war_members.append(
            WarMember(member['mapPosition'], member['townhallLevel'], member['name'], member['tag'], attacked,
                      number_of_attacks, star_points, member_attack1_tag, member_attack1_stars,
                      member_attack1_destruction, member_attack2_tag, member_attack2_stars,
                      member_attack2_destruction))

    return sorted(war_members, key=lambda x: x.map_pos, reverse=False)


def no_atk(war_json):
    if check_war_state(war_json) == 'preparation':

        return f'You are still preparing for war, nobody has attacked.'

    elif check_war_state(war_json) == 'inWar':

        clan_status, opp_status = clan_opp_status(war_json)
        no_attack_string = ''
        war_members = []
        for war_member in war_json[clan_status]['members']:
            star_points = 0
            number_of_attacks = 0
            member_attack1_tag = ''
            member_attack1_stars = 0
            member_attack1_destruction = 0
            member_attack2_tag = ''
            member_attack2_stars = 0
            member_attack2_destruction = 0
            if 'attacks' in war_member:
                attacked = True
                for points in war_member['attacks']:
                    star_points += points['stars']
                    number_of_attacks += 1

            else:
                attacked = False

            war_members.append(
                WarMember(war_member['mapPosition'], war_member['townhallLevel'], war_member['name'], war_member['tag'],
                          attacked,
                          number_of_attacks, star_points, member_attack1_tag, member_attack1_stars,
                          member_attack1_destruction, member_attack2_tag, member_attack2_stars,
                          member_attack2_destruction))

        sorted_war_members = sorted(war_members, key=lambda x: x.map_pos, reverse=False)

        if any(not mem.get('has_attacked') for mem in sorted_war_members):
            for obj in sorted_war_members:
                if not obj.has_attacked:
                    no_attack_string += f'{obj.name}, '

            # removing the last ' ' and ',' from the string
            no_attack_string = no_attack_string[:-2]
            no_attack_string += f' have not attacked.'

        else:
            no_attack_string = 'Everyone has attacked'

        return no_attack_string

    elif war_json['state'] == 'warEnded':
        clan_status, opp_status = clan_opp_status(war_json)
        no_attack_string = ''
        war_members = []
        for war_member in war_json[clan_status]['members']:
            star_points = 0
            number_of_attacks = 0
            member_attack1_tag = ''
            member_attack1_stars = 0
            member_attack1_destruction = 0
            member_attack2_tag = ''
            member_attack2_stars = 0
            member_attack2_destruction = 0
            if 'attacks' in war_member:
                attacked = True
                for points in war_member['attacks']:
                    star_points += points['stars']
                    number_of_attacks += 1

            else:
                attacked = False

            war_members.append(
                WarMember(war_member['mapPosition'], war_member['townhallLevel'], war_member['name'], war_member['tag'],
                          attacked,
                          number_of_attacks, star_points, member_attack1_tag, member_attack1_stars,
                          member_attack1_destruction, member_attack2_tag, member_attack2_stars,
                          member_attack2_destruction))

        sorted_war_members = sorted(war_members, key=lambda x: x.map_pos, reverse=False)

        if any(not mem.get('has_attacked') for mem in sorted_war_members):
            for obj in sorted_war_members:
                if not obj.has_attacked:
                    no_attack_string += f'{obj.name}, '

            # removing the last ' ' and ',' from the string
            no_attack_string = no_attack_string[:-2]
            no_attack_string += f' did not attack.'

        else:
            no_attack_string = 'Everyone attacked'

        return no_attack_string

    elif check_war_state(war_json) == 'notInWar':

        return f'Currently searching for war'

    else:
        return f'something went wrong finding out who did not attack. Breakpoint: no_atk/warStatus'


def long_war_overview(war_json):

    if check_war_state(war_json) == 'preparation':
        war_start_time = time_string_changer(war_json['startTime'])
        return f'{date_time_calculator(war_start_time)} until the war starts.'

    elif check_war_state(war_json) == 'inWar':

        war_members = []

        # gets the info for war members
        for member in war_json['clan']['members']:
            star_points = 0
            number_of_attacks = 0
            member_attack1_tag = ''
            member_attack1_stars = 0
            member_attack1_destruction = 0
            member_attack2_tag = ''
            member_attack2_stars = 0
            member_attack2_destruction = 0
            if 'attacks' in member:
                attacked = True
                for points in member['attacks']:
                    star_points += points['stars']
                    number_of_attacks += 1

            else:
                attacked = False

            # make attack one stars, attack one percent and attack two stars and attack two percent
            war_members.append(
                WarMember(member['mapPosition'], member['townhallLevel'], member['name'], member['tag'], attacked,
                          number_of_attacks, star_points, member_attack1_tag, member_attack1_stars,
                          member_attack1_destruction, member_attack2_tag, member_attack2_stars,
                          member_attack2_destruction))

        sorted_war_members = sorted(war_members, key=lambda x: x.map_pos, reverse=False)
        war_member_text = f'{curr_war_overview(TheMightyHeroesTag)}'
        for obj in sorted_war_members:
            war_member_text += f'{obj.name} is a th {obj.th} position {obj.map_pos}'
            if obj.stars == 1:
                star_text = 'star'

            else:
                star_text = 'stars'

            if obj.has_attacked:
                if obj.attacks > 1:
                    attacks_text = 'attacks'
                else:
                    attacks_text = 'attack'

                war_member_text += f' and has made {obj.attacks} {attacks_text} for {obj.stars} {star_text}'

            else:
                war_member_text += ' and has NOT made an attack'

            war_member_text += f'---------'

        return war_member_text

    elif check_war_state(war_json) == 'warEnded':
        clan_status, opp_status = clan_opp_status(war_json)
        opponent_name = war_json['opponent']['name']

        return f'The war against {opponent_name} has ended, TheMightyHeroes {calculate_win_lose(war_json, clan_status, opp_status)}'

    elif check_war_state(war_json) == 'notInWar':

        return f'Currently searching for war'

    else:
        return 'Well... something went wrong'


def clan_opp_status(war_json):
    if war_json['clan']['tag'] == fullClanTag:
        clan_status = 'clan'
        opp_status = 'opponent'
    elif war_json['opponent']['tag'] == fullClanTag:
        clan_status = 'opponent'
        opp_status = 'clan'
    else:
        return 'something went wrong, breakpoint: clan_opp_status'

    return clan_status, opp_status


def json_response(tag, responder):
    clash_base_url = f'https://api.clashofclans.com/v1'
    players = f'/players/%23'
    clans = f'/clans/%23'
    cwl_war = '/clanwarleagues/wars/%23'
    current_war_closer = '/currentwar'
    league_group_closer = '/leaguegroup'
    members_closer = '/members'

    if responder == 'clans':
        response = requests.get(f'{clash_base_url}{clans}{tag}', headers=header)

    elif responder == 'currentwar':
        response = requests.get(f'{clash_base_url}{clans}{tag}{current_war_closer}', headers=header)

    elif responder == 'members':
        response = requests.get(f'{clash_base_url}{clans}{tag}{members_closer}', headers=header)

    elif responder == 'players':
        response = requests.get(f'{clash_base_url}{players}{tag}', headers=header)

    elif responder == 'cwlGroup':
        response = requests.get(f'{clash_base_url}{clans}{tag}{current_war_closer}{league_group_closer}', headers=header)

    elif responder == 'cwlWar':
        response = requests.get(f'{clash_base_url}{cwl_war}{tag}', headers=header)

    else:
        response = requests.get(f'{clash_base_url}{clans}{tag}{current_war_closer}', headers=header)
        print('Something went wrong. Breakpoint: json_response responder')

    return response.json()


def check_war_state(json_data):
    return json_data['state']


# todo get this to work for preparation or ended
def get_curr_cwl_war(cwl_group_json):
    cwl_state = cwl_group_json['state']
    # round_list is a list containing all the lists of war tags

    round_list = get_cwl_rounds(cwl_group_json)
    # goes through every round to find the current war
    for cwl_round in reversed(round_list):
        if not cwl_round[0] == '#0':
            # checking if the specified round is the current round
            cwl_war_json = json_response(cwl_round[0][1:], 'cwlWar')
            if cwl_war_json['state'] == cwl_state:
                # check each war in the current round for TheMightyHeroes in 'clan' or 'opponent'
                for cwl_war in cwl_round:
                    curr_war_json = json_response(cwl_war[1:], 'cwlWar')
                    if curr_war_json['clan']['tag'] == fullClanTag or curr_war_json['opponent']['tag'] == fullClanTag:
                        return cwl_war
    return 'something went wrong. Breakpoint: get_curr_cwl_war'


def get_cwl_rounds(cwl_group_json):
    cwl_rounds = []
    for cwl_round in cwl_group_json['rounds']:
        war_tag_list = []
        for war_tag in cwl_round['warTags']:
            war_tag_list.append(war_tag)
        cwl_rounds.append(war_tag_list)
    return cwl_rounds


def get_response():
    print('getting a response')


def get_each_attack(count, json_data, mem):
    if count == 0:
        attack_position = find_enemy_position(json_data, mem.attack1_tag)
        atk_stars = mem.attack1_stars

    else:
        attack_position = find_enemy_position(json_data, mem.attack2_tag)
        atk_stars = mem.attack2_stars

    if atk_stars == 1:
        star_text = 'star'

    else:
        star_text = 'stars'

    return f'{mem.name} attacked enemy position {attack_position} for {atk_stars} {star_text}'


def find_enemy_position(json_data, enemy_tag):
    war_json = json_data
    enemy_position = '*enemy position not found*'
    for enemy in war_json['opponent']['members']:
        if enemy_tag == enemy['tag']:
            enemy_position = enemy['mapPosition']

    return enemy_position


def time_string_changer(time):
    time = time[:-5:]
    time = time[0: 8:] + time[8 + 1::]
    return time


def date_time_calculator(datef):
    dt_now = datetime.now()
    dt_string = dt_now.strftime("%Y%m%d%H%M%S")

    date_time_format = '%Y%m%d%H%M%S'
    diff = datetime.strptime(datef, date_time_format) - datetime.strptime(dt_string, date_time_format)
    diff = diff - timedelta(hours=6, minutes=0)

    seconds = diff.seconds
    minutes = int(seconds % 3600 / 60)
    hours = int(seconds / 3600)
    remaining_seconds = seconds - hours * 3600 - minutes * 60

    time_remainder = ''

    if diff.days > 0:
        if diff.days == 1:
            days_text = 'day'
        else:
            days_text = 'days'

        time_remainder += f'{diff.days} {days_text}, '
    if hours > 0:
        if hours == 1:
            hour_text = 'hour'
        else:
            hour_text = 'hours'

        time_remainder += f'{hours} {hour_text}, '
    if minutes > 0:
        if minutes == 1:
            minute_text = 'minute'
        else:
            minute_text = 'minutes'

        time_remainder += f'{minutes} {minute_text}, '
    if seconds > 0:
        if seconds == 1:
            second_text = 'second'
        else:
            second_text = 'seconds'

        time_remainder += f'{remaining_seconds} {second_text}, '

    # removing the ', ' from the end of the string
    time_remainder = time_remainder[:-2]

    return time_remainder
