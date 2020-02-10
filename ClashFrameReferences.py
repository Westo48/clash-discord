import requests
from datetime import datetime, timedelta


# Classes
# this War class is for normal and CWL wars
class War:
    def __init__(self, state, team_size, preparation_start_time, start_time, end_time, clan_tag, clan_name, clan_level, clan_attacks, clan_stars, clan_destruction_percentage, clan_members, opponent_tag, opponent_name, opponent_level, opponent_attacks, opponent_stars, opponent_destruction_percentage, opponent_members):
        self.state = state
        self.team_size = team_size
        self.preparation_start_time = preparation_start_time
        self.start_time = start_time
        self.end_time = end_time
        self.clan_tag = clan_tag
        self.clan_name = clan_name
        self.clan_level = clan_level
        self.clan_attacks = clan_attacks
        self.clan_stars = clan_stars
        self.clan_destruction_percentage = clan_destruction_percentage
        self.clan_members = clan_members
        self.opponent_tag = opponent_tag
        self.opponent_name = opponent_name
        self.opponent_level = opponent_level
        self.opponent_attacks = opponent_attacks
        self.opponent_stars = opponent_stars
        self.opponent_destruction_percentage = opponent_destruction_percentage
        self.opponent_members = opponent_members

    def get(self, param):
        pass


class WarMember:
    def __init__(self, tag, name, th, map_position, attacks):
        self.tag = tag
        self.name = name
        self.th = th
        self.map_position = map_position
        self.attacks = attacks

    def get(self, param):
        pass


class WarAttack:
    def __init__(self, attacker_tag, defender_tag, stars, destruction_percent, order):
        self.attacker_tag = attacker_tag
        self.defender_tag = defender_tag
        self.stars = stars
        self.destruction_percent = destruction_percent
        self.order = order

    def get(self, param):
        pass


class CWLGroup:
    def __init__(self, state, season, clans, rounds):
        self.state = state
        self.season = season
        self.clans = clans
        self.rounds = rounds

    def get(self, param):
        pass


# ? make a clan/opp status to easily see which one is the users clan and which is not
class CWLClan:
    def __init__(self, tag, name, clan_lvl):
        self.tag = tag
        self.name = name
        self.clan_lvl = clan_lvl

    def get(self, param):
        pass


class CWLWar:
    def __init__(self, war_tag, state, team_size, preparation_start_time, start_time, end_time, clan_tag, clan_name, clan_level, clan_attacks, clan_stars, clan_destruction_percentage, clan_members, opponent_tag, opponent_name, opponent_level, opponent_attacks, opponent_stars, opponent_destruction_percentage, opponent_members):
        self.war_tag = war_tag
        self.state = state
        self.team_size = team_size
        self.preparation_start_time = preparation_start_time
        self.start_time = start_time
        self.end_time = end_time
        self.clan_tag = clan_tag
        self.clan_name = clan_name
        self.clan_level = clan_level
        self.clan_attacks = clan_attacks
        self.clan_stars = clan_stars
        self.clan_destruction_percentage = clan_destruction_percentage
        self.clan_members = clan_members
        self.opponent_tag = opponent_tag
        self.opponent_name = opponent_name
        self.opponent_level = opponent_level
        self.opponent_attacks = opponent_attacks
        self.opponent_stars = opponent_stars
        self.opponent_destruction_percentage = opponent_destruction_percentage
        self.opponent_members = opponent_members

    def get(self, param):
        pass


class Player:
    def __init__(self, player_tag, player_name, th_lvl, xp_lvl, trophies, best_trophies, war_stars, builder_hall_lvl, vs_trophies, best_vs_trophies, role, donations, donations_received, clan_tag, clan_name, clan_lvl, league_id, league_name, troops, heroes, spells):
        self.player_tag = player_tag
        self.player_name = player_name
        self.th_lvl = th_lvl
        self.xp_lvl = xp_lvl
        self.trophies = trophies
        self.best_trophies = best_trophies
        self.war_stars = war_stars
        self.builder_hall_lvl = builder_hall_lvl
        self.vs_trophies = vs_trophies
        self.best_vs_trophies = best_vs_trophies
        self.role = role
        self.donations = donations
        self.donations_received = donations_received
        self.clan_tag = clan_tag
        self.clan_name = clan_name
        self.clan_lvl = clan_lvl
        self.league_id = league_id
        self.league_name = league_name
        self.troops = troops
        self.heroes = heroes
        self.spells = spells

    def get(self, param):
        pass


class Troop:
    def __init__(self, name, lvl, max_lvl, village):
        self.name = name
        self.lvl = lvl
        self.max_lvl = max_lvl
        self.village = village

    def get(self, param):
        pass


class Hero:
    def __init__(self, name, lvl, max_lvl, village):
        self.name = name
        self.lvl = lvl
        self.max_lvl = max_lvl
        self.village = village

    def get(self, param):
        pass


class Spell:
    def __init__(self, name, lvl, max_lvl, village):
        self.name = name
        self.lvl = lvl
        self.max_lvl = max_lvl
        self.village = village

    def get(self, param):
        pass


class Clan:
    def __init__(self, tag, name, clan_type, description, clan_lvl, clan_points, clan_vs_points, war_wins, war_ties, war_losses, members):
        self.tag = tag
        self.name = name
        self.clan_type = clan_type
        self.description = description
        self.clan_lvl = clan_lvl
        self.clan_points = clan_points
        self.clan_vs_points = clan_vs_points
        self.war_wins = war_wins
        self.war_ties = war_ties
        self.war_losses = war_losses
        self.members = members

    def get(self, param):
        pass


class ClanMember:
    def __init__(self, tag, name, role, exp_lvl, league_id, league_name, trophies, vs_trophies, clan_rank, previous_clan_rank, donations, donations_received):
        self.tag = tag
        self.name = name
        self.role = role
        self.exp_lvl = exp_lvl
        self.league_id = league_id
        self.league_name = league_name
        self.trophies = trophies
        self.vs_trophies = vs_trophies
        self.clan_rank = clan_rank
        self.previous_clan_rank = previous_clan_rank
        self.donations = donations
        self.donations_received = donations_received

    def get(self, param):
        pass


# War


# returns clan status of 'clan' or 'opponent' based on the clan given, default is clan_status='clan' opp_status='opponent'
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

# CWL


# Player


# todo this should be on the TimeReference py file
# Time
# ? change the remaining_seconds to seconds
def date_time_calculator(date_final):
    date_final = time_string_changer(date_final)
    dt_now = datetime.now()
    dt_string = dt_now.strftime("%Y%m%d%H%M%S")

    date_time_format = '%Y%m%d%H%M%S'
    diff = datetime.strptime(date_final, date_time_format) - datetime.strptime(dt_string, date_time_format)
    diff = diff - timedelta(hours=6, minutes=0)

    days = diff.days
    seconds = diff.seconds
    minutes = int(seconds % 3600 / 60)
    hours = int(seconds / 3600)
    remaining_seconds = seconds - hours * 3600 - minutes * 60

    return days, hours, minutes, remaining_seconds


def time_string_changer(time):
    time = time[:-5:]
    time = time[0: 8:] + time[8 + 1::]
    return time
