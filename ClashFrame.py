from ClashFrameReferences import *
from datetime import datetime, timedelta
import json
import re


# have them set the header
# ! MAKE SURE TO SET clan_tag CORRECTLY it is set with # at the beginning


# War

# returns War class object
# todo take in a War class object instead of the raw json file
def war_overview(clan_tag, header):
    war_json = json_response(clan_tag, 'war', header)
    war_state = war_json['state']
    # todo double check this actually has the necessary data, if it does then consolidate the prep, inWar, and warEnded states
    if war_state == 'notInWar':
        return War(war_state, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    # this will work for 'preparation', 'inWar', and 'warEnded' states
    else:
        # this will tell you if your clan is the clan or opponent in eyes of the API
        clan_status, opp_status = clan_opp_status(war_json, clan_tag)

        clan_members_list = []
        opp_members_list = []

        for member in war_json[clan_status]['members']:
            member_attacks = []

            if 'attacks' in member:
                for attack in member['attacks']:
                    member_attacks.append(WarAttack(attack['attackerTag'], attack['defenderTag'], attack['stars'], attack['destructionPercentage'], attack['order']))

            clan_members_list.append(WarMember(member['tag'], member['name'], member['townhallLevel'], member['mapPosition'], member_attacks))

        clan_members_list = sorted(clan_members_list, key=lambda x: x.map_position, reverse=False)

        for member in war_json[opp_status]['members']:
            member_attacks = []

            if 'attacks' in member:
                for attack in member['attacks']:
                    member_attacks.append(WarAttack(attack['attackerTag'], attack['defenderTag'], attack['stars'], attack['destructionPercentage'], attack['order']))

            opp_members_list.append(WarMember(member['tag'], member['name'], member['townhallLevel'], member['mapPosition'], member_attacks))

        opp_members_list = sorted(opp_members_list, key=lambda x: x.map_position, reverse=False)

        return War(war_state, war_json['teamSize'], war_json['preparationStartTime'], war_json['startTime'], war_json['endTime'], war_json[f'{clan_status}']['tag'], war_json[f'{clan_status}']['name'], war_json[f'{clan_status}']['clanLevel'], war_json[f'{clan_status}']['attacks'], war_json[f'{clan_status}']['stars'], war_json[f'{clan_status}']['destructionPercentage'], clan_members_list, war_json[f'{opp_status}']['tag'], war_json[f'{opp_status}']['name'], war_json[f'{opp_status}']['clanLevel'], war_json[f'{opp_status}']['attacks'], war_json[f'{opp_status}']['stars'], war_json[f'{opp_status}']['destructionPercentage'], opp_members_list)


# takes in a war object returns touple = war_state, days, hours, minutes, seconds
def war_time(war):
    if war.state == 'preparation':
        war_start_time = time_string_changer(war.start_time)
        days, hours, minutes, seconds = date_time_calculator(war_start_time)

        return war.state, days, hours, minutes, seconds

    elif war.state == 'inWar':
        war_end_time = time_string_changer(war.end_time)
        days, hours, minutes, seconds = date_time_calculator(war_end_time)

        return war.state, days, hours, minutes, seconds

    # covers 'warEnded' and 'notInWar' states
    else:
        days = 0
        hours = 0
        minutes = 0
        seconds = 0

        return war.state, days, hours, minutes, seconds


# CWL

# returns CWLGroup class object
def cwl_group(clan_tag, header):
    cwl_group_json = json_response(clan_tag, 'cwlGroup', header)
    clans = []
    # gets a list of CWLClan class objects
    for clan in cwl_group_json['clans']:
        clans.append(CWLClan(clan['tag'], clan['name'], clan['clanLevel']))

    # rounds is a list of war_tags list which is a list of war tags in a specified round
    rounds = []
    for cwl_round in cwl_group_json['rounds']:
        war_tags = []
        # the war tag will include #
        for war_tag in cwl_round['warTags']:
            war_tags.append(war_tag)
        rounds.append(war_tags)

    return CWLGroup(cwl_group_json['state'], cwl_group_json['season'], clans, rounds)


def cwl_war_overview(clan_tag, war_tag, header):
    war_json = json_response(war_tag, 'cwlWar', header)
    war_state = war_json['state']
    # todo double check this actually has the necessary data, if it does then consolidate the prep, inWar, and warEnded states
    if war_state == 'notInWar':
        return CWLWar(war_state, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    # this will work for 'preparation', 'inWar', and 'warEnded' states
    else:
        # this will tell you if your clan is the clan or opponent in eyes of the API
        clan_status, opp_status = clan_opp_status(war_json, clan_tag)

        clan_members_list = []
        opp_members_list = []

        for member in war_json[clan_status]['members']:
            member_attacks = []

            if 'attacks' in member:
                for attack in member['attacks']:
                    member_attacks.append(WarAttack(attack['attackerTag'], attack['defenderTag'], attack['stars'], attack['destructionPercentage'], attack['order']))

            clan_members_list.append(WarMember(member['tag'], member['name'], member['townhallLevel'], member['mapPosition'], member_attacks))

        clan_members_list = sorted(clan_members_list, key=lambda x: x.map_position, reverse=False)

        for member in war_json[opp_status]['members']:
            member_attacks = []

            if 'attacks' in member:
                for attack in member['attacks']:
                    member_attacks.append(WarAttack(attack['attackerTag'], attack['defenderTag'], attack['stars'], attack['destructionPercentage'], attack['order']))

            opp_members_list.append(WarMember(member['tag'], member['name'], member['townhallLevel'], member['mapPosition'], member_attacks))

        opp_members_list = sorted(opp_members_list, key=lambda x: x.map_position, reverse=False)

        return CWLWar(war_tag, war_state, war_json['teamSize'], war_json['preparationStartTime'], war_json['startTime'], war_json['endTime'], war_json[f'{clan_status}']['tag'], war_json[f'{clan_status}']['name'], war_json[f'{clan_status}']['clanLevel'], war_json[f'{clan_status}']['attacks'], war_json[f'{clan_status}']['stars'], war_json[f'{clan_status}']['destructionPercentage'], clan_members_list, war_json[f'{opp_status}']['tag'], war_json[f'{opp_status}']['name'], war_json[f'{opp_status}']['clanLevel'], war_json[f'{opp_status}']['attacks'], war_json[f'{opp_status}']['stars'], war_json[f'{opp_status}']['destructionPercentage'], opp_members_list)


# Player

# returns Player class object
def player(player_tag, header):
    player_json = json_response(player_tag, 'player', header)
    # ! role and clan info not available if player is not in a clan
    if 'clan' not in player_json:
        role = ''
        clan_tag = ''
        clan_name = ''
        clan_lvl = 0
    else:
        role = player_json['role']
        clan_tag = player_json['clan']['tag']
        clan_name = player_json['clan']['name']
        clan_lvl = player_json['clan']['clanLevel']

    if 'league' not in player_json:
        league_id = 0
        league_name = ''
    else:
        league_id = player_json['league']['id']
        league_name = player_json['league']['name']

    troops = []
    heroes = []
    spells = []

    for troop in player_json['troops']:
        troops.append(Troop(troop['name'], troop['level'], troop['maxLevel'], troop['village']))
    for hero in player_json['heroes']:
        heroes.append(Hero(hero['name'], hero['level'], hero['maxLevel'], hero['village']))
    for spell in player_json['spells']:
        spells.append(Spell(spell['name'], spell['level'], spell['maxLevel'], spell['village']))

    return Player(player_json['tag'], player_json['name'], player_json['townHallLevel'], player_json['expLevel'], player_json['trophies'], player_json['bestTrophies'], player_json['warStars'], player_json['builderHallLevel'], player_json['versusTrophies'], player_json['bestVersusTrophies'], role, player_json['donations'], player_json['donationsReceived'], clan_tag, clan_name, clan_lvl, league_id, league_name, troops, heroes, spells)


# take in clan_json and member_name to return a specific player_tag
def find_member(clan_object, member_name):
    tag = ''
    for member in clan_object.members:
        if member.name.lower() == member_name.lower():
            tag = member.tag
            break
    return tag


# takes in a Player class object and gives a Troop/Hero/Spell class object
def find_troop(player_object, troop_name):
    found = False
    requested = ''
    if not found:
        for troop in player_object.troops:
            if troop.name.lower() == troop_name.lower():
                found = True
                requested = troop
                break
    if not found:
        for hero in player_object.heroes:
            if hero.name.lower() == troop_name.lower():
                found = True
                requested = hero
                break
    if not found:
        for spell in player_object.spells:
            if spell.name.lower() == troop_name.lower():
                found = True
                requested = spell
                break

    return requested


# Clan

# returns Clan class object
def clan(clan_tag, header):
    clan_json = json_response(clan_tag, 'clan', header)
    members = []
    for member in clan_json['memberList']:
        league_id = ''
        league_name = ''
        if 'league' in member:
            league_id = member['league']['id']
            league_name = member['league']['name']
        members.append(
            ClanMember(member['tag'], member['name'], member['role'], member['expLevel'], league_id, league_name,
                       member['trophies'], member['versusTrophies'], member['clanRank'], member['previousClanRank'],
                       member['donations'], member['donationsReceived']))

    return Clan(clan_json['tag'], clan_json['name'], clan_json['type'], clan_json['description'],
                clan_json['clanLevel'], clan_json['clanPoints'], clan_json['clanVersusPoints'], clan_json['warWins'],
                clan_json['warTies'], clan_json['warLosses'], members)


# JSON caller

# returns the json data
# ! using this method to validate tags and remove the #
def json_response(tag, responder, header):
    # removing the # on the tag for api calls
    tag = tag[1:]

    clash_base_url = f'https://api.clashofclans.com/v1'
    players = f'/players/%23'
    clans = f'/clans/%23'
    cwl_war = '/clanwarleagues/wars/%23'
    current_war_closer = '/currentwar'
    league_group_closer = '/leaguegroup'
    members_closer = '/members'

    if responder == 'clan':
        response = requests.get(f'{clash_base_url}{clans}{tag}', headers=header)

    elif responder == 'war':
        response = requests.get(f'{clash_base_url}{clans}{tag}{current_war_closer}', headers=header)

    elif responder == 'members':
        response = requests.get(f'{clash_base_url}{clans}{tag}{members_closer}', headers=header)

    elif responder == 'player':
        response = requests.get(f'{clash_base_url}{players}{tag}', headers=header)

    elif responder == 'cwlGroup':
        response = requests.get(f'{clash_base_url}{clans}{tag}{current_war_closer}{league_group_closer}',
                                headers=header)

    elif responder == 'cwlWar':
        response = requests.get(f'{clash_base_url}{cwl_war}{tag}', headers=header)

    else:
        response = requests.get(f'{clash_base_url}{clans}{tag}{current_war_closer}', headers=header)
        print('Something went wrong. Breakpoint: json_response responder')

    return response.json()

