import disnake
import coc
from asyncio.tasks import sleep
from disnake.ext import commands
from data import ClashDiscord_Client_Data
import responders.ClashResponder as clash_responder
import responders.DiscordResponder as discord_responder
import responders.RazBotDB_Responder as db_responder
from utils import discord_utils

client_data = ClashDiscord_Client_Data.ClashDiscord_Data()

coc_client = coc.login(
    email=discord_responder.get_client_email(),
    password=discord_responder.get_client_password()
)

intents = disnake.Intents.all()

bot = commands.Bot(
    command_prefix=client_data.prefix,
    intents=intents,
    test_guilds=discord_responder.get_client_test_guilds())
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f"RazBot is ready")


@bot.slash_command(
    description="misc parent")
async def misc(inter):
    pass


@misc.sub_command(
    brief='misc', description='misc command'
)
async def hellothere(inter):
    await inter.response.send_message(content=f'General Kenobi')


@misc.sub_command(
    brief='misc', description="gets the bot ping"
)
async def ping(inter):
    """
        gets the bot ping

        Parameters
        ----------
        inter: disnake interaction object
    """

    await inter.response.defer()

    await inter.edit_original_message(
        content=f"pong {round(inter.bot.latency, 3) * 1000}ms")


# misc link
@misc.sub_command_group(
    brief='misc',
    description="group for misc link commands"
)
async def link(inter):
    """
        group for misc link commands
    """

    pass


@link.sub_command(
    brief='misc', description="gets a clash of stats link"
)
async def clashofstats(inter, player_tag: str):
    """
        gets a clash of stats link

        Parameters
        ----------
        player_tag: player tag to search
    """

    await inter.response.defer()

    player = await clash_responder.get_player(player_tag, coc_client)

    if player is None:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=f"could not find player with tag {player_tag}",
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    await inter.edit_original_message(
        content=(discord_responder.link_clash_of_stats(player)))


@link.sub_command(
    brief='misc', description="gets a ChocolateClash link"
)
async def chocolateclash(inter, player_tag: str):
    """
        gets a ChocolateClash link

        Parameters
        ----------
        player_tag: player tag to search
    """

    await inter.response.defer()

    player = await clash_responder.get_player(player_tag, coc_client)

    if player is None:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=f"could not find player with tag {player_tag}",
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    await inter.edit_original_message(
        content=discord_responder.link_chocolate_clash(player))


# Player

@bot.slash_command()
async def player(inter):
    """
        parent for player commands
    """

    # defer for every command
    await inter.response.defer()


# player info
@player.sub_command_group()
async def info(inter):
    """
        group for player info commands
    """

    pass


@info.sub_command()
async def overview(
    inter,
    user: disnake.User = discord_utils.command_param_dict['user'],
    tag: str = discord_utils.command_param_dict['tag']
):
    """
        get player information

        Parameters
        ----------
        user (optional): user to search for active player
        tag (optional): tag to search
    """

    # setting user to author if not specified
    if user is None:
        user = inter.author

    db_player_obj = db_responder.read_player_active(user.id)

    verification_payload = await discord_responder.player_verification(
        db_player_obj, user, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    player = verification_payload['player_obj']

    # player tag selected
    if tag is not None:
        player = await clash_responder.get_player(tag, coc_client)

        if player is None:
            embed_description = f"could not find player with tag {tag}"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(embed_list, inter)
            return

    field_dict_list = discord_responder.player_info(
        player, inter.client.emojis, client_data.emojis)

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{player.name} {player.tag}",
        bot_user_name=inter.me.display_name,
        thumbnail=player.league.icon,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@info.sub_command()
async def recruit(
    inter,
    user: disnake.User = discord_utils.command_param_dict['user'],
    tag: str = discord_utils.command_param_dict['tag']
):
    """
        get player recruitment information

        Parameters
        ----------
        user (optional): user to search for active player
        tag (optional): tag to search
    """

    # setting user to author if not specified
    if user is None:
        user = inter.author

    db_player_obj = db_responder.read_player_active(user.id)

    verification_payload = await discord_responder.player_verification(
        db_player_obj, user, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    player = verification_payload['player_obj']

    # player tag selected
    if tag is not None:
        player = await clash_responder.get_player(tag, coc_client)

        if player is None:
            embed_description = f"could not find player with tag {tag}"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(embed_list, inter)
            return

    player_field_dict_list = discord_responder.player_info(
        player, inter.client.emojis, client_data.emojis)

    embed_list = []

    embed_list.extend(discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{player.name} {player.tag}",
        bot_user_name=inter.me.display_name,
        thumbnail=player.league.icon,
        field_list=player_field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    ))

    unit_field_dict_list = discord_responder.unit_lvl_all(
        player, inter.client.emojis, client_data.emojis)

    embed_list.extend(discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{player.name} units",
        bot_user_name=inter.me.display_name,
        thumbnail=player.league.icon,
        field_list=unit_field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    ))

    await discord_responder.send_embed_list(embed_list, inter)

    player_links = ""

    player_links += discord_responder.link_clash_of_stats(player)

    player_links += "\n\n"

    player_links += discord_responder.link_chocolate_clash(player)

    await inter.send(content=player_links)


# player unit
@player.sub_command_group(
    brief='player',
    description="group for player unit commands"
)
async def unit(inter):
    """
        group for player unit commands
    """

    pass


