import requests
import json
import CWLWar
from CWLWar import get as get_cwl_war


class CWLGroup(object):
    """
    CWLGroup
        Instance Attributes
            state (str): CWL state
                'preparation', 'inWar', 'ended'
            season (str): season of clan war league
            clans (list): list of clans in clan war league group
                GWLClan
            rounds (list): list of rounds
                rounds consist of list of war tags
    """

    def __init__(self, state, season, clans, rounds):
        self.state = state
        self.season = season
        self.clans = clans
        self.rounds = rounds

    # return a cwl_war object
    def find_current_war(self, clan_tag, header):
        for cwl_round in self.rounds:
            if cwl_round[0] == '#0':
                return cwl_round[0]
            cwl_war = get_cwl_war(cwl_round[0], clan_tag, header)
            # given the correct round is found
            if (cwl_war.state == 'inWar'
                    or cwl_war.state == 'preparation'):
                # go through the war tags to find the correct clan tag
                for war_tag in cwl_round:
                    cwl_war = get_cwl_war(war_tag, clan_tag, header)
                    if cwl_war.clan.tag == clan_tag:
                        return cwl_war

    def find_preparation_war(self, clan_tag, header):
        for cwl_round in self.rounds:
            if cwl_round[0] == '#0':
                return cwl_round[0]
            cwl_war = get_cwl_war(cwl_round[0], clan_tag, header)
            # given the correct round is found
            # ? add warEnded for catching errors
            if cwl_war.state == 'preparation':
                # go through the war tags to find the correct clan tag
                for war_tag in cwl_round:
                    cwl_war = get_cwl_war(war_tag, clan_tag, header)
                    if cwl_war.clan.tag == clan_tag:
                        return cwl_war

    def find_specified_war(self, clan_tag, round_int, header):
        round_int -= 1
        if 0 <= round_int <= 6:
            if self.rounds[round_int][0] == '#0':
                return self.rounds[round_int][0]
            for war_tag in self.rounds[round_int]:
                if war_tag != '#0':
                    cwl_war = get_cwl_war(war_tag, clan_tag, header)
                    if cwl_war.clan.tag == clan_tag:
                        return cwl_war


class CWLClan(object):
    """
    CWLClan
        Instance Attributes
            tag (str): clan's tag
            name (str): clan's name
            clan_lvl (int): clan's clan level
            members (list): list of clan's war league eligable members
                CWLClanMember
    """

    def __init__(self, tag, name, clan_lvl, members):
        self.tag = tag
        self.name = name
        self.clan_lvl = clan_lvl
        self.members = members


class CWLClanMember(object):
    """
    CWLClanMember
        Instance Attributes
            tag (str): clan member's player tag
            name (str): clan member's player name
            th_lvl (int): clan member's player home town hall level
    """

    def __init__(self, tag, name, th_lvl):
        self.tag = tag
        self.name = name
        self.th_lvl = th_lvl


def get(clan_tag, header):
    """Takes in a clan tag and returns the associated CWL group"""
    group_json = json_response(clan_tag, header)

    # grab a list of the clans
    clans = []
    for clan in group_json['clans']:
        # grab a list of the members in the clan
        members = []
        for member in clan['members']:
            members.append(CWLClanMember(
                member['tag'], member['name'], member['townHallLevel'])
            )
        clans.append(CWLClan(
            clan['tag'], clan['name'], clan['clanLevel'], members)
        )

    # grab a list of the rounds
    rounds = []
    for cwl_round in group_json['rounds']:
        war_tags = []
        for war_tag in cwl_round['warTags']:
            war_tags.append(war_tag)
        rounds.append(war_tags)

    return CWLGroup(group_json['state'], group_json['season'], clans, rounds)


def json_response(tag, header):
    tag = tag[1:]
    url = f'https://api.clashofclans.com/v1/clans/%23{tag}'\
        '/currentwar/leaguegroup'
    return requests.get(url, headers=header).json()
