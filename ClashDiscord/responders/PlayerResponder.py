from coc import (
    Client as CocClient,
    NotFound,
    Maintenance,
    GatewayError,
)

from responders.DiscordResponder import get_emoji


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
        'name': th_emoji,
        'value': "Town Hall Level",
        'inline': True
    })
    league_emoji = get_emoji(
        player_obj.league.name, discord_emoji_list, client_emoji_list)
    field_dict_list.append({
        'name': league_emoji,
        'value': "League",
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
                "Legend League", discord_emoji_list, client_emoji_list)
            field_dict_list.append({
                'name': f"**{legend_league_emoji} Best Rank | Trophies**",
                'value': (
                    f"{player_obj.legend_statistics.best_season.rank} | "
                    f"{player_obj.legend_statistics.best_season.trophies}"
                ),
                'inline': True
            })
        if player_obj.legend_statistics.current_season:
            if (player_obj.legend_statistics.current_season.rank is not None and
                    player_obj.legend_statistics.current_season.trophies is not None):
                legend_league_emoji = get_emoji(
                    "Legend League", discord_emoji_list, client_emoji_list)
                field_dict_list.append({
                    'name': f"**{legend_league_emoji} Current Rank | Trophies**",
                    'value': (
                        f"{player_obj.legend_statistics.current_season.rank} | "
                        f"{player_obj.legend_statistics.current_season.trophies}"
                    ),
                    'inline': True
                })
        if player_obj.legend_statistics.previous_season:
            legend_league_emoji = get_emoji(
                "Legend League", discord_emoji_list, client_emoji_list)
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
        war_preference_emoji = get_emoji(
            player_obj.war_opted_in, discord_emoji_list, client_emoji_list)
        field_dict_list.append({
            'name': '**War Preference**',
            'value': war_preference_emoji,
            'inline': True
        })
    else:
        field_dict_list.append({
            'name': '**Clan**',
            'value': f"{player_obj.name} is not in a clan",
            'inline': True
        })

    hero_value = ""
    for hero in player_obj.heroes:
        # hero isn't a home base hero
        if not hero.is_home_base:
            continue

        hero_emoji = get_emoji(
            hero.name, discord_emoji_list, client_emoji_list)

        try:
            max_level_for_townhall = hero.get_max_level_for_townhall(
                player_obj.town_hall)
        except:
            max_level_for_townhall = hero.max_level

        hero_value += (f"{hero_emoji} `{hero.level} | "
                       f"{max_level_for_townhall} | "
                       f"{hero.max_level}`\n")

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

        try:
            max_level_for_townhall = pet.get_max_level_for_townhall(
                player_obj.town_hall)
        except:
            max_level_for_townhall = pet.max_level

        pet_value += (f"{pet_emoji} `{pet.level} | "
                      f"{max_level_for_townhall} | "
                      f"{pet.max_level}`\n")

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


def link_clash_of_stats(player):
    """
        returns a formatted player's link to Clash of Stats page

        Args:
            player ([obj]): coc.py player object

        Returns:
            [str]: string of formatted player's link to Clash of Stats page
    """

    base_url = "https://www.clashofstats.com/players/"
    summary_url = "/summary"
    player_url = f"{player.name} {player.tag}"
    player_url = player_url.replace(" ", "-")
    player_url = player_url.replace("#", "")

    clash_of_stats_player_url = base_url+player_url+summary_url

    formatted_string = (
        f"[{player.name} clash of stats]"
        f"({clash_of_stats_player_url})"
    )

    return formatted_string


def link_chocolate_clash(player):
    """
        returns a formatted player's link to Chocolate Clash page

        Args:
            player ([obj]): coc.py player object

        Returns:
            [str]: string of formatted player's link to Chocolate Clash page
    """

    base_url = "https://chocolateclash.com/cc_n/member.php?tag="
    player_url = player.tag.replace("#", "")

    chocolateclash_player_url = base_url+player_url

    formatted_string = (
        f"[{player.name} ChocolateClash]"
        f"({chocolateclash_player_url})"
    )

    return formatted_string
