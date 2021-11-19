import math
import Clan
from Player import super_troop_list
import ClashResponder as clash_responder


# PLAYER

def player_verification(db_player_obj, user_obj, header):
    """
        verifying a player
        and returning verification payload

        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            header (dict): clash api key header

        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj)
    """

    if not db_player_obj:
        # user active player not found
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "no active player claimed",
                'value': user_obj.mention
            }],
            'player_obj': None
        }

    player_obj = clash_responder.get_player(
        db_player_obj.player_tag, header)
    if not player_obj:
        # player with tag from db not found
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "could not find player",
                'value': db_player_obj.player_tag
            }],
            'player_obj': None
        }

    verification_payload = {
        'verified': True,
        'field_dict_list': None,
        'player_obj': player_obj
    }
    return verification_payload


def player_clan_verification(db_player_obj, user_obj, header):
    """
        verifying a player is in a clan
        and returning verification payload

        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            header (dict): clash api key header

        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj)
    """

    player_verification_payload = (player_verification(
        db_player_obj, user_obj, header))
    if not player_verification_payload['verified']:
        return player_verification_payload

    player_obj = player_verification_payload['player_obj']
    if not player_obj.clan_tag:
        # player not in a clan
        return {
            'verified': False,
            'field_dict_list': [{
                'name': (f"{player_obj.name} "
                         f"{player_obj.tag}"),
                'value': "not in a clan"
            }],
            'player_obj': player_obj
        }

    verification_payload = {
        'verified': True,
        'field_dict_list': None,
        'player_obj': player_obj
    }
    return verification_payload


def player_leadership_verification(db_player_obj, user_obj, header):
    """
        verifying a player is in a clan and leadership
        and returning verification payload

        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            header (dict): clash api key header

        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj)
    """

    player_clan_verification_payload = (player_clan_verification(
        db_player_obj, user_obj, header))
    if not player_clan_verification_payload['verified']:
        return player_clan_verification_payload

    player_obj = player_clan_verification_payload['player_obj']
    if player_obj.role != "leader" and player_obj.role != "coLeader":
        # player not leader or coleader
        return {
            'verified': False,
            'field_dict_list': [{
                'name': (f"{player_obj.name} "
                         f"{player_obj.tag}"),
                'value': "not in leadership"
            }],
            'player_obj': player_obj
        }

    verification_payload = {
        'verified': True,
        'field_dict_list': None,
        'player_obj': player_obj
    }
    return verification_payload


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

    if player_obj.war_preference:
        field_dict_list.append({
            'name': '**War Preference**',
            'value': "in",
            'inline': True
        })
    else:
        field_dict_list.append({
            'name': '**War Preference**',
            'value': "out",
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
            'name': player_obj.name,
            'value': f"has no active super troops"
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

def clan_verification(db_player_obj, user_obj, header):
    """
        verifying a clan
        and returning verification payload

        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            header (dict): clash api key header

        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj, clan_obj)
    """

    player_clan_verification_payload = (player_clan_verification(
        db_player_obj, user_obj, header))
    if not player_clan_verification_payload['verified']:
        return player_clan_verification_payload

    player_obj = player_clan_verification_payload['player_obj']

    clan_obj = clash_responder.get_clan(
        player_obj.clan_tag, header)
    if not clan_obj:
        # clan with tag from player not found
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "could not find clan",
                'value': player_obj.clan_tag
            }],
            'player_obj': player_obj,
            'clan_obj': clan_obj
        }

    verification_payload = {
        'verified': True,
        'field_dict_list': None,
        'player_obj': player_obj,
        'clan_obj': clan_obj
    }
    return verification_payload


def clan_lineup(clan_obj, header):
    clan_lineup_dict = clash_responder.clan_lineup(clan_obj, header)

    field_dict_list = []

    for th in clan_lineup_dict:
        if clan_lineup_dict[th] > 0:
            field_dict_list.append({
                'name': f"Town Hall {th}",
                'value': f"{clan_lineup_dict[th]}",
                'inline': False
            })

    return field_dict_list


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


def clan_war_preference(clan_obj, header):
    in_count = 0
    for member in clan_obj.members:
        player_obj = clash_responder.get_player(member.tag, header)
        if player_obj.war_preference:
            in_count += 1

    field_dict_list = []

    field_dict_list.append({
        'name': "in",
        'value': f"{in_count}",
        'inline': False
    })
    field_dict_list.append({
        'name': "out",
        'value': f"{len(clan_obj.members) - in_count}",
        'inline': False
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
            'name': clan_obj.name,
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
            'name': donator.player.name,
            'value': value
        })

    return field_dict_list


