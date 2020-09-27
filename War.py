import requests
import json
from datetime import datetime, timedelta


class War(object):
    """
    War
        Instance Attributes
            state (str): State the war is currently in
            team_size (int): Amount of members in the war
            preparation_start_time (str): Unformatted start time of war prep
            start_time (str): Unformatted start time of war
            end_time (str): Unformatted end time of war
            clan (WarClan): WarClan object of requested clan
                regardless of clan/opponent standing from API
            opponent (WarClan): WarClan object of opposing clan
                regardless of clan/opponent standing from API
    """

    def __init__(
        self, state, team_size, preparation_start_time,
        start_time, end_time, clan, opponent
    ):
        self.state = state
        self.team_size = team_size
        self.preparation_start_time = preparation_start_time
        self.start_time = start_time
        self.end_time = end_time
        self.clan = clan
        self.opponent = opponent

    # returns days, hours, minutes, seconds
    def war_time(self, time_zone):
        if self.state == 'preparation':
            days, hours, minutes, seconds = date_time_calculator(
                self.start_time, time_zone)

        elif self.state == 'inWar':
            days, hours, minutes, seconds = date_time_calculator(
                self.end_time, time_zone)

        # covers warEnded and notInWar states
        else:
            days = 0
            hours = 0
            minutes = 0
            seconds = 0

        return (
            days,
            hours,
            minutes,
            seconds
        )

    def string_date_time(self, time_zone):
        if (self.state == 'warEnded'
                or self.state == 'notInWar'):
            return ''
        days, hours, minutes, seconds = date_time_calculator(
            self.start_time, time_zone)
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

    def string_scoreboard(self):
        # + diff == winning, - diff == losing
        star_difference = (self.clan.stars
                           - self.opponent.stars)
        destruction_difference = (self.clan.destruction_percentage
                                  - self.opponent.destruction_percentage)
        # if it has a difference of 1 it will just say 'star'
        if pow(star_difference, 2) == 1:
            star_string = 'star'
        else:
            star_string = 'stars'

        if self.state == 'inWar':
            win_string = 'winning'
            loss_string = 'losing'
            # if +, so if winning
            if star_difference > 0:
                return f'winning by {abs(star_difference)} {star_string}'
            elif star_difference < 0:
                return f'losing by {abs(star_difference)} {star_string}'
            # if the clan's stars are tied
            else:
                # if +, so if winning
                if destruction_difference > 0:
                    return f'winning by {round(abs(destruction_difference), 2)} destruction percentage.'
                elif destruction_difference < 0:
                    return f'losing by {round(abs(destruction_difference), 2)} destruction percentage.'
                else:
                    return 'tied'

        elif self.state == 'warEnded':
            win_string = 'won'
            loss_string = 'lost'
            # if +, so if winning
            if star_difference > 0:
                return f'won by {abs(star_difference)} {star_string}'
            elif star_difference < 0:
                return f'lost by {abs(star_difference)} {star_string}'
            # if the clan's stars are tied
            else:
                # if +, so if winning
                if destruction_difference > 0:
                    return f'won by {round(abs(destruction_difference), 2)} destruction percentage.'
                elif destruction_difference < 0:
                    return f'lost by {round(abs(destruction_difference), 2)} destruction percentage.'
                else:
                    return 'tied'
        else:
            return f' not in war.'

    # returns a list of members that have not attacked
    def no_attack(self):
        no_attack_members = []
        for member in self.clan.members:
            if len(member.attacks) != member.possible_attack_count:
                no_attack_members.append(member)
        return no_attack_members

    def find_defender(self, defender_tag):
        for defender_member in self.opponent.members:
            if defender_tag == defender_member.tag:
                return defender_member


