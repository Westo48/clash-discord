import disnake
import coc
from asyncio.tasks import sleep
from disnake.ext import commands
import ClashDiscord_Client_Data
import ClashResponder as clash_responder
import DiscordResponder as discord_responder
import RazBotDB_Responder as db_responder

client_data = ClashDiscord_Client_Data.ClashDiscord_Data()

coc_client = coc.login(
    email=discord_responder.get_client_email(),
    password=discord_responder.get_client_password()
)

intents = disnake.Intents.all()

bot = commands.Bot(
    command_prefix=discord_responder.get_client_prefix(),
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


# Player

@bot.slash_command(
    brief='player',
    description="parent for player commands"
)
async def player(inter):
    """
        parent for player commands
    """

    pass


@player.sub_command(
    brief='player',
    description="get information about your active player"
)
async def info(inter):
    """
        get information about your active player
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.player_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']

    field_dict_list = discord_responder.player_info(player_obj)

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{player_obj.name} {player_obj.tag}",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=player_obj.league.icon,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@player.sub_command(
    brief='player',
    description="get information about a specified player"
)
async def find(inter, player_tag: str):
    """
        get information about a requested player

        Parameters
        ----------
        player_tag: player tag to search
    """

    await inter.response.defer()

    player_obj = await clash_responder.get_player(player_tag, coc_client)

    if player_obj is None:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=f"could not find player with tag {player_tag}",
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=[],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    field_dict_list = discord_responder.player_info(player_obj)

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{player_obj.name} {player_obj.tag}",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=player_obj.league.icon,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@player.sub_command(
    brief='player',
    description="get information about a member's active player"
)
async def memberinfo(inter, user: disnake.User):
    """
        get information about a specified player

        Parameters
        ----------
        user: user to search for active player
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(user.id)

    verification_payload = await discord_responder.player_verification(
        db_player_obj, user, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']

    field_dict_list = discord_responder.player_info(player_obj)

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{player_obj.name} {player_obj.tag}",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=player_obj.league.icon,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@player.sub_command(
    brief='player',
    description='get level information for a specified unit'
)
async def unitlvl(inter, unit_name: str):
    """
        get information about a specified player

        Parameters
        ----------
        unit_name: name of the unit you would like information on
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.player_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']

    unit_obj = clash_responder.find_unit(player_obj, unit_name)
    field_dict_list = [discord_responder.unit_lvl(
        player_obj, unit_obj, unit_name)]
    # unit_obj not found
    # set title to player name
    if not unit_obj:
        title_string = player_obj.name
    # unit_obj found
    # set title to player_name unit_name
    else:
        title_string = f"{player_obj.name} {unit_obj.name}"

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=title_string,
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=player_obj.league.icon,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@player.sub_command(
    brief='player',
    description='get all your unit levels'
)
async def allunitlvl(inter):
    """
        get all your unit levels
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.player_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']

    field_dict_list = discord_responder.unit_lvl_all(player_obj)
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{player_obj.name} units",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=player_obj.league.icon,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@player.sub_command(
    brief='player',
    description='get all your hero levels'
)
async def allherolvl(inter):
    """
        get all your hero levels
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.player_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']

    field_dict_list = discord_responder.hero_lvl_all(player_obj)
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{player_obj.name} heroes",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=player_obj.league.icon,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@player.sub_command(
    brief='player',
    description='get all your pet levels'
)
async def allpetlvl(inter):
    """
        get all your pet levels
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.player_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']

    field_dict_list = discord_responder.pet_lvl_all(player_obj)
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{player_obj.name} pets",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=player_obj.league.icon,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@player.sub_command(
    brief='player',
    description='get all your troop levels'
)
async def alltrooplvl(inter):
    """
        get all your troop levels
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.player_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']

    field_dict_list = discord_responder.troop_lvl_all(player_obj)
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{player_obj.name} troops",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=player_obj.league.icon,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@player.sub_command(
    brief='player',
    description='get all your spell levels'
)
async def allspelllvl(inter):
    """
        get all your spell levels
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.player_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']

    field_dict_list = discord_responder.spell_lvl_all(player_obj)
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{player_obj.name} spells",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=player_obj.league.icon,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@player.sub_command(
    brief='player',
    description='get all your siege levels'
)
async def allsiegelvl(inter):
    """
        get all your siege levels
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.player_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']

    field_dict_list = discord_responder.siege_lvl_all(player_obj)
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{player_obj.name} sieges",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=player_obj.league.icon,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@player.sub_command(
    brief='player',
    description='check to see what super troops you have active'
)
async def supertroop(inter):
    """
        check to see what super troops you have active
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.player_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']

    active_super_troop_list = clash_responder.player_active_super_troops(
        player_obj)

    field_dict_list = discord_responder.active_super_troops(
        player_obj, active_super_troop_list)
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{player_obj.name} super troops",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=player_obj.league.icon,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@player.sub_command(
    brief='player',
    description='returns the user linked to a requested player'
)
async def finduser(inter, player_tag: str):
    """
        returns the user linked to a requested player

        Parameters
        ----------
        player_tag: player tag to search
    """

    await inter.response.defer()

    player_obj = await clash_responder.get_player(player_tag, coc_client)

    # player with given tag not found
    if player_obj is None:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=f"could not find player with tag {player_tag}",
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=[],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    field_dict_list = [discord_responder.find_user_from_tag(
        player_obj, inter.guild.members)]

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=None,
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=player_obj.league.icon,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


# Clan

@bot.slash_command(
    brief='clan',
    description="parent for clan commands"
)
async def clan(inter):
    """
        parent for clan commands
    """

    pass


