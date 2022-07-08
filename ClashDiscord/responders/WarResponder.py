from coc import (
    Client as CocClient,
    WarRound,
    NotFound,
    Maintenance,
    PrivateWarLog,
    GatewayError,
    ClanWar,
)

from responders.DiscordResponder import get_emoji, get_th_emoji
import responders.ClashResponder as clash_responder


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


def war_no_attack(war: ClanWar, missed_attacks, discord_emoji_list, client_emoji_list):
    if war is None:
        return [{
            'name': f"not in war",
            'value': f"you are not in war"
        }]

    if war.state == "preparation":
        time_string = clash_responder.string_date_time(war)

        return [{
            'name': f"{time_string}",
            'value': f"left before war starts, nobody has attacked"
        }]

    # setting past or present tense of missed or is missing
    if war.state == "inWar":
        missed_string = "is missing "

    else:
        missed_string = "missed "

    field_dict_list = []
    map_position_index = 0

    for member in war.clan.members:
        map_position_index += 1

        missing_attack_count = (
            war.attacks_per_member - len(member.attacks))

        # not missing any attacks
        if missing_attack_count == 0:
            continue

        # missed attacks specified
        if missed_attacks is not None:
            # skip members who are missing attacks other than what is specified
            if missing_attack_count != missed_attacks:
                continue

        th_emoji = get_emoji(
            member.town_hall, discord_emoji_list, client_emoji_list)

        missing_attack_string = (
            clash_responder.string_attack(missing_attack_count))

        field_dict_list.append({
            'name': (f"{map_position_index}: {th_emoji} "
                     f"{member.name} {member.tag}"),
            'value': (f"{missed_string}"
                      f"{missing_attack_count} {missing_attack_string}")
        })

    if len(field_dict_list) == 0:
        return [{
            'name': f"no missed attacks",
            'value': (f"all {war.team_size} {war.clan.name} "
                      f"war members attacked")
        }]

    return field_dict_list


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

        if member_obj.star_count > 0 and member_obj.star_count <= 3:
            star_string = star_emoji * member_obj.star_count
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
    empty_star_emoji = get_emoji(
        "Empty War Star", discord_emoji_list, client_emoji_list)
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
            star_string += empty_star_emoji*(3-attack_obj.stars)

            if attack_obj.stars == 3:
                field_value += (
                    f"{defender_obj.map_position}. "
                    f"{defender_obj.name} {defender_th_emoji}\n"
                    f"{star_string} 100%\n\n"
                )
            else:
                field_value += (
                    f"{defender_obj.map_position}. "
                    f"{defender_obj.name} {defender_th_emoji}\n"
                    f"{star_string} "
                    f"{round(attack_obj.destruction, 2)}%\n\n"
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


def war_open_bases(
        war: ClanWar, star_count: int,
        discord_emoji_list, client_emoji_list):
    if war is None:
        return [{
            'name': f"not in war",
            'value': f"you are not in war"
        }]

    if war.state == "preparation":
        time_string = clash_responder.string_date_time(war)

        return [{
            'name': f"{time_string}",
            'value': f"left before war starts, nobody has attacked"
        }]

    field_dict_list = []

    star_emoji = get_emoji(
        "War Star", discord_emoji_list, client_emoji_list)
    empty_star_emoji = get_emoji(
        "Empty War Star", discord_emoji_list, client_emoji_list)

    position_index = 0
    for opponent in war.opponent.members:
        position_index += 1

        # there is no opponent attack
        if opponent.best_opponent_attack is None:
            opponent_th_emoji = get_emoji(
                opponent.town_hall, discord_emoji_list, client_emoji_list)

            field_dict_list.append({
                "name": (
                    f"{position_index}: {opponent_th_emoji} "
                    f"{opponent.name} {opponent.tag}"
                ),
                "value": (
                    f"not attacked"
                )
            })

            continue

        if opponent.best_opponent_attack.stars <= star_count:
            opponent_th_emoji = get_emoji(
                opponent.town_hall, discord_emoji_list, client_emoji_list)

            opp_star_count = opponent.best_opponent_attack.stars

            star_string = star_emoji*opp_star_count
            star_string += empty_star_emoji*(3-opp_star_count)

            field_dict_list.append({
                "name": (
                    f"{position_index}: {opponent_th_emoji} "
                    f"{opponent.name} {opponent.tag}"
                ),
                "value": (
                    f"{star_string} "
                    f"{opponent.best_opponent_attack.destruction}%"
                )
            })

            continue

    # no open bases
    if len(field_dict_list) == 0:
        field_dict_list.append({
            "name": f"no open bases",
            "value": f"with less than {star_count+1} {star_emoji}"
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


def war_lineup_overview(
        war: ClanWar,
        discord_emoji_list, client_emoji_list):
    field_dict_list = []

    clan_th_count_dict = clash_responder.war_clan_lineup(war.clan)

    field_name = f"{war.clan.name} {war.clan.tag}"

    th_count_dict = clash_responder.war_clan_lineup(war.clan)

    field_value = ""

    for th in th_count_dict:
        if th_count_dict[th] == 0:
            continue

        th_emoji = get_th_emoji(
            coc_name=th,
            discord_emoji_list=discord_emoji_list,
            client_emoji_list=client_emoji_list)

        field_value += f"{th_emoji}: {th_count_dict[th]}\n"

    field_dict_list.append({
        'name': field_name,
        'value': field_value,
        'inline': False
    })

    opp_th_count_dict = clash_responder.war_clan_lineup(war.opponent)

    field_name = f"{war.opponent.name} {war.opponent.tag}"

    th_count_dict = clash_responder.war_clan_lineup(war.opponent)

    field_value = ""

    for th in th_count_dict:
        if th_count_dict[th] == 0:
            continue

        th_emoji = get_th_emoji(
            coc_name=th,
            discord_emoji_list=discord_emoji_list,
            client_emoji_list=client_emoji_list)

        field_value += f"{th_emoji}: {th_count_dict[th]}\n"

    field_dict_list.append({
        'name': field_name,
        'value': field_value,
        'inline': False
    })

    return field_dict_list


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
