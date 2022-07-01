from disnake import (
    ApplicationCommandInteraction
)
from coc import (
    Client as CocClient,
    WarRound,
    NotFound,
    Maintenance,
    PrivateWarLog,
    GatewayError,
    Clan,
    ClanWar,
    ClanWarLeagueGroup
)

from responders import (
    RazBotDB_Responder as db_responder
)
import responders.ClashResponder as clash_responder
import responders.RazBotDB_Responder as db_responder
from utils import coc_utils


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


async def player_leadership_verification(db_player_obj, user_obj, guild_id, coc_client):
    """
        verifying a player is in a clan and leadership
        and returning verification payload

        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            guild_id (obj): discord server id
            coc_client (obj): coc.py client

        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj)
    """

    db_user = db_responder.read_user(user_obj.id)
    db_guild = db_responder.read_guild(guild_id)

    if db_user is None:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': f"user is not claimed",
                'value': f"{user_obj.mention} must claim a user"
            }],
            'player_obj': None
        }

    if db_guild is None:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': f"server is not claimed",
                'value': f"server must be claimed"
            }],
            'player_obj': None
        }

    # skip leadership verification if user is guild admin or super user
    if db_guild is not None:
        if (db_guild.admin_user_id == user_obj.id or
                db_user.super_user):

            verification_payload = await player_verification(
                db_player_obj, user_obj, coc_client)

            return verification_payload

    db_clan_list = db_responder.read_clan_list_from_guild(guild_id)
    db_player_list = db_responder.read_player_list(user_obj.id)

    if len(db_clan_list) == 0:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': f"no clans have been claimed",
                'value': f"please claim a clan to use leadership commands"
            }],
            'player_obj': None
        }
    if len(db_player_list) == 0:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': f"no players have been claimed",
                'value': f"please claim a player to use leadership commands"
            }],
            'player_obj': None
        }

    # check for leadership in any claimed clan
    for db_player in db_player_list:
        try:
            player_obj = await coc_client.get_player(db_player.player_tag)
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
                    'value': db_player.player_tag
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

        # player not leader or coleader
        # check next player
        if (player_obj.role.value != "leader" and
                player_obj.role.value != "coLeader"):
            continue

        for db_clan in db_clan_list:
            try:
                clan_obj = await coc_client.get_clan(db_clan.clan_tag)
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
                        'value': db_clan.clan_tag
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

            # player that is in leadership is in the clan
            if player_obj.clan.tag == clan_obj.tag:
                return {
                    'verified': True,
                    'field_dict_list': None,
                    'player_obj': player_obj
                }

    verification_payload = {
        'verified': False,
        'field_dict_list': [{
            'name': f"not in leadership",
            'value': f"{user_obj.mention} must be in leadership to run command"
        }],
        'player_obj': None
    }
    return verification_payload


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


async def clan_leadership_verification(
        db_player_obj, user_obj, guild_id, coc_client):
    """
        verifying a clan through player_leadership_verification
        and returning verification payload

        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            guild_id (obj): discord server id
            coc_client (obj): coc.py client

        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj, clan_obj)
    """

    player_leadership_verification_payload = (await player_leadership_verification(
        db_player_obj, user_obj, guild_id, coc_client))

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


# WAR