def super_troop_search(clan_obj, donor_list, unit_name):
    if len(donor_list) == 0:
        return [{
            'name': clan_obj.name,
            'value': f"does not have {unit_name} activated"
        }]

    field_dict_list = []
    for donator in donor_list:
        field_dict_list.append({
            'name': donator.name,
            'value': f"has {unit_name} active"
        })

    return field_dict_list


# WAR

def war_verification(db_player_obj, user_obj, header):
    """
        verifying a war
        and returning verification payload

        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            header (dict): clash api key header

        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj, war_obj)
    """

    player_clan_verification_payload = (player_clan_verification(
        db_player_obj, user_obj, header))

    if not player_clan_verification_payload['verified']:
        return player_clan_verification_payload

    player_obj = player_clan_verification_payload['player_obj']

    war_obj = clash_responder.get_war(
        player_obj.clan_tag, header)
    if not war_obj:
        # clan is not in war
        return {
            'verified': False,
            'field_dict_list': [{
                'name': (f"{player_obj.clan_name} "
                         f"{player_obj.clan_tag}"),
                'value': "not in war"
            }],
            'player_obj': player_obj,
            'war_obj': None
        }

    verification_payload = {
        'verified': True,
        'field_dict_list': None,
        'player_obj': player_obj,
        'war_obj': war_obj
    }
    return verification_payload


def war_leadership_verification(db_player_obj, user_obj, header):
    """
        verifying a war through player_leadership_verification
        and returning verification payload

        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            header (dict): clash api key header

        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj, war_obj)
    """

    player_leadership_verification_payload = (player_leadership_verification(
        db_player_obj, user_obj, header))

    if not player_leadership_verification_payload['verified']:
        return player_leadership_verification_payload

    player_obj = player_leadership_verification_payload['player_obj']

    war_obj = clash_responder.get_war(
        player_obj.clan_tag, header)
    if not war_obj:
        # clan is not in war
        return {
            'verified': False,
            'field_dict_list': [{
                'name': (f"{player_obj.clan_name} "
                         f"{player_obj.clan_tag}"),
                'value': "not in war"
            }],
            'player_obj': player_obj,
            'war_obj': None
        }

    verification_payload = {
        'verified': True,
        'field_dict_list': None,
        'player_obj': player_obj,
        'war_obj': war_obj
    }
    return verification_payload


# returns a string of the war overview
def war_overview(war_obj):
    if not war_obj:
        return [{
            'name': f"not in war",
            'value': f"you are not in war"
        }]

    if war_obj.state == "preparation":
        time_string = war_obj.string_date_time()

        return [{
            'name': f"{time_string}",
            'value': f"left before war starts"
        }]
    elif war_obj.state == "inWar":
        time_string = war_obj.string_date_time()
        scoreboard_string = war_obj.string_scoreboard()

        return [{
            'name': f"{war_obj.clan.name} is {scoreboard_string}",
            'value': f"{time_string} left in war"
        }]
    elif war_obj.state == "warEnded":
        scoreboard_string = war_obj.string_scoreboard()

        return [{
            'name': f"{war_obj.clan.name} {scoreboard_string}",
            'value': f"war has ended"
        }]
    else:
        return [{
            'name': f"not in war",
            'value': f"you are not in war"
        }]


def war_time(war_obj):
    if war_obj.state == "preparation":
        time_string = war_obj.string_date_time()

        return [{
            'name': f"{time_string}",
            'value': f"left before war starts"
        }]
    elif war_obj.state == "inWar":
        time_string = war_obj.string_date_time()

        return [{
            'name': f"{time_string}",
            'value': f"left in war"
        }]
    elif war_obj.state == "warEnded":
        return [{
            'name': f"war ended",
            'value': f"war with {war_obj.opponent.name} has ended"
        }]
    else:
        return [{
            'name': f"not in war",
            'value': f"you are not in war"
        }]


