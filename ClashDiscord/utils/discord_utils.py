import utils.coc_utils as coc_utils
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from data.ClashDiscord_Client_Data import ClashDiscord_Data


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


async def autocomp_emoji_name(
    inter: ApplicationCommandInteraction,
    user_input: str
):
    emoji_name_list = []
    emoji_list = ClashDiscord_Data().emojis
    for emoji in emoji_list:
        emoji_name_list.append(emoji.coc_name)

    autocomp_list = []
    for emoji_name in emoji_name_list:
        if user_input.lower() in emoji_name.lower():
            autocomp_list.append(emoji_name)

    del autocomp_list[25:]
    return [emoji_name for emoji_name in autocomp_list]


command_param_dict = {
    'user': commands.Param(
        name="user",
        description="*optional* user to search for active player",
        default=None
    ),
    'required_user': commands.Param(
        name="user",
        description="user mention"
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
        description="*optional* super troop name to search clan donations",
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
        description="*optional* channel to announce the message",
        default=None
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
        description="api key provided from in game",
        default=None
    ),
    'role': commands.Param(
        name="role",
        description="mentioned discord role"
    ),
    'rank_name': commands.Param(
        name="rank_name",
        description="*optional* requested rank to link to role",
        default=None,
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
            "overview", "member", "count"
        ]
    ),
    'clan_warpreference': commands.Param(
        name="option",
        description="*optional* options for clan warpreference returns",
        default="overview",
        choices=[
            "overview", "count"
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
    'star_count': commands.Param(
        name="star_count",
        description="*optional* star count selection for open bases",
        default=2,
        choices=[
            0, 1, 2
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
    'cwl_scoreboard': commands.Param(
        name="option",
        description="*optional* options for cwl scoreboard returns",
        default="group",
        choices=[
            "group", "rounds", "clan"
        ]
    ),
    'coc_name': commands.Param(
        name="emoji_name",
        description="options for emoji name"
    ),
    'discord_user': commands.Param(
        name="option",
        description="*optional* options for discord user returns",
        default="clan",
        choices=[
            "player", "clan"
        ]
    ),
    'discord_user_tag': commands.Param(
        name="player_tag",
        description="*optional* player tag to search linked user",
        default=None
    ),
    'client_user': commands.Param(
        name="option",
        description="*optional* options for client user returns",
        default="claim",
        choices=[
            "claim"
        ]
    ),
    'client_player': commands.Param(
        name="option",
        description="*optional* options for client player returns",
        default="show",
        choices=[
            "claim", "show", "update", "remove", "sync"
        ]
    ),
    'client_player_tag': commands.Param(
        name="player_tag",
        description="*optional* player tag",
        default=None
    ),
    'client_guild': commands.Param(
        name="option",
        description="*optional* options for client guild returns",
        default="claim",
        choices=[
            "claim"
        ]
    ),
    'client_clan': commands.Param(
        name="option",
        description="*optional* options for client clan returns",
        default="show",
        choices=[
            "claim", "show", "remove"
        ]
    ),
    'client_role': commands.Param(
        name="option",
        description="*optional* options for client role returns",
        default="show",
        choices=[
            "show", "remove"
        ]
    ),
    'client_role_mention': commands.Param(
        name="role",
        description="*optional* mentioned discord role",
        default=None
    ),
    'client_clan_rank_role': commands.Param(
        name="option",
        description="*optional* options for client clan and rank role returns",
        default="claim",
        choices=[
            "claim"
        ]
    ),
    'admin_player': commands.Param(
        name="option",
        description="*optional* options for admin player returns",
        default="show",
        choices=[
            "claim", "show", "remove"
        ]
    ),
    'superuser_guild': commands.Param(
        name="option",
        description="*optional* options for superuser guild returns",
        default="show",
        choices=[
            "show", "remove", "leave"
        ]
    ),
    'guild_id': commands.Param(
        name="guild_id",
        description="*optional* id for guild",
        default=None
    ),
    'superuser_admin': commands.Param(
        name="option",
        description="*optional* options for superuser admin returns",
        default="show",
        choices=[
            "show", "toggle", "remove"
        ]
    ),
    'superuser_player': commands.Param(
        name="option",
        description="*optional* options for superuser player returns",
        default="claim",
        choices=[
            "claim", "remove", "sync"
        ]
    ),
}