@clan.sub_command(
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

    await inter.response.defer()

    clan_obj = await clash_responder.get_clan(clan_tag, coc_client)

    # clan with given tag not found
    if clan_obj is None:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=f"could not find clan with tag {clan_tag}",
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=[],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    field_dict_list = discord_responder.clan_info(clan_obj)

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{clan_obj.name} {clan_obj.tag}",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=clan_obj.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@clan.sub_command(
    brief='clan',
    description="get information about your active player's clan"
)
async def info(inter):
    """
        get information about your active player's clan
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.clan_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']
    clan_obj = verification_payload['clan_obj']

    field_dict_list = discord_responder.clan_info(clan_obj)

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{clan_obj.name} {clan_obj.tag}",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=clan_obj.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@clan.sub_command(
    brief='clan',
    description="get information about mentioned clan"
)
async def mentioninfo(inter, role: disnake.Role):
    """
        get information about mentioned clan

        Parameters
        ----------
        role: role to search for linked clan
    """

    await inter.response.defer()

    # role has been mentioned
    # get clan tag from clan role
    db_clan_role = db_responder.read_clan_role(role.id)

    # role mentioned was not a linked clan role
    if db_clan_role is None:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=f"role mentioned is not linked to a clan",
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=[],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    clan_obj = await clash_responder.get_clan(
        db_clan_role.clan_tag, coc_client)

    # clan with tag from db clan role not found
    if clan_obj is None:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=f"could not find clan with tag {db_clan_role.clan_tag}",
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=[],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    field_dict_list = discord_responder.clan_info(clan_obj)

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{clan_obj.name} {clan_obj.tag}",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=clan_obj.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@clan.sub_command(
    brief='clan',
    description="clan's TH lineup"
)
async def lineup(inter):
    """
        get information about mentioned clan
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.clan_leadership_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']
    clan_obj = verification_payload['clan_obj']

    field_dict_list = await discord_responder.clan_lineup(clan_obj, coc_client)

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{clan_obj.name} lineup",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=clan_obj.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@clan.sub_command(
    brief='clan',
    description="rundown of clan member's war preference"
)
async def warpreference(inter):
    """
        rundown of clan member's war preference
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.clan_leadership_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']
    clan_obj = verification_payload['clan_obj']

    field_dict_list = await discord_responder.clan_war_preference(
        clan_obj, coc_client)

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{clan_obj.name} war preference",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=clan_obj.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )
    for embed in embed_list:
        await inter.send(embed=embed)


@clan.sub_command(
    brief='clan',
    description='shows who can donate the best requested troop'
)
async def donate(inter, unit_name: str):
    """
        get information about mentioned clan

        Parameters
        ----------
        unit_name: name of unit to search clan donations
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.clan_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']
    clan_obj = verification_payload['clan_obj']

    donator_list = await clash_responder.donation(
        clan_obj, unit_name, coc_client)

    field_dict_list = discord_responder.donation(
        clan_obj, donator_list, unit_name)

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{clan_obj.name} {clan_obj.tag}",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=clan_obj.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )
    for embed in embed_list:
        await inter.send(embed=embed)


@clan.sub_command(
    brief='clan',
    description="shows who in your clan has a specified super troop active"
)
async def supertroop(inter, unit_name: str):
    """
        shows who in your clan has a specified super troop active

        Parameters
        ----------
        unit_name: name of unit to search clan super troops
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.clan_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']
    clan_obj = verification_payload['clan_obj']

    super_troop_obj = clash_responder.find_super_troop(
        player_obj, unit_name)

    # super troop was not found
    if super_troop_obj is None:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=f"{unit_name} is not a viable request",
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=[],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    donor_list = await clash_responder.active_super_troop_search(
        super_troop_obj, clan_obj, coc_client)

    field_dict_list = discord_responder.super_troop_search(
        clan_obj, donor_list, super_troop_obj)

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{clan_obj.name} {clan_obj.tag}",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=clan_obj.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@clan.sub_command(
    brief='clan',
    description="returns the users linked to the active player's clan"
)
async def findusers(inter):
    """
        returns the users linked to the active player's clan
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.clan_leadership_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']
    clan_obj = verification_payload['clan_obj']

    field_dict_list = []
    # finding the user for each member in the clan
    for member_obj in clan_obj.members:
        field_dict_list.append(discord_responder.find_user_from_tag(
            member_obj, inter.guild.members))

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{clan_obj.name} linked users",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=clan_obj.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


# War

@bot.slash_command(
    brief='war',
    description="parent for war commands"
)
async def war(inter):
    """
        parent for war commands
    """

    pass