@unit.sub_command(
    brief='player',
    description='get level information for a specified unit'
)
async def find(inter,
               unit_name: str = commands.Param(
                   autocomplete=discord_utils.autocomp_donation)):
    """
        get information about a specified player

        Parameters
        ----------
        unit_name: name of the unit you would like information on
    """

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.player_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    player_obj = verification_payload['player_obj']

    unit_obj = clash_responder.find_player_unit(player_obj, unit_name)
    field_dict_list = [discord_responder.unit_lvl(
        player_obj, unit_obj, unit_name,
        inter.client.emojis, client_data.emojis)]
    # unit_obj not found
    # set title to player name
    if not unit_obj:
        title_string = player_obj.name
    # unit_obj found
    # set title to player_name unit_name
    else:
        title_string = f"{player_obj.name} {unit_obj.name}"

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=title_string,
        bot_user_name=inter.me.display_name,
        thumbnail=player_obj.league.icon,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@unit.sub_command(
    brief='player',
    description="get all unit levels"
)
async def all(inter, user: disnake.User = None,
              unit_type: str = commands.Param(default="all", choices=[
        "all", "hero", "pet", "troop", "spell", "siege"])):
    """
        get all unit levels

        Parameters
        ----------
        user (optional): user to search for active player
    """

    # setting user to author if not specified
    if user is None:
        user = inter.author

    db_player_obj = db_responder.read_player_active(user.id)

    verification_payload = await discord_responder.player_verification(
        db_player_obj, user, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    player_obj = verification_payload['player_obj']

    if unit_type == "all":
        field_dict_list = discord_responder.unit_lvl_all(
            player_obj, inter.client.emojis, client_data.emojis
        )
    elif unit_type == "hero":
        field_dict_list = discord_responder.hero_lvl_all(
            player_obj, inter.client.emojis, client_data.emojis
        )
    elif unit_type == "pet":
        field_dict_list = discord_responder.pet_lvl_all(
            player_obj, inter.client.emojis, client_data.emojis
        )
    elif unit_type == "troop":
        field_dict_list = discord_responder.troop_lvl_all(
            player_obj, inter.client.emojis, client_data.emojis
        )
    elif unit_type == "spell":
        field_dict_list = discord_responder.spell_lvl_all(
            player_obj, inter.client.emojis, client_data.emojis
        )
    elif unit_type == "siege":
        field_dict_list = discord_responder.siege_lvl_all(
            player_obj, inter.client.emojis, client_data.emojis
        )

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{player_obj.name} units",
        bot_user_name=inter.me.display_name,
        thumbnail=player_obj.league.icon,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@unit.sub_command(
    brief='player',
    description="get all unit levels for the player specified"
)
async def alltag(inter, player_tag: str,
                 unit_type: str = commands.Param(default="all", choices=[
        "all", "hero", "pet", "troop", "spell", "siege"])):
    """
        get all unit levels for the player specified
    """

    player_obj = await clash_responder.get_player(player_tag, coc_client)

    if player_obj is None:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=f"could not find player with tag {player_tag}",
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    if unit_type == "all":
        field_dict_list = discord_responder.unit_lvl_all(
            player_obj, inter.client.emojis, client_data.emojis
        )
    elif unit_type == "hero":
        field_dict_list = discord_responder.hero_lvl_all(
            player_obj, inter.client.emojis, client_data.emojis
        )
    elif unit_type == "pet":
        field_dict_list = discord_responder.pet_lvl_all(
            player_obj, inter.client.emojis, client_data.emojis
        )
    elif unit_type == "troop":
        field_dict_list = discord_responder.troop_lvl_all(
            player_obj, inter.client.emojis, client_data.emojis
        )
    elif unit_type == "spell":
        field_dict_list = discord_responder.spell_lvl_all(
            player_obj, inter.client.emojis, client_data.emojis
        )
    elif unit_type == "siege":
        field_dict_list = discord_responder.siege_lvl_all(
            player_obj, inter.client.emojis, client_data.emojis
        )

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{player_obj.name} units",
        bot_user_name=inter.me.display_name,
        thumbnail=player_obj.league.icon,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# player supertroop
@player.sub_command_group(
    brief='player',
    description="group for player supertroop commands"
)
async def supertroop(inter):
    """
        group for player supertroop commands
    """

    pass


@supertroop.sub_command(
    brief='player',
    description="check to see player's active super troops "
)
async def user(inter, user: disnake.User = None):
    """
        check to see player's active super troops

        Parameters
        ----------
        user (optional): user to search for active player
    """

    # setting user to author if not specified
    if user is None:
        user = inter.author

    db_player_obj = db_responder.read_player_active(user.id)

    verification_payload = await discord_responder.player_verification(
        db_player_obj, user, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    player_obj = verification_payload['player_obj']

    active_super_troop_list = clash_responder.player_active_super_troops(
        player_obj)

    field_dict_list = discord_responder.active_super_troops(
        player_obj, active_super_troop_list,
        inter.client.emojis, client_data.emojis
    )
    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{player_obj.name} super troops",
        bot_user_name=inter.me.display_name,
        thumbnail=player_obj.league.icon,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# Clan

@bot.slash_command(
    brief='clan',
    description="parent for clan commands"
)
async def clan(inter):
    """
        parent for clan commands
    """

    # defer for every command
    await inter.response.defer()


# clan info
@clan.sub_command_group(
    brief='clan',
    description="group for clan info commands"
)
async def info(inter):
    """
        group for clan info commands
    """

    pass


@info.sub_command(
    brief='clan',
    description="get information about your active player's clan"
)
async def overview(inter, clan_role: disnake.Role = None):
    """
        get clan information

        Parameters
        ----------
        clan_role (optional): clan role to use linked clan
    """

    # role not mentioned
    if clan_role is None:
        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = await discord_responder.clan_verification(
            db_player_obj, inter.author, coc_client)
    # role has been mentioned
    else:
        verification_payload = await discord_responder.clan_role_verification(
            clan_role, coc_client)

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    clan_obj = verification_payload['clan_obj']

    field_dict_list = discord_responder.clan_info(
        clan_obj, inter.client.emojis, client_data.emojis
    )

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{clan_obj.name} {clan_obj.tag}",
        bot_user_name=inter.me.display_name,
        thumbnail=clan_obj.badge,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@info.sub_command(
    brief='clan',
    description="Enter a clan's tag and get a clan's information"
)
async def find(inter, clan_tag: str):
    """
        get information about a requested clan

        Parameters
        ----------
        clan_tag: clan tag to search
    """

    clan_obj = await clash_responder.get_clan(clan_tag, coc_client)

    # clan with given tag not found
    if clan_obj is None:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=f"could not find clan with tag {clan_tag}",
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    field_dict_list = discord_responder.clan_info(
        clan_obj, inter.client.emojis, client_data.emojis
    )

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{clan_obj.name} {clan_obj.tag}",
        bot_user_name=inter.me.display_name,
        thumbnail=clan_obj.badge,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# clan lineup
@clan.sub_command_group(
    brief='clan',
    description="group for clan lineup commands"
)
async def lineup(inter):
    """
        group for clan lineup commands
    """

    pass


@lineup.sub_command(
    brief='clan',
    description="*leadership* get clan lineup overview information"
)
async def overview(inter, clan_role: disnake.Role = None):
    """
        *leadership*
        get clan lineup overview information

        Parameters
        ----------
        clan_role (optional): clan role to use linked clan
    """

    # role not mentioned
    if clan_role is None:
        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = (
            await discord_responder.clan_leadership_verification(
                db_player_obj, inter.author, inter.guild.id, coc_client))
    # role has been mentioned
    else:
        verification_payload = (
            await discord_responder.clan_role_player_leadership_verification(
                clan_role, inter.author, inter.guild.id, coc_client))

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    clan_obj = verification_payload['clan_obj']

    field_dict_list = await discord_responder.clan_lineup(
        clan_obj, coc_client, inter.client.emojis, client_data.emojis)

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{clan_obj.name} lineup",
        bot_user_name=inter.me.display_name,
        thumbnail=clan_obj.badge,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@lineup.sub_command(
    brief='clan',
    description="*leadership* get clan lineup information for all members"
)
async def member(inter, clan_role: disnake.Role = None):
    """
        *leadership*
        get clan lineup information for all members

        Parameters
        ----------
        clan_role (optional): clan role to use linked clan
    """

    # role not mentioned
    if clan_role is None:
        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = (
            await discord_responder.clan_leadership_verification(
                db_player_obj, inter.author, inter.guild.id, coc_client))
    # role has been mentioned
    else:
        verification_payload = (
            await discord_responder.clan_role_player_leadership_verification(
                clan_role, inter.author, inter.guild.id, coc_client))

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    clan_obj = verification_payload['clan_obj']

    field_dict_list = await discord_responder.clan_lineup_member(
        clan_obj, coc_client, inter.client.emojis, client_data.emojis)

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{clan_obj.name} member lineup",
        bot_user_name=inter.me.display_name,
        thumbnail=clan_obj.badge,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# clan warpreference
@clan.sub_command_group(
    brief='clan',
    description="group for clan war preference commands"
)
async def warpreference(inter):
    """
        group for clan war preference commands
    """

    pass


@warpreference.sub_command(
    brief='clan',
    description="*leadership* rundown of clan's war preference"
)
async def overview(inter, clan_role: disnake.Role = None):
    """
        *leadership*
        rundown of clan's war preference

        Parameters
        ----------
        clan_role (optional): clan role to use linked clan
    """

    # role not mentioned
    if clan_role is None:
        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = (
            await discord_responder.clan_leadership_verification(
                db_player_obj, inter.author, inter.guild.id, coc_client))
    # role has been mentioned
    else:
        verification_payload = (
            await discord_responder.clan_role_player_leadership_verification(
                clan_role, inter.author, inter.guild.id, coc_client))

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    clan_obj = verification_payload['clan_obj']

    field_dict_list = await discord_responder.war_preference_clan(
        clan_obj, coc_client, inter.client.emojis, client_data.emojis)

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{clan_obj.name} war preference",
        bot_user_name=inter.me.display_name,
        thumbnail=clan_obj.badge,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@warpreference.sub_command(
    brief='clan',
    description="*leadership* rundown of clan member's war preference"
)
async def member(inter, clan_role: disnake.Role = None):
    """
        *leadership*
        rundown of clan member's war preference

        Parameters
        ----------
        clan_role (optional): clan role to use linked clan
    """

    # role not mentioned
    if clan_role is None:
        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = (
            await discord_responder.clan_leadership_verification(
                db_player_obj, inter.author, inter.guild.id, coc_client))
    # role has been mentioned
    else:
        verification_payload = (
            await discord_responder.clan_role_player_leadership_verification(
                clan_role, inter.author, inter.guild.id, coc_client))

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    clan_obj = verification_payload['clan_obj']

    embed_description = await discord_responder.war_preference_member(
        clan_obj, coc_client, inter.client.emojis, client_data.emojis)

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{clan_obj.name} member war preference",
        description=embed_description,
        bot_user_name=inter.me.display_name,
        thumbnail=clan_obj.badge,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# clan unit
@clan.sub_command_group(
    brief='clan',
    description="group for clan unit commands"
)
async def unit(inter):
    """
        group for clan unit commands
    """

    pass


@unit.sub_command(
    brief='clan',
    description='shows who can donate the best requested troop'
)
async def donate(
        inter,
        unit_name: str = commands.Param(
            autocomplete=discord_utils.autocomp_donation),
        clan_role: disnake.Role = None):
    """
        get information about mentioned clan

        Parameters
        ----------
        unit_name: name of unit to search clan donations
        clan_role (optional): clan role to use linked clan
    """

    # role not mentioned
    if clan_role is None:
        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = await discord_responder.clan_verification(
            db_player_obj, inter.author, coc_client)
    # role has been mentioned
    else:
        verification_payload = await discord_responder.clan_role_verification(
            clan_role, coc_client)

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    clan_obj = verification_payload['clan_obj']

    donator_list = await clash_responder.donation(
        clan_obj, unit_name, coc_client)

    field_dict_list = discord_responder.donation(
        clan_obj, donator_list, unit_name,
        inter.client.emojis, client_data.emojis
    )

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{clan_obj.name} {clan_obj.tag}",
        bot_user_name=inter.me.display_name,
        thumbnail=clan_obj.badge,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# clan supertroop
@clan.sub_command_group(
    brief='clan',
    description="group for clan supertroop commands"
)
async def supertroop(inter):
    """
        group for clan supertroop commands
    """

    pass


@supertroop.sub_command(
    brief='clan',
    description="shows all active supertroops in the clan"
)
async def active(
    inter,
    clan_role: disnake.Role = None
):
    """
        shows all active supertroops in the clan

        Parameters
        ----------
        clan_role (optional): clan role to use linked clan
    """

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.player_verification(
        db_player_obj, inter.author, coc_client
    )

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    player_obj = verification_payload['player_obj']

    # role not mentioned
    if clan_role is None:
        verification_payload = await discord_responder.clan_verification(
            db_player_obj, inter.author, coc_client)
    # role has been mentioned
    else:
        verification_payload = await discord_responder.clan_role_verification(
            clan_role, coc_client)

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    clan_obj = verification_payload['clan_obj']

    field_dict_list = await discord_responder.clan_super_troop_active(
        clan_obj, inter.client.emojis, client_data.emojis, coc_client)

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{clan_obj.name} active super troops",
        bot_user_name=inter.me.display_name,
        thumbnail=clan_obj.badge,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@supertroop.sub_command(
    brief='clan',
    description="shows who in your clan has a specified super troop active"
)
async def donate(
        inter,
        unit_name: str = commands.Param(
            autocomplete=discord_utils.autocomp_supertroop),
        clan_role: disnake.Role = None):
    """
        shows who in your clan has a specified super troop active

        Parameters
        ----------
        unit_name: name of unit to search clan donations
        clan_role (optional): clan role to use linked clan
    """

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.player_verification(
        db_player_obj, inter.author, coc_client
    )

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    player_obj = verification_payload['player_obj']

    # role not mentioned
    if clan_role is None:
        verification_payload = await discord_responder.clan_verification(
            db_player_obj, inter.author, coc_client)
    # role has been mentioned
    else:
        verification_payload = await discord_responder.clan_role_verification(
            clan_role, coc_client)

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    clan_obj = verification_payload['clan_obj']

    super_troop_name = clash_responder.find_super_troop_name(unit_name)

    # super troop was not found
    if super_troop_name is None:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=f"{unit_name} is not a viable request",
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    donor_list = await clash_responder.active_super_troop_search(
        clan_obj, super_troop_name, coc_client)

    field_dict_list = discord_responder.super_troop_search(
        clan_obj, donor_list, super_troop_name,
        inter.client.emojis, client_data.emojis
    )

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{clan_obj.name} {clan_obj.tag}",
        bot_user_name=inter.me.display_name,
        thumbnail=clan_obj.badge,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# War

@bot.slash_command(
    brief='war',
    description="parent for war commands"
)
async def war(inter):
    """
        parent for war commands
    """

    # defer for every command
    await inter.response.defer()


# war info
@war.sub_command_group(
    brief='war',
    description="group for war info commands"
)
async def info(inter):
    """
        group for war info commands
    """

    pass


@info.sub_command(
    brief='war',
    description="overview of the current war"
)
async def overview(
    inter,
    clan_role: disnake.Role = None,
    war_selection: str = commands.Param(default=None, choices=[
        "previous", "current", "upcoming"])
):
    """
        overview of the current war

        Parameters
        ----------
        clan_role (optional): clan role to use linked clan
        war_selection (optional): cwl war selection
    """

    # role not mentioned
    if clan_role is None:
        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = await discord_responder.war_verification(
            db_player_obj, war_selection, inter.author, coc_client)
    # role has been mentioned
    else:
        verification_payload = await discord_responder.clan_role_war_verification(
            clan_role, war_selection, coc_client)

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_info(
        war_obj, inter.client.emojis, client_data.emojis)

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        bot_user_name=inter.me.display_name,
        thumbnail=war_obj.clan.badge,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@info.sub_command(
    brief='war',
    description="scoreboard for the current war"
)
async def scoreboard(
    inter,
    clan_role: disnake.Role = None,
    war_selection: str = commands.Param(default=None, choices=[
        "previous", "current", "upcoming"])
):
    """
        overview of the current war

        Parameters
        ----------
        clan_role (optional): clan role to use linked clan
        war_selection (optional): cwl war selection
    """

    # role not mentioned
    if clan_role is None:
        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = await discord_responder.war_verification(
            db_player_obj, war_selection, inter.author, coc_client)
    # role has been mentioned
    else:
        verification_payload = await discord_responder.clan_role_war_verification(
            clan_role, war_selection, coc_client)

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_scoreboard(
        war_obj, inter.client.emojis, client_data.emojis)

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        bot_user_name=inter.me.display_name,
        thumbnail=war_obj.clan.badge,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# war clan
@war.sub_command_group(
    brief='war',
    description="group for war clan commands"
)
async def clan(inter):
    """
        group for war clan commands
    """

    pass


@clan.sub_command(
    brief='war',
    description="list of players that missed attacks in the current war"
)
async def noattack(
    inter,
    missed_attacks: int = commands.Param(default=None, choices=[1, 2]),
    clan_role: disnake.Role = None,
    war_selection: str = commands.Param(default=None, choices=[
        "previous", "current", "upcoming"])
):
    """
        list of players that missed attacks in the current war

        Parameters
        ----------
        missed_attacks (optional): specified missed attack count
        clan_role (optional): clan role to use linked clan
        war_selection (optional): cwl war selection
    """

    # role not mentioned
    if clan_role is None:
        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = await discord_responder.war_verification(
            db_player_obj, war_selection, inter.author, coc_client)
    # role has been mentioned
    else:
        verification_payload = await discord_responder.clan_role_war_verification(
            clan_role, war_selection, coc_client)

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_no_attack(war_obj, missed_attacks)

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        bot_user_name=inter.me.display_name,
        thumbnail=war_obj.clan.badge,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@clan.sub_command(
    brief='war',
    description="*leadership* overview of all members in war"
)
async def stars(
    inter,
    clan_role: disnake.Role = None,
    war_selection: str = commands.Param(default=None, choices=[
        "previous", "current", "upcoming"])
):
    """
        *leadership*
        overview of all members in war

        Parameters
        ----------
        clan_role (optional): clan role to use linked clan
        war_selection (optional): cwl war selection
    """

    # role not mentioned
    if clan_role is None:
        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = (
            await discord_responder.war_leadership_verification(
                db_player_obj, war_selection,
                inter.author, inter.guild.id, coc_client))
    # role has been mentioned
    else:
        verification_payload = (
            await discord_responder.clan_role_war_leadership_verification(
                clan_role, war_selection,
                inter.author, inter.guild.id, coc_client))

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_clan_stars(
        war_obj, inter.client.emojis, client_data.emojis)

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        bot_user_name=inter.me.display_name,
        thumbnail=war_obj.clan.badge,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@clan.sub_command(
    brief='war',
    description="*leadership* all attacks for every war member"
)
async def attacks(
    inter,
    clan_role: disnake.Role = None,
    war_selection: str = commands.Param(default=None, choices=[
        "previous", "current", "upcoming"])
):
    """
        *leadership*
        all attacks for every war member

        Parameters
        ----------
        clan_role (optional): clan role to use linked clan
        war_selection (optional): cwl war selection
    """

    # role not mentioned
    if clan_role is None:
        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = (
            await discord_responder.war_leadership_verification(
                db_player_obj, war_selection,
                inter.author, inter.guild.id, coc_client))
    # role has been mentioned
    else:
        verification_payload = (
            await discord_responder.clan_role_war_leadership_verification(
                clan_role, war_selection,
                inter.author, inter.guild.id, coc_client))

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_all_attacks(
        war_obj, inter.client.emojis, client_data.emojis)

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        bot_user_name=inter.me.display_name,
        thumbnail=war_obj.clan.badge,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# war score
@war.sub_command_group(
    brief='war',
    description="group for war score commands"
)
async def score(inter):
    """
        group for war score commands
    """

    pass


@score.sub_command(
    brief='war',
    description="your war member score"
)
async def user(
    inter,
    user: disnake.User = None,
    war_selection: str = commands.Param(default=None, choices=[
        "previous", "current", "upcoming"])
):
    """
        your war member score

        Parameters
        ----------
        user (optional): user to search for active player
        war_selection (optional): cwl war selection
    """

    # setting user to author if not specified
    if user is None:
        user = inter.author

    db_player_obj = db_responder.read_player_active(user.id)

    verification_payload = await discord_responder.war_verification(
        db_player_obj, war_selection, user, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_member_score(
        war_obj, player_obj)
    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{player_obj.name} war score",
        bot_user_name=inter.me.display_name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@score.sub_command(
    brief='war',
    description="*leadership* every clanmate's war member score"
)
async def clan(
    inter,
    clan_role: disnake.Role = None,
    war_selection: str = commands.Param(default=None, choices=[
        "previous", "current", "upcoming"])
):
    """
        *leadership*
        every clanmate's war member score

        Parameters
        ----------
        clan_role (optional): clan role to use linked clan
        war_selection (optional): cwl war selection
    """

    # role not mentioned
    if clan_role is None:
        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = (
            await discord_responder.war_leadership_verification(
                db_player_obj, war_selection,
                inter.author, inter.guild.id, coc_client))
    # role has been mentioned
    else:
        verification_payload = (
            await discord_responder.clan_role_war_leadership_verification(
                clan_role, war_selection,
                inter.author, inter.guild.id, coc_client))

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_clan_score(
        war_obj)
    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        bot_user_name=inter.me.display_name,
        thumbnail=war_obj.clan.badge,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# war lineup
@war.sub_command_group(
    brief='war',
    description="group for war lineup commands"
)
async def lineup(inter):
    """
        group for war lineup commands
    """

    pass


@lineup.sub_command(
    brief='war',
    description="town hall lineup overview for war"
)
async def overview(
    inter,
    clan_role: disnake.Role = None,
    war_selection: str = commands.Param(default=None, choices=[
        "previous", "current", "upcoming"])
):
    """
        town hall lineup overview for war

        Parameters
        ----------
        clan_role (optional): clan role to use linked clan
        war_selection (optional): cwl war selection
    """

    # role not mentioned
    if clan_role is None:
        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = await discord_responder.war_verification(
            db_player_obj, war_selection, inter.author, coc_client)
    # role has been mentioned
    else:
        verification_payload = await discord_responder.clan_role_war_verification(
            clan_role, war_selection, coc_client)

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    war_obj = verification_payload['war_obj']

    await inter.edit_original_message(
        content=discord_responder.war_lineup_overview(war_obj))


@lineup.sub_command(
    brief='war',
    description="town hall lineup for each war member"
)
async def clan(
    inter,
    clan_role: disnake.Role = None,
    war_selection: str = commands.Param(default=None, choices=[
        "previous", "current", "upcoming"])
):
    """
        town hall lineup for each war member

        Parameters
        ----------
        clan_role (optional): clan role to use linked clan
        war_selection (optional): cwl war selection
    """

    # role not mentioned
    if clan_role is None:
        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = (
            await discord_responder.war_verification(
                db_player_obj, war_selection, inter.author, coc_client))
    # role has been mentioned
    else:
        verification_payload = await discord_responder.clan_role_war_verification(
            clan_role, war_selection, coc_client)

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_lineup_clan(
        war_obj, inter.client.emojis, client_data.emojis)
    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        bot_user_name=inter.me.display_name,
        thumbnail=war_obj.clan.badge,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@lineup.sub_command(
    brief='war',
    description="lineup for each war member"
)
async def member(
    inter,
    clan_role: disnake.Role = None,
    war_selection: str = commands.Param(default=None, choices=[
        "previous", "current", "upcoming"])
):
    """
        lineup for each war member

        Parameters
        ----------
        clan_role (optional): clan role to use linked clan
        war_selection (optional): cwl war selection
    """

    # role not mentioned
    if clan_role is None:
        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = await discord_responder.war_verification(
            db_player_obj, war_selection, inter.author, coc_client)
    # role has been mentioned
    else:
        verification_payload = await discord_responder.clan_role_war_verification(
            clan_role, war_selection, coc_client)

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    war_obj = verification_payload['war_obj']

    field_dict_list = (await discord_responder.war_lineup_member(
        war_obj.clan, coc_client, inter.client.emojis, client_data.emojis))

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{war_obj.clan.name} members",
        bot_user_name=inter.me.display_name,
        thumbnail=war_obj.clan.badge,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)

    field_dict_list = await discord_responder.war_lineup_member(
        war_obj.opponent, coc_client, inter.client.emojis, client_data.emojis)

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{war_obj.opponent.name} members",
        bot_user_name=inter.me.display_name,
        thumbnail=war_obj.opponent.badge,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# CWL

@bot.slash_command(
    brief='cwl',
    description="parent for cwl commands"
)
async def cwl(inter):
    """
        parent for cwl commands
    """

    # defer for every command
    await inter.response.defer()


# cwl lineup
@cwl.sub_command_group(
    brief='cwl',
    description="group for cwl lineup commands"
)
async def lineup(inter):
    """
        group for cwl lineup commands
    """

    pass


@lineup.sub_command(
    brief='cwl',
    description="returns the CWL group lineup"
)
async def overview(inter, clan_role: disnake.Role = None):
    """
        returns the CWL group lineup

        Parameters
        ----------
        clan_role (optional): clan role to use linked clan
    """

    # role not mentioned
    if clan_role is None:
        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = await discord_responder.cwl_group_verification(
            db_player_obj, inter.author, coc_client)
    # role has been mentioned
    else:
        verification_payload = await discord_responder.clan_role_cwl_group_verification(
            clan_role, coc_client)

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    cwl_group_obj = verification_payload['cwl_group_obj']

    await inter.edit_original_message(
        content=discord_responder.cwl_lineup(cwl_group_obj))


@lineup.sub_command(
    brief='cwl',
    description="returns the CWL group clan lineup"
)
async def clan(inter, clan_tag: str, clan_role: disnake.Role = None):
    """
        returns the CWL group clan lineup

        Parameters
        ----------
        clan_tag: clan tag to search
        clan_role (optional): clan role to use linked clan
    """

    clan_obj = await clash_responder.get_clan(clan_tag, coc_client)
    # clan with given tag not found
    if clan_obj is None:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=f"could not find clan with tag {clan_tag}",
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # role not mentioned
    if clan_role is None:
        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = (
            await discord_responder.cwl_group_leadership_verification(
                db_player_obj, inter.author, inter.guild.id, coc_client))
    # role has been mentioned
    else:
        verification_payload = (
            await discord_responder.clan_role_cwl_group_leadership_verification(
                clan_role, inter.author, inter.guild.id, coc_client))

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    cwl_group_obj = verification_payload['cwl_group_obj']
    player_clan_obj = verification_payload['clan_obj']
    cwl_clan_obj = coc.utils.get(cwl_group_obj.clans, tag=clan_obj.tag)

    # clan not in specified group
    if cwl_clan_obj is None:
        description = (
            f"{clan_obj.name} {clan_obj.tag} not in cwl group "
            f"with {player_clan_obj.name} {player_clan_obj.tag}"
        )
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    field_dict_list = await discord_responder.war_lineup_member(
        cwl_clan_obj, coc_client, inter.client.emojis, client_data.emojis)
    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{cwl_clan_obj.name} {cwl_clan_obj.tag}",
        bot_user_name=inter.me.display_name,
        thumbnail=cwl_clan_obj.badge,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@lineup.sub_command(
    brief='cwl',
    description="*leadership* returns the CWL group member lineup"
)
async def member(inter, clan_role: disnake.Role = None):
    """
        *leadership*
        returns the CWL group member lineup

        Parameters
        ----------
        clan_role (optional): clan role to use linked clan
    """

    # role not mentioned
    if clan_role is None:
        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = (
            await discord_responder.cwl_group_leadership_verification(
                db_player_obj, inter.author, inter.guild.id, coc_client))
    # role has been mentioned
    else:
        verification_payload = (
            await discord_responder.clan_role_cwl_group_leadership_verification(
                clan_role, coc_client))

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    cwl_group_obj = verification_payload['cwl_group_obj']

    for clan in cwl_group_obj.clans:
        field_dict_list = await discord_responder.war_lineup_member(
            clan, coc_client, inter.client.emojis, client_data.emojis)
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{clan.name} {clan.tag}",
            bot_user_name=inter.me.display_name,
            thumbnail=clan.badge,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)


# cwl score
@cwl.sub_command_group(
    brief='cwl',
    description="group for cwl score commands"
)
async def score(inter):
    """
        group for cwl score commands
    """

    pass


@score.sub_command(
    brief='cwl',
    description="lists each score you have in CWL"
)
async def user(inter, user: disnake.User = None):
    """
        returns specified user's active player's cwl score

        Parameters
        ----------
        user (optional): user to search for active player
    """

    # setting user to author if not specified
    if user is None:
        user = inter.author

    db_player_obj = db_responder.read_player_active(user.id)

    verification_payload = await discord_responder.cwl_group_verification(
        db_player_obj, user, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    player_obj = verification_payload['player_obj']
    cwl_group_obj = verification_payload['cwl_group_obj']

    field_dict_list = await discord_responder.cwl_member_score(
        player_obj, cwl_group_obj, player_obj.clan.tag)
    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{player_obj.name} CWL score",
        bot_user_name=inter.me.display_name,
        thumbnail=player_obj.league.icon,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@score.sub_command(
    brief='cwl',
    description="Lists each member and their score in CWL"
)
async def clan(inter, clan_role: disnake.Role = None):
    """
        *leadership*
        returns all member scores for the specified clan

        Parameters
        ----------
        clan_role (optional): clan role to use linked clan
    """

    # role not mentioned
    if clan_role is None:
        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = (
            await discord_responder.cwl_group_leadership_verification(
                db_player_obj, inter.author, inter.guild.id, coc_client)
        )
    # role has been mentioned
    else:
        verification_payload = (
            await discord_responder.clan_role_cwl_group_leadership_verification(
                clan_role, inter.author, inter.guild.id, coc_client))

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    player_obj = verification_payload['player_obj']
    clan_obj = verification_payload['clan_obj']
    cwl_group_obj = verification_payload['cwl_group_obj']

    field_dict_list = await discord_responder.cwl_clan_score(
        clan_obj, cwl_group_obj)
    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{clan_obj.name} CWL scores",
        bot_user_name=inter.me.display_name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# Discord

@bot.slash_command(
    brief='discord',
    description="parent for discord commands"
)
async def discord(inter):
    """
        parent for discord commands
    """

    pass


# discord help
@discord.sub_command_group(
    brief='client',
    description="group for discord help commands"
)
async def help(inter):
    """
        group for discord help commands
    """

    # defer for every command
    await inter.response.defer()


@help.sub_command(
    brief='discord',
    description="returns help menu"
)
async def info(inter):
    """
        returns help menu
    """

    db_guild_obj = db_responder.read_guild(inter.guild.id)
    db_player_obj = db_responder.read_player_active(inter.author.id)

    if db_player_obj:
        player_obj = await clash_responder.get_player(
            db_player_obj.player_tag, coc_client)
    else:
        player_obj = None

    help_dict = discord_responder.help_main(
        db_guild_obj, inter.author.id, player_obj, client_data.bot_categories)
    field_dict_list = help_dict['field_dict_list']
    emoji_list = help_dict['emoji_list']

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{inter.me.display_name} help menu",
        bot_user_name=inter.me.display_name,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)

    original_message = await inter.original_message()

    for emoji in emoji_list:
        await original_message.add_reaction(emoji)


# discord announce
@discord.sub_command_group(
    brief='client',
    description="group for discord announce commands"
)
async def announce(inter):
    """
        group for discord announce commands
    """

    await inter.response.defer(ephemeral=True)


@announce.sub_command(
    description=("*leadership* "
                 "announces message to specified channel")
)
async def message(inter, channel: disnake.TextChannel, message: str):
    """
        *leadership*
        announces message to specified channel

        Parameters
        ----------
        channel: channel to announce the message
        message: message to send the specified channel
    """

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = (
        await discord_responder.player_leadership_verification(
            db_player_obj, inter.author, inter.guild.id, coc_client))
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    message = "**ANNOUNCEMENT**\n\n" + message

    try:
        await channel.send(content=message)
    except:
        field_dict_list = [{
            "name": "message could not be sent",
            "value": f"please ensure bot is in channel {channel.mention}"
        }]
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    field_dict_list = [{
        "name": "message sent",
        "value": f"channel {channel.mention}"
    }]
    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        bot_user_name=inter.me.display_name,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@announce.sub_command(
    description=("*leadership* "
                 "announces message to specified channel, "
                 "pings user with the specified player tag")
)
async def player(
    inter, channel: disnake.TextChannel,
    message: str, player_tag: str
):
    """
        *leadership*
        announces message to specified channel,
        pings user with the specified player tag

        Parameters
        ----------
        channel: channel to announce the message
        player_tag: player tag to find and ping user
        message: message to send the specified channel
    """

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = (
        await discord_responder.player_leadership_verification(
            db_player_obj, inter.author, inter.guild.id, coc_client))
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    player = await clash_responder.get_player(player_tag, coc_client)

    if player is None:
        field_dict_list = [{
            "name": f"player with tag {player_tag} not found",
            "value": f"please check the tag and try again"
        }]
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    message = f"**{player.name} {player.tag}**\n\n" + message
    message += "\n\n"

    message += discord_responder.user_player_ping(
        player, inter.guild.members)

    try:
        await channel.send(content=message)
    except:
        field_dict_list = [{
            "name": "message could not be sent",
            "value": f"please ensure bot is in channel {channel.mention}"
        }]
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )
        await discord_responder.send_embed_list(embed_list, inter)

        return

    field_dict_list = [{
        "name": "message sent",
        "value": f"channel {channel.mention}"
    }]
    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        bot_user_name=inter.me.display_name,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )
    await discord_responder.send_embed_list(embed_list, inter)


