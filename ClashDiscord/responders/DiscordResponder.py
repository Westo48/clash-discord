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


async def player_leadership_verification(db_player_obj, user_obj, guild_id, coc_client):
    """
        verifying a player is in a clan and leadership
        and returning verification payload

        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            guild_id (obj): discord guild id
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
                'name': f"guild is not claimed",
                'value': f"guild must be claimed"
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


def player_info(player_obj, discord_emoji_list, client_emoji_list):
    field_dict_list = []
    exp_emoji = get_emoji("Exp Level", discord_emoji_list, client_emoji_list)
    field_dict_list.append({
        'name': exp_emoji,
        'value': player_obj.exp_level,
        'inline': True
    })
    th_emoji = get_emoji(
        player_obj.town_hall, discord_emoji_list, client_emoji_list)
    field_dict_list.append({
        'name': '**TH Lvl**',
        'value': th_emoji,
        'inline': True
    })
    trophy_emoji = get_emoji(
        "Trophy", discord_emoji_list, client_emoji_list)
    field_dict_list.append({
        'name': trophy_emoji,
        'value': player_obj.trophies,
        'inline': True
    })
    field_dict_list.append({
        'name': (
            f"**{trophy_emoji} Best**"),
        'value': player_obj.best_trophies,
        'inline': True
    })
    if player_obj.legend_statistics:
        legend_trophy_emoji = get_emoji(
            "Legend Trophy", discord_emoji_list, client_emoji_list)
        field_dict_list.append({
            'name': legend_trophy_emoji,
            'value': player_obj.legend_statistics.legend_trophies,
            'inline': True
        })
        if player_obj.legend_statistics.best_season:
            legend_league_emoji = get_emoji(
                player_obj.league.name, discord_emoji_list, client_emoji_list)
            field_dict_list.append({
                'name': f"**{legend_league_emoji} Best Rank | Trophies**",
                'value': (
                    f"{player_obj.legend_statistics.best_season.rank} | "
                    f"{player_obj.legend_statistics.best_season.trophies}"
                ),
                'inline': True
            })
        if player_obj.legend_statistics.current_season:
            field_dict_list.append({
                'name': f"**{legend_league_emoji} Current Rank | Trophies**",
                'value': (
                    f"{player_obj.legend_statistics.current_season.rank} | "
                    f"{player_obj.legend_statistics.current_season.trophies}"
                ),
                'inline': True
            })
        if player_obj.legend_statistics.previous_season:
            field_dict_list.append({
                'name': f"**{legend_league_emoji} Previous Rank | Trophies**",
                'value': (
                    f"{player_obj.legend_statistics.previous_season.rank} | "
                    f"{player_obj.legend_statistics.previous_season.trophies}"
                ),
                'inline': True
            })
    player_star = get_emoji(
        "Player Star", discord_emoji_list, client_emoji_list)
    field_dict_list.append({
        'name': f"**{player_star} War Stars**",
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

    war_preference_emoji = get_emoji(
        player_obj.war_opted_in, discord_emoji_list, client_emoji_list)
    field_dict_list.append({
        'name': '**War Preference**',
        'value': war_preference_emoji,
        'inline': True
    })

    hero_value = ""
    for hero in player_obj.heroes:
        # hero isn't a home base hero
        if not hero.is_home_base:
            continue

        hero_emoji = get_emoji(
            hero.name, discord_emoji_list, client_emoji_list)

        emoji_str = hero_emoji
        hero_value += f"{hero_emoji} {hero.level}\n"

    if hero_value != "":
        # remove trailing space in hero value
        hero_value = hero_value[:-1]
        field_dict_list.append({
            'name': f"**Heroes**",
            'value': hero_value,
            'inline': True
        })

    pet_value = ""
    for pet in player_obj.hero_pets:
        # pet isn't a home base pet
        if not pet.is_home_base:
            continue

        pet_emoji = get_emoji(
            pet.name, discord_emoji_list, client_emoji_list)

        emoji_str = pet_emoji
        pet_value += f"{pet_emoji} {pet.level}\n"

    if pet_value != "":
        # remove trailing space in pet value
        pet_value = pet_value[:-1]
        field_dict_list.append({
            'name': f"**Pets**",
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


def unit_lvl(
    player_obj, unit_obj, unit_name,
    discord_emoji_list, client_emoji_list
):
    if not unit_obj:
        # unit not found response
        return {
            'name': f"could not find {unit_name}",
            'value': f"you either do not have it unlocked or it is misspelled"
        }

    unit_emoji = get_emoji(
        unit_obj.name, discord_emoji_list, client_emoji_list)

    try:
        max_level_for_townhall = unit_obj.get_max_level_for_townhall(
            player_obj.town_hall)
    except:
        max_level_for_townhall = unit_obj.max_level

    return {
        'name': f"{unit_emoji}",
        'value': (
            f"**{unit_obj.level} | "
            f"{max_level_for_townhall} | "
            f"{unit_obj.max_level}**"
        )
    }


def unit_lvl_group(
    player_obj, unit_group, group_title,
    discord_emoji_list, client_emoji_list
):

    # if there are no units in the group, return empty list
    if len(unit_group) == 0:
        return[]

    field_value = ""
    index = 0
    for unit in unit_group:
        index += 1
        unit_emoji = get_emoji(
            unit.name, discord_emoji_list, client_emoji_list)

        try:
            max_level_for_townhall = unit.get_max_level_for_townhall(
                player_obj.town_hall)
        except:
            max_level_for_townhall = unit.max_level

        field_value += f"{unit_emoji} "

        # if unit.level is a two digit number
        if unit.level > 9:
            level_str = unit.level
        else:
            level_str = f" {unit.level}"

        # if max_level_for_townhall is a two digit number
        if max_level_for_townhall > 9:
            max_level_for_townhall_str = max_level_for_townhall
        else:
            max_level_for_townhall_str = f" {max_level_for_townhall}"

        # if unit.max_level is a two digit number
        if unit.max_level > 9:
            max_level_str = unit.max_level
        else:
            max_level_str = f" {unit.max_level}"

        field_value += (
            f"`{level_str}|"
            f"{max_level_for_townhall_str}|"
            f"{max_level_str}`"
        )

        if (index % 2) == 0:
            field_value += "\n"
        else:
            field_value += " "

    return [{
        'name': f"**{group_title}**",
        'value': field_value,
        'inline': False
    }]


def unit_lvl_all(
    player_obj, discord_emoji_list, client_emoji_list
):
    field_dict_list = []
    field_dict_list += hero_lvl_all(
        player_obj, discord_emoji_list, client_emoji_list)
    field_dict_list += pet_lvl_all(
        player_obj, discord_emoji_list, client_emoji_list)
    field_dict_list += troop_lvl_all(
        player_obj, discord_emoji_list, client_emoji_list)
    field_dict_list += spell_lvl_all(
        player_obj, discord_emoji_list, client_emoji_list)
    field_dict_list += siege_lvl_all(
        player_obj, discord_emoji_list, client_emoji_list)
    return field_dict_list


def hero_lvl_all(
    player, discord_emoji_list, client_emoji_list
):
    group_title = "Heroes"
    # get unit group
    unit_group = []
    for hero in player.heroes:
        # hero isn't a home base hero
        if not hero.is_home_base:
            continue
        unit_group.append(hero)

    return unit_lvl_group(player, unit_group, group_title,
                          discord_emoji_list, client_emoji_list)


def pet_lvl_all(
    player, discord_emoji_list, client_emoji_list
):
    group_title = "Pets"
    # get unit group
    unit_group = []
    for pet in player.hero_pets:
        # pet isn't a home base pet
        if not pet.is_home_base:
            continue
        unit_group.append(pet)

    return unit_lvl_group(player, unit_group, group_title,
                          discord_emoji_list, client_emoji_list)


def troop_lvl_all(
    player, discord_emoji_list, client_emoji_list
):
    elixir_title = "Elixir Troops"
    dark_title = "Dark Troops"
    # get unit groups
    elixir_group = []
    dark_group = []
    for troop in player.home_troops:
        # troop isn't a home base troop
        if not troop.is_home_base:
            continue

        # troop is a super troop
        if troop.is_super_troop:
            continue

        # troop is a siege
        if troop.is_siege_machine:
            continue

        if troop.is_elixir_troop:
            elixir_group.append(troop)
        else:
            dark_group.append(troop)

    elixir_group_fields = unit_lvl_group(
        player, elixir_group, elixir_title,
        discord_emoji_list, client_emoji_list
    )
    dark_group_fields = unit_lvl_group(
        player, dark_group, dark_title,
        discord_emoji_list, client_emoji_list
    )

    return elixir_group_fields + dark_group_fields


def spell_lvl_all(
    player, discord_emoji_list, client_emoji_list
):
    elixir_title = "Elixir Spells"
    dark_title = "Dark Spells"
    # get unit groups
    elixir_group = []
    dark_group = []
    for spell in player.spells:
        # spell isn't a home base spell
        if not spell.is_home_base:
            continue

        if spell.is_elixir_spell:
            elixir_group.append(spell)
        else:
            dark_group.append(spell)

    elixir_group_fields = unit_lvl_group(
        player, elixir_group, elixir_title,
        discord_emoji_list, client_emoji_list
    )
    dark_group_fields = unit_lvl_group(
        player, dark_group, dark_title,
        discord_emoji_list, client_emoji_list
    )

    return elixir_group_fields + dark_group_fields


def siege_lvl_all(
    player, discord_emoji_list, client_emoji_list
):
    group_title = "Sieges"
    # get unit group
    unit_group = []
    for troop in player.home_troops:
        # troop isn't a home base troop
        if not troop.is_home_base:
            continue

        # troop is a super troop
        if troop.is_super_troop:
            continue

        # troop is NOT a siege
        if not troop.is_siege_machine:
            continue

        unit_group.append(troop)

    return unit_lvl_group(player, unit_group, group_title,
                          discord_emoji_list, client_emoji_list)


def active_super_troops(
    player_obj, active_super_troop_list,
    discord_emoji_list, client_emoji_list
):
    if len(active_super_troop_list) == 0:
        return [{
            'name': f"{player_obj.name} {player_obj.tag}",
            'value': f"no active super troops"
        }]
    else:
        field_dict_list = []
        for troop_obj in active_super_troop_list:
            troop_emoji = get_emoji(
                troop_obj.name, discord_emoji_list, client_emoji_list
            )
            field_dict_list.append({
                'name': f"{troop_emoji}",
                'value': f"{troop_obj.name}"
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


async def clan_leadership_verification(
        db_player_obj, user_obj, guild_id, coc_client):
    """
        verifying a clan through player_leadership_verification
        and returning verification payload

        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            guild_id (obj): discord guild id
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


