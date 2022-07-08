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

from responders.DiscordResponder import (
    get_emoji,
    get_th_emoji
)
import responders.ClashResponder as clash_responder

from disnake.utils import get


def cwl_info(cwl_group: ClanWarLeagueGroup):
    """
        embed
            title
                clan name, tag, league name
            description
                current round
            current war status

    """


def cwl_info_scoreboard(war, discord_emoji_list, client_emoji_list):
    if not war:
        return [{
            'name': f"not in war",
            'value': f"you are not in war"
        }]

    time_string = clash_responder.string_date_time(war)
    if war.state == "preparation":

        return [{
            'name': f"{war.clan.name} vs. {war.opponent.name}",
            'value': f"{time_string} left before war starts"
        }]

    field_dict_list = []

    # overview: state, time remaining, win/lose/tie, score
    star_emoji = get_emoji(
        "War Star", discord_emoji_list, client_emoji_list)
    scoreboard_string = clash_responder.string_scoreboard(war, star_emoji)

    # getting the overview
    if war.state == "inWar":
        field_name = f"{war.clan.name} vs. {war.opponent.name}"
        field_value = f"{war.clan.name} is {scoreboard_string} "
        field_value = f"{time_string} left in war"

    else:
        field_name = f"{war.clan.name} vs. {war.opponent.name}"
        field_value = f"{war.clan.name} {scoreboard_string} "
        field_value += f"war has ended"

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


def cwl_lineup(cwl_group: ClanWarLeagueGroup,
               discord_emoji_list, client_emoji_list):
    field_dict_list = []

    for clan in cwl_group.clans:

        field_name = f"{clan.name} {clan.tag}"

        th_count_dict = clash_responder.war_clan_lineup(clan)

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


def cwl_lineup_clan(
    cwl_clan, coc_client, discord_emoji_list, client_emoji_list
):
    field_dict_list = []
    return_string = ""
    count_index = 0
    sorted_members = sorted(
        cwl_clan.members, key=lambda member: member.town_hall, reverse=True)

    for member in sorted_members:
        count_index += 1

        th_emoji = get_th_emoji(
            member.town_hall, discord_emoji_list, client_emoji_list)

        return_string += f"{count_index}: {th_emoji} {member.name}"
        return_string += "\n"

    # remove the last 1 character of the string
    # removing "\n"
    return_string = return_string[:-1]

    return return_string


async def cwl_lineup_member(
    cwl_clan, coc_client, discord_emoji_list, client_emoji_list
):
    field_dict_list = []
    sorted_members = sorted(
        cwl_clan.members, key=lambda member: member.town_hall, reverse=True)
    map_position_index = 0

    for member in sorted_members:
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


async def cwl_clan_score(clan_obj, cwl_group: ClanWarLeagueGroup):
    if not cwl_group:
        return [{
            'name': f"{clan_obj.name} is not in CWL",
            'value': "there is no score"
        }]

    scored_members = (
        await clash_responder.cwl_clan_member_scoreboard_list(
            cwl_group, clan_obj))

    sorted_scored_members = sorted(
        scored_members, key=lambda member: member.score, reverse=True)

    field_dict_list = []
    for member in sorted_scored_members:
        field_dict_list.append({
            'name': member.name,
            'value': f"{round(member.score, 3)}"
        })
    return field_dict_list