async def war_verification(
        db_player_obj, war_selection, user_obj, coc_client):
    """
        verifying a war
        and returning verification payload

        Args:
            db_player_obj (obj): player object from db
            war_selection (str): cwl war selection
                ["preparation", "current", "upcoming", None]
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

    cwl_group = await clash_responder.get_cwl_group(
        player_obj.clan.tag, coc_client)

    cwl_enum_round = coc_utils.get_war_specified(war_selection, cwl_group)

    try:
        war_obj = await coc_client.get_current_war(
            player_obj.clan.tag, cwl_round=cwl_enum_round)

        # specifically for last day of CWl
        if cwl_group is not None:
            # amount of rounds matches the number of rounds
            if len(cwl_group.rounds) == cwl_group.number_of_rounds:
                last_round_war = await coc_client.get_league_war(cwl_group.rounds[-1][0])

                # last war is either in war or war ended
                if last_round_war.state != "preparation":
                    # change current to prep
                    if cwl_enum_round == WarRound.current_war:
                        cwl_enum_round = WarRound.current_preparation

                    # change current previous to current
                    elif cwl_enum_round == WarRound.previous_war:
                        cwl_enum_round = WarRound.current_war

                    war_obj = await coc_client.get_current_war(
                        player_obj.clan.tag, cwl_round=cwl_enum_round)

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


async def war_leadership_verification(
        db_player_obj, war_selection, user_obj, guild_id, coc_client):
    """
        verifying a war through player_leadership_verification
        and returning verification payload

        Args:
            db_player_obj (obj): player object from db
            war_selection (str): cwl war selection
                ["preparation", "current", "upcoming", None]
            user_obj (obj): discord user obj
            guild_id (obj): discord server id
            coc_client (obj): coc.py client

        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj, war_obj)
    """

    player_leadership_verification_payload = (await player_leadership_verification(
        db_player_obj, user_obj, guild_id, coc_client))

    if not player_leadership_verification_payload['verified']:
        return player_leadership_verification_payload

    player_obj = player_leadership_verification_payload['player_obj']

    cwl_group = await clash_responder.get_cwl_group(
        player_obj.clan.tag, coc_client)

    cwl_enum_round = coc_utils.get_war_specified(war_selection, cwl_group)

    try:
        war_obj = await coc_client.get_current_war(
            player_obj.clan.tag, cwl_round=cwl_enum_round)

        # specifically for last day of CWl
        if cwl_group is not None:
            # amount of rounds matches the number of rounds
            if len(cwl_group.rounds) == cwl_group.number_of_rounds:
                last_round_war = await coc_client.get_league_war(cwl_group.rounds[-1][0])

                # last war is either in war or war ended
                if last_round_war.state != "preparation":
                    # change current to prep
                    if cwl_enum_round == WarRound.current_war:
                        cwl_enum_round = WarRound.current_preparation

                    # change current previous to current
                    elif cwl_enum_round == WarRound.previous_war:
                        cwl_enum_round = WarRound.current_war

                    war_obj = await coc_client.get_current_war(
                        player_obj.clan.tag, cwl_round=cwl_enum_round)

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


async def cwl_group_leadership_verification(db_player_obj, user_obj, guild_id, coc_client):
    """
        verifying a cwl group through player_leadership_verification
        and returning verification payload
        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            guild_id (obj): discord server id
            coc_client (obj): coc.py client
        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj, clan_obj, cwl_group_obj)
    """

    clan_leadership_verification_payload = (
        await clan_leadership_verification(
            db_player_obj, user_obj, guild_id, coc_client)
    )

    if not clan_leadership_verification_payload['verified']:
        return clan_leadership_verification_payload

    player_obj = clan_leadership_verification_payload['player_obj']
    clan_obj = clan_leadership_verification_payload['clan_obj']

    try:
        cwl_group_obj = await coc_client.get_league_group(clan_obj.tag)
    except Maintenance:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "Clash of Clans is under maintenance",
                'value': "please try again later"
            }],
            'player_obj': None,
            'clan_obj': None,
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
            'clan_obj': None,
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
            'clan_obj': None,
            'cwl_group_obj': None
        }

    verification_payload = {
        'verified': True,
        'field_dict_list': None,
        'player_obj': player_obj,
        'clan_obj': clan_obj,
        'cwl_group_obj': cwl_group_obj
    }
    return verification_payload


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


async def cwl_war_leadership_verification(db_player_obj, user_obj, guild_id, coc_client):
    """
        verifying a cwl war through cwl_group_leadership_verification
        and returning verification payload
        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            guild_id (obj): discord server id
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


# DB


async def clan_role_verification(
        clan_role, coc_client):
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


async def clan_role_player_verification(
        clan_role, user, guild_id, coc_client):
    """
        verifying a player is in the clan linked to the clan role
        and returning verification payload

        Args:
            clan_role (obj): discord role
            user (obj): discord user object
            guild_id (obj): discord server id
            coc_client (obj): coc.py client

        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj, clan_obj)
    """

    db_guild = db_responder.read_guild(guild_id)
    db_user = db_responder.read_user(user.id)

    clan_verification_payload = (await clan_role_verification(
        clan_role, coc_client))

    # clan role verification failed
    # clan in maintenance, not found, or gateway error
    if not clan_verification_payload['verified']:
        return clan_verification_payload

    clan_obj = clan_verification_payload['clan_obj']

    # skip verification if user is guild admin or super user
    if db_guild is not None:
        if (db_guild.admin_user_id == user.id or
                db_user.super_user):

            db_player_obj = db_responder.read_player_active(user.id)
            player_verification_payload = (
                await player_verification(db_player_obj, user, coc_client))

            if not player_verification_payload['verified']:
                return player_verification_payload

            player_obj = player_verification_payload['player_obj']

            verification_payload = {
                'verified': True,
                'field_dict_list': None,
                'player_obj': player_obj,
                'clan_obj': clan_obj
            }
            return verification_payload

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


