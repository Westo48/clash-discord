import math
from coc import NotFound, Maintenance, PrivateWarLog, GatewayError
import data.RazBot_Data as RazBot_Data
import responders.ClashResponder as clash_responder
import responders.RazBotDB_Responder as db_responder
from disnake.utils import get


# CLIENT


def get_client_discord_id():
    """
        returns RazBot_Data client discord id
    """

    return RazBot_Data.RazBot_Data().discord_id


def get_client_token():
    """
        returns RazBot_Data client token
    """

    return RazBot_Data.RazBot_Data().token


def get_client_test_guilds():
    """
        returns RazBot_Data client test guilds
    """

    test_guilds = RazBot_Data.RazBot_Data().test_guilds

    if len(test_guilds) > 0:
        return test_guilds

    else:
        return None


def get_client_email():
    """
        returns RazBot_Data client coc email
    """

    return RazBot_Data.RazBot_Data().coc_dev_email


def get_client_password():
    """
        returns RazBot_Data client coc password
    """

    return RazBot_Data.RazBot_Data().coc_dev_password


# PLAYER


async def player_verification(db_player_obj, user_obj, coc_client):
    """
        verifying a player
        and returning verification payload

        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            coc_client (obj): coc.py client

        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj)
    """

    # user active player not found
    if not db_player_obj:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "no active player claimed",
                'value': user_obj.mention
            }],
            'player_obj': None
        }

    try:
        player_obj = await coc_client.get_player(db_player_obj.player_tag)
    except Maintenance:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "Clash of Clans is under maintenance",
                'value': "please try again later"
            }],
            'player_obj': None
        }
    except NotFound:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "could not find player",
                'value': db_player_obj.player_tag
            }],
            'player_obj': None
        }
    except GatewayError:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "coc.py ran into a gateway error",
                'value': "please try again later"
            }],
            'player_obj': None
        }

    verification_payload = {
        'verified': True,
        'field_dict_list': None,
        'player_obj': player_obj
    }
    return verification_payload


async def player_clan_verification(db_player_obj, user_obj, coc_client):
    """
        verifying a player is in a clan
        and returning verification payload

        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            coc_client (obj): coc.py client

        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj)
    """

    player_verification_payload = (await player_verification(
        db_player_obj, user_obj, coc_client))

    # player verification failed
    # player in maintenance or not found
    if not player_verification_payload['verified']:
        return player_verification_payload

    player_obj = player_verification_payload['player_obj']

    # player not in a clan
    if not player_obj.clan:
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