@war.sub_command(
    brief='war',
    description="overview of the current war"
)
async def info(inter):
    """
        overview of the current war
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.war_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_info(war_obj)

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@war.sub_command(
    brief='war',
    description="time remaining in the current war")
async def time(inter):
    """
        time remaining in the current war
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.war_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_time(war_obj)

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@war.sub_command(
    brief='war',
    description="list of players that missed attacks in the current war"
)
async def noattack(inter):
    """
        list of players that missed attacks in the current war
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.war_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_no_attack(war_obj)

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@war.sub_command(
    brief='war',
    description="overview of all members in war"
)
async def clanstars(inter):
    """
        overview of all members in war
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.war_leadership_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_members_overview(war_obj)

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@war.sub_command(
    brief='war',
    description="all attacks for every war member"
)
async def allattacks(inter):
    """
        all attacks for every war member
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.war_leadership_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_all_attacks(war_obj)

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@war.sub_command(
    brief='war',
    description="your war member score"
)
async def score(inter):
    """
        your war member score
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.war_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_member_standing(
        war_obj, player_obj)
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{player_obj.name} war score",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@war.sub_command(
    brief='war',
    description="requested war member's score"
)
async def memberscore(inter, user: disnake.User):
    """
        requested war member's score

        Parameters
        ----------
        user: user to search for active player's war member score
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(user.id)

    verification_payload = await discord_responder.war_verification(
        db_player_obj, user, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_member_standing(
        war_obj, player_obj)
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{player_obj.name} war score",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@war.sub_command(
    brief='war',
    description="every clanmate's war member score"
)
async def clanscore(inter):
    """
        every clanmate's war member score
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.war_leadership_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_all_member_standing(
        war_obj)
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@war.sub_command(
    brief='war',
    description="town hall lineup for war"
)
async def lineup(inter):
    """
        town hall lineup for war
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.war_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    await inter.edit_original_message(content=discord_responder.war_lineup(war_obj))


@war.sub_command(
    brief='war',
    description="town hall lineup for each war member"
)
async def memberlineup(inter):
    """
        town hall lineup for each war member
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.war_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_member_lineup(
        war_obj)
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


# CWL Group

@bot.slash_command(
    brief='cwl',
    description="parent for cwl commands"
)
async def cwl(inter):
    """
        parent for cwl commands
    """

    pass


@cwl.sub_command(
    brief='cwl',
    description="returns the CWL group lineup"
)
async def lineup(inter):
    """
        returns the CWL group lineup
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.cwl_group_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']
    cwl_group_obj = verification_payload['cwl_group_obj']

    await inter.edit_original_message(
        content=discord_responder.cwl_lineup(cwl_group_obj))


@cwl.sub_command(
    brief='cwl',
    description="lists each score you have in CWL"
)
async def score(inter):
    """
        returns the CWL group lineup
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.cwl_group_verification(
        db_player_obj, inter.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']
    cwl_group_obj = verification_payload['cwl_group_obj']

    field_dict_list = discord_responder.cwl_member_standing(
        player_obj, cwl_group_obj, player_obj.clan.tag, coc_client)
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{player_obj.name} CWL score",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=player_obj.league.icon,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@cwl.sub_command(
    brief='cwl',
    description="lists each score the specified member has in CWL"
)
async def memberscore(inter, user: disnake.User):
    """
        lists each score the specified member has in CWL

        Parameters
        ----------
        user: user to search for active player's cwl member score
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(user.id)

    verification_payload = await discord_responder.cwl_group_verification(
        db_player_obj, user, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']
    cwl_group_obj = verification_payload['cwl_group_obj']

    field_dict_list = discord_responder.cwl_member_standing(
        cwl_group_obj, player_obj.clan.tag)
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{player_obj.name} CWL score",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=player_obj.league.icon,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@cwl.sub_command(
    brief='cwl',
    description="Lists each member and their score in CWL"
)
async def clanscore(inter):
    """
        returns the CWL group lineup
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = (
        await discord_responder.cwl_group_leadership_verification(
            db_player_obj, inter.author, coc_client))
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player_obj = verification_payload['player_obj']
    cwl_group_obj = verification_payload['cwl_group_obj']

    field_dict_list = discord_responder.cwl_clan_standing(
        cwl_group_obj, player_obj.clan.tag)
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{player_obj.clan.name} CWL scores",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


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


@discord.sub_command(
    brief='discord',
    description="returns help menu"
)
async def help(inter):
    """
        returns help menu
    """

    await inter.response.defer()

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
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{inter.bot.user.name} help menu",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=None,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)

    original_message = await inter.original_message()

    for emoji in emoji_list:
        await original_message.add_reaction(emoji)


@discord.sub_command(
    description=("*leadership* "
                 "announces message to specified channel")
)
async def announce(inter, channel: disnake.TextChannel, message: str):
    """
        *leadership*
        announces message to specified channel

        Parameters
        ----------
        channel: channel to announce the message
        message: message to send the specified channel
    """

    await inter.response.defer(ephemeral=True)

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = (
        await discord_responder.player_leadership_verification(
            db_player_obj, inter.author, coc_client))
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    try:
        await channel.send(content=message)
    except:
        field_dict_list = [{
            "name": "message could not be sent",
            "value": f"please ensure bot is in channel {channel.mention}"
        }]
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=field_dict_list,
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )
        await inter.send(embeds=embed_list)

        return

    field_dict_list = [{
        "name": "message sent",
        "value": f"channel {channel.mention}"
    }]
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=None,
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=None,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )
    await inter.send(embeds=embed_list)


@discord.sub_command(
    description=("*leadership* "
                 "announces message to specified channel, "
                 "pings user with the specified player tag")
)
async def announceplayer(
    inter, channel: disnake.TextChannel,
    player_tag: str, message: str
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

    await inter.response.defer(ephemeral=True)

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = (
        await discord_responder.player_leadership_verification(
            db_player_obj, inter.author, coc_client))
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    player = await clash_responder.get_player(player_tag, coc_client)

    if player is None:
        field_dict_list = [{
            "name": f"player with tag {player_tag} not found",
            "value": f"please check the tag and try again"
        }]
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=field_dict_list,
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )
        await inter.edit_original_message(embeds=embed_list)
        return

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
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=field_dict_list,
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )
        await inter.send(embeds=embed_list)

        return

    field_dict_list = [{
        "name": "message sent",
        "value": f"channel {channel.mention}"
    }]
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=None,
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=None,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )
    await inter.send(embeds=embed_list)