# todo if nobody has attacked logic
# returns a string of the war no attack response
def war_no_attack(war_obj):
    if war_obj.state == "preparation":
        time_string = war_obj.string_date_time()

        return [{
            'name': f"{time_string}",
            'value': f"left before war starts, nobody has attacked"
        }]

    elif war_obj.state == "inWar":
        no_attack_list = war_obj.no_attack()
        if len(no_attack_list) == 0:
            return [{
                'name': f"no missed attacks",
                'value': (f"all {war_obj.team_size} {war_obj.clan.name} "
                          f"war members attacked")
            }]
        field_dict_list = []
        for member in no_attack_list:
            field_dict_list.append({
                'name': f"{member.name}",
                'value': f"is missing attacks"
            })
        return field_dict_list

    elif war_obj.state == "warEnded":
        no_attack_list = war_obj.no_attack()
        if len(no_attack_list) == 0:
            return [{
                'name': f"no missed attacks",
                'value': (f"all {war_obj.team_size} {war_obj.clan.name} "
                          f"war members attacked")
            }]
        field_dict_list = []
        for member in no_attack_list:
            field_dict_list.append({
                'name': f"{member.name}",
                'value': f"missed attacks"
            })
        return field_dict_list

    else:
        return [{
            'name': f"not in war",
            'value': f"you are not in war"
        }]


# returns a list of all war members and their stars
def war_members_overview(war_obj):
    "returns a list of all war members and their stars"

    if war_obj.state == "preparation":
        time_string = war_obj.string_date_time()

        return [{
            'name': f"{time_string}",
            'value': f"left before war starts, nobody has attacked"
        }]
    elif war_obj.state == "inWar":
        field_dict_list = []
        for member in war_obj.clan.members:
            if len(member.attacks) == 0:
                # no atk response
                field_dict_list.append({
                    'name': f"{member.map_position}. {member.name}",
                    'value': f"has not attacked"
                })
            else:
                field_dict_list.append({
                    'name': f"{member.map_position}. {member.name}",
                    'value': (
                        f"attacked {len(member.attacks)} "
                        f"{member.string_member_attack_times()} for "
                        f"{member.stars} {member.string_member_stars()}"
                    )
                })
        return field_dict_list
    elif war_obj.state == "warEnded":
        for member in war_obj.clan.members:
            field_dict_list = []
            if len(member.attacks) == 0:
                # no atk response
                field_dict_list.append({
                    'name': f"{member.map_position}. {member.name}",
                    'value': f"did not attack"
                })
            else:
                field_dict_list.append({
                    'name': f"{member.map_position}. {member.name}",
                    'value': (
                        f"attacked {len(member.attacks)} "
                        f"{member.string_member_attack_times()} for "
                        f"{member.stars} {member.string_member_stars()}"
                    )
                })
        return field_dict_list
    else:
        return [{
            'name': f"not in war",
            'value': f"you are not in war"
        }]


# returns a list of war attack string responses for all war members
def war_all_attacks(war_obj):

    if war_obj.state == 'preparation':
        time_string = war_obj.string_date_time()

        return [{
            'name': f"{time_string}",
            'value': f"left before war starts, nobody has attacked"
        }]
    elif war_obj.state == 'inWar':
        field_dict_list = []

        for member in war_obj.clan.members:
            if len(member.attacks) == 0:
                # no atk response
                field_dict_list.append({
                    'name': f"{member.map_position}. {member.name}",
                    'value': f"has not attacked"
                })
            else:
                for attack in member.attacks:

                    defender = war_obj.find_defender(attack.defender_tag)

                    if attack.stars == 0 or attack.stars == 3:
                        value_string = (
                            f"{attack.stars} {attack.string_attack_stars()} "
                            f"against {defender.map_position}. "
                            f"{defender.name} TH {defender.th_lvl}"
                        )
                    else:
                        value_string = (
                            f"{attack.stars} {attack.string_attack_stars()}, "
                            f"{round(attack.destruction_percent, 2)}% "
                            f"against {defender.map_position}. "
                            f"{defender.name} TH {defender.th_lvl}"
                        )
                    field_dict_list.append({
                        'name': f"{member.map_position}. {member.name}",
                        'value': value_string
                    })
        return field_dict_list

    elif war_obj.state == 'warEnded':
        field_dict_list = []

        for member in war_obj.clan.members:
            if len(member.attacks) == 0:
                # no atk response
                field_dict_list.append({
                    'name': (f"{member.map_position}. {member.name} "
                             f"TH {member.th_lvl}"),
                    'value': f"did not attack"
                })
            else:
                for attack in member.attacks:

                    defender = war_obj.find_defender(attack.defender_tag)

                    if attack.stars == 0 or attack.stars == 3:
                        value_string = (
                            f"{attack.stars} {attack.string_attack_stars()} "
                            f"against {defender.map_position}. "
                            f"{defender.name} TH {defender.th_lvl}"
                        )
                    else:
                        value_string = (
                            f"{attack.stars} {attack.string_attack_stars()}, "
                            f"{round(attack.destruction_percent, 2)}% "
                            f"against {defender.map_position}. "
                            f"{defender.name} TH {defender.th_lvl}"
                        )
                    field_dict_list.append({
                        'name': f"{member.map_position}. {member.name}",
                        'value': value_string
                    })
        return field_dict_list

    else:
        return [{
            'name': f"not in war",
            'value': f"you are not in war"
        }]


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

