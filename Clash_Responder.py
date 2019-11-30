import requests
from datetime import datetime, timedelta


class WarMember:
    def __init__(self, map_pos, th, name, tag, has_attacked, attacks, stars):
        self.map_pos = map_pos
        self.th = th
        self.name = name
        self.tag = tag
        self.has_attacked = has_attacked
        self.attacks = attacks
        self.stars = stars

    def get(self, param):
        pass


RazgrizTag = 'RGQ8RGU9'
TheMightyHeroesTag = 'JJRJGVR0'
headers = {
    'Accept': 'application/json',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjkyNWJjYzg1LWFhZDktNGM2NC05M2Y2LWM4MWEwZGVhOGUwNiIsImlhdCI6MTU3NDYyMjY3Nywic3ViIjoiZGV2ZWxvcGVyLzdjZmJkOWFjLTFlYzAtNDI3OS1jODM2LTU0YzMxN2FlZmE4NiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjEwOC4yMTEuOTUuMjU0Il0sInR5cGUiOiJjbGllbnQifV19.gdc-4-OEZzsYBLk8HfqZBH-idvlK1vX9nim91XEqLgwNAyarfZquxfkZDKPsswUGyiXRIFV7Am3RB7iWtd9T5w'
}


def get_response():
    print('getting a response')


def get_user(user_tag):
    # return user profile info
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + user_tag, headers=headers)
    user_json = response.json()
    print(user_json['name'])


def get_user_levels(user_tag):
    # return user profile level info
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + user_tag, headers=headers)
    user_json = response.json()
    print(user_json['name'] + ' is a ' + user_json['role'] + ' in ' + user_json['clan']['name'])
    for hero in user_json['heroes']:
        print(hero['name'] + ' is level ' + str(hero['level']) + ' max is ' + str(hero['maxLevel']))
    for troop in user_json['troops']:
        print(troop['name'] + ' is level ' + str(troop['level']) + ' max is ' + str(troop['maxLevel']))
    for spell in user_json['spells']:
        print(spell['name'] + ' is level ' + str(spell['level']) + ' max is ' + str(spell['maxLevel']))


def get_clan(clan_tag):
    # submit a clan search
    response = requests.get('https://api.clashofclans.com/v1/clans/%23' + clan_tag, headers=headers)
    clan_json = response.json()
    print(clan_json['name'] + ' is level ' + str(clan_json['clanLevel']))


def current_war_overview(clan_tag):
    # getting the current war of the given clan
    response = requests.get('https://api.clashofclans.com/v1/clans/%23' + clan_tag + '/currentwar', headers=headers)
    war_json = response.json()

    if check_war_state(war_json) == 'preparation':
        war_start_time = time_string_changer(war_json['startTime'])
        return f'{date_time_calculator(war_start_time)} until the war starts.'

    elif check_war_state(war_json) == 'inWar':
        war_end_time = time_string_changer(war_json['endTime'])
        dt_now = datetime.now()
        dt_string = dt_now.strftime("%Y%m%d%H%M%S")

        war_members = []
        for member in war_json['clan']['members']:
            star_points = 0
            number_of_attacks = 0
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
                          number_of_attacks, star_points))

        sorted_war_members = sorted(war_members, key=lambda x: x.map_pos, reverse=False)
        for obj in sorted_war_members:
            war_member_text = f'{obj.name} is a th {obj.th} position {obj.map_pos}'
            if obj.stars == 1:
                star_amnt = 'star'

            else:
                star_amnt = 'stars'

            if obj.has_attacked:
                if obj.attacks > 1:
                    war_member_text += f' and has made {obj.attacks} attacks and gotten {obj.stars} {star_amnt}'
                else:
                    war_member_text += f' and has made {obj.attacks} attack and gotten {obj.stars} {star_amnt}'

            else:
                war_member_text += ' and has NOT made an attack'

            # find some way to simplify this to not give all that info
            # print(war_member_text)
            # print('---------')
        return f'{date_time_calculator(war_end_time)} until the war ends.'

    elif check_war_state(war_json) == 'warEnded':
        opponent_name = war_json['opponent']['name']

        return f'The war against {opponent_name} has ended, TheMightyHeroes {calculate_win_lose(clan_tag)}'

    elif check_war_state(war_json) == 'notInWar':

        return f'Currently searching for war'

    else:
        return 'Well... something went wrong'