@discord.sub_command(
    description=("*leadership* "
                 "announces message to specified channel, "
                 "pings all in current war")
)
async def announcewar(inter, channel: disnake.TextChannel, message: str):
    """
        *leadership*
        announces message to specified channel,
        pings all in current war

        Parameters
        ----------
        channel: channel to announce the message
        message: message to send the specified channel
    """

    await inter.response.defer(ephemeral=True)

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = (
        await discord_responder.war_leadership_verification(
            db_player_obj, inter.author, coc_client))
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    war = verification_payload['war_obj']

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
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=field_dict_list,
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )
        await inter.send(embeds=embed_list)

        return

    field_dict_list = [{
        "name": "message sent",
        "value": f"channel {channel.mention}"
    }]
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=None,
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=None,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )
    await inter.send(embeds=embed_list)


@discord.sub_command(
    description=("*leadership* "
                 "announces message to channel, "
                 "pings all in war missing attacks")
)
async def announcewarnoatk(inter, channel: disnake.TextChannel, message: str):
    """
        *leadership*
        announces message to channel,
        pings all in war missing attacks

        Parameters
        ----------
        channel: channel to announce the message
        message: message to send the specified channel
    """

    await inter.response.defer(ephemeral=True)

    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = (
        await discord_responder.war_leadership_verification(
            db_player_obj, inter.author, coc_client))
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    war = verification_payload['war_obj']

    message += "\n\n"

    war_member_no_attack_list = clash_responder.war_no_attack(war)

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
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=field_dict_list,
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )
        await inter.send(embeds=embed_list)

        return

    field_dict_list = [{
        "name": "message sent",
        "value": f"channel {channel.mention}"
    }]
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=None,
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=None,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )
    await inter.send(embeds=embed_list)


@discord.sub_command(
    brief='discord',
    description="update your roles"
)
async def role(inter):
    """
        update your roles
    """

    await inter.response.defer()

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
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=embed_dict["title"],
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=embed_dict["thumbnail"],
            field_list=embed_dict["field_dict_list"],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.send(embeds=embed_list)


@discord.sub_command(
    brief='discord',
    description="update mentioned user's roles"
)
async def rolemember(inter, user: disnake.User):
    """
        update mentioned user's roles

        Parameters
        ----------
        user: user to update roles
    """

    await inter.response.defer()

    db_guild_obj = db_responder.read_guild(inter.guild.id)

    # if guild is not claimed
    if not db_guild_obj:
        await inter.edit_original_message(
            content=f"{inter.guild.name} has not been claimed")
        return

    # getting author's db player obj for leadership verification
    db_player_obj = db_responder.read_player_active(inter.author.id)

    verification_payload = await discord_responder.player_leadership_verification(
        db_player_obj, inter.author, coc_client)

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embeds=embed_list)
        return

    embed_dict_list = await discord_responder.update_roles(
        user, inter.guild, coc_client)

    for embed_dict in embed_dict_list:

        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=inter.bot.user.avatar.url,
            title=embed_dict["title"],
            description=None,
            bot_prefix=inter.bot.command_prefix,
            bot_user_name=inter.bot.user.name,
            thumbnail=embed_dict["thumbnail"],
            field_list=embed_dict["field_dict_list"],
            image_url=None,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await inter.send(embeds=embed_list)


