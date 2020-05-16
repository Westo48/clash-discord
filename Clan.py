import requests
import json
import re


class Clan(object):

    """
    Clan
        Instance Attributes
            tag: str
            name: str
            clan_type: str
            description: str
            clan_lvl: int
            donation_upgrade: int
            clan_points: int
            clan_vs_points: int
            required_trophies: int
            war_frequency: str
            war_win_streak: int
            war_wins: int
            war_ties: int
            war_losses: int
            is_war_log_public: bool
            war_league_id: int
            war_league_name: str
            members: list
                ClanMember objects
    """

    def __init__(
        self, tag, name, clan_type, description, clan_lvl, donation_upgrade,
        clan_points, clan_vs_points, required_trophies,
        war_frequency, war_win_streak, war_wins, war_ties, war_losses,
        is_war_log_public, war_league_id, war_league_name, members
    ):
        self.tag = tag
        self.name = name
        self.clan_type = clan_type
        self.description = description
        self.clan_lvl = clan_lvl
        self.donation_upgrade = donation_upgrade
        self.clan_points = clan_points
        self.clan_vs_points = clan_vs_points
        self.required_trophies = required_trophies
        self.war_frequency = war_frequency
        self.war_win_streak = war_win_streak
        self.war_wins = war_wins
        self.war_ties = war_ties
        self.war_losses = war_losses
        self.is_war_log_public = is_war_log_public
        self.war_league_id = war_league_id
        self.war_league_name = war_league_name
        self.members = members

    # returns the player tag of the member
    def find_member(self, member_name):
        # formatting the name from '-' to ' '
        member_name = re.sub('[-]', ' ', member_name)
        # search through all members in the clan
        for member in self.members:
            if member.name.lower() == member_name.lower():
                return member.tag
        return ''


class ClanMember(object):
    """
    ClanMember
        Instance Attributes
            tag (str): The clan member's player tag
            name (str): The clan member's player name
            role (str): The clan member's role in the clan
            exp_lvl (int): The clan member's player experience level
            league_id (int): The clan member's player league ID
            league_name (str): The clan member's player league name
            trophies (int): The clan member's player trophie count
            vs_trophies (int): The clan member's player versus trophie count
            clan_rank (int): The clan member's rank in the clan
                current season
            previous_clan_rank (int): The clan member's prior rank in the clan
                current season
            donations (int): The clan member's donations given
                current season
            donations_received (int): The clan member's donations received
                current season
    """

    def __init__(
        self, tag, name, role, exp_lvl, league_id, league_name,
        trophies, vs_trophies, clan_rank, previous_clan_rank,
        donations, donations_received
    ):
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


def get(clan_tag, header):
    """Takes in the clan's tag and returns a Clan object"""

    clan_json = json_response(clan_tag, header)
    if clan_json['clanLevel'] < 5:
        donation_upgrade = 0
    elif clan_json['clanLevel'] < 10:
        donation_upgrade = 1
    else:
        donation_upgrade = 2

    members = []
    for member in clan_json['memberList']:
        if 'versusTrophies' not in clan_json:
            vs_trophies = 0
        else:
            vs_trophies = member['versusTrophies']
        members.append(ClanMember(
            member['tag'], member['name'], member['role'], member['expLevel'],
            member['league']['id'], member['league']['name'],
            member['trophies'], vs_trophies, member['clanRank'],
            member['previousClanRank'], member['donations'],
            member['donationsReceived'])
        )

    return Clan(
        clan_json['tag'], clan_json['name'], clan_json['type'],
        clan_json['description'], clan_json['clanLevel'], donation_upgrade,
        clan_json['clanPoints'], clan_json['clanVersusPoints'],
        clan_json['requiredTrophies'], clan_json['warFrequency'],
        clan_json['warWinStreak'], clan_json['warWins'], clan_json['warTies'],
        clan_json['warLosses'], clan_json['isWarLogPublic'],
        clan_json['warLeague']['id'], clan_json['warLeague']['name'], members
    )


def json_response(tag, header):
    tag = tag[1:]
    url = f'https://api.clashofclans.com/v1/clans/%23{tag}'
    return requests.get(url, headers=header).json()
