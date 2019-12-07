import requests
from datetime import datetime, timedelta
import json
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


RazgrizTag = 'RGQ8RGU9'
TheMightyHeroesTag = 'JJRJGVR0'
header = {
    'Accept': 'application/json',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjkyNWJjYzg1LWFhZDktNGM2NC05M2Y2LWM4MWEwZGVhOGUwNiIsImlhdCI6MTU3NDYyMjY3Nywic3ViIjoiZGV2ZWxvcGVyLzdjZmJkOWFjLTFlYzAtNDI3OS1jODM2LTU0YzMxN2FlZmE4NiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjEwOC4yMTEuOTUuMjU0Il0sInR5cGUiOiJjbGllbnQifV19.gdc-4-OEZzsYBLk8HfqZBH-idvlK1vX9nim91XEqLgwNAyarfZquxfkZDKPsswUGyiXRIFV7Am3RB7iWtd9T5w'
}


def get_response():
    print('getting a response')


def get_user(user_tag):
    # return user profile info
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + user_tag, headers=header)
    user_json = response.json()
    print(user_json['name'])


def get_user_levels(user_tag):
    # return user profile level info
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + user_tag, headers=header)
    user_json = response.json()
    print(user_json['name'] + ' is a ' + user_json['role'] + ' in ' + user_json['clan']['name'])
    for hero in user_json['heroes']:
        print(hero['name'] + ' is level ' + str(hero['level']) + ' max is ' + str(hero['maxLevel']))
    for troop in user_json['troops']:
        print(troop['name'] + ' is level ' + str(troop['level']) + ' max is ' + str(troop['maxLevel']))
    for spell in user_json['spells']:
        print(spell['name'] + ' is level ' + str(spell['level']) + ' max is ' + str(spell['maxLevel']))


def get_clan(clan_tag):
    clan_json = json_response(clan_tag, 'clans')
    return clan_json['name'] + ' is level ' + str(clan_json['clanLevel'])


def json_response(tag, responder):
    players_url = f'https://api.clashofclans.com/v1/players/%23'
    clans_url = f'https://api.clashofclans.com/v1/clans/%23'
    current_war_closer = '/currentwar'
    members_closer = '/members'

    if responder == 'clans':
        response = requests.get(f'{clans_url}{tag}', headers=header)

    elif responder == 'currentwar':
        response = requests.get(f'{clans_url}{tag}{current_war_closer}', headers=header)

    elif responder == 'members':
        response = requests.get(f'{clans_url}{tag}{members_closer}', headers=header)

    elif responder == 'players':
        response = requests.get(f'{players_url}{tag}', headers=header)

    else:
        response = requests.get(f'{clans_url}{tag}{current_war_closer}', headers=header)
        print('Something went wrong. Breakpoint: json_response responder')

    return response.json()


def long_war_overview(clan_tag):
    # getting the current war of the given clan
    war_json = json_response(clan_tag, 'currentwar')

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
        opponent_name = war_json['opponent']['name']

        return f'The war against {opponent_name} has ended, TheMightyHeroes {calculate_win_lose(clan_tag)}'

    elif check_war_state(war_json) == 'notInWar':

        return f'Currently searching for war'

    else:
        return 'Well... something went wrong'


def search_clans():
    # search for a clan
    response = requests.get('https://api.clashofclans.com/v1/clans?name=test', headers=header)
    clan_json = response.json()
    for clan in clan_json['items']:
        print(clan['name'] + ' is level ' + str(clan['clanLevel']))


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


def calculate_win_lose(clan_tag):
    response = requests.get('https://api.clashofclans.com/v1/clans/%23' + clan_tag + '/currentwar', headers=header)
    war_json = response.json()
    clan_stars = war_json['clan']['stars']
    clan_destruction = war_json['clan']['destructionPercentage']
    opponent_stars = war_json['opponent']['stars']
    opponent_destruction = war_json['opponent']['destructionPercentage']
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


# either use the json data or the clan tag
def check_war_state(json_data):
    return json_data['state']


# existing elif statement hinders this from being useful, needs more reformatting
def war_time(clan_tag):
    war_json = json_response(clan_tag, 'currentwar')

    if check_war_state(war_json) == 'preparation':
        war_start_time = time_string_changer(war_json['startTime'])
        return f'{date_time_calculator(war_start_time)} until the war starts.'

    elif check_war_state(war_json) == 'inWar':
        war_end_time = time_string_changer(war_json['endTime'])
        return f'{date_time_calculator(war_end_time)} until the war ends.'

    elif check_war_state(war_json) == 'warEnded':
        return f'The war has ended'

    elif check_war_state(war_json) == 'notInWar':

        return f'Currently searching for war'

    else:
        return 'Well something went wrong, better let someone know'