async def clan_role_player_leadership_verification(
        clan_role, user, guild_id, coc_client):
    """
        verifying a player is in leadership of specified clan
        and returning verification payload

        Args:
            clan_role (obj): discord role
            user (obj): discord user object
            guild_id (obj): discord server id
            coc_client (obj): coc.py client

        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj, clan_obj)
    """

    db_guild = db_responder.read_guild(guild_id)
    db_user = db_responder.read_user(user.id)

    clan_role_player_verification_payload = (await clan_role_player_verification(
        clan_role, user, guild_id, coc_client))

    # player clan verification failed
    # player clash in maintenance, not found, gateway error, or player not in clan
    if not clan_role_player_verification_payload['verified']:
        return clan_role_player_verification_payload

    clan_obj = clan_role_player_verification_payload['clan_obj']
    player_obj = clan_role_player_verification_payload['player_obj']

    # skip leadership verification if user is guild admin or super user
    if db_guild is not None:
        if (db_guild.admin_user_id == user.id or
                db_user.super_user):
            verification_payload = {
                'verified': True,
                'field_dict_list': None,
                'player_obj': player_obj,
                'clan_obj': clan_obj
            }
            return verification_payload

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


async def clan_role_war_verification(
        clan_role, war_selection, coc_client):
    """
        verifying a war from clan role
        and returning verification payload

        Args:
            clan_role (obj): discord role
            war_selection (str): cwl war selection
                ["preparation", "current", "upcoming", None]
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

    cwl_group = await clash_responder.get_cwl_group(
        clan_obj.tag, coc_client)

    cwl_enum_round = coc_utils.get_war_specified(war_selection, cwl_group)

    try:
        war_obj = await coc_client.get_current_war(
            clan_obj.tag, cwl_round=cwl_enum_round)

        # specifically for last day of CWl
        if cwl_group is not None:
            # amount of rounds matches the number of rounds
            if len(cwl_group.rounds) == cwl_group.number_of_rounds:
                last_round_war = await coc_client.get_league_war(cwl_group.rounds[-1][0])

                # last war is either in war or war ended
                if last_round_war.state != "preparation":
                    # change current to prep
                    if cwl_enum_round == WarRound.current_war:
                        cwl_enum_round = WarRound.current_preparation

                    # change current previous to current
                    elif cwl_enum_round == WarRound.previous_war:
                        cwl_enum_round = WarRound.current_war

                    war_obj = await coc_client.get_current_war(
                        clan_obj.tag, cwl_round=cwl_enum_round)

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


async def clan_role_war_leadership_verification(
        clan_role, war_selection, user, guild_id, coc_client):
    """
        verifying a war through clan_role_player_leadership_verification
        and returning verification payload

        Args:
            clan_role (obj): discord role
            war_selection (str): cwl war selection
                ["preparation", "current", "upcoming", None]
            user (obj): discord user obj
            guild_id (obj): discord server id
            coc_client (obj): coc.py client

        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj, war_obj)
    """

    clan_player_leadership_verification_payload = (
        await clan_role_player_leadership_verification(
            clan_role, user, guild_id, coc_client))

    if not clan_player_leadership_verification_payload['verified']:
        return clan_player_leadership_verification_payload

    player_obj = clan_player_leadership_verification_payload['player_obj']
    clan_obj = clan_player_leadership_verification_payload['clan_obj']

    cwl_group = await clash_responder.get_cwl_group(
        clan_obj.tag, coc_client)

    cwl_enum_round = coc_utils.get_war_specified(war_selection, cwl_group)

    try:
        war_obj = await coc_client.get_current_war(
            clan_obj.tag, cwl_round=cwl_enum_round)

        # specifically for last day of CWl
        if cwl_group is not None:
            if cwl_group.state == "inWar":
                # last war is the current war
                if war_obj.state != "inWar":
                    # change current to prep
                    if cwl_enum_round == WarRound.current_war:
                        cwl_enum_round = WarRound.current_preparation

                    # change current previous to current
                    elif cwl_enum_round == WarRound.previous_war:
                        cwl_enum_round = WarRound.current_war

                    war_obj = await coc_client.get_current_war(
                        clan_obj.tag, cwl_round=cwl_enum_round)

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


async def clan_role_cwl_group_verification(
        clan_role, coc_client):
    """
        verifying a cwl group from clan role
        and returning verification payload
        Args:
            clan_role (obj): discord role
            coc_client (obj): coc.py client
        Returns:
            dict: verification_payload
                (verified, field_dict_list, clan_obj, cwl_group_obj)
    """

    clan_role_verification_payload = (
        await clan_role_verification(clan_role, coc_client))

    # player clan verification failed
    # player clash in maintenance, not found, or player not in clan
    if not clan_role_verification_payload['verified']:
        return clan_role_verification_payload

    clan_obj = clan_role_verification_payload['clan_obj']

    try:
        cwl_group_obj = await coc_client.get_league_group(clan_obj.tag)
    except Maintenance:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "Clash of Clans is under maintenance",
                'value': "please try again later"
            }],
            'clan_obj': None,
            'cwl_group_obj': None
        }
    except NotFound:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "CWL group not found",
                'value': f"{clan_obj.name} {clan_obj.tag}"
            }],
            'clan_obj': None,
            'cwl_group_obj': None
        }
    except GatewayError:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "coc.py ran into a gateway error",
                'value': "please try again later"
            }],
            'clan_obj': None,
            'cwl_group_obj': None
        }

    verification_payload = {
        'verified': True,
        'field_dict_list': None,
        'clan_obj': clan_obj,
        'cwl_group_obj': cwl_group_obj
    }
    return verification_payload


async def clan_role_cwl_group_leadership_verification(
        clan_role, user, guild_id, coc_client):
    """
        verifying a cwl group from clan role
        and returning verification payload
        Args:
            clan_role (obj): discord role
            user (obj): discord user obj
            guild_id (obj): discord server id
            coc_client (obj): coc.py client
        Returns:
            dict: verification_payload
                (verified, field_dict_list, player_obj, clan_obj, cwl_group_obj)
    """

    clan_player_leadership_verification_payload = (
        await clan_role_player_leadership_verification(
            clan_role, user, guild_id, coc_client))

    if not clan_player_leadership_verification_payload['verified']:
        return clan_player_leadership_verification_payload

    player_obj = clan_player_leadership_verification_payload['player_obj']
    clan_obj = clan_player_leadership_verification_payload['clan_obj']

    try:
        cwl_group_obj = await coc_client.get_league_group(clan_obj.tag)
    except Maintenance:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "Clash of Clans is under maintenance",
                'value': "please try again later"
            }],
            'player_obj': None,
            'clan_obj': None,
            'cwl_group_obj': None
        }
    except NotFound:
        return {
            'verified': False,
            'field_dict_list': [{
                'name': "CWL group not found",
                'value': f"{clan_obj.name} {clan_obj.tag}"
            }],
            'player_obj': None,
            'clan_obj': None,
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
            'clan_obj': None,
            'cwl_group_obj': None
        }

    verification_payload = {
        'verified': True,
        'field_dict_list': None,
        'player_obj': player_obj,
        'clan_obj': clan_obj,
        'cwl_group_obj': cwl_group_obj
    }
    return verification_payload


def guild_admin_verification(
    inter: ApplicationCommandInteraction
):
    """
        verifying author is a server admin, admin user, or super user
        and returning verification payload
        Args:
            inter (obj): disnake ApplicationCommandInteraction 
        Returns:
            dict: verification_payload
                (verified, embed_list, db_guild, db_author)
    """

    db_guild = db_responder.read_guild(inter.guild.id)

    # guild not claimed
    if not db_guild:
        embed_description = f"{inter.guild.name} has not been claimed"

        return {
            'verified': False,
            'embed_list': embed_description,
            'db_guild': None,
            'db_author': None
        }

    db_author = db_responder.read_user(inter.author.id)

    # author not claimed
    if not db_author:
        embed_description = f"{inter.author.mention} has not been claimed"

        return {
            'verified': False,
            'embed_list': embed_description,
            'db_guild': db_guild,
            'db_author': None
        }

    is_guild_admin = db_guild.admin_user_id == inter.author.id

    # user is not guild admin and is not super user and is not admin user
    if (not is_guild_admin
            and not db_author.super_user
            and not db_author.admin):
        embed_description = f"{inter.author.mention} is not guild's admin"

        return {
            'verified': False,
            'embed_list': embed_description,
            'db_guild': db_guild,
            'db_author': db_author
        }

    verification_payload = {
        'verified': True,
        'embed_list': None,
        'db_guild': db_guild,
        'db_author': db_author
    }
    return verification_payload