class WarClan(object):
    """
    WarClan
        Instance Attributes
            status (str): Denotes whether the clan is the API clan or oppenent
            tag (str): Clan's tag
            name (str): Clan's name
            lvl (int): Clan's clan level
            attack_count (int): Clan's attack count
            stars (int): Clan's star count
            destruction_percentage (int): Clan's destruction percentage
            members (list): List of clan members participating in war
                WarMember objects
            score (int): Clan's war score
    """

    def __init__(
        self, status, tag, name, lvl, attack_count,
        stars, destruction_percentage, members, score
    ):
        self.status = status
        self.tag = tag
        self.name = name
        self.lvl = lvl
        self.attack_count = attack_count
        self.stars = stars
        self.destruction_percentage = destruction_percentage
        self.members = members
        self.score = score


class WarMember(object):
    """
    WarMember
        Instance Attributes
            tag (str): WarMember's player tag
            name (str): WarMember's player name
            th_lvl (int): WarMember's player home town hall level
            map_position (int): WarMember's position on the war map
            stars (int): WarMember's star count in current war
            attacks (list): List of WarMember's attacks in current war
                WarMemberAttack objects
            score (int): Member's war score
    """

    def __init__(
        self, tag, name, th_lvl,
        map_position, stars, possible_attack_count, attacks, score
    ):
        self.tag = tag
        self.name = name
        self.th_lvl = th_lvl
        self.map_position = map_position
        self.stars = stars
        self.possible_attack_count = possible_attack_count
        self.attacks = attacks
        self.score = score

    # returns 'time' or 'times'
    def string_member_attack_times(self):
        if len(self.attacks) == 1:
            return 'time'
        else:
            return 'times'

    # returns 'star' or 'stars'
    def string_member_stars(self):
        if self.stars == 1:
            return 'star'
        else:
            return 'stars'


class WarMemberAttack(object):
    """
    WarMemberAttack
        Instance Attributes
            attacker_tag (str): player tag of attacker
            defender_tag (str): player tag of defender
            stars (int): stars earned in attack
            destruction_percent (int): destruction percent earned in attack
            order (int): order of attack in war
            score (int): attack score
    """

    def __init__(
        self, attacker_tag, defender_tag,
        stars, destruction_percent, order, score
    ):
        self.attacker_tag = attacker_tag
        self.defender_tag = defender_tag
        self.stars = stars
        self.destruction_percent = destruction_percent
        self.order = order
        self.score = score

    def string_attack_stars(self):
        "returns string 'star' or 'stars'"
        if self.stars == 1:
            return 'star'
        else:
            return 'stars'