@discord.sub_command(
    brief='discord',
    description="update roles of every member in the server"
)
async def roleall(inter):
    """
        update roles of every member in the server
    """

    await inter.response.defer()

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
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=None,
        description="updating roles",
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=None,
        field_list=[],
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.send(embeds=embed_list)

    for user in inter.guild.members:
        if user.bot:
            continue

        embed_dict_list = await discord_responder.update_roles(
            user, inter.guild, coc_client)

        for embed_dict in embed_dict_list:

            embed_list = discord_responder.embed_message(
                Embed=disnake.Embed,
                color=disnake.Color(client_data.embed_color),
                icon_url=inter.bot.user.avatar.url,
                title=embed_dict["title"],
                description=None,
                bot_prefix=inter.bot.command_prefix,
                bot_user_name=inter.bot.user.name,
                thumbnail=embed_dict["thumbnail"],
                field_list=embed_dict["field_dict_list"],
                image_url=None,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await inter.send(embeds=embed_list)

    # telling the user that the bot is done updating roles
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=None,
        description="update complete",
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=None,
        field_list=[],
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.send(embeds=embed_list)


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
    # if user wasn't claimed and now is
    if user:
        await inter.edit_original_message(
            content=f"{inter.author.mention} is now claimed")
    # if user was already claimed
    else:
        await inter.edit_original_message(
            content=f"{inter.author.mention} has already been claimed")


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
        await inter.edit_original_message(
            content=f"player with tag {player_tag} was not found")
        return

    # confirm user has been claimed
    db_user_obj = db_responder.read_user(inter.author.id)
    if not db_user_obj:
        # user has not been claimed
        db_user_obj = db_responder.claim_user(inter.author.id)
        if not db_user_obj:
            # user could not be claimed
            await inter.edit_original_message(
                content=f"{inter.author.mention} user couldn't be claimed")
            return

    # confirm player has not been claimed
    db_player_obj = db_responder.read_player_from_tag(player_obj.tag)
    # player has already been claimed
    if db_player_obj:
        await inter.edit_original_message(
            content=(f"{player_obj.name} {player_obj.tag} "
                     f"has already been claimed"))
        return

    # authenticate player api key
    player_verified = await clash_responder.verify_token(
        api_key, player_obj.tag, coc_client)
    # api key could not be verified
    if not player_verified:
        await inter.edit_original_message(
            content=(f"verification for "
                     f"player tag {player_obj.tag} has failed"))
        return

    # user claimed
    # player is valid
    # player hasn't been claimed
    # player is authenticated
    db_player_obj = db_responder.claim_player(
        inter.author.id, player_obj.tag)

    if db_player_obj:
        # if succesfully claimed
        await inter.edit_original_message(
            content=(f"{player_obj.name} {player_obj.tag} "
                     f"is now claimed by {inter.author.mention}"))
    else:
        # if failed to claim
        await inter.edit_original_message(
            content=(f"Could not claim {player_obj.name} "
                     f"{player_obj.tag} for {inter.author.mention}"))


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
        await inter.edit_original_message(
            content=(f"{inter.author.mention} does not have any "
                     f"claimed players"))
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
        await inter.edit_original_message(
            content=f"player with tag {player_tag} not found")
        return

    db_player_obj = db_responder.read_player(inter.author.id, player_obj.tag)

    # if requested player is not claimed
    if not db_player_obj:
        await inter.edit_original_message(
            content=(
                f"{inter.author.mention} "
                f"has not claimed "
                f"{player_obj.name} {player_obj.tag}"
            ))
        return

    # if requested player is the active player
    if db_player_obj.active:
        await inter.edit_original_message(
            content=(
                f"{player_obj.name} {player_obj.tag} "
                f"is already your active player "
                f"{inter.author.mention}"
            ))
        return

    else:
        db_player_obj = db_responder.update_player_active(
            inter.author.id, player_obj.tag)
        await inter.edit_original_message(
            content=(
                f"{player_obj.name} {player_obj.tag} is now "
                f"your active player {inter.author.mention}"
            ))
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
        await inter.edit_original_message(
            content=f"player with tag {player_tag} not found")
        return

    db_player_obj = db_responder.read_player(inter.author.id, player_obj.tag)

    # db player not found
    if not db_player_obj:
        await inter.edit_original_message(
            content=(f"{player_obj.name} {player_obj.tag} "
                     f"is not claimed by {inter.author.mention}"))
        return

    db_del_player_obj = db_responder.delete_player(
        inter.author.id, player_obj.tag)

    # player was not deleted
    if db_del_player_obj:
        await inter.edit_original_message(content=(
            f"{player_obj.name} {player_obj.tag} "
            f"could not be deleted "
            f"from {inter.author.mention} player list"
        ))
        return

    db_active_player_obj = db_responder.read_player_active(inter.author.id)

    # active player found
    # no need to change the active player
    if db_active_player_obj:
        await inter.edit_original_message(content=(
            f"{player_obj.name} {player_obj.tag} "
            f"has been deleted "
            f"from {inter.author.mention} player list"
        ))
        return

    # no active player found
    # check if there are any other players
    db_player_obj_list = db_responder.read_player_list(
        inter.author.id)

    # no additional players claimed
    if len(db_player_obj_list) == 0:
        await inter.edit_original_message(content=(
            f"{player_obj.name} {player_obj.tag} "
            f"has been deleted, "
            f"{inter.author.mention} has no more claimed players"
        ))
        return

    # additional players claimed by user
    # update the first as the new active
    db_updated_player_obj = db_responder.update_player_active(
        inter.author.id, db_player_obj_list[0].player_tag)

    # update not successful
    if not db_updated_player_obj:
        await inter.edit_original_message(content=(
            f"{player_obj.name} {player_obj.tag} "
            f"has been deleted, could not update active player, "
            f"{inter.author.mention} has no active players"
        ))
        return

    # update was successful
    clash_updated_player_obj = await clash_responder.get_player(
        db_updated_player_obj.player_tag, coc_client)

    # clash player not found
    if not clash_updated_player_obj:
        await inter.edit_original_message(content=(
            f"{player_obj.name} {player_obj.tag} "
            f"has been deleted, "
            f"{inter.author.mention} active is now set to "
            f"{db_updated_player_obj.player_tag}, "
            f"could not find player in clash of clans"
        ))
        return

    # player deleted
    # active player updated
    # clash player found
    await inter.edit_original_message(content=(
        f"{player_obj.name} {player_obj.tag} "
        f"has been deleted, "
        f"{inter.author.mention} active is now set to "
        f"{clash_updated_player_obj.name} "
        f"{clash_updated_player_obj.tag}"
    ))


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
        await inter.edit_original_message(
            content=f"{inter.author.mention} has not been claimed")
        return

    db_guild_obj = db_responder.read_guild(inter.guild.id)

    # guild already claimed
    if db_guild_obj:
        await inter.edit_original_message(
            content=f"{inter.guild.name} has already been claimed")
        return

    db_claimed_guild = db_responder.claim_guild(
        inter.author.id, inter.guild.id)

    # guild already claimed or could not be claimed
    if not db_claimed_guild:
        await inter.edit_original_message(
            content=f"{inter.guild.name} could not be claimed")
        return

    await inter.edit_original_message(
        content=(f"{inter.guild.name} is now claimed "
                 f"by admin user {inter.author.mention}")
    )


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
    description="claim the requested clan"
)
async def claim(inter, clan_tag: str):
    """
        claim the requested clan

        Parameters
        ----------
        clan_tag: clan tag to claim
    """

    db_guild_obj = db_responder.read_guild(inter.guild.id)

    # guild not claimed
    if not db_guild_obj:
        await inter.edit_original_message(
            content=f"{inter.guild.name} has not been claimed")
        return

    db_user_obj = db_responder.read_user(inter.author.id)

    # user not claimed
    if not db_user_obj:
        await inter.edit_original_message(
            content=f"{inter.author.mention} has not been claimed")
        return

    # user is not guild admin and is not super user
    if (not db_guild_obj.admin_user_id == inter.author.id
            and not db_user_obj.super_user):
        await inter.edit_original_message(
            content=f"{inter.author.mention} is not guild's admin")
        return

    clan_obj = await clash_responder.get_clan(clan_tag, coc_client)

    # clan not found
    if not clan_obj:
        await inter.edit_original_message(
            content=f"couldn't find clan {clan_tag}")
        return

    claimed_clan_obj = db_responder.read_clan(inter.guild.id, clan_obj.tag)

    # already claimed
    if claimed_clan_obj:
        await inter.edit_original_message(content=(
            f"{clan_obj.name} has already been claimed for "
            f"{inter.guild.name}"))
        return

    db_player_obj_list = db_responder.read_player_list(inter.author.id)

    # no claimed player
    if len(db_player_obj_list) == 0:
        await inter.edit_original_message(
            content=f"{inter.author.mention} has no claimed players")
        return

    user_in_clan = False

    # validating any player in player list is in requested clan
    for db_player_obj in db_player_obj_list:
        player_obj = await clash_responder.get_player(
            db_player_obj.player_tag, coc_client)

        # player in clan
        if player_obj.clan.tag == clan_obj.tag:
            user_in_clan = True
            break

    # player not in requested clan
    if not user_in_clan:
        await inter.edit_original_message(
            content=f"{inter.author.mention} is not in {clan_obj.name}")
        return

    db_clan_obj = db_responder.claim_clan(inter.guild.id, clan_obj.tag)

    # clan not claimed
    if not db_clan_obj:
        await inter.edit_original_message(
            content=f"couldn't claim {clan_obj.name}")
        return

    await inter.edit_original_message(
        content=f"{clan_obj.name} has been claimed")


