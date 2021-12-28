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

# home_troop_option=commands.option_enum(
# coc.HERO_ORDER +
# coc.HERO_PETS_ORDER +
# coc.HOME_TROOP_ORDER +
# coc.SPELL_ORDER
# )


@bot.event
async def on_ready():
    print(f"RazBot is ready")


@bot.command(
    aliases=['helpme'],
    brief='discord',
    description='Returns the help text you see before you'
)
async def help(ctx):
    async with ctx.typing():
        db_guild_obj = db_responder.read_guild(ctx.guild.id)
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    if db_player_obj:
        player_obj = await clash_responder.get_player(
            db_player_obj.player_tag, coc_client)
    else:
        player_obj = None

    help_dict = discord_responder.help_main(
        db_guild_obj, ctx.author.id, player_obj, client_data.bot_categories)
    field_dict_list = help_dict['field_dict_list']
    emoji_list = help_dict['emoji_list']

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=ctx.bot.user.avatar.url,
        title=f"{ctx.bot.user.name} help menu",
        description=None,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=None,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=ctx.author.avatar.url
    )

    for embed in embed_list:
        message = await ctx.send(embed=embed)

    for emoji in emoji_list:
        await message.add_reaction(emoji)


@bot.slash_command(
    brief='misc', description='misc command'
)
async def hellothere(inter):
    await inter.response.send_message(f'General Kenobi')


@bot.slash_command(
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
    description="get information about a specified player"
)
async def findplayer(inter, player_tag: str):
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


@bot.slash_command(
    brief='player',
    description="get information about your active player"
)
async def player(inter):
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


@bot.slash_command(
    brief='player',
    description="get information about a member's active player"
)
async def playermember(inter, user: disnake.User):
    """
        get information about a specified player

        Parameters
        ----------
        user: user to search for active player
    """

    await inter.response.defer()

    db_player_obj = db_responder.read_player_active(user.id)

    player_obj = await clash_responder.get_player(db_player_obj.player_tag, coc_client)

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