async def player_leadership_verification(db_player_obj, user_obj, coc_client):
    """
        verifying a player is in a clan and leadership
        and returning verification payload

        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            coc_client (obj): coc.py client

        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj)
    """

    player_clan_verification_payload = (await player_clan_verification(
        db_player_obj, user_obj, coc_client))

    # player clan verification failed
    # player clash in maintenance, not found, or player not in clan
    if not player_clan_verification_payload['verified']:
        return player_clan_verification_payload

    player_obj = player_clan_verification_payload['player_obj']
    # player not leader or coleader
    if (player_obj.role.value != "leader" and
            player_obj.role.value != "coLeader"):
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
        'value': player_obj.exp_level,
        'inline': True
    })
    field_dict_list.append({
        'name': '**TH Lvl**',
        'value': player_obj.town_hall,
        'inline': True
    })
    if player_obj.town_hall_weapon:
        field_dict_list.append({
            'name': '**TH Weapon Lvl**',
            'value': player_obj.town_hall_weapon,
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
    if player_obj.legend_statistics:
        field_dict_list.append({
            'name': '**Legend Trophies**',
            'value': player_obj.legend_statistics.legend_trophies,
            'inline': True
        })
        if player_obj.legend_statistics.best_season:
            field_dict_list.append({
                'name': '**Best Rank | Trophies**',
                'value': (
                    f"{player_obj.legend_statistics.best_season.rank} | "
                    f"{player_obj.legend_statistics.best_season.trophies}"
                ),
                'inline': True
            })
        if player_obj.legend_statistics.current_season:
            field_dict_list.append({
                'name': '**Current Rank | Trophies**',
                'value': (
                    f"{player_obj.legend_statistics.current_season.rank} | "
                    f"{player_obj.legend_statistics.current_season.trophies}"
                ),
                'inline': True
            })
        if player_obj.legend_statistics.previous_season:
            field_dict_list.append({
                'name': '**Previous Rank | Trophies**',
                'value': (
                    f"{player_obj.legend_statistics.previous_season.rank} | "
                    f"{player_obj.legend_statistics.previous_season.trophies}"
                ),
                'inline': True
            })

    field_dict_list.append({
        'name': '**War Stars**',
        'value': player_obj.war_stars,
        'inline': True
    })
    if player_obj.clan:
        field_dict_list.append({
            'name': '**Clan**',
            'value': (f"[{player_obj.clan.name}]"
                      f"({player_obj.clan.share_link})"),
            'inline': True
        })
        field_dict_list.append({
            'name': '**Clan Role**',
            'value': player_obj.role.in_game_name,
            'inline': True
        })
    else:
        field_dict_list.append({
            'name': '**Clan**',
            'value': f"{player_obj.name} is not in a clan",
            'inline': True
        })

    if player_obj.war_opted_in:
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
            hero_value = f'{hero.level}'
        elif hero.name == 'Archer Queen':
            hero_title += ' | AQ'
            hero_value += f' | {hero.level}'
        elif hero.name == 'Grand Warden':
            hero_title += ' | GW'
            hero_value += f' | {hero.level}'
        elif hero.name == 'Royal Champion':
            hero_title += ' | RC'
            hero_value += f' | {hero.level}'
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
    for pet in player_obj.hero_pets:
        if pet.name == 'L.A.S.S.I':
            pet_title = 'LA'
            pet_value = f'{pet.level}'
        elif pet.name == 'Mighty Yak':
            pet_title += ' | MY'
            pet_value += f' | {pet.level}'
        elif pet.name == 'Electro Owl':
            pet_title += ' | EO'
            pet_value += f' | {pet.level}'
        elif pet.name == 'Unicorn':
            pet_title += ' | UC'
            pet_value += f' | {pet.level}'
    if pet_title != '':
        field_dict_list.append({
            'name': f'**{pet_title}**',
            'value': pet_value,
            'inline': True
        })

    field_dict_list.append({
        'name': '**Link**',
        'value': (f"[{player_obj.name}]"
                  f"({player_obj.share_link})"),
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

    try:
        max_level_for_townhall = unit_obj.get_max_level_for_townhall(
            player_obj.town_hall)
    except:
        max_level_for_townhall = unit_obj.max_level

    # unit is max lvl
    if unit_obj.level == unit_obj.max_level:
        return {
            'name': f"{unit_obj.name} lvl {unit_obj.level}",
            'value': f"max lvl"
        }
    # unit is max for th, but not total max
    elif (unit_obj.level == max_level_for_townhall):
        return {
            'name': f"{unit_obj.name} lvl {unit_obj.level}",
            'value': (
                f"TH {player_obj.town_hall} max: {max_level_for_townhall}\n"
                f"max: {unit_obj.max_level}"
            )
        }
    # unit is not max for th nor is it total max
    else:
        # unit max is the same as th max
        if (unit_obj.max_level == max_level_for_townhall):
            return {
                'name': f"{unit_obj.name} lvl {unit_obj.level}",
                'value': f"max: {unit_obj.max_level}"
            }
        # unit max is not the same as th max
        else:
            return {
                'name': f"{unit_obj.name} lvl {unit_obj.level}",
                'value': (
                    f"TH {player_obj.town_hall} max: {max_level_for_townhall}\n"
                    f"max: {unit_obj.max_level}"
                )
            }


def unit_lvl_all(player_obj):
    field_dict_list = []
    for field_dict in hero_lvl_all(player_obj):
        field_dict_list.append(field_dict)
    for field_dict in pet_lvl_all(player_obj):
        field_dict_list.append(field_dict)
    for field_dict in troop_lvl_all(player_obj):
        field_dict_list.append(field_dict)
    for field_dict in spell_lvl_all(player_obj):
        field_dict_list.append(field_dict)
    for field_dict in siege_lvl_all(player_obj):
        field_dict_list.append(field_dict)
    return field_dict_list


def hero_lvl_all(player_obj):
    field_dict_list = []
    for hero_obj in player_obj.heroes:
        # hero isn't a home base hero
        if not hero_obj.is_home_base:
            continue
        field_dict_list.append(unit_lvl(
            player_obj, hero_obj, hero_obj.name))
    return field_dict_list


def pet_lvl_all(player_obj):
    field_dict_list = []
    for pet_obj in player_obj.hero_pets:
        # pet isn't a home base pet
        if not pet_obj.is_home_base:
            continue
        field_dict_list.append(unit_lvl(
            player_obj, pet_obj, pet_obj.name))
    return field_dict_list


def troop_lvl_all(player_obj):
    field_dict_list = []
    for troop_obj in player_obj.home_troops:
        # troop isn't a home base troop
        if not troop_obj.is_home_base:
            continue

        # troop is a super troop
        if troop_obj.is_super_troop:
            continue

        # troop is a siege
        if troop_obj.is_siege_machine:
            continue

        field_dict_list.append(unit_lvl(
            player_obj, troop_obj, troop_obj.name))
    return field_dict_list


def siege_lvl_all(player_obj):
    field_dict_list = []
    for troop_obj in player_obj.home_troops:
        # troop isn't a home base troop
        if not troop_obj.is_home_base:
            continue

        # troop is a super troop
        if troop_obj.is_super_troop:
            continue

        # troop is NOT a siege
        if not troop_obj.is_siege_machine:
            continue

        field_dict_list.append(unit_lvl(
            player_obj, troop_obj, troop_obj.name))
    return field_dict_list


def spell_lvl_all(player_obj):
    field_dict_list = []
    for spell_obj in player_obj.spells:
        # spell isn't a home base spell
        if not spell_obj.is_home_base:
            continue
        field_dict_list.append(unit_lvl(
            player_obj, spell_obj, spell_obj.name))
    return field_dict_list


def active_super_troops(player_obj, active_super_troop_list):
    if len(active_super_troop_list) == 0:
        return [{
            'name': player_obj.name,
            'value': f"has no active super troops"
        }]
    else:
        field_dict_list = []
        for troop_obj in active_super_troop_list:
            field_dict_list.append({
                'name': troop_obj.name,
                'value': f"is active"
            })
        return field_dict_list


# CLAN

async def clan_verification(db_player_obj, user_obj, coc_client):
    """
        verifying a clan
        and returning verification payload

        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            coc_client (obj): coc.py client

        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj, clan_obj)
    """

    player_clan_verification_payload = (await player_clan_verification(
        db_player_obj, user_obj, coc_client))

    # player clan verification failed
    # player clash in maintenance, not found, or player not in clan
    if not player_clan_verification_payload['verified']:
        return player_clan_verification_payload

    player_obj = player_clan_verification_payload['player_obj']

    clan_obj = await player_obj.get_detailed_clan()
    # clan with tag from player not found
    if not clan_obj:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': f"{player_obj.name} {player_obj.tag}",
                'value': "not in a clan"
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


async def clan_leadership_verification(db_player_obj, user_obj, coc_client):
    """
        verifying a clan through player_leadership_verification
        and returning verification payload

        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            coc_client (obj): coc.py client

        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj, clan)
    """

    player_leadership_verification_payload = (await player_leadership_verification(
        db_player_obj, user_obj, coc_client))

    # player leadership verification failed
    # player clash in maintenance, not found, or player not in leadership
    if not player_leadership_verification_payload['verified']:
        return player_leadership_verification_payload

    player_obj = player_leadership_verification_payload['player_obj']

    # player is not in clan
    clan_obj = await player_obj.get_detailed_clan()

    if not clan_obj:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': f"{player_obj.name} {player_obj.tag}",
                'value': "not in a clan"
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


def clan_info(clan_obj):
    field_dict_list = []

    field_dict_list.append({
        'name': "**Description**",
        'value': clan_obj.description,
        'inline': False
    })
    field_dict_list.append({
        'name': "**Members**",
        'value': clan_obj.member_count,
        'inline': True
    })
    field_dict_list.append({
        'name': "**Clan Lvl**",
        'value': clan_obj.level,
        'inline': True
    })
    field_dict_list.append({
        'name': "**Clan War League**",
        'value': clan_obj.war_league.name,
        'inline': True
    })
    field_dict_list.append({
        'name': "**Total Points**",
        'value': clan_obj.points,
        'inline': True
    })
    field_dict_list.append({
        'name': "**Link**",
        'value': (f"[{clan_obj.name}]({clan_obj.share_link})"),
        'inline': True
    })

    return field_dict_list


async def clan_lineup(clan_obj, coc_client):
    clan_lineup_dict = await clash_responder.clan_lineup(clan_obj, coc_client)

    field_dict_list = []

    for th in clan_lineup_dict:
        if clan_lineup_dict[th] > 0:
            field_dict_list.append({
                'name': f"Town Hall {th}",
                'value': f"{clan_lineup_dict[th]}",
                'inline': False
            })

    return field_dict_list


async def clan_war_preference(clan_obj, coc_client):
    in_count = 0
    for member in clan_obj.members:
        player_obj = await coc_client.get_player(member.tag)
        if player_obj.war_opted_in:
            in_count += 1

    field_dict_list = []

    field_dict_list.append({
        'name': "in",
        'value': f"{in_count}",
        'inline': False
    })
    field_dict_list.append({
        'name': "out",
        'value': f"{clan_obj.member_count - in_count}",
        'inline': False
    })

    return field_dict_list


def donation(clan_obj, donator_list, unit_name):
    # unit is a hero or pet
    if donator_list is None:
        return [{
            'name': f"{unit_name}",
            'value': "not a valid donatable unit"
        }]
    # nobody can donate unit
    if len(donator_list) == 0:
        return [{
            'name': clan_obj.name,
            'value': f"unable to donate {unit_name}"
        }]

    field_dict_list = []
    donation_upgrade = clash_responder.clan_donation_upgrade(clan_obj)

    # donators can donate max
    if ((donator_list[0].unit_obj.level + donation_upgrade) >=
            donator_list[0].unit_obj.max_level):
        value = (
            f"{donator_list[0].unit_obj.name} "
            f"lvl {donator_list[0].unit_obj.max_level}, "
            f"max"
        )
    else:
        value = (
            f"{donator_list[0].unit_obj.name} "
            f"lvl {donator_list[0].unit_obj.level + donation_upgrade} "
            f"max is {donator_list[0].unit_obj.max_level}"
        )

    for donator in donator_list:
        field_dict_list.append({
            'name': donator.player_obj.name,
            'value': value
        })

    return field_dict_list


def super_troop_search(clan_obj, donor_list, super_troop_obj):
    if len(donor_list) == 0:
        return [{
            'name': clan_obj.name,
            'value': f"does not have {super_troop_obj.name} activated"
        }]

    field_dict_list = []
    for donator in donor_list:
        field_dict_list.append({
            'name': donator.name,
            'value': f"has {super_troop_obj.name} active"
        })

    return field_dict_list


# WAR

async def war_verification(db_player_obj, user_obj, coc_client):
    """
        verifying a war
        and returning verification payload

        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            coc_client (obj): coc.py client

        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj, war_obj)
    """

    player_clan_verification_payload = (await player_clan_verification(
        db_player_obj, user_obj, coc_client))

    # player clan verification failed
    # player clash in maintenance, not found, or player not in clan
    if not player_clan_verification_payload['verified']:
        return player_clan_verification_payload

    player_obj = player_clan_verification_payload['player_obj']

    try:
        war_obj = await coc_client.get_current_war(player_obj.clan.tag)
    except Maintenance:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "Clash of Clans is under maintenance",
                'value': "please try again later"
            }],
            'player_obj': None,
            'war_obj': None
        }
    except NotFound:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "war not found",
                'value': f"{player_obj.clan.name} {player_obj.clan.tag}"
            }],
            'player_obj': None,
            'war_obj': None
        }
    except PrivateWarLog:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': f"{player_obj.clan.name} {player_obj.clan.tag}",
                'value': "war log is private"
            }],
            'player_obj': None,
            'war_obj': None
        }
    except GatewayError:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "coc.py ran into a gateway error",
                'value': "please try again later"
            }],
            'player_obj': None,
            'war_obj': None
        }
    except TypeError:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "ClashDiscord ran into a type error",
                'value': "please try again later"
            }],
            'player_obj': None,
            'war_obj': None
        }

    # clan is not in war
    if not war_obj:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': (f"{player_obj.clan.name} "
                         f"{player_obj.clan.tag}"),
                'value': "not in war"
            }],
            'player_obj': player_obj,
            'war_obj': None
        }

    # clan is not in war
    if war_obj.state == "notInWar":
        return {
            'verified': False,
            'field_dict_list': [{
                'name': (f"{player_obj.clan.name} "
                         f"{player_obj.clan.tag}"),
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


async def war_leadership_verification(db_player_obj, user_obj, coc_client):
    """
        verifying a war through player_leadership_verification
        and returning verification payload

        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            coc_client (obj): coc.py client

        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj, war_obj)
    """

    player_leadership_verification_payload = (await player_leadership_verification(
        db_player_obj, user_obj, coc_client))

    if not player_leadership_verification_payload['verified']:
        return player_leadership_verification_payload

    player_obj = player_leadership_verification_payload['player_obj']

    try:
        war_obj = await coc_client.get_current_war(player_obj.clan.tag)
    except Maintenance:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "Clash of Clans is under maintenance",
                'value': "please try again later"
            }],
            'player_obj': None,
            'war_obj': None
        }
    except NotFound:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "war not found",
                'value': f"{player_obj.clan.name} {player_obj.clan.tag}"
            }],
            'player_obj': None,
            'war_obj': None
        }
    except PrivateWarLog:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': f"{player_obj.clan.name} {player_obj.clan.tag}",
                'value': "war log is private"
            }],
            'player_obj': None,
            'war_obj': None
        }
    except GatewayError:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "coc.py ran into a gateway error",
                'value': "please try again later"
            }],
            'player_obj': None,
            'war_obj': None
        }
    except TypeError:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "ClashDiscord ran into a type error",
                'value': "please try again later"
            }],
            'player_obj': None,
            'war_obj': None
        }

    # clan is not in war
    if not war_obj:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': (f"{player_obj.clan.name} "
                         f"{player_obj.clan.tag}"),
                'value': "not in war"
            }],
            'player_obj': player_obj,
            'war_obj': None
        }

    # clan is not in war
    if war_obj.state == "notInWar":
        return {
            'verified': False,
            'field_dict_list': [{
                'name': (f"{player_obj.clan.name} "
                         f"{player_obj.clan.tag}"),
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


def war_info(war_obj):
    if not war_obj:
        return [{
            'name': f"not in war",
            'value': f"you are not in war"
        }]

    if war_obj.state == "preparation":
        time_string = clash_responder.string_date_time(war_obj)

        return [{
            'name': f"{time_string}",
            'value': f"left before war starts"
        }]
    elif war_obj.state == "inWar":
        time_string = clash_responder.string_date_time(war_obj)
        scoreboard_string = clash_responder.string_scoreboard(war_obj)

        return [{
            'name': f"{war_obj.clan.name} is {scoreboard_string}",
            'value': f"{time_string} left in war"
        }]
    elif war_obj.state == "warEnded":
        scoreboard_string = clash_responder.string_scoreboard(war_obj)

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
    if not war_obj:
        return [{
            'name': f"not in war",
            'value': f"you are not in war"
        }]

    if war_obj.state == "preparation":
        time_string = clash_responder.string_date_time(war_obj)

        return [{
            'name': f"{time_string}",
            'value': f"left before war starts"
        }]
    elif war_obj.state == "inWar":
        time_string = clash_responder.string_date_time(war_obj)

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


def war_no_attack(war_obj):
    if war_obj.state == "preparation":
        time_string = clash_responder.string_date_time(war_obj)

        return [{
            'name': f"{time_string}",
            'value': f"left before war starts, nobody has attacked"
        }]

    elif war_obj.state == "inWar":
        no_attack_list = clash_responder.war_no_attack(war_obj)
        if len(no_attack_list) == 0:
            return [{
                'name': f"no missed attacks",
                'value': (f"all {war_obj.team_size} {war_obj.clan.name} "
                          f"war members attacked")
            }]
        field_dict_list = []
        for member_obj in no_attack_list:
            field_dict_list.append({
                'name': f"{member_obj.name}",
                'value': f"is missing attacks"
            })
        return field_dict_list

    elif war_obj.state == "warEnded":
        no_attack_list = clash_responder.war_no_attack(war_obj)
        if len(no_attack_list) == 0:
            return [{
                'name': f"no missed attacks",
                'value': (f"all {war_obj.team_size} {war_obj.clan.name} "
                          f"war members attacked")
            }]
        field_dict_list = []
        for member_obj in no_attack_list:
            field_dict_list.append({
                'name': f"{member_obj.name}",
                'value': f"missed attacks"
            })
        return field_dict_list

    else:
        return [{
            'name': f"not in war",
            'value': f"you are not in war"
        }]


def war_members_overview(war_obj):
    "returns a list of all war members and their stars"

    if war_obj.state == "preparation":
        time_string = clash_responder.string_date_time(war_obj)

        return [{
            'name': f"{time_string}",
            'value': f"left before war starts, nobody has attacked"
        }]
    elif war_obj.state == "inWar":
        field_dict_list = []
        map_position_index = 0
        # no atk response
        for member_obj in war_obj.clan.members:
            map_position_index += 1
            if len(member_obj.attacks) == 0:
                field_dict_list.append({
                    'name': f"{map_position_index}. {member_obj.name}",
                    'value': f"has not attacked"
                })
            else:
                field_dict_list.append({
                    'name': f"{map_position_index}. {member_obj.name}",
                    'value': (
                        f"attacked {len(member_obj.attacks)} "
                        f"{clash_responder.string_attack_times(member_obj.attacks)} "
                        f"for {member_obj.star_count} "
                        f"{clash_responder.string_member_stars(member_obj.star_count)}"
                    )
                })
        return field_dict_list
    elif war_obj.state == "warEnded":
        field_dict_list = []
        map_position_index = 0
        # no atk response
        for member_obj in war_obj.clan.members:
            map_position_index += 1
            if len(member_obj.attacks) == 0:
                field_dict_list.append({
                    'name': f"{map_position_index}. {member_obj.name}",
                    'value': f"did not attack"
                })
            else:
                field_dict_list.append({
                    'name': f"{map_position_index}. {member_obj.name}",
                    'value': (
                        f"attacked {len(member_obj.attacks)} "
                        f"{clash_responder.string_attack_times(member_obj.attacks)} "
                        f"for {member_obj.star_count} "
                        f"{clash_responder.string_member_stars(member_obj.star_count)}"
                    )
                })
        return field_dict_list
    else:
        return [{
            'name': f"not in war",
            'value': f"you are not in war"
        }]


def war_all_attacks(war_obj):

    if war_obj.state == 'preparation':
        time_string = clash_responder.string_date_time(war_obj)

        return [{
            'name': f"{time_string}",
            'value': f"left before war starts, nobody has attacked"
        }]
    elif war_obj.state == 'inWar' or war_obj.state == "warEnded":
        field_dict_list = []
        map_position_index = 0
        # no atk response
        for member_obj in war_obj.clan.members:
            map_position_index += 1
            if len(member_obj.attacks) == 0:
                if war_obj.state == "inWar":
                    field_dict_list.append({
                        'name': (f"{map_position_index}. {member_obj.name} "
                                 f"TH {member_obj.town_hall}"),
                        'value': f"has not attacked"
                    })
                else:
                    field_dict_list.append({
                        'name': (f"{map_position_index}. {member_obj.name} "
                                 f"TH {member_obj.town_hall}"),
                        'value': f"did not attack"
                    })
                continue

            for attack_obj in member_obj.attacks:

                defender_obj = clash_responder.find_defender(
                    war_obj.opponent, attack_obj.defender_tag)

                if attack_obj.stars == 0 or attack_obj.stars == 3:
                    value_string = (
                        f"{attack_obj.stars} "
                        f"{clash_responder.string_member_stars(attack_obj.stars)} "
                        f"against {map_position_index}. "
                        f"{defender_obj.name} TH {defender_obj.town_hall}"
                    )
                else:
                    value_string = (
                        f"{attack_obj.stars} "
                        f"{clash_responder.string_member_stars(attack_obj.stars)} "
                        f"{round(attack_obj.destruction, 2)}% "
                        f"against {map_position_index}. "
                        f"{defender_obj.name} TH {defender_obj.town_hall}"
                    )
                field_dict_list.append({
                    'name': (
                        f"{map_position_index}. "
                        f"{member_obj.name} "
                        f"TH {member_obj.town_hall}"
                    ),
                    'value': value_string
                })
        return field_dict_list

    else:
        return [{
            'name': f"not in war",
            'value': f"you are not in war"
        }]


def war_member_score(war_obj, player):
    "returns a response list of member scores"
    field_dict_list = []
    if war_obj.state == "notInWar":
        field_dict_list.append({
            "name": "you are not in war",
            "value": "there is no score"
        })
        return field_dict_list

    # member check before preparation check to see if the member is in the war
    # find member in war
    found = False
    for war_member in war_obj.clan.members:
        if war_member.tag == player.tag:
            member = war_member
            found = True
            break
    if not found:
        return [{
            'name': f"{player.name}",
            'value': f"not found in war"
        }]

    if war_obj.state == "preparation":
        field_dict_list.append({
            "name": "war has not started",
            "value": "there is no score"
        })
        return field_dict_list

    scored_member = clash_responder.member_score(member, war_obj)
    field_dict_list.append({
        "name": scored_member.name,
        "value": f"{round(scored_member.score, 3)}"
    })
    return field_dict_list


def war_clan_score(war_obj):
    "returns a response list of all member scores"
    return_list = []
    if war_obj.state == "notInWar":
        return_list.append({
            "name": "you are not in war",
            "value": "there is no score"
        })
        return return_list
    if war_obj.state == "preparation":
        return_list.append({
            "name": "war has not started",
            "value": "there is no score"
        })
        return return_list

    scored_member_list = []
    # getting scored_member for each clan member
    for member in war_obj.clan.members:
        scored_member_list.append(
            clash_responder.member_score(member, war_obj))

    scored_member_list = sorted(
        scored_member_list, key=lambda member: member.score, reverse=True)
    for member in scored_member_list:
        return_list.append({
            "name": member.name,
            "value": f"{round(member.score, 3)}"
        })
    return return_list


def war_lineup(war_obj):
    # prepping message and title
    message = (
        "```\n"
        "War Lineup\n"
        "14 | 13 | 12 | 11 | 10 | 9  | 8\n"
        "-------------------------------\n"
    )
    # prepping clan lineup message
    clan_lineup = f"{war_obj.clan.name}\n"
    clan_lineup_dict = clash_responder.war_clan_lineup(war_obj.clan)
    for th in clan_lineup_dict:
        if th >= 8:
            clan_lineup += f"{clan_lineup_dict[th]}"
            if clan_lineup_dict[th] >= 10:
                # if it is a double digit number
                clan_lineup += " | "
            else:
                # if it is a single digit number add an extra space
                clan_lineup += "  | "
    # removes the last 4 characters '  | ' of the string
    clan_lineup = clan_lineup[:-4]
    clan_lineup += "\n\n"
    message += clan_lineup

    # prepping opponent lineup message
    opp_lineup = f"{war_obj.opponent.name}\n"
    opp_lineup_dict = clash_responder.war_clan_lineup(war_obj.opponent)
    for th in opp_lineup_dict:
        if th >= 8:
            opp_lineup += f"{opp_lineup_dict[th]}"
            if opp_lineup_dict[th] >= 10:
                # if it is a double digit number
                opp_lineup += " | "
            else:
                # if it is a single digit number add an extra space
                opp_lineup += "  | "
    # removes the last 4 characters '  | ' of the string
    opp_lineup = opp_lineup[:-4]
    opp_lineup += "\n\n"
    message += opp_lineup

    message += "```"
    return message


def war_member_lineup(war_obj):
    field_dict_list = []
    map_position_index = 0
    for clan_member in war_obj.clan.members:
        map_position_index += 1
        # subtract 1 for indexing purposes
        opp_member_obj = war_obj.opponent.members[map_position_index-1]
        field_dict_list.append({
            "name": f"{map_position_index}",
            "value": (
                f"{clan_member.town_hall} | {clan_member.name}\n"
                f"{opp_member_obj.town_hall} | {opp_member_obj.name}\n"
            ),
            "inline": False
        })

    return field_dict_list


# CWL

async def cwl_group_verification(db_player_obj, user_obj, coc_client):
    """
        verifying a cwl group
        and returning verification payload
        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            coc_client (obj): coc.py client
        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj, cwl_group_obj)
    """

    player_clan_verification_payload = (await player_clan_verification(
        db_player_obj, user_obj, coc_client))

    if not player_clan_verification_payload['verified']:
        return player_clan_verification_payload

    player_obj = player_clan_verification_payload['player_obj']

    try:
        cwl_group_obj = await coc_client.get_league_group(player_obj.clan.tag)
    except Maintenance:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "Clash of Clans is under maintenance",
                'value': "please try again later"
            }],
            'player_obj': None,
            'cwl_group_obj': None
        }
    except NotFound:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "CWL group not found",
                'value': f"{player_obj.clan.name} {player_obj.clan.tag}"
            }],
            'player_obj': None,
            'cwl_group_obj': None
        }
    except GatewayError:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "coc.py ran into a gateway error",
                'value': "please try again later"
            }],
            'player_obj': None,
            'cwl_group_obj': None
        }

    verification_payload = {
        'verified': True,
        'field_dict_list': None,
        'player_obj': player_obj,
        'cwl_group_obj': cwl_group_obj
    }
    return verification_payload