@clan.sub_command(
    brief='client',
    description="clans claimed by a discord guild",
    hidden=True
)
async def show(inter):
    """
        clans claimed by a discord guild

        Parameters
        ----------
        clan_tag: clan tag to claim
    """

    db_guild_obj = db_responder.read_guild(inter.guild.id)

    # guild not claimed
    if not db_guild_obj:
        await inter.edit_original_message(
            content=f"{inter.guild.name} has not been claimed")
        return

    db_user_obj = db_responder.read_user(inter.author.id)

    # user not claimed
    if not db_user_obj:
        await inter.edit_original_message(
            content=f"{inter.author.mention} has not been claimed")
        return

    # user is not guild admin and is not super user
    if (not db_guild_obj.admin_user_id == inter.author.id
            and not db_user_obj.super_user):
        await inter.edit_original_message(
            content=f"{inter.author.mention} is not guild's admin")
        return

    db_clan_obj_list = db_responder.read_clan_list_from_guild(inter.guild.id)

    # guild has no claimed clans
    if len(db_clan_obj_list) == 0:
        await inter.edit_original_message(
            content=f"{inter.guild.name} does not have any claimed clans")
        return

    message = f"{inter.guild.name} has claimed "
    for item in db_clan_obj_list:
        clan = await clash_responder.get_clan(
            item.clan_tag, coc_client)
        message += f"{clan.name} {clan.tag}, "

    # cuts the last two characters from the string ', '
    message = message[:-2]

    await inter.edit_original_message(content=message)


@clan.sub_command(
    brief='client',
    description="deletes the requested clan claim"
)
async def remove(inter, clan_tag: str):
    """
        deletes the requested clan claim

        Parameters
        ----------
        clan_tag: clan tag to delete from client
    """

    db_guild_obj = db_responder.read_guild(inter.guild.id)

    # guild not claimed
    if not db_guild_obj:
        await inter.edit_original_message(
            content=f"{inter.guild.name} has not been claimed")
        return

    db_user_obj = db_responder.read_user(inter.author.id)

    # user not claimed
    if not db_user_obj:
        await inter.edit_original_message(
            content=f"{inter.author.mention} has not been claimed")
        return

    # user is not guild admin and is not super user
    if (not db_guild_obj.admin_user_id == inter.author.id
            and not db_user_obj.super_user):
        await inter.edit_original_message(
            content=f"{inter.author.mention} is not guild's admin")
        return

    clan_obj = await clash_responder.get_clan(clan_tag, coc_client)

    # clan not found
    if not clan_obj:
        await inter.edit_original_message(
            content=f"couldn't find clan {clan_tag}")
        return

    db_clan_obj = db_responder.read_clan(inter.guild.id, clan_obj.tag)
    # clan not claimed by guild
    if not db_clan_obj:
        await inter.edit_original_message(
            content=f"{clan_obj.name} has not been claimed "
            f"by {inter.guild.name}")
        return

    db_clan_deletion = db_responder.delete_clan(inter.guild.id, clan_obj.tag)
    # clan was found after deletion
    if db_clan_deletion:
        await inter.edit_original_message(
            content=f"{clan_obj.name} could not be deleted")
        return

    await inter.edit_original_message(
        content=(f"{clan_obj.name} has been deleted "
                 f"from {inter.guild.name}"))


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
    description="shows all roles claimed by a discord guild"
)
async def show(inter):
    """
        shows all roles claimed by a discord guild
    """

    db_user_obj = db_responder.read_user(inter.author.id)

    db_guild_obj = db_responder.read_guild(inter.guild.id)
    # guild not claimed
    if not db_guild_obj:
        await inter.edit_original_message(
            content=f"{inter.guild.name} has not been claimed")
        return

    # user not claimed
    if not db_user_obj:
        await inter.edit_original_message(
            content=f"{inter.author.mention} has not been claimed")
        return

    # user is not guild admin and is not super user
    if (not db_guild_obj.admin_user_id == inter.author.id
            and not db_user_obj.super_user):
        await inter.edit_original_message(
            content=f"{inter.author.mention} is not guild's admin")
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
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=inter.bot.user.avatar.url,
        title=f"{inter.guild.name} claimed roles",
        description=None,
        bot_prefix=inter.bot.command_prefix,
        bot_user_name=inter.bot.user.name,
        thumbnail=None,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await inter.edit_original_message(embeds=embed_list)