async def cwl_clan_noatk(clan, cwl_group: ClanWarLeagueGroup,
                         coc_client, discord_emoji_list, client_emoji_list):
    if cwl_group is None:
        return [{
            'name': f"{clan.name} is not in CWL",
            'value': "there is no score"
        }]

    cwl_clan = get(cwl_group.clans, tag=clan.tag)

    if cwl_clan is None:
        return [{
            'name': f"{clan.name} is not in CWL",
            'value': "there is no score"
        }]

    scored_members = (
        await clash_responder.cwl_clan_member_scoreboard_list(
            cwl_group, clan))

    no_atk_members = []

    # missed attacks
    for scored_member in scored_members:
        # made all attacks
        if scored_member.potential_attack_count == scored_member.attack_count:
            continue

        no_atk_members.append(scored_member)

    if len(no_atk_members) == 0:
        return [{
            'name': f"no missed attacks",
            'value': (f"all {len(cwl_clan.members)} {clan.name} "
                      f"cwl members attacked")
        }]

    field_dict_list = []
    for member in no_atk_members:
        player = await coc_client.get_player(member.tag)
        th_emoji = get_th_emoji(
            player.town_hall, discord_emoji_list, client_emoji_list)

        attacks_missed = member.potential_attack_count - member.attack_count

        attack_string = clash_responder.string_attack(attacks_missed)

        field_dict_list.append({
            'name': f"{th_emoji} {player.name}",
            'value': (f"{member.attack_count}/{member.potential_attack_count} "
                      f"attacks")
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


async def cwl_scoreboard_group(
        cwl_group, discord_emoji_list, client_emoji_list, coc_client):
    field_dict_list = []

    clan_scoreboards = []

    ended_war_count = 0
    # getting the ended war count
    for war_round in cwl_group.rounds:
        war = await coc_client.get_league_war(war_round[0])

        if war.state == "warEnded":
            ended_war_count += 1
            continue

        break

    for clan in cwl_group.clans:
        clan_scoreboard = await clash_responder.cwl_clan_scoreboard(
            cwl_group, clan)

        clan_scoreboards.append(clan_scoreboard)

    clan_scoreboards.sort(reverse=True, key=lambda x: (x.stars, x.destruction))
    star_emoji = get_emoji(
        "War Star", discord_emoji_list, client_emoji_list)
    position_index = 0

    for clan_scoreboard in clan_scoreboards:
        position_index += 1

        # getting the avg destruction %
        if ended_war_count == 0:
            destruction = clan_scoreboard.destruction

        else:
            destruction = clan_scoreboard.destruction / ended_war_count

        field_name = f"**{position_index}: {clan_scoreboard.clan.name}**"
        field_value = (f"{clan_scoreboard.stars} {star_emoji}\n"
                       f"{round(destruction, 2)}% destruction")

        field_dict_list.append({
            'name': field_name,
            'value': field_value
        })

    return field_dict_list


async def cwl_scoreboard_round(
        cwl_group: ClanWarLeagueGroup, cwl_round, round_index,
        discord_emoji_list, client_emoji_list, coc_client):

    field_dict_list = []
    star_emoji = get_emoji(
        "War Star", discord_emoji_list, client_emoji_list)

    for war_tag in cwl_round:
        war = await coc_client.get_league_war(war_tag)

        # set opponent war status
        if war.status == "lost":
            opponent_status = "won"

        if war.status == "won":
            opponent_status = "lost"

        if war.status == "tied":
            opponent_status = "tied"

        field_dict_list.append({
            "name": f"{war.clan.name} | {war.opponent.name}",
            "value": (
                f"{war.status} | {opponent_status}"
                f"\n"
                f"{war.clan.stars} {star_emoji} "
                f"| {war.opponent.stars} {star_emoji}"
                f"\n"
                f"{round(war.clan.destruction, 2)}% "
                f"| {round(war.opponent.destruction, 2)}%"
            )
        })

    return field_dict_list


async def cwl_scoreboard_clan(
    inter: ApplicationCommandInteraction,
    cwl_group: ClanWarLeagueGroup,
    clan: Clan, coc_client: CocClient,
    discord_emoji_list, client_emoji_list
):
    field_dict_list = []

    for cwl_clan in cwl_group.clans:
        # specified clan is found
        if cwl_clan.tag == clan.tag:
            break

    # making sure clan was found in cwl_group
    if cwl_clan.tag != clan.tag:
        field_dict_list.append({
            "name": f"{clan.name} {clan.tag}",
            "value": "not found in given CWL group"
        })
        return field_dict_list

    # get a list of all CWLWar objects
    cwl_wars = []
    async for war in cwl_group.get_wars_for_clan(clan.tag):
        if war.state == "warEnded":
            cwl_wars.append(war)

    # get a list of all CWLWarMembers their scores
    scored_members = []
    for member in cwl_clan.members:
        scored_member = clash_responder.cwl_member_score(cwl_wars, member)

        if scored_member.participated_wars == 0:
            continue

        scored_members.append(scored_member)

    scored_members.sort(reverse=True, key=lambda x: (
        x.stars, x.destruction, x.score))

    position_index = 0
    for scored_member in scored_members:
        position_index += 1

        player = await coc_client.get_player(scored_member.tag)
        th_emoji = get_th_emoji(
            player.town_hall, discord_emoji_list, client_emoji_list)
        star_emoji = get_emoji(
            "War Star", discord_emoji_list, client_emoji_list)

        # getting the avg destruction %
        if scored_member.participated_wars == 0:
            destruction = scored_member.destruction

        else:
            destruction = (scored_member.destruction
                           / scored_member.participated_wars)

        field_dict_list.append({
            "name": (
                f"{position_index}: {th_emoji} {scored_member.name}"
            ),
            "value": (
                f"{scored_member.stars} {star_emoji}\n"
                f"{round(destruction, 2)}% destruction\n"
                f"{scored_member.attack_count}/"
                f"{scored_member.potential_attack_count} attacks\n"
                f"{round(scored_member.score, 2)} "
                f"{inter.me.display_name} score"
            )
        })

    return field_dict_list