def cwl_group_verification(db_player_obj, user_obj, header):
    """
        verifying a cwl group
        and returning verification payload
        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            header (dict): clash api key header
        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj, cwl_group_obj)
    """

    player_clan_verification_payload = (player_clan_verification(
        db_player_obj, user_obj, header))

    if not player_clan_verification_payload['verified']:
        return player_clan_verification_payload

    player_obj = player_clan_verification_payload['player_obj']

    cwl_group_obj = clash_responder.get_cwl_group(
        player_obj.clan_tag, header)
    if not cwl_group_obj:
        # clan is not in cwl
        return {
            'verified': False,
            'field_dict_list': [{
                'name': (f"{player_obj.clan_name} "
                         f"{player_obj.clan_tag}"),
                'value': "not in cwl"
            }],
            'player_obj': player_obj,
            'cwl_group_obj': None
        }

    verification_payload = {
        'verified': True,
        'field_dict_list': None,
        'player_obj': player_obj,
        'cwl_group_obj': cwl_group_obj
    }
    return verification_payload


def cwl_group_leadership_verification(db_player_obj, user_obj, header):
    """
        verifying a cwl group through player_leadership_verification
        and returning verification payload
        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            header (dict): clash api key header
        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj, cwl_group_obj)
    """

    player_leadership_verification_payload = (player_leadership_verification(
        db_player_obj, user_obj, header))

    if not player_leadership_verification_payload['verified']:
        return player_leadership_verification_payload

    player_obj = player_leadership_verification_payload['player_obj']

    cwl_group_obj = clash_responder.get_cwl_group(
        player_obj.clan_tag, header)
    if not cwl_group_obj:
        # clan is not in cwl
        return {
            'verified': False,
            'field_dict_list': [{
                'name': (f"{player_obj.clan_name} "
                         f"{player_obj.clan_tag}"),
                'value': "not in cwl"
            }],
            'player_obj': player_obj,
            'cwl_group_obj': None
        }

    verification_payload = {
        'verified': True,
        'field_dict_list': None,
        'player_obj': player_obj,
        'cwl_group_obj': cwl_group_obj
    }
    return verification_payload


def cwl_lineup(cwl_group):
    message = (
        "```\n"
        "CWL Group Lineup\n"
        "14 | 13 | 12 | 11 | 10 | 9  | 8\n"
        "-------------------------------\n"
    )
    for clan in cwl_group.clans:
        lineup_message = f"{clan.name}\n"
        clan_lineup_dict = clash_responder.cwl_clan_lineup(clan)
        for th in clan_lineup_dict:
            if th >= 8:
                lineup_message += f"{clan_lineup_dict[th]}"
                if clan_lineup_dict[th] >= 10:
                    # if it is a double digit number
                    lineup_message += " | "
                else:
                    # if it is a single digit number add an extra space
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
        return [{
            'name': "you are not in CWL",
            'value': "there is no score"
        }]

    # get a list of all CWLWar objects
    cwl_wars = []
    for cwl_round in cwl_group.rounds:
        cwl_war = cwl_group.find_specified_war(
            clan_tag, cwl_group.rounds.index(cwl_round), header)
        if not cwl_war == '#0':
            if cwl_war.state == 'warEnded':
                cwl_wars.append(cwl_war)

    if len(cwl_wars) < 2:
        return [{
            'name': "not enough wars",
            'value': "please wait till round two has ended to score members"
        }]

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
                        scored_member.war_count, len(cwl_wars))
                    scored_member.score = avg_score * participation_multiplier
                    cwl_war_members.append(scored_member)

    sorted_cwl_war_members = sorted(
        cwl_war_members, key=lambda member: member.score, reverse=True)
    field_dict_list = []
    for member in sorted_cwl_war_members:
        field_dict_list.append({
            'name': member.name,
            'value': f"{round(member.score, 3)}"
        })
    return field_dict_list