@announce.sub_command(
    description=("announces message to specified channel, "
                 "pings all that can donate the requested unit")
)
async def donate(
    inter,
    channel: disnake.TextChannel,
    message: str,
    unit_name: str = commands.Param(
        autocomplete=discord_utils.autocomp_donation),
    clan_role: disnake.Role = None
):
    """
        announces message to specified channel,
        pings all that can donate the requested unit

        Parameters
        ----------
        unit_name: name of unit to search clan donations
        channel: channel to announce the message
        message: message to send the specified channel
        clan_role (optional): clan role to use linked clan
    """

    # role not mentioned
    if clan_role is None:
        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = (
            await discord_responder.clan_verification(
                db_player_obj, inter.author, coc_client)
        )
    # role has been mentioned
    else:
        verification_payload = (
            await discord_responder.clan_role_verification(
                clan_role, coc_client))

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    clan = verification_payload['clan_obj']

    donator_list = await clash_responder.donation(
        clan, unit_name, coc_client)

    # unit is either hero, pet or is an incorrect unit
    if donator_list is None:
        await inter.edit_original_message(
            content=f"{unit_name} is not a valid donatable unit")
        return

    formatted_unit_name = clash_responder.find_unit_name(unit_name)

    unit_emoji = discord_responder.get_emoji(
        formatted_unit_name, inter.client.emojis, client_data.emojis)

    message = f"{unit_emoji} **DONORS**\n\n" + message
    message += "\n\n"

    # nobody in the clan can donate the requested unit
    if len(donator_list) == 0:
        message += f"{clan.name} is unable to donate {unit_emoji}"

    else:

        for donor in donator_list:
            donor_ping = discord_responder.user_player_ping(
                donor.player_obj, inter.guild.members)
            message += (f"{donor_ping}, ")

        # cuts the last two characters from the string ', '
        message = message[:-2]

    try:
        await channel.send(content=(message))
    except:
        field_dict_list = [{
            "name": "message could not be sent",
            "value": f"please ensure bot is in channel {channel.mention}"
        }]
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )
        await discord_responder.send_embed_list(embed_list, inter)

        return

    field_dict_list = [{
        "name": "message sent",
        "value": f"channel {channel.mention}"
    }]
    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        bot_user_name=inter.me.display_name,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )
    await discord_responder.send_embed_list(embed_list, inter)