async def cwl_group_leadership_verification(db_player_obj, user_obj, coc_client):
    """
        verifying a cwl group through player_leadership_verification
        and returning verification payload
        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            coc_client (obj): coc.py client
        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj, cwl_group_obj)
    """

    player_leadership_verification_payload = (
        await player_leadership_verification(
            db_player_obj, user_obj, coc_client)
    )

    if not player_leadership_verification_payload['verified']:
        return player_leadership_verification_payload

    player_obj = player_leadership_verification_payload['player_obj']

    try:
        cwl_group_obj = await coc_client.get_league_group(player_obj.clan.tag)
    except Maintenance:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "Clash of Clans is under maintenance",
                'value': "please try again later"
            }],
            'player_obj': None,
            'cwl_group_obj': None
        }
    except NotFound:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "CWL group not found",
                'value': f"{player_obj.clan.name} {player_obj.clan.tag}"
            }],
            'player_obj': None,
            'cwl_group_obj': None
        }
    except GatewayError:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "coc.py ran into a gateway error",
                'value': "please try again later"
            }],
            'player_obj': None,
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
        "CWL Lineup\n"
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


async def cwl_clan_score(player_obj, cwl_group, clan_tag):
    if not cwl_group:
        return [{
            'name': "{player_obj.name} is not in CWL",
            'value': "there is no score"
        }]

    # get a list of all CWLWar objects
    cwl_wars = []
    async for war in cwl_group.get_wars_for_clan(clan_tag):
        if war.state == "warEnded":
            cwl_wars.append(war)

    if len(cwl_wars) < 2:
        return [{
            'name': "not enough wars",
            'value': "please wait till round two has ended to score members"
        }]

    # get the cwl clan
    for clan in cwl_group.clans:
        if clan.tag == clan_tag:
            cwl_clan = clan
            break

    # get a list of all CWLWarMembers their scores
    scored_members = []
    for member in cwl_clan.members:
        scored_member = clash_responder.cwl_member_score(cwl_wars, member)
        if scored_member.participated_wars != 0:
            scored_members.append(scored_member)

    sorted_scored_members = sorted(
        scored_members, key=lambda member: member.score, reverse=True)
    field_dict_list = []
    for member in sorted_scored_members:
        field_dict_list.append({
            'name': member.name,
            'value': f"{round(member.score, 3)}"
        })
    return field_dict_list


