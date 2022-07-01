from coc import (
    Client as CocClient,
    NotFound,
    Maintenance,
    PrivateWarLog,
    GatewayError,
    Clan,
)

from responders.DiscordResponder import (
    get_emoji,
    get_war_opted_in_emoji,
    get_th_emoji,
    get_clan_war_league_emoji
)
import responders.ClashResponder as clash_responder

from utils import coc_utils


def clan_info(
        clan_obj, discord_emoji_list, client_emoji_list):
    field_dict_list = []

    if (clan_obj.description is not None
            and clan_obj.description != ""):
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
    clan_obj, coc_client, discord_emoji_list, client_emoji_list
):
    field_dict_list = []
    return_string = ""

    for member in clan_obj.members:
        player = await clash_responder.get_player(member.tag, coc_client)

        # just in case player returned None
        if player is None:
            continue

        th_emoji = get_th_emoji(
            player.town_hall, discord_emoji_list, client_emoji_list)

        return_string += f"{member.clan_rank}: {th_emoji} {player.name}"
        return_string += "\n"

    # remove the last 1 character of the string
    # removing "\n"
    return_string = return_string[:-1]

    return return_string


async def clan_lineup_count(
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

        th_emoji = get_th_emoji(
            player.town_hall, discord_emoji_list, client_emoji_list)

        field_name = (f"{member.clan_rank}: {th_emoji} {player.name} "
                      f"{player.tag} {player.role.in_game_name}")

        field_value = ""

        for hero in player.heroes:
            if not hero.is_home_base:
                continue

            hero_emoji = get_emoji(
                hero.name, discord_emoji_list, client_emoji_list)

            max_level_for_townhall = hero.get_max_level_for_townhall(
                player.town_hall)

            field_value += f"{hero_emoji} {hero.level}"
            field_value += f"|{max_level_for_townhall}"
            field_value += f"|{hero.max_level}"
            field_value += f"\n"

        # no heroes in field value
        if field_value == "":
            field_value = "_ _"

        else:
            # remove the last 1 character of the string
            # removing "\n"
            field_value = field_value[:-1]

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
    in_emoji = get_war_opted_in_emoji(
        "True", discord_emoji_list, client_emoji_list)
    out_emoji = get_war_opted_in_emoji(
        "False", discord_emoji_list, client_emoji_list)

    embed_description = ""
    in_string = ""
    out_string = ""

    for member in clan_obj.members:
        player = await coc_client.get_player(member.tag)
        th_emoji = get_emoji(
            player.town_hall, discord_emoji_list, client_emoji_list)

        if player.war_opted_in:
            in_string += (
                f"{in_emoji} {th_emoji} {player.name}\n")

        else:
            out_string += (
                f"{out_emoji} {th_emoji} {player.name}\n")

    embed_description = in_string+out_string

    # remove trailing space in field value
    embed_description = embed_description[:-1]

    return embed_description


def donation(clan_obj, donator_list, unit_name,
             discord_emoji_list, client_emoji_list):
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
            'name': f"{donator.player_obj.name} {donator.player_obj.tag}",
            'value': value
        })

    return field_dict_list


async def clan_super_troop_active(
        clan, discord_emoji_list, client_emoji_list, coc_client):
    super_troop_list = coc_utils.get_super_troop_order()

    fields_dict_list = []

    for super_troop in super_troop_list:
        donor_list = await clash_responder.active_super_troop_search(
            clan, super_troop, coc_client)

        field_name = get_emoji(
            super_troop, discord_emoji_list, client_emoji_list)

        field_value = ""

        for player in donor_list:
            player_super_troop = player.get_troop(super_troop)
            if player_super_troop.is_active:
                field_value += f"{player.name} {player.tag}\n"

        # remove trailing space in field value
        field_value = field_value[:-1]

        # no players have super troop activated
        if field_value == "":
            continue

        fields_dict_list.append({
            'name': field_name,
            'value': field_value
        })

    if len(fields_dict_list) == 0:
        fields_dict_list.append({
            'name': f"{clan.name} {clan.tag}",
            'value': f"no super troops active"
        })

    return fields_dict_list


def super_troop_search(clan_obj, donor_list, super_troop_name,
                       discord_emoji_list, client_emoji_list):

    unit_emoji = get_emoji(
        super_troop_name, discord_emoji_list, client_emoji_list)

    if len(donor_list) == 0:
        return [{
            'name': clan_obj.name,
            'value': f"does not have {unit_emoji} activated"
        }]

    field_dict_list = []
    for donator in donor_list:
        field_dict_list.append({
            'name': f"{donator.name} {donator.tag}",
            'value': f"has {unit_emoji} active"
        })

    return field_dict_list