@announce.sub_command(
    description=("announces message to specified channel, "
                 "pings all that have the requested super troop active")
)
async def supertroop(
    inter,
    channel: disnake.TextChannel,
    message: str,
    unit_name: str = commands.Param(
        autocomplete=discord_utils.autocomp_supertroop),
    clan_role: disnake.Role = None
):
    """
        announces message to specified channel,
        pings all that have the requested super troop active

        Parameters
        ----------
        unit_name: name of unit to search clan donations
        channel: channel to announce the message
        message: message to send the specified channel
        clan_role (optional): clan role to use linked clan
    """

    # role not mentioned
    if clan_role is None:
        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = (
            await discord_responder.clan_verification(
                db_player_obj, inter.author, coc_client)
        )
    # role has been mentioned
    else:
        verification_payload = (
            await discord_responder.clan_role_verification(
                clan_role, coc_client))

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    clan = verification_payload['clan_obj']

    super_troop_name = clash_responder.find_super_troop_name(unit_name)

    if super_troop_name is None:
        await inter.edit_original_message(
            content=f"{unit_name} is not super troop")
        return

    donator_list = await clash_responder.active_super_troop_search(
        clan, super_troop_name, coc_client)

    # unit is either hero, pet or is an incorrect unit
    if donator_list is None:
        await inter.edit_original_message(
            content=f"{unit_name} is not a super troop")
        return

    unit_emoji = discord_responder.get_emoji(
        super_troop_name, inter.client.emojis, client_data.emojis)

    message = f"{unit_emoji} **DONORS**\n\n" + message
    message += "\n\n"

    # nobody in the clan can donate the requested unit
    if len(donator_list) == 0:
        message += f"{clan.name} is unable to donate {unit_emoji}"

    else:

        for donor in donator_list:
            donor_ping = discord_responder.user_player_ping(
                donor, inter.guild.members)
            message += (f"{donor_ping}, ")

        # cuts the last two characters from the string ', '
        message = message[:-2]

    try:
        await channel.send(content=message)
    except:
        field_dict_list = [{
            "name": "message could not be sent",
            "value": f"please ensure bot is in channel {channel.mention}"
        }]
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )
        await discord_responder.send_embed_list(embed_list, inter)

        return

    field_dict_list = [{
        "name": "message sent",
        "value": f"channel {channel.mention}"
    }]
    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        bot_user_name=inter.me.display_name,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )
    await discord_responder.send_embed_list(embed_list, inter)


@announce.sub_command(
    description=("*leadership* "
                 "announces message to specified channel, "
                 "pings all in current war")
)
async def war(
    inter, channel: disnake.TextChannel, message: str,
    clan_role: disnake.Role = None,
    war_selection: str = commands.Param(default=None, choices=[
        "previous", "current", "upcoming"])
):
    """
        *leadership*
        announces message to specified channel,
        pings all in current war

        Parameters
        ----------
        channel: channel to announce the message
        message: message to send the specified channel
        clan_role (optional): clan role to use linked clan
        war_selection (optional): cwl war selection
    """

    # role not mentioned
    if clan_role is None:
        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = (
            await discord_responder.war_leadership_verification(
                db_player_obj, war_selection,
                inter.author, inter.guild.id, coc_client))
    # role has been mentioned
    else:
        verification_payload = (
            await discord_responder.clan_role_war_leadership_verification(
                clan_role, war_selection,
                inter.author, inter.guild.id, coc_client))

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    war = verification_payload['war_obj']

    message = "**WAR ANNOUNCEMENT**\n\n" + message
    message += "\n\n"

    for war_member in war.clan.members:
        member_message = discord_responder.user_player_ping(
            war_member, inter.guild.members)
        message += (f"{member_message}, ")

    # cuts the last two characters from the string ', '
    message = message[:-2]

    try:
        await channel.send(content=message)
    except:
        field_dict_list = [{
            "name": "message could not be sent",
            "value": f"please ensure bot is in channel {channel.mention}"
        }]
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )
        await discord_responder.send_embed_list(embed_list, inter)

        return

    field_dict_list = [{
        "name": "message sent",
        "value": f"channel {channel.mention}"
    }]
    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        bot_user_name=inter.me.display_name,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )
    await discord_responder.send_embed_list(embed_list, inter)


@announce.sub_command(
    description=("*leadership* "
                 "announces message to channel, "
                 "pings all in war missing attacks")
)
async def warnoattack(
    inter, channel: disnake.TextChannel, message: str,
    missed_attacks: int = commands.Param(default=None, choices=[1, 2]),
    clan_role: disnake.Role = None,
    war_selection: str = commands.Param(default=None, choices=[
        "previous", "current", "upcoming"])
):
    """
        *leadership*
        announces message to channel,
        pings all in war missing attacks

        Parameters
        ----------
        channel: channel to announce the message
        message: message to send the specified channel
        missed_attacks (optional): specified missed attack count
        clan_role (optional): clan role to use linked clan
        war_selection (optional): cwl war selection
    """

    # role not mentioned
    if clan_role is None:
        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = (
            await discord_responder.war_leadership_verification(
                db_player_obj, war_selection,
                inter.author, inter.guild.id, coc_client))
    # role has been mentioned
    else:
        verification_payload = (
            await discord_responder.clan_role_war_leadership_verification(
                clan_role, war_selection,
                inter.author, inter.guild.id, coc_client))

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    war = verification_payload['war_obj']

    if missed_attacks is None:
        message = "**MISSING WAR ATTACKS**\n\n" + message
    else:
        if missed_attacks == 1:
            message = "**MISSING 1 ATTACK**\n\n" + message
        else:
            message = "**MISSING 2 ATTACKS**\n\n" + message

    message += "\n\n"

    war_member_no_attack_list = clash_responder.war_no_attack(
        war, missed_attacks)

    for war_member in war_member_no_attack_list:
        member_message = discord_responder.user_player_ping(
            war_member, inter.guild.members)
        message += (f"{member_message}, ")

    # cuts the last two characters from the string ', '
    message = message[:-2]

    try:
        await channel.send(content=message)
    except:
        field_dict_list = [{
            "name": "message could not be sent",
            "value": f"please ensure bot is in channel {channel.mention}"
        }]
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )
        await discord_responder.send_embed_list(embed_list, inter)

        return

    field_dict_list = [{
        "name": "message sent",
        "value": f"channel {channel.mention}"
    }]
    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        bot_user_name=inter.me.display_name,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )
    await discord_responder.send_embed_list(embed_list, inter)


# discord role
@discord.sub_command_group(
    brief='client',
    description="group for discord role commands"
)
async def role(inter):
    """
        group for discord role commands
    """

    await inter.response.defer()


@role.sub_command(
    brief='discord',
    description="update your roles"
)
async def self(inter):
    """
        update your roles
    """

    db_guild_obj = db_responder.read_guild(inter.guild.id)

    # if guild is not claimed
    if not db_guild_obj:
        await inter.edit_original_message(
            content=f"{inter.guild.name} has not been claimed")
        return

    embed_dict_list = await discord_responder.update_roles(
        inter.author, inter.guild, coc_client)

    for embed_dict in embed_dict_list:

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=embed_dict["title"],
            bot_user_name=inter.me.display_name,
            thumbnail=embed_dict["thumbnail"],
            field_list=embed_dict["field_dict_list"],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)


@role.sub_command(
    brief='discord',
    description="*leadership* update mentioned user's roles"
)
async def member(inter, user: disnake.User):
    """
        *leadership*
        update mentioned user's roles

        Parameters
        ----------
        user: user to update roles
    """

    db_guild_obj = db_responder.read_guild(inter.guild.id)

    # if guild is not claimed
    if not db_guild_obj:
        await inter.edit_original_message(
            content=f"{inter.guild.name} has not been claimed")
        return

    # getting author's db player obj for leadership verification
    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.player_leadership_verification(
        db_player_obj, inter.author, inter.guild.id, coc_client)

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    embed_dict_list = await discord_responder.update_roles(
        user, inter.guild, coc_client)

    for embed_dict in embed_dict_list:

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=embed_dict["title"],
            bot_user_name=inter.me.display_name,
            thumbnail=embed_dict["thumbnail"],
            field_list=embed_dict["field_dict_list"],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)


@role.sub_command(
    brief='discord',
    description="*admin* roles every member in the server"
)
async def all(inter):
    """
        *admin*
        update roles every member in the server
    """

    db_guild_obj = db_responder.read_guild(inter.guild.id)

    if not db_guild_obj:
        # if guild is not claimed
        await inter.edit_original_message(
            content=f"{inter.guild.name} has not been claimed")
        return

    db_user_obj = db_responder.read_user(inter.author.id)

    # if user is not claimed
    if not db_user_obj:
        await inter.edit_original_message(
            content=f"{inter.author.mention} has not been claimed")
        return

    # if author is not guild admin and is not super user
    if (not db_guild_obj.admin_user_id == inter.author.id
            and not db_user_obj.super_user):

        await inter.edit_original_message(
            content=f"{inter.author.mention} is not guild's admin")
        return

    # telling the user that the bot is updating roles
    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description="updating roles",
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)

    for user in inter.guild.members:
        if user.bot:
            continue

        embed_dict_list = await discord_responder.update_roles(
            user, inter.guild, coc_client)

        for embed_dict in embed_dict_list:

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                title=embed_dict["title"],
                bot_user_name=inter.me.display_name,
                thumbnail=embed_dict["thumbnail"],
                field_list=embed_dict["field_dict_list"],
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(embed_list, inter)

    # telling the user that the bot is done updating roles
    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description="update complete",
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# discord emoji
@discord.sub_command_group(
    brief='client',
    description="group for discord emoji commands"
)
async def emoji(inter):
    """
        group for discord emoji commands
    """

    await inter.response.defer(ephemeral=True)