@role.sub_command(
    brief='client',
    description=("remove the claimed discord role, "
                 "the role will not be deleted from discord")
)
async def remove(inter, role: disnake.Role):
    """
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
        await inter.edit_original_message(
            content=f"{inter.guild.name} has not been claimed")
        return

    # user not claimed
    if not db_user_obj:
        await inter.edit_original_message(
            content=f"{inter.author.mention} has not been claimed")
        return

    # user is not guild admin and is not super user
    if (not db_guild_obj.admin_user_id == inter.author.id
            and not db_user_obj.super_user):
        await inter.edit_original_message(
            content=f"{inter.author.mention} is not guild's admin")
        return

    db_clan_role_obj = db_responder.read_clan_role(role.id)

    # claimed role is clan role
    if db_clan_role_obj:
        # delete clan role
        db_clan_role_deletion = db_responder.delete_clan_role(role.id)
        # clan role found after deletion
        if db_clan_role_deletion:
            await inter.edit_original_message(
                content=f"{role.mention} claim could not be removed")
            return

        # clan role deleted
        await inter.edit_original_message(
            content=f"{role.mention} claim was removed")
        return

    db_rank_role_obj = db_responder.read_rank_role(role.id)

    # claimed role is rank role
    if db_rank_role_obj:
        # delete rank role
        db_rank_role_deletion = db_responder.delete_rank_role(role.id)
        # rank role found after deletion
        if db_rank_role_deletion:
            await inter.edit_original_message(
                content=f"{role.mention} claim could not be removed")
            return

        # rank role deleted
        await inter.edit_original_message(
            content=f"{role.mention} claim was removed")
        return

    await inter.edit_original_message(
        content=f"{role.mention} is not claimed")


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
    description="claim a clan's discord role"
)
async def claim(inter, role: disnake.Role, clan_tag: str):
    """
        claim a clan's discord role

        Parameters
        ----------
        role: role object to claim and link to claimed clan
        clan_tag: clan tag to link to role
    """

    clan_obj = await clash_responder.get_clan(clan_tag, coc_client)

    # clan not found
    if not clan_obj:
        await inter.edit_original_message(
            content=f"couldn't find clan {clan_tag}")
        return

    db_guild_obj = db_responder.read_guild(inter.guild.id)

    # guild not claimed
    if not db_guild_obj:
        await inter.edit_original_message(
            content=f"{inter.guild.name} has not been claimed")
        return

    db_user_obj = db_responder.read_user(inter.author.id)

    # user not claimed
    if not db_user_obj:
        await inter.edit_original_message(
            content=f"{inter.author.mention} has not been claimed")
        return

    # user is not guild admin and is not super user
    if (not db_guild_obj.admin_user_id == inter.author.id
            and not db_user_obj.super_user):
        await inter.edit_original_message(
            content=f"{inter.author.mention} is not guild's admin")
        return

    db_clan_obj = db_responder.read_clan(inter.guild.id, clan_obj.tag)

    # clan not claimed by guild
    if not db_clan_obj:
        await inter.edit_original_message(
            content=(f"{clan_obj.name} has not been claimed "
                     f"by {inter.guild.name}"))
        return

    # confirm clan role has not been claimed
    db_clan_role_obj = db_responder.read_clan_role(role.id)

    # clan role has been claimed
    if db_clan_role_obj:
        await inter.edit_original_message(
            content=(f"{role.mention} has already been claimed "
                     f"for clan {db_clan_role_obj.clan_tag}"))
        return

    # confirm rank role has not been claimed
    db_rank_role_obj = db_responder.read_rank_role(role.id)

    # rank role has been claimed
    if db_rank_role_obj:
        await inter.edit_original_message(
            content=(f"{role.mention} has already been claimed "
                     f"for rank {db_rank_role_obj.model_name}"))
        return

    # claim clan role
    claimed_clan_role_obj = db_responder.claim_clan_role(
        role.id, inter.guild.id, clan_obj.tag)

    # clan role could not be claimed
    if not claimed_clan_role_obj:
        await inter.edit_original_message(
            content=(f"could not claim {role.mention} "
                     f"for clan {clan_obj.tag}"))
        return

    await inter.edit_original_message(
        content=f"{role.mention} has been claimed for clan {clan_obj.tag}")


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
    description="claim a rank's discord role"
)
async def claim(inter, role: disnake.Role,
                rank_name: str = commands.Param(choices=[
        "leader", "co-leader", "elder", "member", "uninitiated"])
):
    """
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
        await inter.edit_original_message(
            content=f"{rank_name} is not a valid rank")
        return

    db_guild_obj = db_responder.read_guild(inter.guild.id)
    # guild not claimed
    if not db_guild_obj:
        await inter.edit_original_message(
            content=f"{inter.guild.name} has not been claimed")
        return

    db_user_obj = db_responder.read_user(inter.author.id)
    # user not claimed
    if not db_user_obj:
        await inter.edit_original_message(
            content=f"{inter.author.mention} has not been claimed")
        return

    # user is not guild admin and is not super user
    if (not db_guild_obj.admin_user_id == inter.author.id
            and not db_user_obj.super_user):
        await inter.edit_original_message(
            content=f"{inter.author.mention} is not guild's admin")
        return

    # confirm clan role has not been claimed
    db_clan_role_obj = db_responder.read_clan_role(role.id)
    # clan role has been claimed
    if db_clan_role_obj:
        await inter.edit_original_message(
            content=(f"{role.mention} has already been claimed for clan "
                     f"{db_clan_role_obj.clan_tag}"))
        return

    # confirm rank role has not been claimed
    db_rank_role_obj = db_responder.read_rank_role(role.id)
    # rank role has been claimed
    if db_rank_role_obj:
        await inter.edit_original_message(
            content=(f"{role.mention} has already been claimed for rank "
                     f"{db_rank_role_obj.model_name}"))
        return

    # claim rank role
    claimed_rank_role_obj = db_responder.claim_rank_role(
        role.id, inter.guild.id, rank_name)
    # rank role could not be claimed
    if not claimed_rank_role_obj:
        await inter.edit_original_message(
            content=(f"could not claim {role.mention} for rank "
                     f"{db_rank_role_obj.model_name}"))
        return

    await inter.edit_original_message(
        content=(f"{role.mention} has been claimed for rank "
                 f"{claimed_rank_role_obj.model_name}"))