@bot.slash_command(
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


@bot.slash_command(
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


@bot.slash_command(
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


@bot.slash_command(
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


@bot.slash_command(
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


@bot.slash_command(
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


@bot.slash_command(
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


@bot.slash_command(
    brief='player',
    description='check to see what super troops you have active'
)
async def activesupertroop(inter):
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


@bot.slash_command(
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
    description="Enter a clan's tag and get a clan's information"
)
async def findclan(inter, clan_tag: str):
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


@bot.slash_command(
    brief='clan',
    description="get information about your active player's clan"
)
async def clan(inter):
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


@bot.slash_command(
    brief='clan',
    description="get information about mentioned clan"
)
async def clanmention(inter, role: disnake.Role):
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


@bot.command(
    brief='clan',
    description="clan's TH lineup"
)
async def clanlineup(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = await discord_responder.clan_leadership_verification(
        db_player_obj, ctx.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    clan_obj = verification_payload['clan_obj']

    field_dict_list = await discord_responder.clan_lineup(
        clan_obj, coc_client)

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=ctx.bot.user.avatar.url,
        title=f"{clan_obj.name} lineup",
        description=None,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=clan_obj.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=ctx.author.avatar.url
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


@bot.command(
    aliases=['warpreference'],
    brief='clan',
    description="rundown of clan member's war preference"
)
async def clanwarpreference(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = await discord_responder.clan_leadership_verification(
        db_player_obj, ctx.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    clan_obj = verification_payload['clan_obj']

    field_dict_list = await discord_responder.clan_war_preference(
        clan_obj, coc_client)

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=ctx.bot.user.avatar.url,
        title=f"{clan_obj.name} war preference",
        description=None,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=clan_obj.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=ctx.author.avatar.url
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


@bot.command(
    aliases=['donate'],
    brief='clan',
    description='Enter a troop name to see who in the clan '
                'is best suited to donate that troop.'
)
async def donation(ctx, *, unit_name):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = await discord_responder.clan_verification(
        db_player_obj, ctx.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
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
        icon_url=ctx.bot.user.avatar.url,
        title=f"{clan_obj.name} {clan_obj.tag}",
        description=None,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=clan_obj.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=ctx.author.avatar.url
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


@bot.command(
    aliases=['searchsupertroop'],
    brief='clan',
    description='Search who in the clan has a requested super troop active.'
)
async def supertroopsearch(ctx, *, unit_name):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = await discord_responder.clan_verification(
        db_player_obj, ctx.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    clan_obj = verification_payload['clan_obj']

    super_troop_obj = clash_responder.find_super_troop(
        player_obj, unit_name)
    # super troop was not found
    if not super_troop_obj:
        await ctx.send(f"{unit_name} is not a viable request")
        return

    donor_list = await clash_responder.active_super_troop_search(
        super_troop_obj, clan_obj, coc_client)

    field_dict_list = discord_responder.super_troop_search(
        clan_obj, donor_list, super_troop_obj)

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=ctx.bot.user.avatar.url,
        title=f"{clan_obj.name} {clan_obj.tag}",
        description=None,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=clan_obj.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=ctx.author.avatar.url
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


@bot.command(
    aliases=['findclanuser', 'findclanmemberusers'],
    brief='clan',
    description="returns the users linked to the active player's clan",
    hidden=True
)
async def findclanusers(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(
            ctx.author.id)

    verification_payload = await discord_responder.clan_leadership_verification(
        db_player_obj, ctx.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    clan_obj = verification_payload['clan_obj']

    field_dict_list = []
    # finding the user for each member in the clan
    for member_obj in clan_obj.members:
        field_dict_list.append(discord_responder.find_user_from_tag(
            member_obj, ctx.guild.members))

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=ctx.bot.user.avatar.url,
        title=f"{clan_obj.name} linked users",
        description=None,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=clan_obj.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=ctx.author.avatar.url
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


# War
# todo warmember gets a war overview for a specific war member

@bot.command(
    aliases=['waroverview'],
    brief='war',
    description='returns an overview of the current war'
)
async def war(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = await discord_responder.war_verification(
        db_player_obj, ctx.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_info(war_obj)

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=ctx.bot.user.avatar.url,
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        description=None,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=ctx.author.avatar.url
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


@bot.command(
    brief='war',
    description='Returns the time remaining in the current war')
async def wartime(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = await discord_responder.war_verification(
        db_player_obj, ctx.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_time(war_obj)

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=ctx.bot.user.avatar.url,
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        description=None,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=ctx.author.avatar.url
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


@bot.command(
    aliases=['warnoatk'],
    brief='war',
    description='Returns a list of players that have/did not use '
                'all possible attacks in the current war'
)
async def warnoattack(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = await discord_responder.war_verification(
        db_player_obj, ctx.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_no_attack(war_obj)

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=ctx.bot.user.avatar.url,
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        description=None,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=ctx.author.avatar.url
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


@bot.command(
    aliases=['warclan', 'warstars'],
    brief='war',
    description='overview of all members in war',
    hidden=True
)
async def warclanstars(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = await discord_responder.war_leadership_verification(
        db_player_obj, ctx.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_members_overview(war_obj)

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=ctx.bot.user.avatar.url,
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        description=None,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=ctx.author.avatar.url
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


@bot.command(
    aliases=['warallatk'],
    brief='war',
    description='shows all attacks for every member',
    hidden=True
)
async def warallattacks(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = await discord_responder.war_leadership_verification(
        db_player_obj, ctx.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_all_attacks(war_obj)

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=ctx.bot.user.avatar.url,
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        description=None,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=ctx.author.avatar.url
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


@bot.command(
    brief='war',
    description='shows your member score'
)
async def warscore(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = await discord_responder.war_verification(
        db_player_obj, ctx.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_member_standing(
        war_obj, player_obj)
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=ctx.bot.user.avatar.url,
        title=f"{player_obj.name} war score",
        description=None,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=ctx.author.avatar.url
    )

    for embed in embed_list:
        await ctx.send(embed=embed)


@bot.command(
    brief='war',
    description='shows the requested member score'
)
async def warmemberscore(ctx):
    # user has not been mentioned
    if len(ctx.message.mentions) == 0:
        await ctx.send(f"you have to mention a member")
        return

    discord_member = ctx.message.mentions[0]
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(discord_member.id)

    verification_payload = await discord_responder.war_verification(
        db_player_obj, ctx.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_member_standing(
        war_obj, player_obj)
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=ctx.bot.user.avatar.url,
        title=f"{player_obj.name} war score",
        description=None,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=ctx.author.avatar.url
    )

    for embed in embed_list:
        await ctx.send(embed=embed)


@bot.command(
    brief='war',
    description='shows every member score',
    hidden=True
)
async def warclanscore(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = await discord_responder.war_leadership_verification(
        db_player_obj, ctx.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_all_member_standing(
        war_obj)
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=ctx.bot.user.avatar.url,
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        description=None,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=ctx.author.avatar.url
    )

    for embed in embed_list:
        await ctx.send(embed=embed)


@bot.command(
    brief='war',
    description='town hall lineup for war'
)
async def warlineup(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = await discord_responder.war_verification(
        db_player_obj, ctx.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    await ctx.send(discord_responder.war_lineup(war_obj))


@bot.command(
    brief='war',
    description='town hall lineup for each war member'
)
async def warmemberlineup(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = await discord_responder.war_verification(
        db_player_obj, ctx.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_member_lineup(
        war_obj)
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=ctx.bot.user.avatar.url,
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        description=None,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=ctx.author.avatar.url
    )

    for embed in embed_list:
        await ctx.send(embed=embed)


# CWL Group
# todo cwl_group overview, scoreboard, cwl_clan_noatk

@bot.command(
    aliases=['cwlgroup'],
    brief='cwlgroup',
    description='Returns the CWL group lineup',
    hidden=False
)
async def cwllineup(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = await discord_responder.cwl_group_verification(
        db_player_obj, ctx.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    cwl_group_obj = verification_payload['cwl_group_obj']

    await ctx.send(discord_responder.cwl_lineup(cwl_group_obj))


@bot.command(
    brief='cwlgroup',
    description='Lists each member and their score in CWL',
    hidden=True
)
async def cwlclanscore(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = (
        await discord_responder.cwl_group_leadership_verification(
            db_player_obj, ctx.author, coc_client))
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    cwl_group_obj = verification_payload['cwl_group_obj']

    field_dict_list = discord_responder.cwl_clan_standing(
        cwl_group_obj, player_obj.clan.tag)
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=ctx.bot.user.avatar.url,
        title=f"{player_obj.clan.name} CWL scores",
        description=None,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=ctx.author.avatar.url
    )

    for embed in embed_list:
        await ctx.send(embed=embed)


@bot.command(
    brief='cwlgroup',
    description='Lists each score you have in CWL'
)
async def cwlscore(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = await discord_responder.cwl_group_verification(
        db_player_obj, ctx.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    cwl_group_obj = verification_payload['cwl_group_obj']

    field_dict_list = discord_responder.cwl_member_standing(
        player_obj, cwl_group_obj, player_obj.clan.tag, coc_client)
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=ctx.bot.user.avatar.url,
        title=f"{player_obj.name} CWL score",
        description=None,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.league.icon,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=ctx.author.avatar.url
    )

    for embed in embed_list:
        await ctx.send(embed=embed)


@bot.command(
    aliases=['cwlclanmatescore'],
    brief='cwlgroup',
    description='Lists each score the specified member has in CWL'
)
async def cwlmemberscore(ctx):
    # user has not been mentioned
    if len(ctx.message.mentions) == 0:
        await ctx.send(f"you have to mention a member")
        return

    discord_member = ctx.message.mentions[0]
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(discord_member.id)

    verification_payload = await discord_responder.cwl_group_verification(
        db_player_obj, discord_member, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    cwl_group_obj = verification_payload['cwl_group_obj']

    field_dict_list = discord_responder.cwl_member_standing(
        cwl_group_obj, player_obj.clan.tag)
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=ctx.bot.user.avatar.url,
        title=f"{player_obj.name} CWL score",
        description=None,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.league.icon,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=ctx.author.avatar.url
    )

    for embed in embed_list:
        await ctx.send(embed=embed)


# CWL War
# todo cwlwar war_time_prep, war_overview_prep, war_overview_round,

@bot.command(
    aliases=['cwlwar'],
    brief='cwlwar',
    description='Returns an overview of the current CWL war'
)
async def cwlwaroverview(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = await discord_responder.cwl_war_verification(
        db_player_obj, ctx.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    cwl_war_obj = verification_payload['cwl_war_obj']

    field_dict_list = discord_responder.war_info(
        cwl_war_obj)
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=ctx.bot.user.avatar.url,
        title=f"{cwl_war_obj.clan.name} vs. {cwl_war_obj.opponent.name}",
        description=None,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=ctx.author.avatar.url
    )

    for embed in embed_list:
        await ctx.send(embed=embed)


@bot.command(
    brief='cwlwar',
    description='Returns the time remaining in the current CWL war'
)
async def cwlwartime(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = await discord_responder.cwl_war_verification(
        db_player_obj, ctx.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    cwl_war_obj = verification_payload['cwl_war_obj']

    field_dict_list = discord_responder.war_time(
        cwl_war_obj)
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=ctx.bot.user.avatar.url,
        title=f"{cwl_war_obj.clan.name} vs. {cwl_war_obj.opponent.name}",
        description=None,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=ctx.author.avatar.url
    )

    for embed in embed_list:
        await ctx.send(embed=embed)


@bot.command(
    aliases=['cwlwarnoatk'],
    brief='cwlwar',
    description='Returns a list of players that have/did not use '
                'all possible attacks in the current CWL war'
)
async def cwlwarnoattack(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = await discord_responder.cwl_war_verification(
        db_player_obj, ctx.author, coc_client)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    cwl_war_obj = verification_payload['cwl_war_obj']

    field_dict_list = discord_responder.war_no_attack(
        cwl_war_obj)
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=ctx.bot.user.avatar.url,
        title=f"{cwl_war_obj.clan.name} vs. {cwl_war_obj.opponent.name}",
        description=None,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=ctx.author.avatar.url
    )

    for embed in embed_list:
        await ctx.send(embed=embed)


@bot.command(
    aliases=['cwlwarallatk'],
    brief='cwlwar',
    description='showing all attacks for every member in the current war',
    hidden=True
)
async def cwlwarallattack(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = (
        await discord_responder.cwl_war_leadership_verification(
            db_player_obj, ctx.author, coc_client))
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    cwl_war_obj = verification_payload['cwl_war_obj']

    field_dict_list = discord_responder.war_all_attacks(
        cwl_war_obj)
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=ctx.bot.user.avatar.url,
        title=f"{cwl_war_obj.clan.name} vs. {cwl_war_obj.opponent.name}",
        description=None,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.clan.badge,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=ctx.author.avatar.url
    )

    for embed in embed_list:
        await ctx.send(embed=embed)


# Discord

@bot.command(
    aliases=['mentionraz'],
    brief='testing',
    description=('This will send a message to mention Razgriz'),
    hidden=True
)
async def mentionrazgriz(ctx):
    field_dict_list = []
    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=ctx.bot.user.avatar.url,
        title=f"mention testing",
        description=None,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail={'small': "https://i.imgur.com/JBt2Kwt.gif"},
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=ctx.author.avatar.url
    )

    for embed in embed_list:
        await ctx.send(embed=embed)


@bot.command(
    aliases=['emoji'],
    brief='testing',
    description=('emoji testing'),
    hidden=True
)
async def emojitesting(ctx):
    await ctx.send(f"this is currently not in use, only for emoji testing")


@bot.command(
    aliases=['roleme'],
    brief='discord',
    description=('this will give you your clan role '
                 'here in Discord')
)
async def role(ctx):
    async with ctx.typing():
        db_guild_obj = db_responder.read_guild(ctx.guild.id)

    # if guild is not claimed
    if not db_guild_obj:
        await ctx.send(f"{ctx.guild.name} has not been claimed")
        return

    # setting disord_user_obj to author
    discord_user_obj = ctx.author

    db_player_obj_list = db_responder.read_player_list(discord_user_obj.id)
    # if player is not claimed
    if len(db_player_obj_list) == 0:
        field_dict_list = [{
            "name": f"no claimed players",
            "value": f"{discord_user_obj.mention}"
        }]

        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=f"{discord_user_obj.display_name}",
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=field_dict_list,
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    # getting a list of all claimed players
    player_obj_list = []
    for db_obj in db_player_obj_list:
        player_obj = await clash_responder.get_player(
            db_obj.player_tag, coc_client)
        if player_obj:
            player_obj_list.append(player_obj)
        # player was not found from tag
        else:
            await ctx.send(f"couldn't find player from tag "
                           f"{db_obj.player_tag}")
            return

    # get needed roles
    needed_role_list = []
    for player_obj in player_obj_list:
        # claimed clan validation
        db_clan_obj = db_responder.read_clan(ctx.guild.id, player_obj.clan.tag)
        # clan not found
        if not db_clan_obj:
            field_dict_list = [{
                "name": f"{player_obj.clan.name} {player_obj.clan.tag}",
                "value": f"not claimed in {ctx.guild.name} server"
            }]

            embed_list = discord_responder.embed_message(
                Embed=disnake.Embed,
                color=disnake.Color(client_data.embed_color),
                icon_url=ctx.bot.user.avatar.url,
                title=f"{discord_user_obj.display_name} {player_obj.name}",
                description=None,
                bot_prefix=ctx.prefix,
                bot_user_name=ctx.bot.user.name,
                thumbnail=player_obj.league.icon,
                field_list=field_dict_list,
                image_url=None,
                author_display_name=ctx.author.display_name,
                author_avatar_url=ctx.author.avatar.url
            )
            for embed in embed_list:
                await ctx.send(embed=embed)

            continue

        # get discord clan and rank roles
        db_clan_role_obj = db_responder.read_clan_role_from_tag(
            ctx.guild.id, player_obj.clan.tag)
        db_rank_role_obj = (db_responder.read_rank_role_from_guild_and_clash(
            ctx.guild.id, player_obj.role.value))

        if not db_clan_role_obj and not db_rank_role_obj:
            field_dict_list = [{
                "name": f"clan and rank roles not claimed",
                "value": f"please claim proper roles"
            }]

            embed_list = discord_responder.embed_message(
                Embed=disnake.Embed,
                color=disnake.Color(client_data.embed_color),
                icon_url=ctx.bot.user.avatar.url,
                title=f"{discord_user_obj.display_name} {player_obj.name}",
                description=None,
                bot_prefix=ctx.prefix,
                bot_user_name=ctx.bot.user.name,
                thumbnail=player_obj.league.icon,
                field_list=field_dict_list,
                image_url=None,
                author_display_name=ctx.author.display_name,
                author_avatar_url=ctx.author.avatar.url
            )
            for embed in embed_list:
                await ctx.send(embed=embed)

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
            ctx.guild.id, "uninitiated"
        )
        if uninitiated_role:
            needed_role_list.append(uninitiated_role.discord_role_id)

    # get rid of duplicates
    needed_role_list = list(dict.fromkeys(needed_role_list))

    # get current roles
    current_discord_role_list = []
    for current_role in discord_user_obj.roles:
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

    add_role_id_list, remove_role_id_list = discord_responder.role_add_remove_list(
        needed_role_list, current_role_list)

    # get objects of roles to add from id's
    add_role_obj_list = []
    for add_role_id in add_role_id_list:
        # returns None if role is not found
        add_role_obj = disnake.utils.get(ctx.guild.roles, id=add_role_id)
        # role was found in guild.roles
        if add_role_obj:
            add_role_obj_list.append(add_role_obj)
        else:
            await ctx.send(
                f"could not find role for id {add_role_id}, "
                f"please ensure claimed roles and discord roles match"
            )

    # get objects of roles to remove from id's
    remove_role_obj_list = []
    for remove_role_id in remove_role_id_list:
        # returns None if role is not found
        remove_role_obj = disnake.utils.get(
            ctx.guild.roles, id=remove_role_id)
        if remove_role_obj:
            # role was found in guild.roles
            remove_role_obj_list.append(remove_role_obj)
        else:
            await ctx.send(
                f"could not find role for id {remove_role_id}, "
                f"please ensure claimed roles and discord roles match"
            )

    # add roles
    for add_role_obj in add_role_obj_list:
        await discord_user_obj.add_roles(add_role_obj)

    # remove roles
    for remove_role_obj in remove_role_obj_list:
        await discord_user_obj.remove_roles(remove_role_obj)

    # no roles added or removed
    if len(add_role_obj_list) == 0 and len(remove_role_obj_list) == 0:
        field_dict_list = [{
            "name": f"no roles changed",
            "value": f"{discord_user_obj.mention}"
        }]

        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=f"{discord_user_obj.display_name}",
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=field_dict_list,
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)

    # roles have been added or removed
    else:
        field_dict_list = []

        # adding makeshift title
        field_dict_list.append({
            "name": f"roles changed",
            "value": discord_user_obj.mention,
            "inline": True
        })

        # adding added roles to field dict list
        for role in add_role_obj_list:
            field_dict_list.append({
                "name": f"added role",
                "value": role.name
            })

        # adding removed roles to field dict list
        for role in remove_role_obj_list:
            field_dict_list.append({
                "name": f"removed role",
                "value": role.name
            })

        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=f"{discord_user_obj.display_name}",
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=field_dict_list,
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)


# usable by leader and co leader
@bot.command(
    aliases=['roleplayer'],
    brief='discord',
    description=('this will role the mentioned user'),
    hidden=True
)
async def rolemember(ctx):
    if len(ctx.message.mentions) == 0:
        # user has not been mentioned
        await ctx.send(f"you have to mention a member")
        return

    async with ctx.typing():
        db_guild_obj = db_responder.read_guild(ctx.guild.id)

    # if guild is not claimed
    if not db_guild_obj:
        await ctx.send(f"{ctx.guild.name} has not been claimed")
        return

    # getting author's db player obj for leadership verification
    db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = await discord_responder.player_leadership_verification(
        db_player_obj, ctx.author, coc_client)

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=None,
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']

    # setting disord_user_obj to mentioned user
    discord_user_obj = ctx.message.mentions[0]

    db_player_obj_list = db_responder.read_player_list(discord_user_obj.id)
    # if player is not claimed
    if len(db_player_obj_list) == 0:
        field_dict_list = [{
            "name": f"no claimed players",
            "value": f"{discord_user_obj.mention}"
        }]

        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=f"{discord_user_obj.display_name}",
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=field_dict_list,
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    # getting a list of all claimed players
    player_obj_list = []
    for db_obj in db_player_obj_list:
        player_obj = await clash_responder.get_player(
            db_obj.player_tag, coc_client)
        if player_obj:
            player_obj_list.append(player_obj)
        # player was not found from tag
        else:
            await ctx.send(f"couldn't find player from tag "
                           f"{db_obj.player_tag}")
            return

    # get needed roles
    needed_role_list = []
    for player_obj in player_obj_list:
        # claimed clan validation
        db_clan_obj = db_responder.read_clan(ctx.guild.id, player_obj.clan.tag)
        # clan not found
        if not db_clan_obj:
            field_dict_list = [{
                "name": f"{player_obj.clan.name} {player_obj.clan.tag}",
                "value": f"not claimed in {ctx.guild.name} server"
            }]

            embed_list = discord_responder.embed_message(
                Embed=disnake.Embed,
                color=disnake.Color(client_data.embed_color),
                icon_url=ctx.bot.user.avatar.url,
                title=f"{discord_user_obj.display_name} {player_obj.name}",
                description=None,
                bot_prefix=ctx.prefix,
                bot_user_name=ctx.bot.user.name,
                thumbnail=player_obj.league.icon,
                field_list=field_dict_list,
                image_url=None,
                author_display_name=ctx.author.display_name,
                author_avatar_url=ctx.author.avatar.url
            )
            for embed in embed_list:
                await ctx.send(embed=embed)

            continue

        # get discord clan and rank roles
        db_clan_role_obj = db_responder.read_clan_role_from_tag(
            ctx.guild.id, player_obj.clan.tag)
        db_rank_role_obj = (db_responder.read_rank_role_from_guild_and_clash(
            ctx.guild.id, player_obj.role.value))

        if not db_clan_role_obj and not db_rank_role_obj:
            field_dict_list = [{
                "name": f"clan and rank roles not claimed",
                "value": f"please claim proper roles"
            }]

            embed_list = discord_responder.embed_message(
                Embed=disnake.Embed,
                color=disnake.Color(client_data.embed_color),
                icon_url=ctx.bot.user.avatar.url,
                title=f"{discord_user_obj.display_name} {player_obj.name}",
                description=None,
                bot_prefix=ctx.prefix,
                bot_user_name=ctx.bot.user.name,
                thumbnail=player_obj.league.icon,
                field_list=field_dict_list,
                image_url=None,
                author_display_name=ctx.author.display_name,
                author_avatar_url=ctx.author.avatar.url
            )
            for embed in embed_list:
                await ctx.send(embed=embed)

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
            ctx.guild.id, "uninitiated"
        )
        if uninitiated_role:
            needed_role_list.append(uninitiated_role.discord_role_id)

    # get rid of duplicates
    needed_role_list = list(dict.fromkeys(needed_role_list))

    # get current roles
    current_discord_role_list = []
    for current_role in discord_user_obj.roles:
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

    add_role_id_list, remove_role_id_list = discord_responder.role_add_remove_list(
        needed_role_list, current_role_list)

    # get objects of roles to add from id's
    add_role_obj_list = []
    for add_role_id in add_role_id_list:
        # returns None if role is not found
        add_role_obj = disnake.utils.get(ctx.guild.roles, id=add_role_id)
        if add_role_obj:
            # role was found in guild.roles
            add_role_obj_list.append(add_role_obj)
        else:
            await ctx.send(
                f"could not find role for id {add_role_id}, "
                f"please ensure claimed roles and discord roles match"
            )

    # get objects of roles to remove from id's
    remove_role_obj_list = []
    for remove_role_id in remove_role_id_list:
        # returns None if role is not found
        remove_role_obj = disnake.utils.get(
            ctx.guild.roles, id=remove_role_id)
        if remove_role_obj:
            # role was found in guild.roles
            remove_role_obj_list.append(remove_role_obj)
        else:
            await ctx.send(
                f"could not find role for id {remove_role_id}, "
                f"please ensure claimed roles and discord roles match"
            )

    # add roles
    for add_role_obj in add_role_obj_list:
        await discord_user_obj.add_roles(add_role_obj)

    # remove roles
    for remove_role_obj in remove_role_obj_list:
        await discord_user_obj.remove_roles(remove_role_obj)

    # no roles added or removed
    if len(add_role_obj_list) == 0 and len(remove_role_obj_list) == 0:
        field_dict_list = [{
            "name": f"no roles changed",
            "value": f"{discord_user_obj.mention}"
        }]

        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=f"{discord_user_obj.display_name}",
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=field_dict_list,
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)

    # roles have been added or removed
    else:
        field_dict_list = []

        # adding makeshift title
        field_dict_list.append({
            "name": f"roles changed",
            "value": discord_user_obj.mention,
            "inline": True
        })

        # adding added roles to field dict list
        for role in add_role_obj_list:
            field_dict_list.append({
                "name": f"added role",
                "value": role.name
            })

        # adding removed roles to field dict list
        for role in remove_role_obj_list:
            field_dict_list.append({
                "name": f"removed role",
                "value": role.name
            })

        embed_list = discord_responder.embed_message(
            Embed=disnake.Embed,
            color=disnake.Color(client_data.embed_color),
            icon_url=ctx.bot.user.avatar.url,
            title=f"{discord_user_obj.display_name}",
            description=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=field_dict_list,
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=ctx.author.avatar.url
        )
        for embed in embed_list:
            await ctx.send(embed=embed)


@bot.command(
    aliases=['roleguild'],
    brief='discord',
    description=('this will role all members in the guild'),
    hidden=True
)
async def roleall(ctx):
    async with ctx.typing():
        db_guild_obj = db_responder.read_guild(ctx.guild.id)

    if not db_guild_obj:
        # if guild is not claimed
        await ctx.send(f"{ctx.guild.name} has not been claimed")
        return

    async with ctx.typing():
        db_user_obj = db_responder.read_user(ctx.author.id)

    # if user is not claimed
    if not db_user_obj:
        await ctx.send(f"{ctx.author.mention} has not been claimed")
        return

    # if author is not guild admin and is not super user
    if (not db_guild_obj.admin_user_id == ctx.author.id
            and not db_user_obj.super_user):

        await ctx.send(f"{ctx.author.mention} is not guild's admin")
        return

    for discord_user_obj in ctx.guild.members:
        if discord_user_obj.bot:
            continue

        async with ctx.typing():
            db_player_obj_list = db_responder.read_player_list(
                discord_user_obj.id)

        # if player is not claimed
        if len(db_player_obj_list) == 0:
            field_dict_list = [{
                "name": f"no claimed players",
                "value": f"{discord_user_obj.mention}"
            }]

            embed_list = discord_responder.embed_message(
                Embed=disnake.Embed,
                color=disnake.Color(client_data.embed_color),
                icon_url=ctx.bot.user.avatar.url,
                title=f"{discord_user_obj.display_name}",
                description=None,
                bot_prefix=ctx.prefix,
                bot_user_name=ctx.bot.user.name,
                thumbnail=None,
                field_list=field_dict_list,
                image_url=None,
                author_display_name=ctx.author.display_name,
                author_avatar_url=ctx.author.avatar.url
            )
            for embed in embed_list:
                await ctx.send(embed=embed)
            continue

        # getting a list of all claimed players
        player_obj_list = []
        for db_obj in db_player_obj_list:
            player_obj = await clash_responder.get_player(
                db_obj.player_tag, coc_client)
            if player_obj:
                player_obj_list.append(player_obj)
            # player was not found from tag
            else:
                await ctx.send(f"couldn't find player from tag "
                               f"{db_obj.player_tag}")
                continue

        # get needed roles
        needed_role_list = []
        for player_obj in player_obj_list:
            # claimed clan validation
            db_clan_obj = db_responder.read_clan(
                ctx.guild.id, player_obj.clan.tag)
            # clan not found
            if not db_clan_obj:
                field_dict_list = [{
                    "name": f"{player_obj.clan.name} {player_obj.clan.tag}",
                    "value": f"not claimed in {ctx.guild.name} server"
                }]

                embed_list = discord_responder.embed_message(
                    Embed=disnake.Embed,
                    color=disnake.Color(client_data.embed_color),
                    icon_url=ctx.bot.user.avatar.url,
                    title=f"{discord_user_obj.display_name} {player_obj.name}",
                    description=None,
                    bot_prefix=ctx.prefix,
                    bot_user_name=ctx.bot.user.name,
                    thumbnail=player_obj.league.icon,
                    field_list=field_dict_list,
                    image_url=None,
                    author_display_name=ctx.author.display_name,
                    author_avatar_url=ctx.author.avatar.url
                )
                for embed in embed_list:
                    await ctx.send(embed=embed)

                continue

            # get discord clan and rank roles
            db_clan_role_obj = db_responder.read_clan_role_from_tag(
                ctx.guild.id, player_obj.clan.tag)
            db_rank_role_obj = (db_responder.read_rank_role_from_guild_and_clash(
                ctx.guild.id, player_obj.role.value))

            if not db_clan_role_obj and not db_rank_role_obj:
                field_dict_list = [{
                    "name": f"clan and rank roles not claimed",
                    "value": f"please claim proper roles"
                }]

                embed_list = discord_responder.embed_message(
                    Embed=disnake.Embed,
                    color=disnake.Color(client_data.embed_color),
                    icon_url=ctx.bot.user.avatar.url,
                    title=f"{discord_user_obj.display_name} {player_obj.name}",
                    description=None,
                    bot_prefix=ctx.prefix,
                    bot_user_name=ctx.bot.user.name,
                    thumbnail=player_obj.league.icon,
                    field_list=field_dict_list,
                    image_url=None,
                    author_display_name=ctx.author.display_name,
                    author_avatar_url=ctx.author.avatar.url
                )
                for embed in embed_list:
                    await ctx.send(embed=embed)

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
                ctx.guild.id, "uninitiated"
            )
            if uninitiated_role:
                needed_role_list.append(uninitiated_role.discord_role_id)

        # get rid of duplicates
        needed_role_list = list(dict.fromkeys(needed_role_list))

        # get current roles
        current_discord_role_list = []
        for current_role in discord_user_obj.roles:
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

        add_role_id_list, remove_role_id_list = discord_responder.role_add_remove_list(
            needed_role_list, current_role_list)

        # get objects of roles to add from id's
        add_role_obj_list = []
        for add_role_id in add_role_id_list:
            # returns None if role is not found
            add_role_obj = disnake.utils.get(ctx.guild.roles, id=add_role_id)
            if add_role_obj:
                # role was found in guild.roles
                add_role_obj_list.append(add_role_obj)
            else:
                await ctx.send(
                    f"could not find role for id {add_role_id}, "
                    f"please ensure claimed roles and discord roles match"
                )

        # get objects of roles to remove from id's
        remove_role_obj_list = []
        for remove_role_id in remove_role_id_list:
            # returns None if role is not found
            remove_role_obj = disnake.utils.get(
                ctx.guild.roles, id=remove_role_id)
            if remove_role_obj:
                # role was found in guild.roles
                remove_role_obj_list.append(remove_role_obj)
            else:
                await ctx.send(
                    f"could not find role for id {remove_role_id}, "
                    f"please ensure claimed roles and discord roles match"
                )

        # add roles
        for add_role_obj in add_role_obj_list:
            await discord_user_obj.add_roles(add_role_obj)

        # remove roles
        for remove_role_obj in remove_role_obj_list:
            await discord_user_obj.remove_roles(remove_role_obj)

        # no roles added or removed
        if len(add_role_obj_list) == 0 and len(remove_role_obj_list) == 0:
            field_dict_list = [{
                "name": f"no roles changed",
                "value": f"{discord_user_obj.mention}"
            }]

            embed_list = discord_responder.embed_message(
                Embed=disnake.Embed,
                color=disnake.Color(client_data.embed_color),
                icon_url=ctx.bot.user.avatar.url,
                title=f"{discord_user_obj.display_name}",
                description=None,
                bot_prefix=ctx.prefix,
                bot_user_name=ctx.bot.user.name,
                thumbnail=None,
                field_list=field_dict_list,
                image_url=None,
                author_display_name=ctx.author.display_name,
                author_avatar_url=ctx.author.avatar.url
            )
            for embed in embed_list:
                await ctx.send(embed=embed)

        # roles have been added or removed
        else:
            field_dict_list = []

            # adding makeshift title
            field_dict_list.append({
                "name": f"roles changed",
                "value": discord_user_obj.mention,
                "inline": True
            })

            # adding added roles to field dict list
            for role in add_role_obj_list:
                field_dict_list.append({
                    "name": f"added role",
                    "value": role.name
                })

            # adding removed roles to field dict list
            for role in remove_role_obj_list:
                field_dict_list.append({
                    "name": f"removed role",
                    "value": role.name
                })

            embed_list = discord_responder.embed_message(
                Embed=disnake.Embed,
                color=disnake.Color(client_data.embed_color),
                icon_url=ctx.bot.user.avatar.url,
                title=f"{discord_user_obj.display_name}",
                description=None,
                bot_prefix=ctx.prefix,
                bot_user_name=ctx.bot.user.name,
                thumbnail=None,
                field_list=field_dict_list,
                image_url=None,
                author_display_name=ctx.author.display_name,
                author_avatar_url=ctx.author.avatar.url
            )
            for embed in embed_list:
                await ctx.send(embed=embed)


# CLIENT

# client user
@bot.command(
    aliases=['claim_user', 'userclaim'],
    brief='client',
    description=(
        'This will claim a discord user')
)
async def claimuser(ctx):
    async with ctx.typing():
        user = db_responder.claim_user(ctx.author.id)
    # if user wasn't claimed and now is
    if user:
        await ctx.send(f"{ctx.author.mention} is now claimed")
    # if user was already claimed
    else:
        await ctx.send(f"{ctx.author.mention} has already been claimed")


# client player
@bot.command(
    aliases=['playerclaim'],
    brief='client',
    description=(
        "This will verify and claim a player, "
        "a player must be claimed to view and run "
        "many of ClashDiscord commands"
    )
)
async def claimplayer(ctx, player_tag, *, api_key):
    async with ctx.typing():
        # confirm valid player_tag
        player_obj = await clash_responder.get_player(
            player_tag, coc_client)

    # player tag was not valid
    if not player_obj:
        await ctx.send(f"player with tag {player_tag} was not found")
        return

    # confirm user has been claimed
    db_user_obj = db_responder.read_user(ctx.author.id)
    if not db_user_obj:
        # user has not been claimed
        db_user_obj = db_responder.claim_user(ctx.author.id)
        if not db_user_obj:
            # user could not be claimed
            await ctx.send(f"{ctx.author.mention} "
                           f"user couldn't be claimed")
            return

    # confirm player has not been claimed
    db_player_obj = db_responder.read_player_from_tag(player_obj.tag)
    # player has already been claimed
    if db_player_obj:
        await ctx.send(f"{player_obj.name} {player_obj.tag} "
                       f"has already been claimed")
        return

    # authenticate player api key
    player_verified = await clash_responder.verify_token(
        api_key, player_obj.tag, coc_client)
    # api key could not be verified
    if not player_verified:
        await ctx.send(f"verification for "
                       f"player tag {player_obj.tag} has failed")
        return

    # user claimed
    # player is valid
    # player hasn't been claimed
    # player is authenticated
    db_player_obj = db_responder.claim_player(
        ctx.author.id, player_obj.tag)

    if db_player_obj:
        # if succesfully claimed
        await ctx.send(f"{player_obj.name} {player_obj.tag} "
                       f"is now claimed by {ctx.author.mention}")
    else:
        # if failed to claim
        await ctx.send(
            f"Could not claim {player_obj.name} "
            f"{player_obj.tag} for {ctx.author.mention}"
        )


@bot.command(
    aliases=['showplayers', 'showclaimedplayers',
             'showplayersclaim', 'showplayerlist'],
    brief='client',
    description=(
        'Shows players claimed by a discord user')
)
async def showplayerclaim(ctx):
    async with ctx.typing():
        db_player_obj_list = db_responder.read_player_list(ctx.author.id)

    # user has no claimed players
    if len(db_player_obj_list) == 0:
        await ctx.send(f"{ctx.author.mention} does not have any "
                       f"claimed players")
        return

    message = f"{ctx.author.mention} has claimed "
    for db_player_obj in db_player_obj_list:
        player_obj = await clash_responder.get_player(
            db_player_obj.player_tag, coc_client)
        if db_player_obj.active:
            message += f"{player_obj.name} {player_obj.tag} (active), "
        else:
            message += f"{player_obj.name} {player_obj.tag}, "
    # cuts the last two characters from the string ', '
    message = message[:-2]
    await ctx.send(message)


@bot.command(
    aliases=['updateactiveplayer', 'updateplayer'],
    brief='client',
    description=(
        "updates the user's active player")
)
async def updateplayeractive(ctx, player_tag):
    async with ctx.typing():
        player_obj = await clash_responder.get_player(player_tag, coc_client)

    # if player with tag not found
    if not player_obj:
        await ctx.send(f"player with tag {player_tag} not found")
        return

    db_player_obj = db_responder.read_player(ctx.author.id, player_obj.tag)

    # if requested player is not claimed
    if not db_player_obj:
        await ctx.send(f"{ctx.author.mention} "
                       f"has not claimed "
                       f"{player_obj.name} {player_obj.tag}")
        return

    # if requested player is the active player
    if db_player_obj.active:
        await ctx.send(f"{player_obj.name} {player_obj.tag} "
                       f"is already your active player "
                       f"{ctx.author.mention}")
        return

    else:
        db_player_obj = db_responder.update_player_active(
            ctx.author.id, player_obj.tag)
        await ctx.send(f"{player_obj.name} {player_obj.tag} is now "
                       f"your active player {ctx.author.mention}")
        return


@bot.command(
    aliases=['removeplayer'],
    brief='client',
    description=(
        "deletes the user's requested player claim")
)
async def deleteplayer(ctx, player_tag):
    async with ctx.typing():
        player_obj = await clash_responder.get_player(
            player_tag, coc_client)

    # player not found
    if not player_obj:
        await ctx.send(f"player with tag {player_tag} not found")
        return

    db_player_obj = db_responder.read_player(ctx.author.id, player_obj.tag)

    # db player not found
    if not db_player_obj:
        await ctx.send(f"{player_obj.name} {player_obj.tag} "
                       f"is not claimed by {ctx.author.mention}")
        return

    db_del_player_obj = db_responder.delete_player(
        ctx.author.id, player_obj.tag)

    # player was not deleted
    if db_del_player_obj:
        await ctx.send(f"{player_obj.name} {player_obj.tag} "
                       f"could not be deleted "
                       f"from {ctx.author.mention} player list")
        return

    db_active_player_obj = db_responder.read_player_active(ctx.author.id)

    # active player found
    # no need to change the active player
    if db_active_player_obj:
        await ctx.send(f"{player_obj.name} {player_obj.tag} "
                       f"has been deleted "
                       f"from {ctx.author.mention} player list")
        return

    # no active player found
    # check if there are any other players
    db_player_obj_list = db_responder.read_player_list(
        ctx.author.id)

    # no additional players claimed
    if len(db_player_obj_list) == 0:
        await ctx.send(
            f"{player_obj.name} {player_obj.tag} "
            f"has been deleted, "
            f"{ctx.author.mention} has no more claimed players"
        )
        return

    # additional players claimed by user
    # update the first as the new active
    db_updated_player_obj = db_responder.update_player_active(
        ctx.author.id, db_player_obj_list[0].player_tag)

    # update not successful
    if not db_updated_player_obj:
        await ctx.send(
            f"{player_obj.name} {player_obj.tag} "
            f"has been deleted, could not update active player, "
            f"{ctx.author.mention} has no active players"
        )
        return

    # update was successful
    clash_updated_player_obj = await clash_responder.get_player(
        db_updated_player_obj.player_tag, coc_client)

    # clash player not found
    if not clash_updated_player_obj:
        await ctx.send(
            f"{player_obj.name} {player_obj.tag} "
            f"has been deleted, "
            f"{ctx.author.mention} active is now set to "
            f"{db_updated_player_obj.player_tag}, "
            f"could not find player in clash of clans"
        )
        return

    # player deleted
    # active player updated
    # clash player found
    await ctx.send(
        f"{player_obj.name} {player_obj.tag} "
        f"has been deleted, "
        f"{ctx.author.mention} active is now set to "
        f"{clash_updated_player_obj.name} "
        f"{clash_updated_player_obj.tag}"
    )


# client guild
@bot.command(
    aliases=['claim_guild', 'guildclaim'],
    brief='client',
    description=(
        'This will claim a discord guild'),
    hidden=True
)
async def claimguild(ctx):
    async with ctx.typing():
        # getting db user object
        db_user_obj = db_responder.read_user(ctx.author.id)

    # user not found
    if not db_user_obj:
        await ctx.send(f"{ctx.author.mention} has not been claimed")
        return

    db_guild_obj = db_responder.claim_guild(ctx.author.id, ctx.guild.id)

    # guild already claimed or could not be claimed
    if not db_guild_obj:
        await ctx.send(f"{ctx.guild.name} has already been claimed")
        return

    await ctx.send(f"{ctx.guild.name} is now claimed "
                   f"by admin user {ctx.author.mention}")


# client clan
# todo pull the clan tag from the db player to player tag to player.clan.tag
@bot.command(
    aliases=['clanclaim'],
    brief='client',
    description=(
        'This will claim the clan your '
        'active player is currently a member of'),
    hidden=True
)
async def claimclan(ctx, clan_tag):
    async with ctx.typing():
        clan_obj = await clash_responder.get_clan(clan_tag, coc_client)

    # clan not found
    if not clan_obj:
        await ctx.send(f"couldn't find clan {clan_tag}")
        return

    claimed_clan_obj = db_responder.read_clan(ctx.guild.id, clan_obj.tag)

    # already claimed
    if claimed_clan_obj:
        await ctx.send(f"{clan_obj.name} has already been claimed for "
                       f"{ctx.guild.name}")
        return

    db_user_obj = db_responder.read_user(ctx.author.id)

    # user not claimed
    if not db_user_obj:
        await ctx.send(f"{ctx.author.mention} has not been claimed")
        return

    db_guild_obj = db_responder.read_guild(ctx.guild.id)

    # guild not claimed
    if not db_guild_obj:
        await ctx.send(f"{ctx.guild.name} has not been claimed")
        return

    # user is not guild admin and is not super user
    if (not db_guild_obj.admin_user_id == ctx.author.id
            and not db_user_obj.super_user):
        await ctx.send(f"{ctx.author.mention} is not guild's admin")
        return

    db_player_obj_list = db_responder.read_player_list(ctx.author.id)

    # no claimed player
    if len(db_player_obj_list) == 0:
        await ctx.send(f"{ctx.author.mention} has no claimed players")
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
        await ctx.send(f"{ctx.author.mention} is not in {clan_obj.name}")
        return

    db_clan_obj = db_responder.claim_clan(ctx.guild.id, clan_obj.tag)

    # clan not claimed
    if not db_clan_obj:
        await ctx.send(f"couldn't claim {clan_obj.name}")
        return

    await ctx.send(f"{clan_obj.name} has been claimed")


@bot.command(
    aliases=['showclaimclan', 'showclaimedclan',
             'showclaimedclans', 'showclansclaim', 'showclanlist'],
    brief='client',
    description=(
        'Shows clans claimed by a discord guild'),
    hidden=True
)
async def showclanclaim(ctx):
    async with ctx.typing():
        db_guild_obj = db_responder.read_guild(ctx.guild.id)

    # guild not found
    if not db_guild_obj:
        await ctx.send(f"{ctx.guild.name} has not been claimed")
        return

    db_clan_obj_list = db_responder.read_clan_list_from_guild(ctx.guild.id)

    # guild has no claimed clans
    if len(db_clan_obj_list) == 0:
        await ctx.send(f"{ctx.guild.name} does not have any claimed clans")
        return

    message = f"{ctx.guild.name} has claimed "
    for item in db_clan_obj_list:
        clan = await clash_responder.get_clan(
            item.clan_tag, coc_client)
        message += f"{clan.name} {clan.tag}, "

    # cuts the last two characters from the string ', '
    message = message[:-2]

    await ctx.send(message)


@bot.command(
    aliases=['removeclan', 'deleteclanclaim',
             'deleteclaimclan', 'deleteclaimedclan'],
    brief='client',
    description=(
        "deletes the requested clan claim"),
    hidden=True
)
async def deleteclan(ctx, clan_tag):
    async with ctx.typing():
        clan_obj = await clash_responder.get_clan(clan_tag, coc_client)

    # clan not found
    if not clan_obj:
        await ctx.send(f"couldn't find clan {clan_tag}")
        return

    db_user_obj = db_responder.read_user(ctx.author.id)
    # user not claimed
    if not db_user_obj:
        await ctx.send(f"{ctx.author.mention} has not been claimed")
        return

    db_guild_obj = db_responder.read_guild(ctx.guild.id)
    # guild not claimed
    if not db_guild_obj:
        await ctx.send(f"{ctx.guild.name} has not been claimed")
        return

    # user is not guild admin and is not super user
    if (not db_guild_obj.admin_user_id == ctx.author.id
            and not db_user_obj.super_user):
        await ctx.send(f"{ctx.author.mention} is not guild's admin")
        return

    db_clan_obj = db_responder.read_clan(ctx.guild.id, clan_obj.tag)
    # clan not claimed by guild
    if not db_clan_obj:
        await ctx.send(f"{clan_obj.name} has not been claimed "
                       f"by {ctx.guild.name}")
        return

    db_clan_deletion = db_responder.delete_clan(ctx.guild.id, clan_obj.tag)
    # clan was found after deletion
    if db_clan_deletion:
        await ctx.send(f"{clan_obj.name} could not be deleted")
        return

    await ctx.send(f"{clan_obj.name} has been deleted from {ctx.guild.name}")


# client roles
@bot.command(
    aliases=['showroles', 'showclaimedroles'],
    brief='client',
    description=(
        'shows roles claimed by a discord guild'),
    hidden=True
)
async def showroleclaim(ctx):
    async with ctx.typing():
        db_guild_obj = db_responder.read_guild(ctx.guild.id)

    # guild not found
    if not db_guild_obj:
        await ctx.send(f"{ctx.guild.name} has not been claimed")
        return

    field_dict_list = []

    db_clan_role_list = db_responder.read_guild_clan_role(ctx.guild.id)

    # guild has no claimed clan roles
    if len(db_clan_role_list) == 0:
        field_dict_list.append({
            'name': f"server has no claimed clan roles",
            'value': f"use `claimclanrole` to claim a clan role"
        })

    else:
        for db_role in db_clan_role_list:
            discord_role = disnake.utils.get(
                ctx.guild.roles, id=db_role.discord_role_id)

            # discord role is claimed, but not found in server
            if not discord_role:
                deleted_db_role = db_responder.delete_clan_role(
                    db_role.discord_role_id)

                field_dict_list.append({
                    'name': f"clan tag {db_role.clan_tag}",
                    'value': f"role {db_role.discord_role_id} *deleted*"
                })
                continue

            clan = await clash_responder.get_clan(db_role.clan_tag, coc_client)

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

    db_rank_role_list = db_responder.read_guild_rank_role(ctx.guild.id)

    # guild has no claimed rank roles
    if len(db_rank_role_list) == 0:
        field_dict_list.append({
            'name': f"server has no claimed rank roles",
            'value': f"use `claimrankrole` to claim a rank role"
        })

    else:
        for db_role in db_rank_role_list:
            discord_role = disnake.utils.get(
                ctx.guild.roles, id=db_role.discord_role_id)

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

    embed_list = discord_responder.embed_message(
        Embed=disnake.Embed,
        color=disnake.Color(client_data.embed_color),
        icon_url=ctx.bot.user.avatar.url,
        title=f"{ctx.guild.name} claimed roles",
        description=None,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=None,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=ctx.author.avatar.url
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


# client clan role
@bot.command(
    aliases=['clanroleclaim'],
    brief='client',
    description=(
        "This will claim a clan's discord role"),
    hidden=True
)
async def claimclanrole(ctx, clan_tag):
    # role was not mentioned or more than one role mentioned
    if (len(ctx.message.role_mentions) == 0
            or len(ctx.message.role_mentions) > 1):
        await ctx.send(f"one role must be mentioned")
        return

    role = ctx.message.role_mentions[0]

    async with ctx.typing():
        clan_obj = await clash_responder.get_clan(clan_tag, coc_client)

    # clan not found
    if not clan_obj:
        await ctx.send(f"couldn't find clan {clan_tag}")
        return

    db_user_obj = db_responder.read_user(ctx.author.id)
    # user not claimed
    if not db_user_obj:
        await ctx.send(f"{ctx.author.mention} has not been claimed")
        return

    db_guild_obj = db_responder.read_guild(ctx.guild.id)
    # guild not claimed
    if not db_guild_obj:
        await ctx.send(f"{ctx.guild.name} has not been claimed")
        return

    # user is not guild admin and is not super user
    if (not db_guild_obj.admin_user_id == ctx.author.id
            and not db_user_obj.super_user):
        await ctx.send(f"{ctx.author.mention} is not guild's admin")
        return

    db_clan_obj = db_responder.read_clan(ctx.guild.id, clan_obj.tag)
    # clan not claimed by guild
    if not db_clan_obj:
        await ctx.send(f"{clan_obj.name} has not been claimed "
                       f"by {ctx.guild.name}")
        return

    # confirm clan role has not been claimed
    db_clan_role_obj = db_responder.read_clan_role(role.id)
    # clan role has been claimed
    if db_clan_role_obj:
        await ctx.send(f"{role.mention} has already been claimed "
                       f"for clan {db_clan_role_obj.clan_tag}")
        return

    # confirm rank role has not been claimed
    db_rank_role_obj = db_responder.read_rank_role(role.id)
    # rank role has been claimed
    if db_rank_role_obj:
        await ctx.send(f"{role.mention} has already been claimed "
                       f"for rank {db_rank_role_obj.model_name}")
        return

    # claim clan role
    claimed_clan_role_obj = db_responder.claim_clan_role(
        role.id, ctx.guild.id, clan_obj.tag)
    # clan role could not be claimed
    if not claimed_clan_role_obj:
        await ctx.send(f"could not claim {role.mention} "
                       f"for clan {clan_obj.tag}")
        return

    await ctx.send(
        f"{role.mention} has been claimed for clan {clan_obj.tag}")


@bot.command(
    aliases=['removeclanroleclaim'],
    brief='client',
    description=(
        "this will remove the claimed clan's discord role, "
        "the role will not be deleted from discord"),
    hidden=True
)
async def removeclaimclanrole(ctx):
    # role was not mentioned or more than one role mentioned
    if (len(ctx.message.role_mentions) == 0
            or len(ctx.message.role_mentions) > 1):
        await ctx.send(f"one role must be mentioned")
        return

    role = ctx.message.role_mentions[0]

    async with ctx.typing():
        db_user_obj = db_responder.read_user(ctx.author.id)

    # user not claimed
    if not db_user_obj:
        await ctx.send(f"{ctx.author.mention} has not been claimed")
        return

    db_guild_obj = db_responder.read_guild(ctx.guild.id)
    # guild not claimed
    if not db_guild_obj:
        await ctx.send(f"{ctx.guild.name} has not been claimed")
        return

    # user is not guild admin and is not super user
    if (not db_guild_obj.admin_user_id == ctx.author.id
            and not db_user_obj.super_user):
        await ctx.send(f"{ctx.author.mention} is not guild's admin")
        return

    db_clan_role_obj = db_responder.read_clan_role(role.id)
    # clan role not claimed
    if not db_clan_role_obj:
        await ctx.send(f"{role.mention} is not claimed")
        return

    # delete clan role
    db_clan_role_deletion = db_responder.delete_clan_role(role.id)
    # clan role found after deletion
    if db_clan_role_deletion:
        await ctx.send(f"{role.mention} claim could not be removed")
        return

    await ctx.send(f"{role.mention} claim was removed")


# client rank role
@bot.command(
    aliases=['rankroleclaim'],
    brief='client',
    description=(
        "This will claim a rank's discord role"),
    hidden=True
)
async def claimrankrole(ctx, rank_role_name):
    # role was not mentioned or more than one role mentioned
    if (len(ctx.message.role_mentions) == 0
            or len(ctx.message.role_mentions) > 1):
        await ctx.send(f"one role must be mentioned")
        return

    role = ctx.message.role_mentions[0]

    async with ctx.typing():
        # validate given role name with model
        rank_role_model_obj = db_responder.read_rank_role_model(
            rank_role_name)

    # rank role name invalid
    if not rank_role_model_obj:
        await ctx.send(f"{rank_role_name} is not a valid rank")
        return

    db_user_obj = db_responder.read_user(ctx.author.id)
    # user not claimed
    if not db_user_obj:
        await ctx.send(f"{ctx.author.mention} has not been claimed")
        return

    db_guild_obj = db_responder.read_guild(ctx.guild.id)
    # guild not claimed
    if not db_guild_obj:
        await ctx.send(f"{ctx.guild.name} has not been claimed")
        return

    # user is not guild admin and is not super user
    if (not db_guild_obj.admin_user_id == ctx.author.id
            and not db_user_obj.super_user):
        await ctx.send(f"{ctx.author.mention} is not guild's admin")
        return

    # confirm clan role has not been claimed
    db_clan_role_obj = db_responder.read_clan_role(role.id)
    # clan role has been claimed
    if db_clan_role_obj:
        await ctx.send(f"{role.mention} has already been claimed "
                       f"for clan {db_clan_role_obj.clan_tag}")
        return

    # confirm rank role has not been claimed
    db_rank_role_obj = db_responder.read_rank_role(role.id)
    # rank role has been claimed
    if db_rank_role_obj:
        await ctx.send(f"{role.mention} has already been claimed "
                       f"for rank {db_rank_role_obj.model_name}")
        return

    # claim rank role
    claimed_rank_role_obj = db_responder.claim_rank_role(
        role.id, ctx.guild.id, rank_role_name)
    # rank role could not be claimed
    if not claimed_rank_role_obj:
        await ctx.send(f"could not claim {role.mention} "
                       f"for rank {db_rank_role_obj.model_name}")
        return

    await ctx.send(f"{role.mention} has been claimed "
                   f"for rank {claimed_rank_role_obj.model_name}")


@bot.command(
    aliases=['removerankroleclaim'],
    brief='client',
    description=(
        "this will remove the claimed rank's discord role, "
        "the role will not be deleted from discord"),
    hidden=True
)
async def removeclaimrankrole(ctx):
    # role was not mentioned or more than one role mentioned
    if (len(ctx.message.role_mentions) == 0
            or len(ctx.message.role_mentions) > 1):
        await ctx.send(f"one role must be mentioned")
        return

    role = ctx.message.role_mentions[0]

    async with ctx.typing():
        db_user_obj = db_responder.read_user(ctx.author.id)

    # user not claimed
    if not db_user_obj:
        await ctx.send(f"{ctx.author.mention} has not been claimed")
        return

    db_guild_obj = db_responder.read_guild(ctx.guild.id)
    # guild not claimed
    if not db_guild_obj:
        await ctx.send(f"{ctx.guild.name} has not been claimed")
        return

    # user is not guild admin and is not super user
    if (not db_guild_obj.admin_user_id == ctx.author.id
            and not db_user_obj.super_user):
        await ctx.send(f"{ctx.author.mention} is not guild's admin")
        return

    db_rank_role_obj = db_responder.read_rank_role(role.id)
    # rank role not claimed
    if not db_rank_role_obj:
        await ctx.send(f"{role.mention} is not claimed")
        return

    # delete rank role
    db_rank_role_deletion = db_responder.delete_rank_role(role.id)
    # rank role found after deletion
    if db_rank_role_deletion:
        await ctx.send(f"{role.mention} claim could not be removed")
        return

    await ctx.send(f"{role.mention} claim was removed")


# client super user administration

# super user client guild
@bot.command(
    aliases=['removeguild'],
    brief='clientsuperuser',
    description=("delete a claimed guild from id"),
    hidden=True
)
async def removeguildclaim(ctx, guild_id):

    db_author_obj = db_responder.read_user(ctx.author.id)
    # author is not claimed
    if not db_author_obj:
        await ctx.send(f"{ctx.author.mention} is not claimed")
        return

    # author is not super user
    if not db_author_obj.super_user:
        await ctx.send(f"{ctx.author.mention} is not super user")
        return

    # confirm guild is claimed
    db_guild_obj = db_responder.read_guild(guild_id)
    # guild isn't claimed
    if not db_guild_obj:
        await ctx.send(f"guild with id {guild_id} is not claimed")
        return

    deleted_guild_obj = db_responder.delete_guild(guild_id)
    # guild could not be deleted
    if deleted_guild_obj:
        await ctx.send(f"guild with id {guild_id} could not be deleted")
        return

    # guild was deleted properly
    await ctx.send(f"guild with id {guild_id} was deleted")


# super user client user
@bot.command(
    aliases=['removeuser'],
    brief='clientsuperuser',
    description=('delete a claimed user'),
    hidden=True
)
async def removeuserclaim(ctx, user_id):

    db_author_obj = db_responder.read_user(ctx.author.id)
    # author is not claimed
    if not db_author_obj:
        await ctx.send(f"{ctx.author.mention} is not claimed")
        return

    # author is not super user
    if not db_author_obj.super_user:
        await ctx.send(f"{ctx.author.mention} is not super user")
        return

    # confirm user is claimed
    db_user_obj = db_responder.read_user(user_id)
    # user isn't claimed
    if not db_user_obj:
        await ctx.send(f"user with id {user_id} is not claimed")
        return

    deleted_user_obj = db_responder.delete_user(user_id)
    # user could not be deleted
    if deleted_user_obj:
        await ctx.send(f"user with id {user_id} could not be deleted")
        return

    # user was deleted properly
    await ctx.send(f"user with id {user_id} was deleted")


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
        bot_category, client_data.bot_categories, ctx.bot.all_commands)
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
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=None,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=user.display_name,
        author_avatar_url=(user.avatar.url +
                           user.avatar_url._url)
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
        await ctx.send(f"command '{ctx.invoked_with}' could not be found")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"command '{ctx.invoked_with}' "
                       f"requires more information")
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
        await inter.send(f"command '{inter.invoked_with}' could not be found")
    elif isinstance(exception, commands.MissingRequiredArgument):
        await inter.send(f"command '{inter.invoked_with}' "
                         f"requires more information")
    elif hasattr(exception.original, "text"):
        await inter.send(f"there was an error that I have not accounted for, "
                         f"please let Razgriz know.\n\n"
                         f"error text: `{exception.original.text}`")
    elif hasattr(exception.original, "args"):
        await inter.send(f"there was an error that I have not accounted for, "
                         f"please let Razgriz know.\n\n"
                         f"error text: `{exception.original.args[0]}`")
    else:
        await inter.send(f"there was an error that I have not accounted for, "
                         f"please let Razgriz know")

bot.run(discord_responder.get_client_token())