@emoji.sub_command(
    brief='discord', description="sends specified emoji"
)
async def message(inter, coc_name: str):
    """
        sends specified emoji

        Parameters
        ----------
        coc_name: name of emoji to search for
    """

    await inter.edit_original_message(content="getting emoji")

    emoji = discord_responder.get_emoji(
        coc_name, inter.client.emojis, client_data.emojis)

    if emoji is None:
        await inter.edit_original_message(
            content=f"{coc_name} emoji not found")
        return

    await inter.send(content=emoji)

    await inter.edit_original_message(content=f"{emoji} emoji sent")


# discord user
@discord.sub_command_group(
    brief='discord',
    description="group for discord user commands"
)
async def user(inter):
    """
        group for discord user commands
    """

    await inter.response.defer()


@user.sub_command(
    brief='discord',
    description='returns the user linked to a requested player'
)
async def player(inter, player_tag: str):
    """
        returns the user linked to a requested player

        Parameters
        ----------
        player_tag: player tag to search
    """

    player_obj = await clash_responder.get_player(player_tag, coc_client)

    # player with given tag not found
    if player_obj is None:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=f"could not find player with tag {player_tag}",
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    field_dict_list = [discord_responder.find_user_from_tag(
        player_obj, inter.guild.members)]

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        bot_user_name=inter.me.display_name,
        thumbnail=player_obj.league.icon,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@user.sub_command(
    brief='discord',
    description="returns the users linked to the active player's clan"
)
async def clan(inter, clan_role: disnake.Role = None):
    """
        returns the users linked to the active player's clan

        Parameters
        ----------
        clan_role (optional): clan role to use linked clan
    """

    # role not mentioned
    if clan_role is None:
        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = (
            await discord_responder.clan_leadership_verification(
                db_player_obj, inter.author, inter.guild.id, coc_client))
    # role has been mentioned
    else:
        verification_payload = (
            await discord_responder.clan_role_player_leadership_verification(
                clan_role, inter.author, inter.guild.id, coc_client))

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=verification_payload['field_dict_list'],
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    clan_obj = verification_payload['clan_obj']

    field_dict_list = []
    # finding the user for each member in the clan
    for member_obj in clan_obj.members:
        field_dict_list.append(discord_responder.find_user_from_tag(
            member_obj, inter.guild.members))

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{clan_obj.name} linked users",
        bot_user_name=inter.me.display_name,
        thumbnail=clan_obj.badge,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# CLIENT

@bot.slash_command(
    brief='client',
    description="parent for client commands"
)
async def client(inter):
    """
        parent for client commands
    """

    # defer for every command
    await inter.response.defer()


# client info
@client.sub_command_group(
    brief='client',
    description="group for client info commands"
)
async def info(inter):
    """
        group for client info commands
    """

    pass


@info.sub_command(
    brief='client',
    description="relevant overview for the client"
)
async def overview(inter):
    """
        relevant overview for the client
    """

    field_dict_list = []

    field_dict_list.extend(discord_responder.client_info(
        inter.client, client_data))

    db_guild = db_responder.read_guild(inter.guild.id)

    field_dict_list.extend(discord_responder.client_guild_info(
        inter.guild, db_guild))

    db_players = db_responder.read_player_list(inter.author.id)

    field_dict_list.extend(await discord_responder.client_player_info(
        inter.author, db_players, coc_client))

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{inter.me.display_name} client overview",
        bot_user_name=inter.me.display_name,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# client user
@client.sub_command_group(
    brief='client',
    description="group for client user commands"
)
async def user(inter):
    """
        group for client user commands
    """

    pass


@user.sub_command(
    brief='client',
    description="claim your discord user"
)
async def claim(inter):
    """
        claim your discord user
    """

    user = db_responder.claim_user(inter.author.id)

    # user wasn't claimed and now is
    if user:
        embed_description = f"{inter.author.mention} is now claimed"

    # user was already claimed
    else:
        embed_description = f"{inter.author.mention} has already been claimed"

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# client player
@client.sub_command_group(
    brief='client',
    description="group for client player commands"
)
async def player(inter):
    """
        group for client player commands
    """

    pass


@player.sub_command(
    brief='client',
    description=(
        "verify and claim a player, "
        "a player must be claimed to view and run "
        "many of ClashDiscord commands"
    )
)
async def claim(inter, player_tag: str, api_key: str):
    """
        verify and claim a player,
        a player must be claimed to view and run
        many of ClashDiscord commands

        Parameters
        ----------
        player_tag: player tag to search
        api_key: api key provide from in game
    """

    # confirm valid player_tag
    player_obj = await clash_responder.get_player(
        player_tag, coc_client)

    # player tag was not valid
    if not player_obj:
        embed_description = f"player with tag {player_tag} was not found"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # confirm user has been claimed
    db_user_obj = db_responder.read_user(inter.author.id)
    if not db_user_obj:
        # user has not been claimed
        db_user_obj = db_responder.claim_user(inter.author.id)
        if not db_user_obj:
            # user could not be claimed
            embed_description = f"{inter.author.mention} user couldn't be claimed"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(embed_list, inter)
            return

    # confirm player has not been claimed
    db_player_obj = db_responder.read_player_from_tag(player_obj.tag)
    # player has already been claimed
    if db_player_obj:
        embed_description = (f"{player_obj.name} {player_obj.tag} "
                             f"has already been claimed")

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # authenticate player api key
    player_verified = await clash_responder.verify_token(
        api_key, player_obj.tag, coc_client)
    # api key could not be verified
    if not player_verified:
        embed_description = (f"verification for "
                             f"player tag {player_obj.tag} has failed")

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # user claimed
    # player is valid
    # player hasn't been claimed
    # player is authenticated
    db_player_obj = db_responder.claim_player(
        inter.author.id, player_obj.tag)

    # succesfully claimed
    if db_player_obj:
        embed_description = (f"{player_obj.name} {player_obj.tag} "
                             f"is now claimed by {inter.author.mention}")
    # failed to claim
    else:
        embed_description = (f"Could not claim {player_obj.name} "
                             f"{player_obj.tag} for {inter.author.mention}")

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@player.sub_command(
    brief='client',
    description="shows players claimed by your discord user"
)
async def show(inter):
    """
        shows players claimed by your discord user
    """

    db_player_obj_list = db_responder.read_player_list(inter.author.id)

    # user has no claimed players
    if len(db_player_obj_list) == 0:
        embed_description = (f"{inter.author.mention} does not have any "
                             f"claimed players")

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    message = f"{inter.author.mention} has claimed "
    for db_player_obj in db_player_obj_list:
        player_obj = await clash_responder.get_player(
            db_player_obj.player_tag, coc_client)
        if db_player_obj.active:
            message += f"{player_obj.name} {player_obj.tag} (active), "
        else:
            message += f"{player_obj.name} {player_obj.tag}, "
    # cuts the last two characters from the string ', '
    message = message[:-2]
    await inter.edit_original_message(content=message)


@player.sub_command(
    brief='client',
    description="updates your active player"
)
async def update(inter, player_tag: str):
    """
        updates author's active player

        Parameters
        ----------
        player_tag: player tag to set as active
    """

    player_obj = await clash_responder.get_player(player_tag, coc_client)

    # if player with tag not found
    if not player_obj:
        embed_description = f"player with tag {player_tag} not found"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_player_obj = db_responder.read_player(inter.author.id, player_obj.tag)

    # if requested player is not claimed
    if not db_player_obj:
        embed_description = (
            f"{inter.author.mention} "
            f"has not claimed "
            f"{player_obj.name} {player_obj.tag}"
        )

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # if requested player is the active player
    if db_player_obj.active:
        embed_description = (
            f"{player_obj.name} {player_obj.tag} "
            f"is already your active player "
            f"{inter.author.mention}"
        )

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    else:
        db_player_obj = db_responder.update_player_active(
            inter.author.id, player_obj.tag)

        embed_description = (
            f"{player_obj.name} {player_obj.tag} is now "
            f"your active player {inter.author.mention}"
        )

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return


@player.sub_command(
    brief='client',
    description="deletes the user's requested player claim"
)
async def remove(inter, player_tag: str):
    """
        updates author's active player

        Parameters
        ----------
        player_tag: player tag to remove
    """

    player_obj = await clash_responder.get_player(player_tag, coc_client)

    # player not found
    if not player_obj:
        embed_description = f"player with tag {player_tag} not found"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_player_obj = db_responder.read_player(inter.author.id, player_obj.tag)

    # db player not found
    if not db_player_obj:
        embed_description = (f"{player_obj.name} {player_obj.tag} "
                             f"is not claimed by {inter.author.mention}")

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_del_player_obj = db_responder.delete_player(
        inter.author.id, player_obj.tag)

    # player was not deleted
    if db_del_player_obj:
        embed_description = (
            f"{player_obj.name} {player_obj.tag} "
            f"could not be deleted "
            f"from {inter.author.mention} player list"
        )

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_active_player_obj = db_responder.read_player_active(inter.author.id)

    # active player found
    # no need to change the active player
    if db_active_player_obj:
        embed_description = (
            f"{player_obj.name} {player_obj.tag} "
            f"has been deleted "
            f"from {inter.author.mention} player list"
        )

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # no active player found
    # check if there are any other players
    db_player_obj_list = db_responder.read_player_list(
        inter.author.id)

    # no additional players claimed
    if len(db_player_obj_list) == 0:
        embed_description = (
            f"{player_obj.name} {player_obj.tag} "
            f"has been deleted, "
            f"{inter.author.mention} has no more claimed players"
        )

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # additional players claimed by user
    # update the first as the new active
    db_updated_player_obj = db_responder.update_player_active(
        inter.author.id, db_player_obj_list[0].player_tag)

    # update not successful
    if not db_updated_player_obj:
        embed_description = (
            f"{player_obj.name} {player_obj.tag} "
            f"has been deleted, could not update active player, "
            f"{inter.author.mention} has no active players"
        )

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # update was successful
    clash_updated_player_obj = await clash_responder.get_player(
        db_updated_player_obj.player_tag, coc_client)

    # clash player not found
    if not clash_updated_player_obj:
        embed_description = (
            f"{player_obj.name} {player_obj.tag} "
            f"has been deleted, "
            f"{inter.author.mention} active is now set to "
            f"{db_updated_player_obj.player_tag}, "
            f"could not find player in clash of clans"
        )

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # player deleted
    # active player updated
    # clash player found
    embed_description = (
        f"{player_obj.name} {player_obj.tag} "
        f"has been deleted, "
        f"{inter.author.mention} active is now set to "
        f"{clash_updated_player_obj.name} "
        f"{clash_updated_player_obj.tag}"
    )

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# client guild
@client.sub_command_group(
    brief='client',
    description="group for client guild commands"
)
async def guild(inter):
    """
        group for client guild commands
    """

    pass


@guild.sub_command(
    brief='client',
    description=("claim a discord guild and set yourself "
                 "as the guild admin for ClashDiscord")
)
async def claim(inter):
    """
        claim a discord guild and set yourself
        as the guild admin for ClashDiscord
    """

    # getting db user object
    db_user_obj = db_responder.read_user(inter.author.id)

    # user not found
    if not db_user_obj:
        embed_description = f"{inter.author.mention} has not been claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_guild_obj = db_responder.read_guild(inter.guild.id)

    # guild already claimed
    if db_guild_obj:
        embed_description = f"{inter.guild.name} has already been claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_claimed_guild = db_responder.claim_guild(
        inter.author.id, inter.guild.id)

    # guild already claimed or could not be claimed
    if not db_claimed_guild:
        embed_description = f"{inter.guild.name} could not be claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    field_dict_list = [{
        "name": f"{inter.guild.name} is now claimed",
        "value": f"admin user {inter.author.mention}"
    }]

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        bot_user_name=inter.me.display_name,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# client clan
@client.sub_command_group(
    brief='client',
    description="group for client clan commands"
)
async def clan(inter):
    """
        group for client clan commands
    """

    pass