# returns each specified member's CWL War score
def cwl_member_standing(player_obj, cwl_group, clan_tag, header):
    if not cwl_group:
        return [{
            'name': "{player_obj.name} is not in CWL",
            'value': "there is no score"
        }]

    # get a list of all CWLWar objects
    cwl_wars = []
    for cwl_round in cwl_group.rounds:
        cwl_war = cwl_group.find_specified_war(
            clan_tag, cwl_group.rounds.index(cwl_round), header)
        if not cwl_war == '#0':
            if cwl_war.state == 'warEnded':
                cwl_wars.append(cwl_war)

    if len(cwl_wars) < 2:
        return [{
            'name': "not enough wars",
            'value': "please wait till round two has ended to score members"
        }]

    member_round_scores = []
    # find your clan
    found = False
    for clan in cwl_group.clans:
        if clan.tag == clan_tag:
            cwl_group_clan = clan
            found = True
            break
    if not found:
        return [{
            'name': clan_tag,
            'value': f"not found in cwl group"
        }]

    found = False
    for member in cwl_group_clan.members:
        if member.tag == player_obj.tag:
            found = True
            break
    if not found:
        return [{
            'name': f"{player_obj.name}",
            'value': f"not found in cwl group"
        }]

    for war in cwl_wars:
        for war_member in war.clan.members:
            if war_member.tag == player_obj.tag:
                member_round_scores.append(war_member.score)
                break

    if len(member_round_scores) == 0:
        return [{
            'name': f"{player_obj.name}",
            'value': f"did not participate in any wars"
        }]

    elif len(member_round_scores) == 1:
        return [{
            'name': f"{round(member_round_scores[0], 3)}",
            'value': f"for 1 war"
        }]

    else:
        total_score = 0
        for round_score in member_round_scores:
            total_score += round_score
        avg_score = total_score / len(member_round_scores)
        participation_multiplier = math.log(
            len(member_round_scores), len(cwl_wars))
        member_score = avg_score * participation_multiplier

        field_dict_list = [{
            'name': f"{round(member_score, 3)}",
            'value': f"overall score for {len(member_round_scores)} wars"
        }]
        for cwl_round_score in member_round_scores:
            field_dict_list.append({
                'name': f"{round(cwl_round_score, 3)}",
                'value': f"score"
            })

        return field_dict_list


# CWL WAR

def cwl_war_verification(db_player_obj, user_obj, header):
    """
        verifying a cwl war
        and returning verification payload
        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            header (dict): clash api key header
        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj, cwl_war_obj)
    """

    cwl_group_verification_payload = (cwl_group_verification(
        db_player_obj, user_obj, header))

    if not cwl_group_verification_payload['verified']:
        return cwl_group_verification_payload

    player_obj = cwl_group_verification_payload['player_obj']
    cwl_group_obj = cwl_group_verification_payload['cwl_group_obj']

    cwl_war_obj = cwl_group_obj.find_current_war(
        player_obj.clan_tag, header)

    if not cwl_war_obj:
        # clan is not in cwl war
        return {
            'verified': False,
            'field_dict_list': [{
                'name': (f"{player_obj.clan_name} "
                         f"{player_obj.clan_tag}"),
                'value': "not in cwl"
            }],
            'player_obj': player_obj,
            'cwl_war_obj': None
        }

    verification_payload = {
        'verified': True,
        'field_dict_list': None,
        'player_obj': player_obj,
        'cwl_war_obj': cwl_war_obj
    }
    return verification_payload


def cwl_war_leadership_verification(db_player_obj, user_obj, header):
    """
        verifying a cwl war through cwl_group_leadership_verification
        and returning verification payload
        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            header (dict): clash api key header
        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj, cwl_war_obj)
    """

    cwl_group_leadership_verification_payload = (
        cwl_group_leadership_verification(
            db_player_obj, user_obj, header))

    if not cwl_group_leadership_verification_payload['verified']:
        return cwl_group_leadership_verification_payload

    player_obj = cwl_group_leadership_verification_payload['player_obj']
    cwl_group_obj = cwl_group_leadership_verification_payload['cwl_group_obj']

    cwl_war_obj = cwl_group_obj.find_current_war(
        player_obj.clan_tag, header)

    if not cwl_war_obj:
        # clan is not in cwl war
        return {
            'verified': False,
            'field_dict_list': [{
                'name': (f"{player_obj.clan_name} "
                         f"{player_obj.clan_tag}"),
                'value': "not in cwl"
            }],
            'player_obj': player_obj,
            'cwl_war_obj': None
        }

    verification_payload = {
        'verified': True,
        'field_dict_list': None,
        'player_obj': player_obj,
        'cwl_war_obj': cwl_war_obj
    }
    return verification_payload