async def cwl_member_score(player_obj, cwl_group, clan_tag):
    if not cwl_group:
        return [{
            'name': "{player_obj.name} is not in CWL",
            'value': "there is no score"
        }]

    # get a list of all CWLWar objects
    cwl_wars = []
    async for war in cwl_group.get_wars_for_clan(clan_tag):
        if war.state == "warEnded":
            cwl_wars.append(war)

    if len(cwl_wars) < 2:
        return [{
            'name': "not enough wars",
            'value': "please wait till round two has ended to score members"
        }]

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

    scored_member = clash_responder.cwl_member_score(cwl_wars, player_obj)

    field_dict_list = [{
        'name': f"{round(scored_member.score, 3)}",
        'value': f"overall score for {len(cwl_wars)} wars"
    }]

    round_index = 0
    for round_score in scored_member.round_scores:
        round_index += 1
        if round_score == 0:
            field_dict_list.append({
                'name': f"round {round_index} score",
                'value': f"{scored_member.name} did not participate"
            })
        else:
            field_dict_list.append({
                'name': f"round {round_index} score",
                'value': f"{round(round_score, 3)}"
            })

    return field_dict_list


# CWL WAR

async def cwl_war_verification(db_player_obj, user_obj, coc_client):
    """
        verifying a cwl war
        and returning verification payload
        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            coc_client (obj): coc.py client
        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj, cwl_war_obj)
    """

    cwl_group_verification_payload = (await cwl_group_verification(
        db_player_obj, user_obj, coc_client))

    if not cwl_group_verification_payload['verified']:
        return cwl_group_verification_payload

    player_obj = cwl_group_verification_payload['player_obj']
    cwl_group_obj = cwl_group_verification_payload['cwl_group_obj']

    try:
        cwl_war_obj = await coc_client.find_current_war(player_obj.clan.tag)
    except Maintenance:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "Clash of Clans is under maintenance",
                'value': "please try again later"
            }],
            'player_obj': None,
            'cwl_war_obj': None
        }
    except NotFound:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "CWL war not found",
                'value': f"{player_obj.clan.name} {player_obj.clan.tag}"
            }],
            'player_obj': None,
            'cwl_war_obj': None
        }
    except PrivateWarLog:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': f"{player_obj.clan.name} {player_obj.clan.tag}",
                'value': "war log is private"
            }],
            'player_obj': None,
            'cwl_war_obj': None
        }
    except GatewayError:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "coc.py ran into a gateway error",
                'value': "please try again later"
            }],
            'player_obj': None,
            'cwl_group_obj': None
        }

    # clan is not in cwl war
    if not cwl_war_obj:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': (f"{player_obj.clan.name} "
                         f"{player_obj.clan.tag}"),
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