# returns the War object
def get(clan_tag, header):
    """
    Takes in a clan tag and returns the war that clan is engaged in if any
    """
    war_json = json_response(clan_tag, header)
    if war_json['state'] == 'notInWar':
        return War(war_json['state'], 0, 0, 0, 0, [], [])
    else:
        # find whether the clan in clan_tag is clan or opponent in the JSON
        clan_status, opp_status = clan_opp_status(war_json, clan_tag)

        # filling the clan members list
        clan_members = []
        for member in war_json[clan_status]['members']:
            possible_attack_count = 2
            member_attacks = []
            stars = 0
            member_score = (-200)
            if 'attacks' in member:
                for member_attack in member['attacks']:
                    member_score += 100
                    stars += member_attack['stars']

                    star_score = member_attack['stars']/3
                    des_score = member_attack['destructionPercentage']/100
                    # find opp th from attack
                    for opponent in war_json[opp_status]['members']:
                        if opponent['tag'] == member_attack['defenderTag']:
                            defender_th = opponent['townhallLevel']
                            break
                    th_difference = defender_th-member['townhallLevel']
                    attack_score = (((star_score*.75)+(des_score*.25))
                                    * th_multiplier(th_difference))
                    member_score += attack_score
                    member_attacks.append(WarMemberAttack(
                        member_attack['attackerTag'],
                        member_attack['defenderTag'], member_attack['stars'],
                        member_attack['destructionPercentage'],
                        member_attack['order'], attack_score
                    ))
            # adding the current member to the list of clan members
            clan_members.append(WarMember(
                member['tag'], member['name'], member['townhallLevel'],
                member['mapPosition'], stars, possible_attack_count, member_attacks, member_score
            ))
        # sorting clan members by map position
        clan_members = sorted(
            clan_members, key=lambda x: x.map_position, reverse=False)

        clan_score = 0
        for member in clan_members:
            clan_score += member.score
        war_clan = WarClan(
            clan_status, war_json[clan_status]['tag'],
            war_json[clan_status]['name'], war_json[clan_status]['clanLevel'],
            war_json[clan_status]['attacks'], war_json[clan_status]['stars'],
            war_json[clan_status]['destructionPercentage'],
            clan_members, clan_score
        )

        # filling the opp members list
        opp_members = []
        for member in war_json[opp_status]['members']:
            possible_attack_count = 2
            member_attacks = []
            stars = 0
            member_score = (-200)
            if 'attacks' in member:
                for member_attack in member['attacks']:
                    member_score += 100
                    stars += member_attack['stars']

                    star_score = member_attack['stars']/3
                    des_score = member_attack['destructionPercentage']/100
                    # find opp th from attack
                    for opponent in war_json[clan_status]['members']:
                        if opponent['tag'] == member_attack['defenderTag']:
                            defender_th = opponent['townhallLevel']
                            break
                    th_difference = defender_th-member['townhallLevel']
                    attack_score = (((star_score*.75)+(des_score*.25))
                                    * th_multiplier(th_difference))
                    member_score += attack_score

                    member_attacks.append(WarMemberAttack(
                        member_attack['attackerTag'],
                        member_attack['defenderTag'], member_attack['stars'],
                        member_attack['destructionPercentage'],
                        member_attack['order'], attack_score
                    ))
            # adding the current member to the list of opp members
            opp_members.append(WarMember(
                member['tag'], member['name'], member['townhallLevel'],
                member['mapPosition'], stars, possible_attack_count, member_attacks, member_score
            ))

        # sorting opp members by map position
        opp_members = sorted(
            opp_members, key=lambda x: x.map_position, reverse=False)

        opponent_score = 0
        for member in opp_members:
            opponent_score += member.score

        war_opp = WarClan(
            opp_status, war_json[opp_status]['tag'],
            war_json[opp_status]['name'], war_json[opp_status]['clanLevel'],
            war_json[opp_status]['attacks'], war_json[opp_status]['stars'],
            war_json[opp_status]['destructionPercentage'],
            opp_members, opponent_score
        )

    return War(
        war_json['state'], war_json['teamSize'],
        war_json['preparationStartTime'], war_json['startTime'],
        war_json['endTime'], war_clan, war_opp
    )


def json_response(tag, header):
    tag = tag[1:]
    url = f'https://api.clashofclans.com/v1/clans/%23{tag}/currentwar'
    return requests.get(url, headers=header).json()


def clan_opp_status(war_json, clan_tag):
    # this clan_tag includes the # at the beginning
    if war_json['clan']['tag'] == clan_tag:
        clan_status = 'clan'
        opp_status = 'opponent'
    elif war_json['opponent']['tag'] == clan_tag:
        clan_status = 'opponent'
        opp_status = 'clan'
    else:
        clan_status = 'clan'
        opp_status = 'opponent'
    return clan_status, opp_status


def date_time_calculator(date_final, time_zone):
    date_time_format = '%Y%m%d%H%M%S'
    dt_now = datetime.now()
    date_final = time_string_changer(date_final)
    dt_string = dt_now.strftime(date_time_format)
    diff = (datetime.strptime(date_final, date_time_format)
            - datetime.strptime(dt_string, date_time_format))
    diff = (diff
            + timedelta(hours=time_zone, minutes=0))

    days = diff.days
    seconds = diff.seconds
    minutes = int(seconds % 3600 / 60)
    hours = int(seconds / 3600)
    remaining_seconds = (seconds - hours * 3600 - minutes * 60)

    return days, hours, minutes, remaining_seconds


def time_string_changer(time):
    time = time[:-5:]
    time = time[:8] + time[8 + 1:]
    return time


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
