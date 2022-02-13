import utils.coc_utils as coc_utils
from disnake import ApplicationCommandInteraction
from disnake.ext import commands


async def autocomp_unit(
    inter: ApplicationCommandInteraction,
    user_input: str
):
    unit_list = []
    unit_list.extend(coc_utils.get_home_troop_order())
    unit_list.extend(coc_utils.get_spell_order())

    autocomp_list = []
    for unit in unit_list:
        if user_input.lower() in unit.lower():
            autocomp_list.append(unit)

    del autocomp_list[25:]
    return [unit for unit in autocomp_list]


async def autocomp_supertroop(
    inter: ApplicationCommandInteraction,
    user_input: str
):
    unit_list = []
    unit_list.extend(coc_utils.get_super_troop_order())

    autocomp_list = []
    for unit in unit_list:
        if user_input.lower() in unit.lower():
            autocomp_list.append(unit)

    del autocomp_list[25:]
    return [unit for unit in autocomp_list]


command_param_dict = {
    'user': commands.Param(
        name="user",
        description="*optional* user to search for active player",
        default=None
    ),
    'clan_role': commands.Param(
        name="clan_role",
        description="*optional* clan role to use linked clan",
        default=None
    ),
    'tag': commands.Param(
        name="tag",
        description="*optional* tag to search",
        default=None
    ),
    'unit_name': commands.Param(
        name="unit_name",
        description="clash of clans unit name to search for"
    ),
    'super_troop': commands.Param(
        name="super_troop",
        description="*optional* name of super troop to search clan donations",
        default=None
    ),
    'unit_type': commands.Param(
        name="unit_type",
        description="*optional* type of unit to return information for",
        default="all",
        choices=[
            "all", "hero", "pet", "troop", "spell", "siege"
        ]
    ),
    'war_selection': commands.Param(
        name="cwl_war_selection",
        description="*optional* cwl war selection",
        default=None,
        choices=[
            "previous", "current", "upcoming"
        ]
    ),
    'missed_attacks': commands.Param(
        name="missed_attacks",
        description="*optional* specified missed attack count",
        default=None,
        choices=[1, 2]
    ),
    'channel': commands.Param(
        name="channel",
        description="channel to announce the message"
    ),
    'message': commands.Param(
        name="message",
        description="message to send the specified channel"
    ),
    'required_tag': commands.Param(
        name="tag",
        description="tag to search"
    ),
    'api_key': commands.Param(
        name="api_key",
        description="api key provided from in game"
    ),
    'role': commands.Param(
        name="role",
        description="mentioned discord role"
    ),
    'rank_name': commands.Param(
        name="rank_name",
        description="requested rank to link to role",
        choices=[
            "leader", "co-leader", "elder", "member", "uninitiated"
        ]
    ),
    'coc_name': commands.Param(
        name="coc_name",
        description="name of emoji to search for"
    ),
    'player_info': commands.Param(
        name="option",
        description="*optional* options for player info returns",
        default="overview",
        choices=[
            "overview", "recruit"
        ]
    ),
    'player_unit': commands.Param(
        name="option",
        description="*optional* options for player unit returns",
        default="all",
        choices=[
            "all", "find"
        ]
    ),
    'clan_lineup': commands.Param(
        name="option",
        description="*optional* options for clan lineup returns",
        default="overview",
        choices=[
            "overview", "member"
        ]
    ),
    'clan_warpreference': commands.Param(
        name="option",
        description="*optional* options for clan warpreference returns",
        default="overview",
        choices=[
            "overview", "member"
        ]
    ),
    'clan_supertroop': commands.Param(
        name="option",
        description="*optional* options for clan supertroop returns",
        default="active",
        choices=[
            "active", "donate"
        ]
    ),
    'war_stars': commands.Param(
        name="option",
        description="*optional* options for war star returns",
        default="stars",
        choices=[
            "stars", "attacks"
        ]
    ),
    'war_lineup': commands.Param(
        name="option",
        description="*optional* options for war lineup returns",
        default="clan",
        choices=[
            "overview", "clan", "member"
        ]
    ),
}