def curr_war_overview(clan_tag):
    war_json = json_response(clan_tag, 'currentwar')

    if check_war_state(war_json) == 'preparation':
        opponent_name = war_json['opponent']['name']
        war_start_time = time_string_changer(war_json['startTime'])

        return f'You are preparing for war with {opponent_name} with {date_time_calculator(war_start_time)} left before war starts.'

    elif check_war_state(war_json) == 'inWar':
        opponent_name = war_json['opponent']['name']
        war_end_time = time_string_changer(war_json['endTime'])

        # winning or losing will say 'winning/losing by x stars' or 'tied'
        # possibly show destruction win as well 'you have the same number of stars, but you/opponent has more destruction'
        scoreboard = score_calculator(TheMightyHeroesTag)
        return f'You are in war against {opponent_name} with {date_time_calculator(war_end_time)} left in war. You are {scoreboard}.'

    elif check_war_state(war_json) == 'warEnded':
        opponent_name = war_json['opponent']['name']

        # win lose will say 'won/lost by x stars' or 'lost by x% destruction'
        scoreboard = score_calculator(TheMightyHeroesTag)
        return f'The war against {opponent_name} has ended, you {scoreboard}.'

    elif check_war_state(war_json) == 'notInWar':

        return f'Currently searching for war'

    else:
        return f'Something went wrong. Breakpoint: curr_war_overview'


def score_calculator(clan_tag):
    war_json = json_response(clan_tag, 'currentwar')

    if check_war_state(war_json) == 'preparation':
        scoreboard_string = f'You are preparing for war, no score to show'

    elif check_war_state(war_json) == 'inWar':
        clan_stars = war_json['clan']['stars']
        clan_destruction = war_json['clan']['destructionPercentage']
        opp_stars = war_json['opponent']['stars']
        opp_destruction = war_json['opponent']['destructionPercentage']

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
        clan_stars = war_json['clan']['stars']
        clan_destruction = war_json['clan']['destructionPercentage']
        opp_stars = war_json['opponent']['stars']
        opp_destruction = war_json['opponent']['destructionPercentage']

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


def all_attack_stars(clan_tag):
    war_json = json_response(clan_tag, 'currentwar')

    if check_war_state(war_json) == 'preparation':
        war_start_time = time_string_changer(war_json['startTime'])
        return f'{date_time_calculator(war_start_time)} until the war starts.'

    elif check_war_state(war_json) == 'inWar':
        return_line = []

        # gets war member data
        sorted_war_members = get_war_member_info(war_json)

        return_line.append(f'{curr_war_overview(TheMightyHeroesTag)}')

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

        return return_line

    elif check_war_state(war_json) == 'warEnded':
        return_line = []

        # gets war member data
        sorted_war_members = get_war_member_info(war_json)

        return_line.append(f'{curr_war_overview(TheMightyHeroesTag)}')
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
        return_line = []

        # gets war member data
        sorted_war_members = get_war_member_info(war_json)

        return_line.append(f'{curr_war_overview(TheMightyHeroesTag)}')

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
        sorted_war_members = get_war_member_info(war_json)

        return_line.append(f'{curr_war_overview(TheMightyHeroesTag)}')
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


# have this return the sorted war member data
def get_war_member_info(json_data):
    war_members = []

    # gets the info for war members
    for member in json_data['clan']['members']:
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


def no_atk(clan_tag):
    war_json = json_response(clan_tag, 'currentwar')

    if check_war_state(war_json) == 'preparation':

        return f'You are still preparing for war, nobody has attacked.'

    elif check_war_state(war_json) == 'inWar':

        no_attack_string = ''
        war_members = []
        for war_member in war_json['clan']['members']:
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

        no_attack_string = ''
        war_members = []
        for war_member in war_json['clan']['members']:
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


def check_user_troop(player_name, troop_name):
    members_json = json_response(TheMightyHeroesTag, 'members')
    player_tag = ''
    max_for_th = ''
    player_troop_lvl = ''
    player_name.lower()
    troop_name.lower()

    for mem in members_json['items']:
        if mem['name'].lower() == player_name.lower():
            player_name = mem['name']
            player_tag = mem['tag']

    if player_tag == '':
        return 'something went wrong with the player tag'

    player_tag = player_tag[1:]
    player_json = json_response(player_tag, 'players')
    player_th = player_json['townHallLevel']

    for troop in player_json['troops']:
        if troop['name'].lower() == troop_name.lower():
            player_troop_lvl = troop['level']

    for hero in player_json['heroes']:
        if hero['name'].lower() == troop_name.lower():
            player_troop_lvl = hero['level']

    for spell in player_json['spells']:
        full_spell_name = f'{troop_name} Spell'
        if spell['name'].lower() == full_spell_name.lower():
            player_troop_lvl = spell['level']

    if player_troop_lvl == '':
        return 'something went wrong getting the player\'s troop lvl'

    with open(r'C:\Users\Weston\PycharmProjects\ClashDiscord\Troop_Data.json') as troop_file:
        troop_data = json.load(troop_file)
        for item in troop_data['th'][f'{player_th}']:
            for sub_item in troop_data['th'][f'{player_th}'][item]:
                if sub_item['name'].lower() == troop_name:
                    troop_name = sub_item['name']
                    max_for_th = sub_item['thMax']

    if max_for_th == '':
        return 'something went wrong getting the troop'

    return f'{player_name}\'s {troop_name} is lvl {player_troop_lvl}, max for TH {player_th} is {max_for_th}'

# get_user(RazgrizTag)
# get_user_levels(RazgrizTag)
# search_clans()
# get_clan(TheMightyHeroesTag)
# current_war_overview(TheMightyHeroesTag)
# print(war_time(TheMightyHeroesTag))
# print(curr_war_overview(TheMightyHeroesTag))
# print(no_atk(TheMightyHeroesTag))