async def cwl_war_leadership_verification(db_player_obj, user_obj, coc_client):
    """
        verifying a cwl war through cwl_group_leadership_verification
        and returning verification payload
        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            coc_client (obj): coc.py client
        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj, cwl_war_obj)
    """

    cwl_group_leadership_verification_payload = (
        await cwl_group_leadership_verification(
            db_player_obj, user_obj, coc_client))

    if not cwl_group_leadership_verification_payload['verified']:
        return cwl_group_leadership_verification_payload

    player_obj = cwl_group_leadership_verification_payload['player_obj']
    cwl_group_obj = cwl_group_leadership_verification_payload['cwl_group_obj']

    try:
        cwl_war_obj = await coc_client.find_current_war(player_obj.clan.tag)
    except Maintenance:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "Clash of Clans is under maintenance",
                'value': "please try again later"
            }],
            'player_obj': None,
            'cwl_war_obj': None
        }
    except NotFound:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "CWL war not found",
                'value': f"{player_obj.clan.name} {player_obj.clan.tag}"
            }],
            'player_obj': None,
            'cwl_war_obj': None
        }
    except PrivateWarLog:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': f"{player_obj.clan.name} {player_obj.clan.tag}",
                'value': "war log is private"
            }],
            'player_obj': None,
            'cwl_war_obj': None
        }
    except GatewayError:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "coc.py ran into a gateway error",
                'value': "please try again later"
            }],
            'player_obj': None,
            'cwl_group_obj': None
        }

    # clan is not in cwl war
    if not cwl_war_obj:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': (f"{player_obj.clan.name} "
                         f"{player_obj.clan.tag}"),
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
    description,
    bot_prefix,
    bot_user_name,
    thumbnail,
    field_list,
    image_url,
    author_display_name,
    author_avatar_url
):
    embed_list = []
    if title and description:
        embed = Embed(
            colour=color,
            title=title,
            description=description
        )
    elif title and not description:
        embed = Embed(
            colour=color,
            title=title,
        )
    elif not title and description:
        embed = Embed(
            colour=color,
            description=description
        )
    else:
        embed = Embed(
            colour=color
        )

    embed.set_author(
        icon_url=icon_url,
        name=f"[{bot_prefix}] {bot_user_name}"
    )
    if thumbnail:
        embed.set_thumbnail(
            url=thumbnail.small)

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
                    description=description,
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
def help_main(db_guild_obj, user_id, player_obj, bot_categories):
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

    db_user_obj = db_responder.read_user(user_id)
    for category in bot_categories:
        if category.brief == "superuser":
            if not db_user_obj:
                continue
            if not db_user_obj.super_user:
                continue
        if (
            category.brief == "discord" and
            not player_obj or
            category.brief == "player" and
            not player_obj or
            category.brief == "clan" and
            not player_obj or
            category.brief == "war" and
            not player_obj or
            category.brief == "cwl" and
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
        return help_main(db_guild_obj, user_id, player_obj, bot_categories)
    if bot_category.brief == "superuser":
        return help_super_user(db_guild_obj, user_id,
                               bot_category, all_commands)
    if bot_category.brief == "client":
        return help_client(db_guild_obj, user_id, bot_category, all_commands)
    if bot_category.brief == "discord":
        return help_discord(player_obj, bot_category, all_commands)
    if bot_category.brief == "player":
        return help_player(player_obj, bot_category, all_commands)
    if (bot_category.brief == "clan" or
        bot_category.brief == "war" or
            bot_category.brief == "cwl"):
        return help_clan(player_obj, bot_category, all_commands)
    return help_main(db_guild_obj, user_id, player_obj, bot_categories)


def help_super_user(db_guild_obj, user_id, bot_category, all_commands):
    help_dict = {
        'field_dict_list': [],
        'emoji_list': []
    }

    db_user_obj = db_responder.read_user(user_id)

    # if user is not super user
    if not db_user_obj.super_user:
        help_dict['field_dict_list'].append({
            'name': "user is not super user",
            'value': "must be super user to view super user commands"
        })
        return help_dict

    for parent in all_commands.values():
        # command is not in the correct category
        if not bot_category.brief == parent.name:
            continue

        field_dict_list = help_command_dict_list(parent)
        help_dict["field_dict_list"] = field_dict_list
    return help_dict


def help_client(db_guild_obj, user_id, bot_category, all_commands):
    help_dict = {
        'field_dict_list': [],
        'emoji_list': []
    }

    # guild not claimed
    if db_guild_obj is None:
        help_dict['field_dict_list'].append({
            'name': "guild not claimed",
            'value': "please claim guild using `client guild claim`"
        })
        return help_dict

    for parent in all_commands.values():
        # command is not in the correct category
        if not bot_category.brief == parent.name:
            continue

        field_dict_list = help_command_dict_list(parent)

        if len(field_dict_list) == 0:
            help_dict["field_dict_list"].append({
                'name': "guild not claimed",
                'value': "please claim guild using `client claim guild`"
            })
            return help_dict

        help_dict["field_dict_list"] = field_dict_list

    return help_dict


def help_discord(player_obj, bot_category, all_commands):
    help_dict = {
        'field_dict_list': [],
        'emoji_list': []
    }

    for parent in all_commands.values():
        # command is not in the correct category
        if not bot_category.brief == parent.name:
            continue

        field_dict_list = help_command_dict_list(parent)
        help_dict["field_dict_list"] = field_dict_list

    return help_dict


def help_player(player_obj, bot_category, all_commands):
    help_dict = {
        'field_dict_list': [],
        'emoji_list': []
    }

    for parent in all_commands.values():
        # command is not in the correct category
        if not bot_category.brief == parent.name:
            continue

        # player not found
        if player_obj is None:
            help_dict['field_dict_list'].append({
                'name': "player not found",
                'value': "please claim player using `client player claim`"
            })
            return help_dict

        field_dict_list = help_command_dict_list(parent)
        help_dict["field_dict_list"] = field_dict_list

    return help_dict


def help_clan(player_obj, bot_category, all_commands):
    help_dict = {
        'field_dict_list': [],
        'emoji_list': []
    }

    for parent in all_commands.values():
        # command is not in the correct category
        if not bot_category.brief == parent.name:
            continue

        # player not found
        if player_obj is None:
            help_dict['field_dict_list'].append({
                'name': "player not found",
                'value': "please claim player using `client player claim`"
            })
            return help_dict

        # player not in a clan
        if player_obj.clan is None:
            help_dict['field_dict_list'].append({
                'name': "player not in a clan",
                'value': "player must be in a clan to use clan based commands"
            })
            return help_dict

        field_dict_list = help_command_dict_list(parent)
        help_dict["field_dict_list"] = field_dict_list

    return help_dict


def help_command_dict_list(parent):
    field_dict_list = []

    # repeating for each child
    for group in parent.children.values():

        for child in group.children.values():

            field_name = child.qualified_name
            for param in child.docstring["params"]:
                field_name += f" <{param}>"
            field_dict_list.append({
                'name': field_name,
                'value': child.docstring["description"]
            })
    return field_dict_list


# user

def find_user_from_tag(player_obj, member_list):
    """
        finding a user from a requested player

        Args:
            player_obj (obj): clash player object
            member_list (list): list of members in guild

        Returns:
            list: field_dict_list
    """

    db_user_obj = db_responder.read_user_from_tag(player_obj.tag)
    # user with requested player tag not found
    if not db_user_obj:
        return {
            "name": f"{player_obj.name} {player_obj.tag}",
            "value": (f"linked user not found")
        }

    # find user in guild
    user_obj = get(member_list, id=db_user_obj.discord_id)

    # user not found in guild
    if not user_obj:
        return {
            "name": f"{player_obj.name} {player_obj.tag}",
            "value": (f"linked user not in server")
        }

    return {
        "name": f"{player_obj.name} {player_obj.tag}",
        "value": f"claimed by {user_obj.mention}"
    }


def user_player_ping(player, member_list):
    """
        turning a player into a user ping

        Args:
            player (obj): clash player object
                requires player.name and player.tag
            member_list (list): list of members in guild

        Returns:
            string: returns user ping if possible and player info
    """

    db_user = db_responder.read_user_from_tag(player.tag)

    if db_user is None:
        return f"{player.name} {player.tag}"

    user = get(member_list, id=db_user.discord_id)

    if user is None:
        return f"{player.name} {player.tag}"

    return f"{user.mention} ({player.name} {player.tag})"


# roles

async def update_roles(user, guild, coc_client):
    """
        update roles and return embed dict list

        Args:
            user ([disnake.User]): [object for user getting roled]
            guild ([disnake.Guild]): [guild command was called]
            coc_client ([coc.py client]): [coc.py client]

        Returns:
            [embed_dict_list]: [list]
                embed_dict:
                    title [str]: embed title or None
                    field_dict_list [list]: list of field dicts
                    thumbnail [obj]: coc.py thumbnail object or None
    """
    embed_dict_list = []

    db_player_obj_list = db_responder.read_player_list(user.id)
    # player is not claimed
    if len(db_player_obj_list) == 0:
        embed_dict_list.append({
            "title": user.display_name,
            "field_dict_list": [{
                "name": f"no claimed players",
                "value": user.mention
            }],
            "thumbnail": None
        })
        return embed_dict_list

    # getting a list of all claimed players
    player_obj_list = []
    for db_obj in db_player_obj_list:
        player_obj = await clash_responder.get_player(
            db_obj.player_tag, coc_client)

        # player was not found from tag
        if player_obj is None:
            embed_dict_list.append({
                "title": None,
                "field_dict_list": [{
                    "name": db_obj.player_tag,
                    "value": "couldn't find player from tag"
                }],
                "thumbnail": None
            })
            continue

        player_obj_list.append(player_obj)

    # get needed roles
    needed_role_list = []
    for player_obj in player_obj_list:
        # claimed clan validation
        db_clan_obj = db_responder.read_clan(
            guild.id, player_obj.clan.tag)
        # clan not found
        if not db_clan_obj:
            embed_dict_list.append({
                "title": (f"{user.display_name} "
                          f"{player_obj.name} {player_obj.tag}"),
                "field_dict_list": [{
                    "name": f"{player_obj.clan.name} {player_obj.clan.tag}",
                    "value": f"not claimed in {guild.name} server"
                }],
                "thumbnail": player_obj.league.icon
            })
            continue

        # get discord clan and rank roles
        db_clan_role_obj = db_responder.read_clan_role_from_tag(
            guild.id, player_obj.clan.tag)
        db_rank_role_obj = (db_responder.read_rank_role_from_guild_and_clash(
            guild.id, player_obj.role.value))

        if not db_clan_role_obj and not db_rank_role_obj:
            embed_dict_list.append({
                "title": None,
                "field_dict_list": [{
                    "name": (f"role for clan {player_obj.clan.name} "
                             f"{player_obj.clan.tag}"),
                    "value": f"not claimed"
                }],
                "thumbnail": player_obj.clan.badge
            })
            continue

        # add clan role if found
        if db_clan_role_obj:
            needed_role_list.append(db_clan_role_obj.discord_role_id)
        # add rank role if found
        if db_rank_role_obj:
            needed_role_list.append(db_rank_role_obj.discord_role_id)

    # if the user has no needed roles
    if len(needed_role_list) == 0:
        uninitiated_role = db_responder.read_rank_role_from_guild_and_clash(
            guild.id, "uninitiated"
        )
        if uninitiated_role:
            needed_role_list.append(uninitiated_role.discord_role_id)

    # get rid of duplicates
    needed_role_list = list(dict.fromkeys(needed_role_list))

    # get current roles
    current_discord_role_list = []
    for current_role in user.roles:
        current_discord_role_list.append(current_role.id)

    # get current roles that match db roles
    current_db_rank_role_list = db_responder.read_rank_role_list(
        current_discord_role_list)

    current_db_clan_role_list = db_responder.read_clan_role_list(
        current_discord_role_list
    )

    # getting the list of role id's
    current_role_list = []
    for rank_role in current_db_rank_role_list:
        current_role_list.append(rank_role.discord_role_id)
    for clan_role in current_db_clan_role_list:
        current_role_list.append(clan_role.discord_role_id)

    add_role_id_list, remove_role_id_list = role_add_remove_list(
        needed_role_list, current_role_list)

    # get objects of roles to add from id's
    add_role_obj_list = []
    for add_role_id in add_role_id_list:
        # returns None if role is not found
        add_role_obj = get(guild.roles, id=add_role_id)
        # role not found in guild.roles
        if add_role_obj is None:
            embed_dict_list.append({
                "title": None,
                "field_dict_list": [{
                    "name": f"role with id {add_role_id}",
                    "value": f"not found"
                }],
                "thumbnail": None
            })
            continue

        add_role_obj_list.append(add_role_obj)

    # get objects of roles to remove from id's
    remove_role_obj_list = []
    for remove_role_id in remove_role_id_list:
        # returns None if role is not found
        remove_role_obj = get(
            guild.roles, id=remove_role_id)
        # role not found in guild.roles
        if remove_role_obj is None:
            embed_dict_list.append({
                "title": None,
                "field_dict_list": [{
                    "name": f"role for id {remove_role_id}",
                    "value": f"please ensure claimed roles and discord roles match"
                }],
                "thumbnail": None
            })
            continue

        remove_role_obj_list.append(remove_role_obj)

    # add roles
    for add_role_obj in add_role_obj_list:
        await user.add_roles(add_role_obj)

    # remove roles
    for remove_role_obj in remove_role_obj_list:
        await user.remove_roles(remove_role_obj)

    # no roles added or removed
    if len(add_role_obj_list) == 0 and len(remove_role_obj_list) == 0:
        embed_dict_list.append({
            "title": user.display_name,
            "field_dict_list": [{
                "name": f"no roles changed",
                "value": user.mention
            }],
            "thumbnail": None
        })

    # roles have been added or removed
    else:
        field_dict_list = []

        # adding makeshift title
        field_dict_list.append({
            "name": f"roles changed",
            "value": user.mention,
            "inline": True
        })

        # adding added roles to field dict list
        for role in add_role_obj_list:
            field_dict_list.append({
                "name": f"added role",
                "value": role.name
            })

        # adding removed roles to field dict list
        for role in remove_role_obj_list:
            field_dict_list.append({
                "name": f"removed role",
                "value": role.name
            })

        embed_dict_list.append({
            "title": user.display_name,
            "field_dict_list": field_dict_list,
            "thumbnail": None
        })

    return embed_dict_list


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


# DB
async def clan_role_verification(clan_role, coc_client):
    """
        verifying a clan role
        and returning verification payload

        Args:
            clan_role (obj): discord role
            coc_client (obj): coc.py client

        Returns:
            dict: verification_payload
                (verified, field_dict_list, clan_obj)
    """

    # clan role not used
    if clan_role is None:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "clan role not mentioned",
                'value': "please mention a clan role"
            }],
            'clan_obj': None
        }

    # get clan tag from clan role
    db_clan_role = db_responder.read_clan_role(clan_role.id)

    # role mentioned was not a linked clan role
    if db_clan_role is None:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': f"please mention a clan role",
                'value': f"{clan_role.mention} is not linked to a clan"
            }],
            'clan_obj': None
        }

    try:
        clan_obj = await coc_client.get_clan(db_clan_role.clan_tag)
    except Maintenance:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "Clash of Clans is under maintenance",
                'value': "please try again later"
            }],
            'clan_obj': None
        }
    except NotFound:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "could not find clan",
                'value': db_clan_role.clan_tag
            }],
            'clan_obj': None
        }
    except GatewayError:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "coc.py ran into a gateway error",
                'value': "please try again later"
            }],
            'clan_obj': None
        }

    verification_payload = {
        'verified': True,
        'field_dict_list': None,
        'clan_obj': clan_obj
    }
    return verification_payload