def clan_info(
        clan_obj, discord_emoji_list, client_emoji_list):
    field_dict_list = []

    field_dict_list.append({
        'name': "**Description**",
        'value': clan_obj.description,
        'inline': False
    })
    if len(clan_obj.labels) != 0:
        label_value = ""
        for label in clan_obj.labels:
            label_emoji = get_emoji(
                label.name, discord_emoji_list, client_emoji_list)
            label_value += f"{label_emoji} {label.name}\n"

        # removing the last 1 character of label value "\n"
        label_value = label_value[:-1]

        field_dict_list.append({
            'name': "**Clan Labels**",
            'value': label_value,
            'inline': True
        })
    clan_exp_emoji = get_emoji(
        "Clan Exp", discord_emoji_list, client_emoji_list)
    field_dict_list.append({
        'name': "**Clan Level**",
        'value': f"{clan_exp_emoji} {clan_obj.level}",
        'inline': True
    })
    field_dict_list.append({
        'name': "**Members**",
        'value': clan_obj.member_count,
        'inline': True
    })
    if clan_obj.public_war_log:
        win_emoji = get_emoji(
            "True", discord_emoji_list, client_emoji_list)
        war_log_value = f"{win_emoji} {clan_obj.war_wins}\n"

        loss_emoji = get_emoji(
            "False", discord_emoji_list, client_emoji_list)
        war_log_value += f"{loss_emoji} {clan_obj.war_losses}\n"

        tie_emoji = get_emoji(
            "Grey Tick", discord_emoji_list, client_emoji_list)
        war_log_value += f"{tie_emoji} {clan_obj.war_ties}"

        field_dict_list.append({
            'name': "**War Log**",
            'value': war_log_value,
            'inline': True
        })
        field_dict_list.append({
            'name': "**Win Streak**",
            'value': clan_obj.war_win_streak,
            'inline': True
        })
    clan_war_league_emoji = get_clan_war_league_emoji(
        clan_obj.war_league.name, discord_emoji_list, client_emoji_list)
    field_dict_list.append({
        'name': "**Clan War League**",
        'value': f"{clan_war_league_emoji} {clan_obj.war_league.name}",
        'inline': True
    })
    trophy_emoji = get_emoji(
        "Trophy", discord_emoji_list, client_emoji_list)
    field_dict_list.append({
        'name': f"**{trophy_emoji} Total**",
        'value': clan_obj.points,
        'inline': True
    })
    field_dict_list.append({
        'name': "**Link**",
        'value': (f"[{clan_obj.name}]({clan_obj.share_link})"),
        'inline': True
    })

    return field_dict_list