@clan.sub_command(
    brief='client',
    description="*admin* claim the requested clan"
)
async def claim(inter, clan_tag: str):
    """
        *admin*
        claim the requested clan

        Parameters
        ----------
        clan_tag: clan tag to claim
    """

    db_guild_obj = db_responder.read_guild(inter.guild.id)

    # guild not claimed
    if not db_guild_obj:
        embed_description = f"{inter.guild.name} has not been claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_user_obj = db_responder.read_user(inter.author.id)

    # user not claimed
    if not db_user_obj:
        embed_description = f"{inter.author.mention} has not been claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # user is not guild admin and is not super user
    if (not db_guild_obj.admin_user_id == inter.author.id
            and not db_user_obj.super_user):
        embed_description = f"{inter.author.mention} is not guild's admin"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    clan_obj = await clash_responder.get_clan(clan_tag, coc_client)

    # clan not found
    if not clan_obj:
        embed_description = f"couldn't find clan {clan_tag}"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    claimed_clan_obj = db_responder.read_clan(inter.guild.id, clan_obj.tag)

    # already claimed
    if claimed_clan_obj:
        embed_description = (
            f"{clan_obj.name} has already been claimed for "
            f"{inter.guild.name}"
        )

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_clan_obj = db_responder.claim_clan(inter.guild.id, clan_obj.tag)

    # clan not claimed
    if not db_clan_obj:
        embed_description = f"couldn't claim {clan_obj.name}"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    embed_description = f"{clan_obj.name} has been claimed"

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@clan.sub_command(
    brief='client',
    description="*admin* clans claimed by a discord guild",
    hidden=True
)
async def show(inter):
    """
        *admin*
        clans claimed by a discord guild

        Parameters
        ----------
        clan_tag: clan tag to claim
    """

    db_guild_obj = db_responder.read_guild(inter.guild.id)

    # guild not claimed
    if not db_guild_obj:
        embed_description = f"{inter.guild.name} has not been claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_user_obj = db_responder.read_user(inter.author.id)

    # user not claimed
    if not db_user_obj:
        embed_description = f"{inter.author.mention} has not been claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # user is not guild admin and is not super user
    if (not db_guild_obj.admin_user_id == inter.author.id
            and not db_user_obj.super_user):
        embed_description = f"{inter.author.mention} is not guild's admin"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_clan_obj_list = db_responder.read_clan_list_from_guild(inter.guild.id)

    # guild has no claimed clans
    if len(db_clan_obj_list) == 0:
        embed_description = f"{inter.guild.name} does not have any claimed clans"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    embed_title = f"{inter.guild.name} claimed clans"

    field_dict_list = []
    for db_clan in db_clan_obj_list:
        clan = await clash_responder.get_clan(
            db_clan.clan_tag, coc_client)

        field_dict_list.append({
            "name": clan.name,
            "value": clan.tag
        })

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=embed_title,
        bot_user_name=inter.me.display_name,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@clan.sub_command(
    brief='client',
    description="*admin* deletes the requested clan claim"
)
async def remove(inter, clan_tag: str):
    """
        *admin*
        deletes the requested clan claim

        Parameters
        ----------
        clan_tag: clan tag to delete from client
    """

    db_guild_obj = db_responder.read_guild(inter.guild.id)

    # guild not claimed
    if not db_guild_obj:
        embed_description = f"{inter.guild.name} has not been claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_user_obj = db_responder.read_user(inter.author.id)

    # user not claimed
    if not db_user_obj:
        embed_description = f"{inter.author.mention} has not been claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # user is not guild admin and is not super user
    if (not db_guild_obj.admin_user_id == inter.author.id
            and not db_user_obj.super_user):
        embed_description = f"{inter.author.mention} is not guild's admin"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    clan_obj = await clash_responder.get_clan(clan_tag, coc_client)

    # clan not found
    if not clan_obj:
        embed_description = f"couldn't find clan {clan_tag}"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_clan_obj = db_responder.read_clan(inter.guild.id, clan_obj.tag)
    # clan not claimed by guild
    if not db_clan_obj:
        embed_description = (f"{clan_obj.name} has not been claimed by "
                             f"{inter.guild.name}")

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_clan_deletion = db_responder.delete_clan(inter.guild.id, clan_obj.tag)
    # clan was found after deletion
    if db_clan_deletion:
        embed_description = f"{clan_obj.name} could not be deleted"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    embed_description = (f"{clan_obj.name} has been deleted "
                         f"from {inter.guild.name}")

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# client roles
@client.sub_command_group(
    brief='client',
    description="group for client role commands"
)
async def role(inter):
    """
        group for client role commands
    """

    pass


@role.sub_command(
    brief='client',
    description="*admin* shows all roles claimed by a discord guild"
)
async def show(inter):
    """
        *admin*
        shows all roles claimed by a discord guild
    """

    db_user_obj = db_responder.read_user(inter.author.id)

    db_guild_obj = db_responder.read_guild(inter.guild.id)
    # guild not claimed
    if not db_guild_obj:
        embed_description = f"{inter.guild.name} has not been claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # user not claimed
    if not db_user_obj:
        embed_description = f"{inter.author.mention} has not been claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # user is not guild admin and is not super user
    if (not db_guild_obj.admin_user_id == inter.author.id
            and not db_user_obj.super_user):
        embed_description = f"{inter.author.mention} is not guild's admin"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    field_dict_list = []

    db_clan_role_list = db_responder.read_guild_clan_role(inter.guild.id)

    db_rank_role_list = db_responder.read_guild_rank_role(inter.guild.id)

    if len(db_clan_role_list) != 0:
        for db_role in db_clan_role_list:
            discord_role = disnake.utils.get(
                inter.guild.roles, id=db_role.discord_role_id)

            # discord role is claimed, but not found in server
            if not discord_role:
                deleted_db_role = db_responder.delete_clan_role(
                    db_role.discord_role_id)

                field_dict_list.append({
                    'name': f"clan tag {db_role.clan_tag}",
                    'value': f"role {db_role.discord_role_id} *deleted*"
                })
                continue

            clan = await clash_responder.get_clan(
                db_role.clan_tag, coc_client)

            if not clan:
                field_dict_list.append({
                    'name': f"clan tag {db_role.clan_tag}",
                    'value': f"role {discord_role.mention}"
                })
                continue

            field_dict_list.append({
                'name': f"clan {clan.name} tag {db_role.clan_tag}",
                'value': f"role {discord_role.mention}"
            })

    if len(db_rank_role_list) != 0:
        for db_role in db_rank_role_list:
            discord_role = disnake.utils.get(
                inter.guild.roles, id=db_role.discord_role_id)

            # discord role is claimed, but not found in server
            if not discord_role:
                deleted_db_role = db_responder.delete_rank_role(
                    db_role.discord_role_id)

                field_dict_list.append({
                    'name': f"rank {db_role.model_name}",
                    'value': f"role {db_role.discord_role_id} *deleted*"
                })
                continue

            field_dict_list.append({
                'name': f"rank {db_role.model_name}",
                'value': f"role {discord_role.mention}"
            })

    # guild has no claimed rank roles
    if (len(db_clan_role_list) == 0 and
            len(db_rank_role_list) == 0):
        field_dict_list.append({
            'name': f"server has no claimed roles",
            'value': f"please claim a clan or rank role"
        })

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{inter.guild.name} claimed roles",
        bot_user_name=inter.me.display_name,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@role.sub_command(
    brief='client',
    description=("*admin* remove the claimed discord role, "
                 "the role will not be deleted from discord")
)
async def remove(inter, role: disnake.Role):
    """
        *admin*
        remove the claimed discord role,
        the role will not be deleted from discord

        Parameters
        ----------
        role: role object to remove claim
    """

    db_user_obj = db_responder.read_user(inter.author.id)

    db_guild_obj = db_responder.read_guild(inter.guild.id)
    # guild not claimed
    if not db_guild_obj:
        embed_description = f"{inter.guild.name} has not been claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # user not claimed
    if not db_user_obj:
        embed_description = f"{inter.author.mention} has not been claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # user is not guild admin and is not super user
    if (not db_guild_obj.admin_user_id == inter.author.id
            and not db_user_obj.super_user):
        embed_description = f"{inter.author.mention} is not guild's admin"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_clan_role_obj = db_responder.read_clan_role(role.id)

    # claimed role is clan role
    if db_clan_role_obj:
        # delete clan role
        db_clan_role_deletion = db_responder.delete_clan_role(role.id)
        # clan role found after deletion
        if db_clan_role_deletion:
            embed_description = f"{role.mention} claim could not be removed"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(embed_list, inter)
            return

        # clan role deleted
        embed_description = f"{role.mention} claim was removed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_rank_role_obj = db_responder.read_rank_role(role.id)

    # claimed role is rank role
    if db_rank_role_obj:
        # delete rank role
        db_rank_role_deletion = db_responder.delete_rank_role(role.id)
        # rank role found after deletion
        if db_rank_role_deletion:
            embed_description = f"{role.mention} claim could not be removed"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(embed_list, inter)
            return

        # rank role deleted
        embed_description = f"{role.mention} claim was removed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    embed_description = f"{role.mention} is not claimed"

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# client clan role
@client.sub_command_group(
    brief='client',
    description="group for client clan role commands"
)
async def clanrole(inter):
    """
        group for client clan role commands
    """

    pass


@clanrole.sub_command(
    brief='client',
    description="*admin* claim a clan's discord role"
)
async def claim(inter, role: disnake.Role, clan_tag: str):
    """
        *admin*
        claim a clan's discord role

        Parameters
        ----------
        role: role object to claim and link to claimed clan
        clan_tag: clan tag to link to role
    """

    clan_obj = await clash_responder.get_clan(clan_tag, coc_client)

    # clan not found
    if not clan_obj:
        embed_description = f"couldn't find clan {clan_tag}"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_guild_obj = db_responder.read_guild(inter.guild.id)

    # guild not claimed
    if not db_guild_obj:
        embed_description = f"{inter.guild.name} has not been claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_user_obj = db_responder.read_user(inter.author.id)

    # user not claimed
    if not db_user_obj:
        embed_description = f"{inter.author.mention} has not been claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # user is not guild admin and is not super user
    if (not db_guild_obj.admin_user_id == inter.author.id
            and not db_user_obj.super_user):
        embed_description = f"{inter.author.mention} is not guild's admin"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_clan_obj = db_responder.read_clan(inter.guild.id, clan_obj.tag)

    # clan not claimed by guild
    if not db_clan_obj:
        embed_description = (f"{clan_obj.name} has not been claimed by "
                             f"{inter.guild.name}")

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # confirm clan role has not been claimed
    db_clan_role_obj = db_responder.read_clan_role(role.id)

    # clan role has been claimed
    if db_clan_role_obj:
        embed_description = (f"{role.mention} has already been claimed "
                             f"for clan {db_clan_role_obj.clan_tag}")

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # confirm rank role has not been claimed
    db_rank_role_obj = db_responder.read_rank_role(role.id)

    # rank role has been claimed
    if db_rank_role_obj:
        embed_description = (f"{role.mention} has already been claimed "
                             f"for rank {db_rank_role_obj.model_name}")

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # claim clan role
    claimed_clan_role_obj = db_responder.claim_clan_role(
        role.id, inter.guild.id, clan_obj.tag)

    # clan role could not be claimed
    if not claimed_clan_role_obj:
        embed_description = (f"could not claim {role.mention} "
                             f"for clan {clan_obj.tag}")

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    embed_description = f"{role.mention} has been claimed for clan {clan_obj.tag}"

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# client rank role
@client.sub_command_group(
    brief='client',
    description="group for client rank role commands"
)
async def rankrole(inter):
    """
        group for client rank role commands
    """

    pass