# DISCORD

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
            url=thumbnail['small'])

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


# help

def help_main(db_guild_obj, db_player_obj, player_obj, bot_categories):
    help_dict = {
        'field_dict_list': [],
        'emoji_list': []
    }
    if not db_guild_obj:
        for category in bot_categories:
            if category.brief == "client":
                help_dict['field_dict_list'].append({
                    'name': category.name,
                    'value': category.description
                })
                help_dict['emoji_list'].append(category.emoji)
                return help_dict

    for category in bot_categories:
        if (
            category.brief == "discord" and
            not player_obj or
            category.brief == "player" and
            not player_obj or
            category.brief == "clan" and
            not player_obj or
            category.brief == "war" and
            not player_obj or
            category.brief == "cwlgroup" and
            not player_obj or
            category.brief == "cwlwar" and
            not player_obj
        ):
            continue
        help_dict['field_dict_list'].append({
            'name': f"{category.emoji} {category.name}",
            'value': category.description
        })
        help_dict['emoji_list'].append(category.emoji)
    return help_dict


def help_emoji_to_category(emoji, bot_categories):
    for category in bot_categories:
        if category.emoji == emoji:
            return category
    return None


def help_switch(db_guild_obj, db_player_obj, player_obj, user_id, emoji,
                bot_category, bot_categories, all_commands):
    if not bot_category:
        return help_main(db_guild_obj, db_player_obj, player_obj, bot_categories)
    if bot_category.brief == "client":
        return help_client(db_guild_obj, user_id, bot_category, all_commands)
    if bot_category.brief == "discord":
        return help_discord(player_obj, bot_category, all_commands)
    if bot_category.brief == "player":
        return help_player(player_obj, bot_category, all_commands)
    if bot_category.brief == "clan":
        return help_clan(player_obj, bot_category, all_commands)
    if bot_category.brief == "war":
        return help_war(player_obj, bot_category, all_commands)
    if bot_category.brief == "cwlgroup":
        return help_cwlgroup(player_obj, bot_category, all_commands)
    if bot_category.brief == "cwlwar":
        return help_cwlwar(player_obj, bot_category, all_commands)
    return help_main(db_guild_obj, db_player_obj, player_obj, bot_categories)


def help_client(db_guild_obj, user_id, bot_category, all_commands):
    help_dict = {
        'field_dict_list': [],
        'emoji_list': []
    }
    for command_name in all_commands:
        # if the command is in the correct category
        if not bot_category.brief == all_commands[command_name].brief:
            continue
        # if the command is the main command and not an alias
        if command_name != all_commands[command_name].name:
            continue
        # if the command should be shown
        if db_guild_obj:
            if (all_commands[command_name].hidden and
                    db_guild_obj.admin_user_id != user_id):
                continue
            field_name = f"{all_commands[command_name].name}"
            for param in all_commands[command_name].clean_params:
                field_name += f" <{param}>"
            help_dict['field_dict_list'].append({
                'name': field_name,
                'value': all_commands[command_name].description
            })
        if len(help_dict['field_dict_list']) == 0:
            help_dict['field_dict_list'].append({
                'name': "guild not claimed",
                'value': "please claim guild using `!claimguild`"
            })
    return help_dict


def help_discord(player_obj, bot_category, all_commands):
    help_dict = {
        'field_dict_list': [],
        'emoji_list': []
    }
    for command_name in all_commands:
        # if the command is in the correct category
        if not bot_category.brief == all_commands[command_name].brief:
            continue
        # if the command is the main command and not an alias
        if command_name != all_commands[command_name].name:
            continue
        # if there is a player
        if not player_obj:
            continue
        # if the command should be shown
        if (all_commands[command_name].hidden and
                (player_obj.role != "leader" and player_obj.role != "coLeader")):
            continue
        field_name = f"{all_commands[command_name].name}"
        for param in all_commands[command_name].clean_params:
            field_name += f" <{param}>"
        help_dict['field_dict_list'].append({
            'name': field_name,
            'value': all_commands[command_name].description
        })
    return help_dict