async def clan_lineup(
        clan_obj, coc_client, discord_emoji_list, client_emoji_list):
    clan_lineup_dict = await clash_responder.clan_lineup(clan_obj, coc_client)

    field_dict_list = []

    for th in clan_lineup_dict:
        if clan_lineup_dict[th] > 0:
            th_emoji = get_th_emoji(
                f"{th}", discord_emoji_list, client_emoji_list)
            field_dict_list.append({
                'name': f"Town Hall {th}",
                'value': f"{th_emoji} {clan_lineup_dict[th]}",
                'inline': False
            })

    return field_dict_list


async def clan_lineup_member(
    clan_obj, coc_client, discord_emoji_list, client_emoji_list
):
    field_dict_list = []

    for member in clan_obj.members:
        player = await clash_responder.get_player(member.tag, coc_client)

        # just in case player returned None
        if player is None:
            continue

        field_name = (f"{member.clan_rank}: {player.name} {player.tag} "
                      f"{player.role.in_game_name}")

        th_emoji = get_th_emoji(
            player.town_hall, discord_emoji_list, client_emoji_list)
        field_value = f"{th_emoji} {player.town_hall}"

        for hero in player.heroes:
            if not hero.is_home_base:
                continue

            hero_emoji = get_emoji(
                hero.name, discord_emoji_list, client_emoji_list)

            max_level_for_townhall = hero.get_max_level_for_townhall(
                player.town_hall)

            field_value += f"\n"
            field_value += f"{hero_emoji} {hero.level}"
            field_value += f"|{max_level_for_townhall}"
            field_value += f"|{hero.max_level}"

        field_dict_list.append({
            'name': field_name,
            'value': field_value,
            'inline': False
        })

    return field_dict_list