@rankrole.sub_command(
    brief='client',
    description="*admin* claim a rank's discord role"
)
async def claim(inter, role: disnake.Role,
                rank_name: str = commands.Param(choices=[
        "leader", "co-leader", "elder", "member", "uninitiated"])
):
    """
        *admin*
        claim a rank's discord role

        Parameters
        ----------
        role: role object to claim and link to client rank
        rank_name: requested rank to link to role
    """

    # validate given role name with model
    rank_role_model_obj = db_responder.read_rank_role_model(rank_name)

    # rank role name invalid
    if not rank_role_model_obj:
        embed_description = f"{rank_name} is not a valid rank"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_guild_obj = db_responder.read_guild(inter.guild.id)
    # guild not claimed
    if not db_guild_obj:
        embed_description = f"{inter.guild.name} has not been claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_user_obj = db_responder.read_user(inter.author.id)
    # user not claimed
    if not db_user_obj:
        embed_description = f"{inter.author.mention} has not been claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # user is not guild admin and is not super user
    if (not db_guild_obj.admin_user_id == inter.author.id
            and not db_user_obj.super_user):
        embed_description = f"{inter.author.mention} is not guild's admin"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # confirm clan role has not been claimed
    db_clan_role_obj = db_responder.read_clan_role(role.id)
    # clan role has been claimed
    if db_clan_role_obj:
        embed_description = (f"{role.mention} has already been claimed for clan "
                             f"{db_clan_role_obj.clan_tag}")

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # confirm rank role has not been claimed
    db_rank_role_obj = db_responder.read_rank_role(role.id)
    # rank role has been claimed
    if db_rank_role_obj:
        embed_description = (f"{role.mention} has already been claimed for rank "
                             f"{db_rank_role_obj.model_name}")

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # claim rank role
    claimed_rank_role_obj = db_responder.claim_rank_role(
        role.id, inter.guild.id, rank_name)
    # rank role could not be claimed
    if claimed_rank_role_obj is None:
        embed_description = (f"could not claim {role.mention} for rank "
                             f"{db_rank_role_obj.model_name}")

    # rank role was claimed and found
    else:
        embed_description = (f"{role.mention} has been claimed for rank "
                             f"{claimed_rank_role_obj.model_name}")

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# admin
@bot.slash_command(
    brief='admin',
    description="parent for client admin commands"
)
async def admin(inter):
    """
        parent for client admin commands
    """

    # defer for every command
    await inter.response.defer()


# admin player
@admin.sub_command_group(
    brief='admin',
    description="group for admin player commands"
)
async def player(inter):
    """
        group for player commands
    """

    pass


@player.sub_command(
    brief='admin',
    description=(
        "*admin* claim a player for the mentioned user"
    )
)
async def claim(inter, player_tag: str, user: disnake.User):
    """
        *admin*
        claim a player for the mentioned user

        Parameters
        ----------
        player_tag: player tag link user to
        user: user to link player to
    """

    db_author_obj = db_responder.read_user(inter.author.id)
    # author is not claimed
    if not db_author_obj:
        embed_description = f"{inter.author.mention} is not claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # author is not admin
    if not db_author_obj.admin:
        embed_description = f"{inter.author.mention} is not admin"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # confirm user has been claimed
    db_user_obj = db_responder.read_user(user.id)
    if not db_user_obj:
        # user has not been claimed
        db_user_obj = db_responder.claim_user(user.id)
        if not db_user_obj:
            # user could not be claimed
            embed_description = f"{user.mention} user couldn't be claimed"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(embed_list, inter)
            return

    # admin is not a super user and author is not the user
    if (not db_author_obj.super_user
            and db_author_obj.discord_id != db_user_obj.discord_id):
        # admin users are not allowed to update admins or super users
        if db_user_obj.admin or db_user_obj.super_user:
            embed_description = (f"admins are not allowed to update "
                                 f"admins or super users")

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(embed_list, inter)
            return

    # confirm valid player_tag
    player_obj = await clash_responder.get_player(
        player_tag, coc_client)

    # player tag was not valid
    if not player_obj:
        embed_description = f"player with tag {player_tag} was not found"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # confirm player has not been claimed
    db_player_obj = db_responder.read_player_from_tag(player_obj.tag)
    # player has already been claimed
    if db_player_obj:
        embed_description = (f"{player_obj.name} {player_obj.tag} "
                             f"has already been claimed")

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # user claimed
    # player is valid
    # player hasn't been claimed
    db_player_obj = db_responder.claim_player(
        user.id, player_obj.tag)

    # succesfully claimed
    if db_player_obj:
        embed_description = (f"{player_obj.name} {player_obj.tag} "
                             f"is now claimed by {user.mention}")
    # failed to claim
    else:
        embed_description = (f"Could not claim {player_obj.name} "
                             f"{player_obj.tag} for {user.mention}")

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@player.sub_command(
    brief='admin',
    description="*admin* shows players claimed by the mentioned user"
)
async def show(inter, user: disnake.User):
    """
        *admin*
        shows players claimed by the mentioned user

        Parameters
        ----------
        user: user to show player tags
    """

    db_author_obj = db_responder.read_user(inter.author.id)
    # author is not claimed
    if not db_author_obj:
        embed_description = f"{inter.author.mention} is not claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # author is not admin
    if not db_author_obj.admin:
        embed_description = f"{inter.author.mention} is not admin"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # confirm db user exists
    db_user_obj = db_responder.read_user(user.id)
    if db_user_obj is None:
        embed_description = f"{user.mention} has not been claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # admin is not a super user and author is not the user
    if (not db_author_obj.super_user
            and db_author_obj.discord_id != db_user_obj.discord_id):
        # admin users are not allowed to update admins or super users
        if db_user_obj.admin or db_user_obj.super_user:
            embed_description = (f"admins are not allowed to update "
                                 f"admins or super users")

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(embed_list, inter)
            return

    db_player_obj_list = db_responder.read_player_list(user.id)

    # user has no claimed players
    if len(db_player_obj_list) == 0:
        embed_description = (f"{user.mention} does not have any "
                             f"claimed players")

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    message = f"{user.mention} has claimed "
    for db_player_obj in db_player_obj_list:
        player_obj = await clash_responder.get_player(
            db_player_obj.player_tag, coc_client)
        if db_player_obj.active:
            message += f"{player_obj.name} {player_obj.tag} (active), "
        else:
            message += f"{player_obj.name} {player_obj.tag}, "
    # cuts the last two characters from the string ', '
    message = message[:-2]
    await inter.edit_original_message(content=message)


@player.sub_command(
    brief='admin',
    description="*admin* remove a player for the mentioned user"
)
async def remove(inter, player_tag: str, user: disnake.User):
    """
        *admin*
        remove a player for the mentioned user

        Parameters
        ----------
        player_tag: player tag to remove
        user: user to remove player from
    """

    db_author_obj = db_responder.read_user(inter.author.id)
    # author is not claimed
    if not db_author_obj:
        embed_description = f"{inter.author.mention} is not claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # author is not admin
    if not db_author_obj.admin:
        embed_description = f"{inter.author.mention} is not admin"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # confirm db user exists
    db_user_obj = db_responder.read_user(user.id)
    if db_user_obj is None:
        embed_description = f"{user.mention} has not been claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # admin is not a super user and author is not the user
    if (not db_author_obj.super_user
            and db_author_obj.discord_id != db_user_obj.discord_id):
        # admin users are not allowed to update admins or super users
        if db_user_obj.admin or db_user_obj.super_user:
            embed_description = (f"admins are not allowed to update "
                                 f"admins or super users")

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(embed_list, inter)
            return

    # confirm valid player_tag
    player_obj = await clash_responder.get_player(
        player_tag, coc_client)

    # player tag was not valid
    if not player_obj:
        embed_description = f"player with tag {player_tag} was not found"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_player_obj = db_responder.read_player(user.id, player_obj.tag)

    # db player not found
    if not db_player_obj:
        embed_description = (f"{player_obj.name} {player_obj.tag} "
                             f"is not claimed by {user.mention}")

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_del_player_obj = db_responder.delete_player(
        user.id, player_obj.tag)

    # player was not deleted
    if db_del_player_obj:
        embed_description = (
            f"{player_obj.name} {player_obj.tag} "
            f"could not be deleted "
            f"from {user.mention} player list"
        )

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_active_player_obj = db_responder.read_player_active(user.id)

    # active player found
    # no need to change the active player
    if db_active_player_obj:
        embed_description = (
            f"{player_obj.name} {player_obj.tag} "
            f"has been deleted "
            f"from {user.mention} player list"
        )

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # no active player found
    # check if there are any other players
    db_player_obj_list = db_responder.read_player_list(
        user.id)

    # no additional players claimed
    if len(db_player_obj_list) == 0:
        embed_description = (
            f"{player_obj.name} {player_obj.tag} "
            f"has been deleted, "
            f"{user.mention} has no more claimed players"
        )

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # additional players claimed by user
    # update the first as the new active
    db_updated_player_obj = db_responder.update_player_active(
        user.id, db_player_obj_list[0].player_tag)

    # update not successful
    if not db_updated_player_obj:
        embed_description = (
            f"{player_obj.name} {player_obj.tag} "
            f"has been deleted, could not update active player, "
            f"{user.mention} has no active players"
        )

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # update was successful
    clash_updated_player_obj = await clash_responder.get_player(
        db_updated_player_obj.player_tag, coc_client)

    # clash player not found
    if clash_updated_player_obj is None:
        embed_description = (
            f"{player_obj.name} {player_obj.tag} "
            f"has been deleted, "
            f"{user.mention} active is now set to "
            f"{db_updated_player_obj.player_tag}, "
            f"could not find player in clash of clans"
        )

    # player deleted
    # active player updated
    # clash player found
    else:
        embed_description = (
            f"{player_obj.name} {player_obj.tag} "
            f"has been deleted, "
            f"{user.mention} active is now set to "
            f"{clash_updated_player_obj.name} "
            f"{clash_updated_player_obj.tag}"
        )

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# super user administration
@bot.slash_command(
    brief='superuser',
    description="parent for client super user commands"
)
async def superuser(inter):
    """
        parent for client super user commands
    """

    pass


# superuser guild
@superuser.sub_command_group(
    brief='superuser',
    description="group for superuser guild commands"
)
async def guild(inter):
    """
        group for guild commands
    """

    pass


@guild.sub_command(
    brief='superuser',
    description="*super user* shows all guilds ClashDiscord is in"
)
async def show(inter):
    """
        *super user*
        "*super user* shows all guilds ClashDiscord is in
    """

    await inter.response.defer()

    db_author_obj = db_responder.read_user(inter.author.id)
    # author is not claimed
    if not db_author_obj:
        embed_description = f"{inter.author.mention} is not claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # author is not super user
    if not db_author_obj.super_user:
        embed_description = f"{inter.author.mention} is not super user"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    field_dict_list = []

    for guild in inter.client.guilds:
        field_dict_list.append({
            'name': f"{guild.name}",
            'value': f"{guild.id}"
        })

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"**ClashDiscord Guilds**",
        description=f"Guild Count: {len(inter.client.guilds)}",
        bot_user_name=inter.me.display_name,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )
    await discord_responder.send_embed_list(embed_list, inter)


@guild.sub_command(
    brief='superuser',
    description="*super user* delete a claimed guild from id"
)
async def remove(inter, guild_id: str):
    """
        *super user*
        delete a claimed guild from id

        Parameters
        ----------
        guild_id: id for guild to remove claim
    """

    await inter.response.defer(ephemeral=True)

    db_author_obj = db_responder.read_user(inter.author.id)
    # author is not claimed
    if not db_author_obj:
        embed_description = f"{inter.author.mention} is not claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # author is not super user
    if not db_author_obj.super_user:
        embed_description = f"{inter.author.mention} is not super user"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # confirm guild is claimed
    db_guild_obj = db_responder.read_guild(guild_id)
    # guild isn't claimed
    if not db_guild_obj:
        embed_description = f"guild with id {guild_id} is not claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    deleted_guild_obj = db_responder.delete_guild(guild_id)

    # guild was deleted properly
    if deleted_guild_obj is None:
        embed_description = f"guild with id {guild_id} was deleted"

    # guild could not be deleted
    else:
        embed_description = f"guild with id {guild_id} could not be deleted"

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@guild.sub_command(
    brief='superuser',
    description="*super user* force ClashDiscord to leave a guild from id"
)
async def leave(inter, guild_id: str):
    """
        *super user*
        force ClashDiscord to leave a claimed guild from id

        Parameters
        ----------
        guild_id: id for guild for ClashDiscord to leave
    """

    await inter.response.defer(ephemeral=True)

    db_author_obj = db_responder.read_user(inter.author.id)
    # author is not claimed
    if not db_author_obj:
        embed_description = f"{inter.author.mention} is not claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # author is not super user
    if not db_author_obj.super_user:
        embed_description = f"{inter.author.mention} is not super user"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    guild_id = int(guild_id)

    # confirm bot is in guild
    guild = disnake.utils.get(inter.bot.guilds, id=guild_id)
    # bot isn't in guild
    if guild is None:
        embed_description = (f"{inter.me.display_name} "
                             f"is not in guild {guild_id}")

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    await guild.leave()
    deleted_guild = disnake.utils.get(inter.bot.guilds, id=guild.id)

    # guild was deleted properly
    if deleted_guild is None:
        embed_description = (f"{inter.me.display_name} left "
                             f"guild {guild.name} id {guild.id}")

    # guild could not be deleted
    else:
        embed_description = (f"{inter.me.display_name} could not leave "
                             f"guild {guild.name} id {guild.id}")

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# superuser user
@superuser.sub_command_group(
    brief='superuser',
    description="group for superuser user commands"
)
async def user(inter):
    """
        group for user commands
    """

    # defer for every superuser user command
    await inter.response.defer(ephemeral=True)