# client super user administration

@bot.slash_command(
    brief='clientsuperuser',
    description="parent for client super user commands"
)
async def clientsuperuser(inter):
    """
        parent for client super user commands
    """

    # defer for every command
    await inter.response.defer()


@clientsuperuser.sub_command_group(
    brief='clientsuperuser',
    description="group for clientsuperuser guild commands"
)
async def guild(inter):
    """
        group for guild commands
    """

    pass


# super user client guild
@guild.sub_command(
    brief='clientsuperuser',
    description="delete a claimed guild from id"
)
async def removeclaim(inter, guild_id: str):
    """
        claim a clan's discord role

        Parameters
        ----------
        guild_id: id for guild to remove claim
    """

    db_author_obj = db_responder.read_user(inter.author.id)
    # author is not claimed
    if not db_author_obj:
        await inter.edit_original_message(
            content=f"{inter.author.mention} is not claimed")
        return

    # author is not super user
    if not db_author_obj.super_user:
        await inter.edit_original_message(
            content=f"{inter.author.mention} is not super user")
        return

    # confirm guild is claimed
    db_guild_obj = db_responder.read_guild(guild_id)
    # guild isn't claimed
    if not db_guild_obj:
        await inter.edit_original_message(
            content=f"guild with id {guild_id} is not claimed")
        return

    deleted_guild_obj = db_responder.delete_guild(guild_id)
    # guild could not be deleted
    if deleted_guild_obj:
        await inter.edit_original_message(
            content=f"guild with id {guild_id} could not be deleted")
        return

    # guild was deleted properly
    await inter.edit_original_message(
        content=f"guild with id {guild_id} was deleted")


@clientsuperuser.sub_command_group(
    brief='clientsuperuser',
    description="group for clientsuperuser user commands"
)
async def user(inter):
    """
        group for user commands
    """

    pass


# super user client user
@user.sub_command(
    brief='clientsuperuser',
    description="delete a claimed user from id"
)
async def removeclaim(inter, user_id: str):
    """
        claim a clan's discord role

        Parameters
        ----------
        user: id for user to remove claim
    """

    db_author_obj = db_responder.read_user(inter.author.id)
    # author is not claimed
    if not db_author_obj:
        await inter.edit_original_message(
            content=f"{inter.author.mention} is not claimed")
        return

    # author is not super user
    if not db_author_obj.super_user:
        await inter.edit_original_message(
            content=f"{inter.author.mention} is not super user")
        return

    # confirm user is claimed
    db_user_obj = db_responder.read_user(user_id)
    # user isn't claimed
    if not db_user_obj:
        await inter.edit_original_message(
            content=f"user with id {user_id} is not claimed")
        return

    deleted_user_obj = db_responder.delete_user(user_id)
    # user could not be deleted
    if deleted_user_obj:
        await inter.edit_original_message(
            content=f"user with id {user_id} could not be deleted")
        return

    # user was deleted properly
    await inter.edit_original_message(
        content=f"user with id {user_id} was deleted")


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
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=ctx.bot.user.avatar.url,
        title=embed_title,
        description=None,
        bot_prefix=ctx.bot.command_prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=None,
        field_list=field_dict_list,
        image_url=None,
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
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"slash command not used, please use slash commands")

    elif isinstance(error, commands.MissingRequiredArgument):
        if hasattr(ctx, "invoked_with"):
            await ctx.send(f"command '{ctx.invoked_with}' "
                           f"requires more information")

        else:
            await ctx.send(f"command requires more information")

    elif hasattr(error.original, "text"):
        await ctx.send(f"there was an error that I have not accounted for, "
                       f"please let Razgriz know.\n\n"
                       f"error text: `{error.original.text}`")

    elif hasattr(error.original, "args"):
        await ctx.send(f"there was an error that I have not accounted for, "
                       f"please let Razgriz know.\n\n"
                       f"error text: `{error.original.args[0]}`")

    else:
        await ctx.send(f"there was an error that I have not accounted for, "
                       f"please let Razgriz know")


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

bot.run(discord_responder.get_client_token())