async def war_preference_clan(
        clan_obj, coc_client, discord_emoji_list, client_emoji_list):
    in_count = 0
    for member in clan_obj.members:
        player_obj = await coc_client.get_player(member.tag)
        if player_obj.war_opted_in:
            in_count += 1

    field_dict_list = []

    in_emoji = get_war_opted_in_emoji(
        "True", discord_emoji_list, client_emoji_list)
    out_emoji = get_war_opted_in_emoji(
        "False", discord_emoji_list, client_emoji_list)

    field_dict_list.append({
        'name': in_emoji,
        'value': f"{in_count}",
        'inline': False
    })
    field_dict_list.append({
        'name': out_emoji,
        'value': f"{clan_obj.member_count - in_count}",
        'inline': False
    })

    return field_dict_list


async def war_preference_member(
        clan_obj, coc_client, discord_emoji_list, client_emoji_list):
    field_dict_list = []

    in_emoji = get_war_opted_in_emoji(
        "True", discord_emoji_list, client_emoji_list)
    out_emoji = get_war_opted_in_emoji(
        "False", discord_emoji_list, client_emoji_list)

    for member in clan_obj.members:
        player_obj = await coc_client.get_player(member.tag)
        if player_obj.war_opted_in:
            field_dict_list.append({
                'name': f"{player_obj.name} {player_obj.tag}",
                'value': in_emoji,
                'inline': True
            })

            continue

        field_dict_list.append({
            'name': f"{player_obj.name} {player_obj.tag}",
            'value': out_emoji,
            'inline': True
        })

    return field_dict_list


def donation(clan_obj, donator_list, unit_name, discord_emoji_list, client_emoji_list):
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

    unit_emoji = get_emoji(
        donator_list[0].unit_obj.name, discord_emoji_list, client_emoji_list)

    # donators can donate max
    if ((donator_list[0].unit_obj.level + donation_upgrade) >=
            donator_list[0].unit_obj.max_level):
        value = (
            f"{unit_emoji} "
            f"lvl {donator_list[0].unit_obj.max_level}, "
            f"max"
        )
    else:
        value = (
            f"{unit_emoji} "
            f"lvl {donator_list[0].unit_obj.level + donation_upgrade} "
            f"max is {donator_list[0].unit_obj.max_level}"
        )

    for donator in donator_list:
        field_dict_list.append({
            'name': donator.player_obj.name,
            'value': value
        })

    return field_dict_list