async def clan_role_player_verification(clan_role, user, coc_client):
    """
        verifying a player is in the clan linked to the clan role
        and returning verification payload

        Args:
            clan_role (obj): discord role
            user (obj): discord user object
            coc_client (obj): coc.py client

        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj, clan_obj)
    """

    clan_verification_payload = (await clan_role_verification(
        clan_role, coc_client))

    # clan role verification failed
    # clan in maintenance, not found, or gateway error
    if not clan_verification_payload['verified']:
        return clan_verification_payload

    clan_obj = clan_verification_payload['clan_obj']

    db_player_obj_list = db_responder.read_player_list(user.id)

    if len(db_player_obj_list) == 0:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': f"no claimed players",
                'value': f"{user.mention} has no claimed players"
            }],
            'player_obj': None,
            'clan_obj': None
        }

    player_obj = None
    for db_player_obj in db_player_obj_list:
        player_verification_payload = (
            await player_verification(db_player_obj, user, coc_client))

        if not player_verification_payload['verified']:
            return player_verification_payload

        # player is in the specified clan
        if clan_obj.tag == player_verification_payload['player_obj'].clan.tag:
            player_obj = player_verification_payload['player_obj']
            break

    # no players in specified clan
    if player_obj is None:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': f"no players in specified clan",
                'value': f"{user.mention} is not in {clan_obj.name} {clan_obj.tag}"
            }],
            'player_obj': None,
            'clan_obj': clan_obj
        }

    verification_payload = {
        'verified': True,
        'field_dict_list': None,
        'player_obj': player_obj,
        'clan_obj': clan_obj
    }
    return verification_payload