def search_clans():
    # search for a clan
    response = requests.get('https://api.clashofclans.com/v1/clans?name=test', headers=headers)
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
    days_exist = False
    hours_exist = False
    minutes_exist = False
    if diff.days > 0:
        time_remainder += f'There are {diff.days} days, '
        days_exist = True
    if hours > 0:
        if hours == 1:
            hour_text = 'hour'
        else:
            hour_text = 'hours'
        if days_exist:
            time_remainder += f'{hours} {hour_text}, '
        else:
            time_remainder += f'There are {hours} {hour_text}, '
        hours_exist = True
    if minutes > 0:
        if minutes == 1:
            minute_text = 'minute'
        else:
            minute_text = 'minutes'
        if hours_exist:
            time_remainder += f'{minutes} {minute_text}, '
        else:
            time_remainder += f'There are {minutes} {minute_text}, '
        minutes_exist = True
    if seconds > 0:
        if seconds == 1:
            second_text = 'second'
        else:
            second_text = 'seconds'
        if minutes_exist:
            time_remainder += f'and {remaining_seconds} {second_text}'
        else:
            time_remainder += f'There are {remaining_seconds} {second_text}'

    return time_remainder


def calculate_win_lose(clan_tag):
    response = requests.get('https://api.clashofclans.com/v1/clans/%23' + clan_tag + '/currentwar', headers=headers)
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
    response = requests.get('https://api.clashofclans.com/v1/clans/%23' + clan_tag + '/currentwar', headers=headers)
    war_json = response.json()
    if war_json['state'] == 'preparation':
        war_start_time = time_string_changer(war_json['startTime'])
        return f'{date_time_calculator(war_start_time)} until the war starts.'

    elif war_json['state'] == 'inWar':
        war_end_time = time_string_changer(war_json['endTime'])
        return f'{date_time_calculator(war_end_time)} until the war ends.'

    elif war_json['state'] == 'warEnded':
        return f'The war has ended'

    elif check_war_state(war_json) == 'notInWar':

        return f'Currently searching for war'

    else:
        return 'Well something went wrong, better let someone know'


def curr_war_overview(clan_tag):
    response = requests.get('https://api.clashofclans.com/v1/clans/%23' + clan_tag + '/currentwar', headers=headers)
    war_json = response.json()

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
    # possibly use json_data instead of clan_tag
    response = requests.get('https://api.clashofclans.com/v1/clans/%23' + clan_tag + '/currentwar', headers=headers)
    war_json = response.json()
    scoreboard_string = ''

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


def no_atk(clan_tag):
    response = requests.get('https://api.clashofclans.com/v1/clans/%23' + clan_tag + '/currentwar', headers=headers)
    war_json = response.json()

    if check_war_state(war_json) == 'preparation':

        return f'You are still preparing for war, nobody has attacked.'

    elif check_war_state(war_json) == 'inWar':

        no_attack_string = ''
        war_members = []
        for war_member in war_json['clan']['members']:
            star_points = 0
            number_of_attacks = 0
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
                          number_of_attacks, star_points))

        sorted_war_members = sorted(war_members, key=lambda x: x.map_pos, reverse=False)

        if any(not mem.get('has_attacked') for mem in sorted_war_members):
            for obj in sorted_war_members:
                if not obj.has_attacked:
                    no_attack_string += f'{obj.name}, '

            # removing the last ' ' and ',' from the string
            no_attack_string = no_attack_string[:-2]
            no_attack_string += f' has not attacked.'

        else:
            no_attack_string = 'Everyone has attacked'

        return no_attack_string

    elif war_json['state'] == 'warEnded':

        no_attack_string = ''
        war_members = []
        for war_member in war_json['clan']['members']:
            star_points = 0
            number_of_attacks = 0
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
                          number_of_attacks, star_points))

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


# get_user(RazgrizTag)
# get_user_levels(RazgrizTag)
# search_clans()
# get_clan(TheMightyHeroesTag)
# current_war_overview(TheMightyHeroesTag)
# print(war_time(TheMightyHeroesTag))
# print(curr_war_overview(TheMightyHeroesTag))
# print(no_atk(TheMightyHeroesTag))