def super_troop_search(clan_obj, donor_list, super_troop_obj,
                       discord_emoji_list, client_emoji_list):

    unit_emoji = get_emoji(
        super_troop_obj.name, discord_emoji_list, client_emoji_list)

    if len(donor_list) == 0:
        return [{
            'name': clan_obj.name,
            'value': f"does not have {unit_emoji} activated"
        }]

    field_dict_list = []
    for donator in donor_list:
        field_dict_list.append({
            'name': donator.name,
            'value': f"has {unit_emoji} active"
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


async def war_leadership_verification(db_player_obj, user_obj, guild_id, coc_client):
    """
        verifying a war through player_leadership_verification
        and returning verification payload

        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            guild_id (obj): discord guild id
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


def war_info(war_obj, discord_emoji_list, client_emoji_list):
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
        star_emoji = get_emoji(
            "War Star", discord_emoji_list, client_emoji_list)
        time_string = clash_responder.string_date_time(war_obj)
        scoreboard_string = clash_responder.string_scoreboard(
            war_obj, star_emoji)

        return [{
            'name': f"{war_obj.clan.name} is {scoreboard_string}",
            'value': f"{time_string} left in war"
        }]
    elif war_obj.state == "warEnded":
        star_emoji = get_emoji(
            "War Star", discord_emoji_list, client_emoji_list)
        scoreboard_string = clash_responder.string_scoreboard(
            war_obj, star_emoji)

        return [{
            'name': f"{war_obj.clan.name} {scoreboard_string}",
            'value': f"war has ended"
        }]
    else:
        return [{
            'name': f"not in war",
            'value': f"you are not in war"
        }]


def war_scoreboard(war, discord_emoji_list, client_emoji_list):
    if not war:
        return [{
            'name': f"not in war",
            'value': f"you are not in war"
        }]

    time_string = clash_responder.string_date_time(war)
    if war.state == "preparation":

        return [{
            'name': f"{time_string}",
            'value': f"left before war starts"
        }]

    field_dict_list = []

    # overview: state, time remaining, win/lose/tie, score
    star_emoji = get_emoji(
        "War Star", discord_emoji_list, client_emoji_list)
    scoreboard_string = clash_responder.string_scoreboard(war, star_emoji)

    # getting the overview
    if war.state == "inWar":
        field_name = f"{war.clan.name} is {scoreboard_string}"
        field_value = f"{time_string} left in war"

    else:
        field_name = f"{war.clan.name} {scoreboard_string}"
        field_value = f"war has ended"

    field_dict_list.append({
        'name': field_name,
        'value': field_value
    })

    # clan: stars/potential stars, attacks/potential attacks, total destruction
    # getting the clan scoreboard
    clan_scoreboard_fields = clash_responder.war_clan_scoreboard(
        war, war.clan, star_emoji)
    field_dict_list.extend(clan_scoreboard_fields)

    # getting the opponent scoreboard
    opp_scoreboard_fields = clash_responder.war_clan_scoreboard(
        war, war.opponent, star_emoji)
    field_dict_list.extend(opp_scoreboard_fields)

    return field_dict_list


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


def war_clan_stars(war_obj, discord_emoji_list, client_emoji_list):
    "returns a list of all war members and their stars"

    if war_obj is None:
        return [{
            'name': f"not in war",
            'value': f"you are not in war"
        }]

    if war_obj.state == "preparation":
        time_string = clash_responder.string_date_time(war_obj)

        return [{
            'name': f"{time_string}",
            'value': f"left before war starts, nobody has attacked"
        }]

    star_emoji = get_emoji(
        "War Star", discord_emoji_list, client_emoji_list)
    field_dict_list = []

    for member_obj in war_obj.clan.members:

        if member_obj.star_count <= 3:
            star_string = star_emoji*member_obj.star_count
        else:
            star_string = f"{member_obj.star_count} {star_emoji}"

        th_emoji = get_emoji(
            member_obj.town_hall, discord_emoji_list, client_emoji_list)

        if len(member_obj.attacks) == 0:
            if war_obj.state == "inWar":
                field_value = f"has not attacked"
            else:
                field_value = f"did not attack"

            field_dict_list.append({
                'name': (f"{member_obj.map_position}. {member_obj.name} "
                         f"{th_emoji}\n"),
                'value': field_value
            })
        else:
            field_dict_list.append({
                'name': (f"{member_obj.map_position}. {member_obj.name} "
                         f"{th_emoji}"),
                'value': (
                    f"attacked {len(member_obj.attacks)} "
                    f"{clash_responder.string_attack_times(member_obj.attacks)}\n"
                    f"{star_string}"
                )
            })

    return field_dict_list


def war_all_attacks(war_obj, discord_emoji_list, client_emoji_list):

    if war_obj is None:
        return [{
            'name': f"not in war",
            'value': f"you are not in war"
        }]

    if war_obj.state == 'preparation':
        time_string = clash_responder.string_date_time(war_obj)

        return [{
            'name': f"{time_string}",
            'value': f"left before war starts, nobody has attacked"
        }]

    star_emoji = get_emoji(
        "War Star", discord_emoji_list, client_emoji_list)
    field_dict_list = []

    for member_obj in war_obj.clan.members:

        field_value = ""

        th_emoji = get_emoji(
            member_obj.town_hall, discord_emoji_list, client_emoji_list)

        if len(member_obj.attacks) == 0:
            if war_obj.state == "inWar":
                field_value = f"has not attacked"

            else:
                field_value = f"did not attack"

            field_dict_list.append({
                'name': (f"{member_obj.map_position}. {member_obj.name} "
                         f"{th_emoji}"),
                'value': field_value
            })

            continue

        for attack_obj in member_obj.attacks:
            defender_obj = clash_responder.find_defender(
                war_obj.opponent, attack_obj.defender_tag)

            defender_th_emoji = get_emoji(
                defender_obj.town_hall, discord_emoji_list, client_emoji_list)

            star_string = star_emoji*attack_obj.stars

            if attack_obj.stars == 3:
                field_value += (
                    f"{defender_obj.map_position}. "
                    f"{defender_obj.name} {defender_th_emoji}\n"
                    f"{star_string}\n\n"
                )
            else:
                field_value += (
                    f"{defender_obj.map_position}. "
                    f"{defender_obj.name} {defender_th_emoji}\n"
                    f"{round(attack_obj.destruction, 2)}%\n"
                    f"{star_string}\n\n"
                )

        # remove trailing space in field value
        field_value = field_value[:-2]

        field_dict_list.append({
            'name': (
                f"{member_obj.map_position}. "
                f"{member_obj.name} "
                f"{th_emoji}"
            ),
            'value': field_value
        })
    return field_dict_list


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


def war_lineup_overview(war_obj):
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


def war_lineup_clan(war_obj, discord_emoji_list, client_emoji_list):
    field_dict_list = []
    map_position_index = 0
    for clan_member in war_obj.clan.members:
        map_position_index += 1
        # subtract 1 for indexing purposes
        opp_member_obj = war_obj.opponent.members[map_position_index-1]

        member_th_emoji = get_emoji(
            clan_member.town_hall, discord_emoji_list, client_emoji_list)
        opp_th_emoji = get_emoji(
            opp_member_obj.town_hall, discord_emoji_list, client_emoji_list)

        field_dict_list.append({
            "name": f"{map_position_index}",
            "value": (
                f"{member_th_emoji} | {clan_member.name}\n"
                f"{opp_th_emoji} | {opp_member_obj.name}\n"
            ),
            "inline": False
        })

    return field_dict_list


async def war_lineup_member(
    war_clan, coc_client, discord_emoji_list, client_emoji_list
):
    field_dict_list = []

    map_position_index = 0
    for member in war_clan.members:
        player = await clash_responder.get_player(member.tag, coc_client)

        map_position_index += 1

        # just in case player returned None
        if player is None:
            continue

        th_emoji = get_emoji(
            player.town_hall, discord_emoji_list, client_emoji_list)

        field_name = f"{map_position_index}: {player.name} {player.tag}"

        field_value = f"{th_emoji}"

        for hero in player.heroes:
            if not hero.is_home_base:
                continue

            hero_emoji = get_emoji(
                hero.name, discord_emoji_list, client_emoji_list)

            field_value += f"\n"
            field_value += f"{hero_emoji} {hero.level}"

        field_dict_list.append({
            'name': field_name,
            'value': field_value,
            'inline': False
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


async def cwl_group_leadership_verification(db_player_obj, user_obj, guild_id, coc_client):
    """
        verifying a cwl group through player_leadership_verification
        and returning verification payload
        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            guild_id (obj): discord guild id
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


def cwl_lineup(cwl_group):
    message = (
        "```\n"
        "CWL Lineup\n"
        "14 | 13 | 12 | 11 | 10 | 9  | 8\n"
        "-------------------------------\n"
    )
    for clan in cwl_group.clans:
        lineup_message = f"{clan.name} {clan.tag}\n"
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


async def cwl_clan_score(clan_obj, cwl_group):
    if not cwl_group:
        return [{
            'name': f"{clan_obj.name} is not in CWL",
            'value': "there is no score"
        }]

    # get a list of all CWLWar objects
    cwl_wars = []
    async for war in cwl_group.get_wars_for_clan(clan_obj.tag):
        if war.state == "warEnded":
            cwl_wars.append(war)

    if len(cwl_wars) < 2:
        return [{
            'name': "not enough wars",
            'value': "please wait till round two has ended to score members"
        }]

    # get the cwl clan
    for clan in cwl_group.clans:
        if clan.tag == clan_obj.tag:
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
            'name': f"{player_obj.name} is not in CWL",
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


async def cwl_war_leadership_verification(db_player_obj, user_obj, guild_id, coc_client):
    """
        verifying a cwl war through cwl_group_leadership_verification
        and returning verification payload
        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            guild_id (obj): discord guild id
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

    # no fields given
    if len(field_list) == 0:
        embed = initialize_embed(
            Embed,
            color,
            icon_url,
            title,
            description,
            bot_prefix,
            bot_user_name,
            thumbnail,
            image_url,
            author_display_name,
            author_avatar_url
        )
        embed_list.append(embed)
        return embed_list

    while len(field_list) > 0:
        # initialize the current embed
        embed = initialize_embed(
            Embed,
            color,
            icon_url,
            title,
            description,
            bot_prefix,
            bot_user_name,
            thumbnail,
            image_url,
            author_display_name,
            author_avatar_url
        )
        # initialize embed str count
        embed_str_count = 0

        # total up the initialized embed to the count
        embed_str_count += (
            len(embed.title)
            + len(embed.author)
            + len(embed.description)
            + len(embed.footer)
        )

        while len(field_list) > 0:
            # use first field item since they will get deleted
            field = field_list[0]

            field_str_len = (len(str(field['name']))
                             + len(str(field['value'])))
            # embed data is greater than 6000
            if embed_str_count + field_str_len > 6000:
                # add the current embed to the list
                embed_list.append(embed)

                # break the for and restart the while
                break

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

            embed_str_count += (len(str(field['name']))
                                + len(str(field['value'])))

            del field_list[0]

            # embed fields are greater than 25
            # discord doesn't allow more than 25 fields per embed
            if len(embed.fields) == 25:
                # add the current embed to the list
                embed_list.append(embed)

                # break the for and restart the while
                break

        # dont add if exactly 25, already added
        # add the last embed to the list
        if len(embed.fields) != 25 and len(embed.fields) > 0:
            embed_list.append(embed)

    return embed_list


def initialize_embed(
    Embed,
    color,
    icon_url,
    title,
    description,
    bot_prefix,
    bot_user_name,
    thumbnail,
    image_url,
    author_display_name,
    author_avatar_url
):
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

    embed.set_footer(
        text=author_display_name,
        icon_url=author_avatar_url
    )

    return embed


async def send_embed_list(embed_list, inter):
    # embed limit is 10
    # embed char limit is 6000
    # embed field limit is 25

    # prep a list of embeds to send
    # this will be lists of embeds in a list
    total_str = ""
    send_list = []
    add_list = []
    for embed in embed_list:
        embed_str = ""
        # embed would be the discord.Embed instance
        fields = [embed.title, embed.description,
                  embed.footer.text, embed.author.name]

        fields.extend([field.name for field in embed.fields])
        fields.extend([field.value for field in embed.fields])

        for item in fields:
            # if we str(discord.Embed.Empty) we get 'Embed.Empty', when
            # we just want an empty string...
            embed_str += str(item) if str(item) != 'Embed.Empty' else ''

        # embeds will be higher than 6000 if added
        # embeds will have more than 10 embeds if added
        if len(total_str)+len(embed_str) > 6000 or len(add_list) == 10:
            # add the add_list to the send_list
            send_list.append(add_list.copy())

            # clear the add_list
            add_list.clear()

            total_str = ""

        add_list.append(embed)
        total_str += embed_str

        # if the embed is the last embed in the list
        # adding one to index for 0 index start
        if (embed_list.index(embed) + 1) == len(embed_list):
            send_list.append(add_list.copy())
            break

    # send all embeds
    for embeds in send_list:
        await inter.send(embeds=embeds)


# emojis
def get_emoji(coc_name, discord_emoji_list, client_emoji_list):
    client_emoji = get_base_emoji(
        coc_name, discord_emoji_list, client_emoji_list)

    # base emoji found
    if client_emoji is not None:
        return client_emoji

    client_emoji = get_th_emoji(
        coc_name, discord_emoji_list, client_emoji_list)

    # town hall emoji found
    if client_emoji is not None:
        return client_emoji

    client_emoji = get_war_opted_in_emoji(
        coc_name, discord_emoji_list, client_emoji_list)

    # war opted in emoji found
    if client_emoji is not None:
        return client_emoji

    client_emoji = get_clan_war_league_emoji(
        coc_name, discord_emoji_list, client_emoji_list)

    # clan war league emoji found
    if client_emoji is not None:
        return client_emoji

    return coc_name


def get_base_emoji(coc_name, discord_emoji_list, client_emoji_list):
    client_emoji = get(client_emoji_list, coc_name=coc_name)

    # emoji not found in client list
    if client_emoji is None:
        return None

    discord_emoji = get(
        discord_emoji_list,
        name=client_emoji.discord_name, id=client_emoji.discord_id)

    # emoji not found in discord list
    if discord_emoji is None:
        return None

    return (f"<:{discord_emoji.name}:{discord_emoji.id}>")


def get_th_emoji(coc_name, discord_emoji_list, client_emoji_list):
    client_emoji = get(client_emoji_list, coc_name=f"Town Hall {coc_name}")

    # emoji not found in client list
    if client_emoji is None:
        return None

    discord_emoji = get(
        discord_emoji_list,
        name=client_emoji.discord_name, id=client_emoji.discord_id)

    # emoji not found in discord list
    if discord_emoji is None:
        return None

    return (f"<:{discord_emoji.name}:{discord_emoji.id}>")


def get_war_opted_in_emoji(coc_name, discord_emoji_list, client_emoji_list):
    client_emoji = get(client_emoji_list, coc_name=f"war_opted_in={coc_name}")

    # emoji not found in client list
    if client_emoji is None:
        return None

    discord_emoji = get(
        discord_emoji_list,
        name=client_emoji.discord_name, id=client_emoji.discord_id)

    # emoji not found in discord list
    if discord_emoji is None:
        return None

    return (f"<:{discord_emoji.name}:{discord_emoji.id}>")


def get_clan_war_league_emoji(coc_name, discord_emoji_list, client_emoji_list):
    client_emoji = get(client_emoji_list, coc_name=f"Clan War {coc_name}")

    # emoji not found in client list
    if client_emoji is None:
        return None

    discord_emoji = get(
        discord_emoji_list,
        name=client_emoji.discord_name, id=client_emoji.discord_id)

    # emoji not found in discord list
    if discord_emoji is None:
        return None

    return (f"<:{discord_emoji.name}:{discord_emoji.id}>")


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
                "value": role.mention
            })

        # adding removed roles to field dict list
        for role in remove_role_obj_list:
            field_dict_list.append({
                "name": f"removed role",
                "value": role.mention
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


async def clan_role_player_verification(clan_role, user, guild_id, coc_client):
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


async def clan_role_player_leadership_verification(clan_role, user, guild_id, coc_client):
    """
        verifying a player is in leadership of specified clan
        and returning verification payload

        Args:
            clan_role (obj): discord role
            user (obj): discord user object
            guild_id (obj): discord guild id
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


async def clan_role_war_leadership_verification(clan_role, user, guild_id, coc_client):
    """
        verifying a war through clan_role_player_leadership_verification
        and returning verification payload

        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            guild_id (obj): discord guild id
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


async def clan_role_cwl_group_verification(clan_role, coc_client):
    """
        verifying a cwl group from clan role
        and returning verification payload
        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
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


async def clan_role_cwl_group_leadership_verification(clan_role, user, guild_id, coc_client):
    """
        verifying a cwl group from clan role
        and returning verification payload
        Args:
            db_player_obj (obj): player object from db
            user_obj (obj): discord user obj
            guild_id (obj): discord guild id
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