async def clan_role_player_leadership_verification(clan_role, user, coc_client):
    """
        verifying a player is in leadership of specified clan
        and returning verification payload

        Args:
            clan_role (obj): discord role
            user (obj): discord user object
            coc_client (obj): coc.py client

        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj, clan_obj)
    """

    clan_role_player_verification_payload = (await clan_role_player_verification(
        clan_role, user, coc_client))

    # player clan verification failed
    # player clash in maintenance, not found, gateway error, or player not in clan
    if not clan_role_player_verification_payload['verified']:
        return clan_role_player_verification_payload

    clan_obj = clan_role_player_verification_payload['clan_obj']
    player_obj = clan_role_player_verification_payload['player_obj']
    # player not leader or coleader
    if (player_obj.role.value != "leader" and
            player_obj.role.value != "coLeader"):
        return {
            'verified': False,
            'field_dict_list': [{
                'name': (f"{player_obj.name} "
                         f"{player_obj.tag}"),
                'value': "not in leadership"
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


async def clan_role_war_verification(clan_role, coc_client):
    """
        verifying a war from clan role
        and returning verification payload

        Args:
            db_player_obj (obj): player object from db
            coc_client (obj): coc.py client

        Returns:
            dict: verification_payload
                (verified, field_dict_list, war_obj)
    """

    clan_role_verification_payload = (
        await clan_role_verification(clan_role, coc_client))

    # player clan verification failed
    # player clash in maintenance, not found, or player not in clan
    if not clan_role_verification_payload['verified']:
        return clan_role_verification_payload

    clan_obj = clan_role_verification_payload['clan_obj']

    try:
        war_obj = await coc_client.get_current_war(clan_obj.tag)
    except Maintenance:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "Clash of Clans is under maintenance",
                'value': "please try again later"
            }],
            'war_obj': None
        }
    except NotFound:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "war not found",
                'value': f"{clan_obj.name} {clan_obj.tag}"
            }],
            'war_obj': None
        }
    except PrivateWarLog:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': f"{clan_obj.name} {clan_obj.tag}",
                'value': "war log is private"
            }],
            'war_obj': None
        }
    except GatewayError:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "coc.py ran into a gateway error",
                'value': "please try again later"
            }],
            'war_obj': None
        }
    except TypeError:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "ClashDiscord ran into a type error",
                'value': "please try again later"
            }],
            'war_obj': None
        }

    # clan is not in war
    if not war_obj:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': (f"{clan_obj.name} "
                         f"{clan_obj.tag}"),
                'value': "not in war"
            }],
            'war_obj': None
        }

    # clan is not in war
    if war_obj.state == "notInWar":
        return {
            'verified': False,
            'field_dict_list': [{
                'name': (f"{clan_obj.name} "
                         f"{clan_obj.tag}"),
                'value': "not in war"
            }],
            'war_obj': None
        }

    verification_payload = {
        'verified': True,
        'field_dict_list': None,
        'war_obj': war_obj
    }
    return verification_payload