def help_player(player_obj, bot_category, all_commands):
    help_dict = {
        'field_dict_list': [],
        'emoji_list': []
    }
    for command_name in all_commands:
        # if the command is in the correct category
        if not bot_category.brief == all_commands[command_name].brief:
            continue
        # if the command is the main command and not an alias
        if command_name != all_commands[command_name].name:
            continue
        # if there is a player
        if not player_obj:
            continue
        # if the command should be shown
        if (all_commands[command_name].hidden and
                (player_obj.role != "leader" and player_obj.role != "coLeader")):
            continue
        field_name = f"{all_commands[command_name].name}"
        for param in all_commands[command_name].clean_params:
            field_name += f" <{param}>"
        help_dict['field_dict_list'].append({
            'name': field_name,
            'value': all_commands[command_name].description
        })
    return help_dict


def help_clan(player_obj, bot_category, all_commands):
    help_dict = {
        'field_dict_list': [],
        'emoji_list': []
    }
    for command_name in all_commands:
        # if the command is in the correct category
        if not bot_category.brief == all_commands[command_name].brief:
            continue
        # if the command is the main command and not an alias
        if command_name != all_commands[command_name].name:
            continue
        # if there is a player
        if not player_obj:
            continue
        # if the command should be shown
        if (all_commands[command_name].hidden and
                (player_obj.role != "leader" and player_obj.role != "coLeader")):
            continue
        field_name = f"{all_commands[command_name].name}"
        for param in all_commands[command_name].clean_params:
            field_name += f" <{param}>"
        help_dict['field_dict_list'].append({
            'name': field_name,
            'value': all_commands[command_name].description
        })
    return help_dict


def help_war(player_obj, bot_category, all_commands):
    help_dict = {
        'field_dict_list': [],
        'emoji_list': []
    }
    for command_name in all_commands:
        # if the command is in the correct category
        if not bot_category.brief == all_commands[command_name].brief:
            continue
        # if the command is the main command and not an alias
        if command_name != all_commands[command_name].name:
            continue
        # if there is a player
        if not player_obj:
            continue
        # if the command should be shown
        if (all_commands[command_name].hidden and
                (player_obj.role != "leader" and player_obj.role != "coLeader")):
            continue
        field_name = f"{all_commands[command_name].name}"
        for param in all_commands[command_name].clean_params:
            field_name += f" <{param}>"
        help_dict['field_dict_list'].append({
            'name': field_name,
            'value': all_commands[command_name].description
        })
    return help_dict


def help_cwlgroup(player_obj, bot_category, all_commands):
    help_dict = {
        'field_dict_list': [],
        'emoji_list': []
    }
    for command_name in all_commands:
        # if the command is in the correct category
        if not bot_category.brief == all_commands[command_name].brief:
            continue
        # if the command is the main command and not an alias
        if command_name != all_commands[command_name].name:
            continue
        # if there is a player
        if not player_obj:
            continue
        # if the command should be shown
        if (all_commands[command_name].hidden and
                (player_obj.role != "leader" and player_obj.role != "coLeader")):
            continue
        field_name = f"{all_commands[command_name].name}"
        for param in all_commands[command_name].clean_params:
            field_name += f" <{param}>"
        help_dict['field_dict_list'].append({
            'name': field_name,
            'value': all_commands[command_name].description
        })
    return help_dict


def help_cwlwar(player_obj, bot_category, all_commands):
    help_dict = {
        'field_dict_list': [],
        'emoji_list': []
    }
    for command_name in all_commands:
        # if the command is in the correct category
        if not bot_category.brief == all_commands[command_name].brief:
            continue
        # if the command is the main command and not an alias
        if command_name != all_commands[command_name].name:
            continue
        # if there is a player
        if not player_obj:
            continue
        # if the command should be shown
        if (all_commands[command_name].hidden and
                (player_obj.role != "leader" and player_obj.role != "coLeader")):
            continue
        field_name = f"{all_commands[command_name].name}"
        for param in all_commands[command_name].clean_params:
            field_name += f" <{param}>"
        help_dict['field_dict_list'].append({
            'name': field_name,
            'value': all_commands[command_name].description
        })
    return help_dict


# roles


# old

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