@user.sub_command(
    brief='superuser',
    description="*super user* return a list of all admin users"
)
async def adminshow(inter):
    """
        *super user*
        return a list of all admin users
    """

    db_author_obj = db_responder.read_user(inter.author.id)
    # author is not claimed
    if not db_author_obj:
        embed_description = f"{inter.author.mention} is not claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # author is not super user
    if not db_author_obj.super_user:
        embed_description = f"{inter.author.mention} is not super user"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_admin_users = db_responder.read_user_admin_all()

    if len(db_admin_users) == 0:
        embed_description = f"{inter.me.display_name} has no admin users"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # initialize admin user field dict list
    field_dict_list = []
    for admin_user in db_admin_users:
        # get the discord member in the server of the admin user
        member = disnake.utils.get(
            inter.guild.members, id=admin_user.discord_id)

        # member not found in server
        if member is None:
            field_dict_list.append({
                "name": "admin user id",
                "value": f"{admin_user.discord_id}",
                "inline": False
            })

        # member found in server
        else:
            field_dict_list.append({
                "name": "admin user",
                "value": f"{member.mention}",
                "inline": False
            })

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{inter.me.display_name} admin users",
        bot_user_name=inter.me.display_name,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@user.sub_command(
    brief='superuser',
    description="*super user* toggle a user's admin bool"
)
async def admintoggle(inter, user: disnake.User):
    """
        *super user*
        toggle a user's admin bool

        Parameters
        ----------
        user: user toggle admin
    """

    db_author_obj = db_responder.read_user(inter.author.id)
    # author is not claimed
    if not db_author_obj:
        embed_description = f"{inter.author.mention} is not claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # author is not super user
    if not db_author_obj.super_user:
        embed_description = f"{inter.author.mention} is not super user"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # confirm user is claimed
    db_user_obj = db_responder.read_user(user.id)
    # user isn't claimed
    if not db_user_obj:
        embed_description = f"{user.mention} is not claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    updated_user_obj = db_responder.update_toggle_user_admin(user.id)
    # upated user not found
    if updated_user_obj is None:
        embed_description = f"{user.mention} could not be updated"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # user was updated and is now an admin
    if updated_user_obj.admin:
        embed_description = f"{user.mention} is now an admin"

    # user was updated and is now not an admin
    else:
        embed_description = f"{user.mention} is no longer an admin"

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@user.sub_command(
    brief='superuser',
    description="*super user* delete a claimed user from id"
)
async def remove(inter, user: disnake.User):
    """
        *super user*
        claim a clan's discord role

        Parameters
        ----------
        user: user to remove claim
    """

    db_author_obj = db_responder.read_user(inter.author.id)
    # author is not claimed
    if not db_author_obj:
        embed_description = f"{inter.author.mention} is not claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # author is not super user
    if not db_author_obj.super_user:
        embed_description = f"{inter.author.mention} is not super user"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # confirm user is claimed
    db_user_obj = db_responder.read_user(user.id)
    # user isn't claimed
    if not db_user_obj:
        embed_description = f"{user.mention} is not claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    deleted_user_obj = db_responder.delete_user(user.id)

    # user was deleted properly
    if deleted_user_obj is None:
        embed_description = f"{user.mention} was deleted"

    # user could not be deleted
    else:
        embed_description = f"{user.mention} could not be deleted"

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# superuser player
@superuser.sub_command_group(
    brief='superuser',
    description="group for superuser player commands"
)
async def player(inter):
    """
        group for player commands
    """

    # defer for every superuser player command
    await inter.response.defer(ephemeral=True)


@player.sub_command(
    brief='superuser',
    description=(
        "*super user* claim a player for the mentioned user"
    )
)
async def claim(inter, player_tag: str, user: disnake.User):
    """
        *super user*
        claim a player for the mentioned user

        Parameters
        ----------
        player_tag: player tag link user to
        user: user to link player to
    """

    db_author_obj = db_responder.read_user(inter.author.id)
    # author is not claimed
    if not db_author_obj:
        embed_description = f"{inter.author.mention} is not claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # author is not super user
    if not db_author_obj.super_user:
        embed_description = f"{inter.author.mention} is not super user"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # confirm valid player_tag
    player_obj = await clash_responder.get_player(
        player_tag, coc_client)

    # player tag was not valid
    if not player_obj:
        embed_description = f"player with tag {player_tag} was not found"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # confirm user has been claimed
    db_user_obj = db_responder.read_user(user.id)
    if not db_user_obj:
        # user has not been claimed
        db_user_obj = db_responder.claim_user(user.id)
        if not db_user_obj:
            # user could not be claimed
            await inter.edit_original_message(
                content=f"{user.mention} user couldn't be claimed")
            return

    # confirm player has not been claimed
    db_player_obj = db_responder.read_player_from_tag(player_obj.tag)
    # player has already been claimed
    if db_player_obj:
        embed_description = (f"{player_obj.name} {player_obj.tag} "
                             f"has already been claimed")

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # user claimed
    # player is valid
    # player hasn't been claimed
    db_player_obj = db_responder.claim_player(
        user.id, player_obj.tag)

    # failed to claim
    if db_player_obj is None:
        embed_description = (f"Could not claim {player_obj.name} "
                             f"{player_obj.tag} for {user.mention}")

    # succesfully claimed
    else:
        embed_description = (f"{player_obj.name} {player_obj.tag} "
                             f"is now claimed by {user.mention}")

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@player.sub_command(
    brief='superuser',
    description="*super user* remove a player for the mentioned user"
)
async def remove(inter, player_tag: str, user: disnake.User):
    """
        *super user*
        remove a player for the mentioned user

        Parameters
        ----------
        player_tag: player tag to remove
        user: user to remove player from
    """

    db_author_obj = db_responder.read_user(inter.author.id)
    # author is not claimed
    if not db_author_obj:
        embed_description = f"{inter.author.mention} is not claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # author is not super user
    if not db_author_obj.super_user:
        embed_description = f"{inter.author.mention} is not super user"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # confirm valid player_tag
    player_obj = await clash_responder.get_player(
        player_tag, coc_client)

    # player tag was not valid
    if not player_obj:
        embed_description = f"player with tag {player_tag} was not found"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_player_obj = db_responder.read_player(user.id, player_obj.tag)

    # db player not found
    if not db_player_obj:
        embed_description = (f"{player_obj.name} {player_obj.tag} "
                             f"is not claimed by {user.mention}")

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_del_player_obj = db_responder.delete_player(
        user.id, player_obj.tag)

    # player was not deleted
    if db_del_player_obj:
        embed_description = (
            f"{player_obj.name} {player_obj.tag} "
            f"could not be deleted "
            f"from {user.mention} player list"
        )

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_active_player_obj = db_responder.read_player_active(user.id)

    # active player found
    # no need to change the active player
    if db_active_player_obj:
        embed_description = (
            f"{player_obj.name} {player_obj.tag} "
            f"has been deleted "
            f"from {user.mention} player list"
        )

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # no active player found
    # check if there are any other players
    db_player_obj_list = db_responder.read_player_list(
        user.id)

    # no additional players claimed
    if len(db_player_obj_list) == 0:
        embed_description = (
            f"{player_obj.name} {player_obj.tag} "
            f"has been deleted, "
            f"{user.mention} has no more claimed players"
        )

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # additional players claimed by user
    # update the first as the new active
    db_updated_player_obj = db_responder.update_player_active(
        user.id, db_player_obj_list[0].player_tag)

    # update not successful
    if not db_updated_player_obj:
        embed_description = (
            f"{player_obj.name} {player_obj.tag} "
            f"has been deleted, could not update active player, "
            f"{user.mention} has no active players"
        )

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # update was successful
    clash_updated_player_obj = await clash_responder.get_player(
        db_updated_player_obj.player_tag, coc_client)

    # clash player not found
    if clash_updated_player_obj is None:
        embed_description = (
            f"{player_obj.name} {player_obj.tag} "
            f"has been deleted, "
            f"{user.mention} active is now set to "
            f"{db_updated_player_obj.player_tag}, "
            f"could not find player in clash of clans"
        )

    # player deleted
    # active player updated
    # clash player found
    else:
        embed_description = (
            f"{player_obj.name} {player_obj.tag} "
            f"has been deleted, "
            f"{user.mention} active is now set to "
            f"{clash_updated_player_obj.name} "
            f"{clash_updated_player_obj.tag}"
        )

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# client events
@bot.event
async def on_member_join(ctx):
    # get uninitiated role from db
    db_role_obj = db_responder.read_rank_role_from_guild_and_clash(
        ctx.guild.id, 'uninitiated')
    if db_role_obj:
        discord_role_obj = disnake.utils.get(
            ctx.guild.roles, id=db_role_obj.discord_role_id)
        if discord_role_obj:
            await ctx.add_roles(discord_role_obj)


@bot.event
async def on_member_remove(member):
    print(f'{member} has left {member.guild.name} id {member.guild.id}')


@bot.event
async def on_reaction_add(reaction, user):
    # if the reactor is a bot
    if user.bot:
        return

    # if the author of the reacted message is not clash discord
    if (reaction.message.author.id !=
            discord_responder.get_client_discord_id()):
        return

    # if there are no embedded messages
    if len(reaction.message.embeds) == 0:
        return

    # if clash discord embedded message is not a help message
    if 'help' not in reaction.message.embeds[0].title:
        return

    ctx = await bot.get_context(reaction.message)

    db_guild_obj = db_responder.read_guild(ctx.guild.id)
    db_player_obj = db_responder.read_player_active(user.id)

    if db_player_obj:
        player_obj = await clash_responder.get_player(
            db_player_obj.player_tag, coc_client)
    else:
        player_obj = None

    bot_category = discord_responder.help_emoji_to_category(
        reaction.emoji, client_data.bot_categories)

    help_dict = discord_responder.help_switch(
        db_guild_obj, db_player_obj, player_obj, user.id, reaction.emoji,
        bot_category, client_data.bot_categories, ctx.bot.all_slash_commands)
    field_dict_list = help_dict['field_dict_list']
    emoji_list = help_dict['emoji_list']

    if bot_category:
        embed_title = f"{ctx.bot.user.name} {bot_category.name} help"
    else:
        embed_title = f"{ctx.bot.user.name} help menu"

    embed_list = discord_responder.embed_message(
        icon_url=ctx.bot.user.avatar.url,
        title=embed_title,
        bot_user_name=ctx.bot.user.name,
        field_list=field_dict_list,
        author_display_name=user.display_name,
        author_avatar_url=user.avatar.url
    )

    for embed in embed_list:
        await reaction.message.edit(embed=embed)

    await reaction.message.clear_reactions()
    if bot_category:
        await reaction.message.add_reaction(client_data.back_emoji)
    else:
        for emoji in emoji_list:
            await reaction.message.add_reaction(emoji)


@bot.event
async def on_guild_role_delete(role):
    # check if deleted role is a claimed role

    # clan role
    clan_role = db_responder.read_clan_role(role.id)
    # clan role found
    if clan_role:
        deleted_role = db_responder.delete_clan_role(role.id)
        return

    # rank role
    rank_role = db_responder.read_rank_role(role.id)
    # rank role found
    if rank_role:
        deleted_role = db_responder.delete_rank_role(role.id)
        return


@bot.event
async def on_guild_remove(guild):
    # check if removed guild is a claimed guild
    db_guild = db_responder.read_guild(guild.id)

    # guild was claimed
    if db_guild:
        deleted_guild = db_responder.delete_guild(guild.id)
        return


@bot.event
async def on_slash_command_error(inter, exception):
    if isinstance(exception, commands.CommandNotFound):
        await inter.send(
            content=f"command '{inter.invoked_with}' could not be found")

    elif isinstance(exception, commands.MissingRequiredArgument):
        if hasattr(inter, "invoked_with"):
            await inter.send(
                content=(f"command '{inter.invoked_with}' "
                         f"requires more information"))

        else:
            await inter.send(
                content=f"command requires more information")

    elif hasattr(exception.original, "text"):
        await inter.send(
            content=(f"there was an error that I have not accounted for, "
                     f"please let Razgriz know.\n\n"
                     f"error text: `{exception.original.text}`"))

    elif hasattr(exception.original, "args"):
        await inter.send(
            content=(f"there was an error that I have not accounted for, "
                     f"please let Razgriz know.\n\n"
                     f"error text: `{exception.original.args[0]}`"))

    else:
        await inter.send(
            content=(f"there was an error that I have not accounted for, "
                     f"please let Razgriz know"))


if __name__ == "__main__":
    bot.run(discord_responder.get_client_token())