async def clan_role_war_leadership_verification(clan_role, user, coc_client):
    """
        verifying a war through clan_role_player_leadership_verification
        and returning verification payload

        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            coc_client (obj): coc.py client

        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj, war_obj)
    """

    clan_player_leadership_verification_payload = (
        await clan_role_player_leadership_verification(
            clan_role, user, coc_client))

    if not clan_player_leadership_verification_payload['verified']:
        return clan_player_leadership_verification_payload

    player_obj = clan_player_leadership_verification_payload['player_obj']
    clan_obj = clan_player_leadership_verification_payload['clan_obj']

    try:
        war_obj = await coc_client.get_current_war(clan_obj.tag)
    except Maintenance:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "Clash of Clans is under maintenance",
                'value': "please try again later"
            }],
            'player_obj': None,
            'war_obj': None
        }
    except NotFound:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "war not found",
                'value': f"{clan_obj.name} {clan_obj.tag}"
            }],
            'player_obj': None,
            'war_obj': None
        }
    except PrivateWarLog:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': f"{clan_obj.name} {clan_obj.tag}",
                'value': "war log is private"
            }],
            'player_obj': None,
            'war_obj': None
        }
    except GatewayError:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "coc.py ran into a gateway error",
                'value': "please try again later"
            }],
            'player_obj': None,
            'war_obj': None
        }
    except TypeError:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "ClashDiscord ran into a type error",
                'value': "please try again later"
            }],
            'player_obj': None,
            'war_obj': None
        }

    # clan is not in war
    if not war_obj:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': (f"{clan_obj.name} "
                         f"{clan_obj.tag}"),
                'value': "not in war"
            }],
            'player_obj': player_obj,
            'war_obj': None
        }

    # clan is not in war
    if war_obj.state == "notInWar":
        return {
            'verified': False,
            'field_dict_list': [{
                'name': (f"{clan_obj.name} "
                         f"{clan_obj.tag}"),
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
