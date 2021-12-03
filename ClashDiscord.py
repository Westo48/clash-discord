import discord
from asyncio.tasks import sleep
from discord.ext import commands
from discord.utils import get
import RazBot_Data
import ClashDiscord_Client_Data
import ClashResponder as clash_responder
import DiscordResponder as discord_responder
import RazBotDB_Responder as db_responder

razbot_data = RazBot_Data.RazBot_Data()
client_data = ClashDiscord_Client_Data.ClashDiscord_Data()

intents = discord.Intents.all()

client = commands.Bot(
    command_prefix=razbot_data.prefix, intents=intents)
client.remove_command('help')

# todo move entry validation to modules (setting # in front of player tags)
# todo add client, admin, and super user bot categories
# had emoji id as well


@client.event
async def on_ready():
    print(f"RazBot is ready")


# todo allow leader or co-leader
# todo hide clan help if user is not in a clan
@client.command(
    aliases=['helpme'],
    brief='discord',
    description='Returns the help text you see before you'
)
async def help(ctx):
    async with ctx.typing():
        db_guild_obj = db_responder.read_guild(ctx.guild.id)
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    if db_player_obj:
        player_obj = clash_responder.get_player(
            db_player_obj.player_tag, razbot_data.header)
    else:
        player_obj = None

    help_dict = discord_responder.help_main(
        db_guild_obj, ctx.author.id, player_obj, client_data.bot_categories)
    field_dict_list = help_dict['field_dict_list']
    emoji_list = help_dict['emoji_list']

    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{ctx.bot.user.name} help menu",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=None,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )

    for embed in embed_list:
        message = await ctx.send(embed=embed)

    for emoji in emoji_list:
        await message.add_reaction(emoji)


@client.command(
    brief='misc', description='Misc Command'
)
async def hellothere(ctx):
    await ctx.send(f'General Kenobi')


@client.command(
    brief='misc'
)
async def ping(ctx):
    # try typing to not cause error if discord typing is down
    try:
        async with ctx.typing():
            pass
    except:
        pass
    await ctx.send(f'pong {round(ctx.bot.latency, 3) * 1000}ms')


# Player

@client.command(
    aliases=['searchplayer'],
    brief='player',
    description="get information about a specified player"
)
async def findplayer(ctx, *, player_tag):
    async with ctx.typing():
        player_obj = clash_responder.get_player(
            player_tag, razbot_data.header)

    if not player_obj:
        # player with given tag not found
        await ctx.send(f"could not find player with tag {player_tag}")
        return

    field_dict_list = discord_responder.player_info(player_obj)

    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=player_obj.name,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.league_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )

    for embed in embed_list:
        await ctx.send(embed=embed)


@client.command(
    aliases=['showplayer', 'showactiveplayer', 'activeplayer'],
    brief='player',
    description="get information about your active player"
)
async def player(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = discord_responder.player_verification(
        db_player_obj, ctx.author, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']

    field_dict_list = discord_responder.player_info(player_obj)

    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=player_obj.name,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.league_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )

    for embed in embed_list:
        await ctx.send(embed=embed)


@client.command(
    aliases=['showmemberplayer', 'showmemberactiveplayer', 'memberplayer'],
    brief='player',
    description="get information about a member's active player"
)
async def playermember(ctx):
    if len(ctx.message.mentions) == 0:
        # user has not been mentioned
        await ctx.send(f"you have to mention a member")
        return

    # user has been mentioned
    discord_member = ctx.message.mentions[0]
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(discord_member.id)

    verification_payload = discord_responder.player_verification(
        db_player_obj, discord_member, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']

    field_dict_list = discord_responder.player_info(player_obj)

    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=player_obj.name,
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.league_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )

    for embed in embed_list:
        await ctx.send(embed=embed)


@client.command(
    aliases=['trooplvl'],
    brief='player',
    description='get level information for a specified unit'
)
async def unitlvl(ctx, *, unit_name):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = discord_responder.player_verification(
        db_player_obj, ctx.author, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']

    unit_obj = clash_responder.find_unit(player_obj, unit_name)
    field_dict_list = [discord_responder.unit_lvl(
        player_obj, unit_obj, unit_name)]
    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{player_obj.name} {unit_obj.name}",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.league_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


@client.command(
    brief='player',
    description='get all your unit levels',
    hidden=True
)
async def allunitlvl(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = discord_responder.player_verification(
        db_player_obj, ctx.author, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']

    field_dict_list = discord_responder.unit_lvl_all(player_obj)
    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{player_obj.name} units",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.league_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


@client.command(
    brief='player',
    description='get all your hero levels',
    hidden=True
)
async def allherolvl(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = discord_responder.player_verification(
        db_player_obj, ctx.author, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']

    field_dict_list = discord_responder.hero_lvl_all(player_obj)
    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{player_obj.name} heroes",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.league_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


@client.command(
    brief='player',
    description='get all your troop levels',
    hidden=True
)
async def alltrooplvl(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = discord_responder.player_verification(
        db_player_obj, ctx.author, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']

    field_dict_list = discord_responder.troop_lvl_all(player_obj)
    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{player_obj.name} troops",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.league_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


@client.command(
    brief='player',
    description='get all your spell levels',
    hidden=True
)
async def allspelllvl(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = discord_responder.player_verification(
        db_player_obj, ctx.author, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']

    field_dict_list = discord_responder.spell_lvl_all(player_obj)
    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{player_obj.name} spells",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.league_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


@client.command(
    aliases=['activesupertroops', 'supertroop', 'supertroops'],
    brief='player',
    description='Check to see what super troops you have active.'
)
async def activesupertroop(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = discord_responder.player_verification(
        db_player_obj, ctx.author, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']

    active_super_troops = player_obj.find_active_super_troops()

    field_dict_list = discord_responder.active_super_troops(
        player_obj, active_super_troops)
    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{player_obj.name} super troops",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.league_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


# Clan


@client.command(
    aliases=['clansearch'],
    brief='clan',
    description="Enter a clan's tag and get a clan's information"
)
async def findclan(ctx, *, clan_tag):
    async with ctx.typing():
        clan_obj = clash_responder.get_clan(clan_tag, razbot_data.header)

    if not clan_obj:
        # clan with given tag not found
        await ctx.send(f"could not find clan with tag {clan_tag}")
        return

    field_dict_list = discord_responder.clan_info(clan_obj)

    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{clan_obj.name} {clan_obj.tag}",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=clan_obj.clan_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


@client.command(
    aliases=['showclan', 'playerclan', 'showplayerclan'],
    brief='clan',
    description="Get information about your active player's clan"
)
async def clan(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = discord_responder.clan_verification(
        db_player_obj, ctx.author, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    clan_obj = verification_payload['clan_obj']

    field_dict_list = discord_responder.clan_info(clan_obj)

    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{clan_obj.name} {clan_obj.tag}",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=clan_obj.clan_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


@client.command(
    aliases=['showclanmention'],
    brief='clan',
    description="Get information about mentioned clan"
)
async def clanmention(ctx):
    if len(ctx.message.role_mentions) == 0:
        # user has not been mentioned
        await ctx.send(f"you have to mention a clan role")
        return

    # role has been mentioned
    # get clan tag from clan role
    async with ctx.typing():
        db_clan_role = db_responder.read_clan_role(
            ctx.message.role_mentions[0].id)

    if not db_clan_role:
        # role mentioned was not a linked clan role
        await ctx.send(f"role mentioned is not linked to a clan")
        return

    clan_obj = clash_responder.get_clan(
        db_clan_role.clan_tag, razbot_data.header)
    if not clan_obj:
        # clan with tag from db clan role not found
        await ctx.send(f"could not find clan with tag {db_clan_role.clan_tag}")
        return

    field_dict_list = discord_responder.clan_info(clan_obj)

    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{clan_obj.name} {clan_obj.tag}",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=clan_obj.clan_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


@client.command(
    brief='clan',
    description="clan's TH lineup"
)
async def clanlineup(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = discord_responder.clan_verification(
        db_player_obj, ctx.author, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    clan_obj = verification_payload['clan_obj']

    if not (player_obj.role == 'coLeader' or
            player_obj.role == 'leader'):
        # command can only be run by leadership
        await ctx.send(f"command can only be run by leader or co-leader")
        return

    field_dict_list = discord_responder.clan_lineup(
        clan_obj, razbot_data.header)

    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{clan_obj.name} lineup",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=clan_obj.clan_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


@client.command(
    aliases=['warpreference'],
    brief='clan',
    description="rundown of clan member's war preference"
)
async def clanwarpreference(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = discord_responder.clan_verification(
        db_player_obj, ctx.author, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    clan_obj = verification_payload['clan_obj']

    if not (player_obj.role == 'coLeader' or
            player_obj.role == 'leader'):
        # command can only be run by leadership
        await ctx.send(f"command can only be run by leader or co-leader")
        return

    field_dict_list = discord_responder.clan_war_preference(
        clan_obj, razbot_data.header)

    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{clan_obj.name} war preference",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=clan_obj.clan_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


@client.command(
    aliases=['donate'],
    brief='clan',
    description='Enter a troop name to see who in the clan '
                'is best suited to donate that troop.'
)
async def donation(ctx, *, unit_name):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = discord_responder.clan_verification(
        db_player_obj, ctx.author, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    clan_obj = verification_payload['clan_obj']

    donator_list = clash_responder.donation(
        unit_name, clan_obj, razbot_data.header)

    field_dict_list = discord_responder.donation(
        clan_obj, donator_list, unit_name)

    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{clan_obj.name} {clan_obj.tag}",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=clan_obj.clan_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


@client.command(
    aliases=['searchsupertroop'],
    brief='clan',
    description='Search who in the clan has a requested super troop active.'
)
async def supertroopsearch(ctx, *, unit_name):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = discord_responder.clan_verification(
        db_player_obj, ctx.author, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    clan_obj = verification_payload['clan_obj']

    super_troop_name = clash_responder.super_troop_unit_name(
        unit_name)
    if not super_troop_name:
        # super troop was not found
        await ctx.send(f"{unit_name} is not a viable request")
        return

    donor_list = clash_responder.active_super_troop_search(
        super_troop_name, clan_obj, razbot_data.header)

    field_dict_list = discord_responder.super_troop_search(
        clan_obj, donor_list, super_troop_name)

    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{clan_obj.name} {clan_obj.tag}",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=clan_obj.clan_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


# War
# todo warmember gets a war overview for a specific war member

@client.command(
    aliases=['war'],
    brief='war',
    description='Returns an overview of the current war'
)
async def waroverview(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = discord_responder.war_verification(
        db_player_obj, ctx.author, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_overview(war_obj)

    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.clan_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


@client.command(
    brief='war',
    description='Returns the time remaining in the current war')
async def wartime(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = discord_responder.war_verification(
        db_player_obj, ctx.author, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_time(war_obj)

    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.clan_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


@client.command(
    aliases=['warnoatk'],
    brief='war',
    description='Returns a list of players that have/did not use '
                'all possible attacks in the current war'
)
async def warnoattack(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = discord_responder.war_verification(
        db_player_obj, ctx.author, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_no_attack(war_obj)

    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.clan_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


@client.command(
    aliases=['warclan', 'warstars'],
    brief='war',
    description='overview of all members in war',
    hidden=True
)
async def warclanstars(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = discord_responder.war_leadership_verification(
        db_player_obj, ctx.author, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_members_overview(war_obj)

    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.clan_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


@client.command(
    aliases=['warallatk'],
    brief='war',
    description='showing all attacks for every member',
    hidden=True
)
async def warallattacks(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = discord_responder.war_leadership_verification(
        db_player_obj, ctx.author, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_all_attacks(war_obj)

    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.clan_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )
    for embed in embed_list:
        await ctx.send(embed=embed)


@client.command(
    aliases=['warscore'],
    brief='war',
    description='showing every member score',
    hidden=True
)
async def warclanscore(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = discord_responder.war_leadership_verification(
        db_player_obj, ctx.author, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    war_obj = verification_payload['war_obj']

    field_dict_list = discord_responder.war_all_member_standing(
        war_obj)
    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.clan_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )

    for embed in embed_list:
        await ctx.send(embed=embed)


# CWL Group
# todo cwl_group overview, scoreboard, cwl_clan_noatk

@client.command(
    aliases=['cwlgroup'],
    brief='cwlgroup',
    description='Returns the CWL group lineup',
    hidden=False
)
async def cwllineup(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)
    if not db_player_obj:
        # user does not have an active player
        await ctx.send(f"{ctx.author.mention} does not have an active player")
        return

    player_obj = clash_responder.get_player(
        db_player_obj.player_tag, razbot_data.header)
    if not player_obj:
        # player with tag from db not found
        await ctx.send(f"could not find player with tag "
                       f"{db_player_obj.player_tag}")
        return

    if not player_obj.clan_tag:
        # player is found but not in a clan
        await ctx.send(f"{player_obj.name} is not in a clan")
        return

    cwl_group = clash_responder.get_cwl_group(
        player_obj.clan_tag, razbot_data.header)
    if not cwl_group:
        # clan is not in CWL
        field_dict_list = [{
            'name': f"{player_obj.clan_name} {player_obj.clan_tag}",
            'value': f"is not in CWL"
        }]
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=f"{player_obj.clan_name} {player_obj.clan_tag}",
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=player_obj.clan_icons,
            field_list=field_dict_list,
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    await ctx.send(discord_responder.cwl_lineup(cwl_group))


@client.command(
    brief='cwlgroup',
    description='Lists each member and their score in CWL',
    hidden=True
)
async def cwlclanscore(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = discord_responder.cwl_group_leadership_verification(
        db_player_obj, ctx.author, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    cwl_group_obj = verification_payload['cwl_group_obj']

    field_dict_list = discord_responder.cwl_clan_standing(
        cwl_group_obj, player_obj.clan_tag, razbot_data.header)
    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{player_obj.clan_name} CWL scores",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.clan_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )

    for embed in embed_list:
        await ctx.send(embed=embed)


@client.command(
    brief='cwlgroup',
    description='Lists each score you have in CWL'
)
async def cwlscore(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = discord_responder.cwl_group_verification(
        db_player_obj, ctx.author, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    cwl_group_obj = verification_payload['cwl_group_obj']

    field_dict_list = discord_responder.cwl_member_standing(
        player_obj, cwl_group_obj, player_obj.clan_tag, razbot_data.header)
    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{player_obj.name} CWL score",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.league_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )

    for embed in embed_list:
        await ctx.send(embed=embed)


@client.command(
    aliases=['cwlclanmatescore'],
    brief='cwlgroup',
    description='Lists each score the specified member has in CWL'
)
async def cwlmemberscore(ctx):
    if len(ctx.message.mentions) == 0:
        # user has not been mentioned
        await ctx.send(f"you have to mention a member")
        return

    discord_member = ctx.message.mentions[0]
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(discord_member.id)

    verification_payload = discord_responder.cwl_group_verification(
        db_player_obj, discord_member, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    cwl_group_obj = verification_payload['cwl_group_obj']

    field_dict_list = discord_responder.cwl_member_standing(
        player_obj, cwl_group_obj, player_obj.clan_tag, razbot_data.header)
    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{player_obj.name} CWL score",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.league_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )

    for embed in embed_list:
        await ctx.send(embed=embed)


# CWL War
# todo cwlwar war_time_prep, war_overview_prep, war_overview_round,

@client.command(
    aliases=['cwlwar'],
    brief='cwlwar',
    description='Returns an overview of the current CWL war'
)
async def cwlwaroverview(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = discord_responder.cwl_war_verification(
        db_player_obj, ctx.author, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    cwl_war_obj = verification_payload['cwl_war_obj']

    field_dict_list = discord_responder.war_overview(
        cwl_war_obj)
    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{cwl_war_obj.clan.name} vs. {cwl_war_obj.opponent.name}",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.clan_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )

    for embed in embed_list:
        await ctx.send(embed=embed)


@client.command(
    brief='cwlwar',
    description='Returns the time remaining in the current CWL war'
)
async def cwlwartime(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = discord_responder.cwl_war_verification(
        db_player_obj, ctx.author, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    cwl_war_obj = verification_payload['cwl_war_obj']

    field_dict_list = discord_responder.war_time(
        cwl_war_obj)
    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{cwl_war_obj.clan.name} vs. {cwl_war_obj.opponent.name}",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.clan_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )

    for embed in embed_list:
        await ctx.send(embed=embed)


@client.command(
    aliases=['cwlwarnoatk'],
    brief='cwlwar',
    description='Returns a list of players that have/did not use '
                'all possible attacks in the current CWL war'
)
async def cwlwarnoattack(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = discord_responder.cwl_war_verification(
        db_player_obj, ctx.author, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    cwl_war_obj = verification_payload['cwl_war_obj']

    field_dict_list = discord_responder.war_no_attack(
        cwl_war_obj)
    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{cwl_war_obj.clan.name} vs. {cwl_war_obj.opponent.name}",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.clan_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )

    for embed in embed_list:
        await ctx.send(embed=embed)


@client.command(
    aliases=['cwlwarallatk'],
    brief='cwlwar',
    description='showing all attacks for every member in the current war',
    hidden=True
)
async def cwlwarallattack(ctx):
    async with ctx.typing():
        db_player_obj = db_responder.read_player_active(ctx.author.id)

    verification_payload = discord_responder.cwl_war_leadership_verification(
        db_player_obj, ctx.author, razbot_data.header)
    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    player_obj = verification_payload['player_obj']
    cwl_war_obj = verification_payload['cwl_war_obj']

    field_dict_list = discord_responder.war_all_attacks(
        cwl_war_obj)
    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"{cwl_war_obj.clan.name} vs. {cwl_war_obj.opponent.name}",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=player_obj.clan_icons,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )

    for embed in embed_list:
        await ctx.send(embed=embed)


# Discord

@client.command(
    aliases=['mentionraz'],
    brief='testing',
    description=('This will send a message to mention Razgriz'),
    hidden=True
)
async def mentionrazgriz(ctx):
    field_dict_list = []
    embed_list = discord_responder.embed_message(
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=f"mention testing",
        bot_prefix=ctx.prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail={'small': "https://i.imgur.com/JBt2Kwt.gif"},
        field_list=field_dict_list,
        image_url=None,
        author_display_name=ctx.author.display_name,
        author_avatar_url=(ctx.author.avatar_url.BASE +
                           ctx.author.avatar_url._url)
    )

    for embed in embed_list:
        await ctx.send(embed=embed)


@client.command(
    aliases=['emoji'],
    brief='testing',
    description=('emoji testing'),
    hidden=True
)
async def emojitesting(ctx):
    await ctx.send(f"this is currently not in use, only for emoji testing")


@client.command(
    aliases=['roleme'],
    brief='discord',
    description=('This will give you your clan role '
                 'here in Discord.')
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
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=f"{discord_user_obj.display_name}",
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=field_dict_list,
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    # getting a list of all claimed players
    player_obj_list = []
    for db_obj in db_player_obj_list:
        player_obj = clash_responder.get_player(
            db_obj.player_tag, razbot_data.header)
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
        db_clan_obj = db_responder.read_clan(ctx.guild.id, player_obj.clan_tag)
        # clan not found
        if not db_clan_obj:
            field_dict_list = [{
                "name": f"{player_obj.clan_name} {player_obj.clan_tag}",
                "value": f"not claimed in {ctx.guild.name} server"
            }]

            embed_list = discord_responder.embed_message(
                Embed=discord.Embed,
                color=discord.Color(client_data.embed_color),
                icon_url=(ctx.bot.user.avatar_url.BASE +
                          ctx.bot.user.avatar_url._url),
                title=f"{discord_user_obj.display_name} {player_obj.name}",
                bot_prefix=ctx.prefix,
                bot_user_name=ctx.bot.user.name,
                thumbnail=player_obj.league_icons,
                field_list=field_dict_list,
                image_url=None,
                author_display_name=ctx.author.display_name,
                author_avatar_url=(ctx.author.avatar_url.BASE +
                                   ctx.author.avatar_url._url)
            )
            for embed in embed_list:
                await ctx.send(embed=embed)

            continue

        # get discord clan and rank roles
        db_clan_role_obj = db_responder.read_clan_role_from_tag(
            ctx.guild.id, player_obj.clan_tag)
        db_rank_role_obj = (db_responder.read_rank_role_from_guild_and_clash(
            ctx.guild.id, player_obj.role))

        if not db_clan_role_obj and not db_rank_role_obj:
            field_dict_list = [{
                "name": f"clan and rank roles not claimed",
                "value": f"please claim proper roles"
            }]

            embed_list = discord_responder.embed_message(
                Embed=discord.Embed,
                color=discord.Color(client_data.embed_color),
                icon_url=(ctx.bot.user.avatar_url.BASE +
                          ctx.bot.user.avatar_url._url),
                title=f"{discord_user_obj.display_name} {player_obj.name}",
                bot_prefix=ctx.prefix,
                bot_user_name=ctx.bot.user.name,
                thumbnail=player_obj.league_icons,
                field_list=field_dict_list,
                image_url=None,
                author_display_name=ctx.author.display_name,
                author_avatar_url=(ctx.author.avatar_url.BASE +
                                   ctx.author.avatar_url._url)
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
        add_role_obj = discord.utils.get(ctx.guild.roles, id=add_role_id)
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
        remove_role_obj = discord.utils.get(
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
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=f"{discord_user_obj.display_name}",
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=field_dict_list,
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
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
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=f"{discord_user_obj.display_name}",
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=field_dict_list,
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)


# usable by leader and co leader
@client.command(
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

    verification_payload = discord_responder.player_leadership_verification(
        db_player_obj, ctx.author, razbot_data.header)

    if not verification_payload['verified']:
        embed_list = discord_responder.embed_message(
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=None,
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=verification_payload['field_dict_list'],
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
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
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=f"{discord_user_obj.display_name}",
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=field_dict_list,
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)
        return

    # getting a list of all claimed players
    player_obj_list = []
    for db_obj in db_player_obj_list:
        player_obj = clash_responder.get_player(
            db_obj.player_tag, razbot_data.header)
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
        db_clan_obj = db_responder.read_clan(ctx.guild.id, player_obj.clan_tag)
        # clan not found
        if not db_clan_obj:
            field_dict_list = [{
                "name": f"{player_obj.clan_name} {player_obj.clan_tag}",
                "value": f"not claimed in {ctx.guild.name} server"
            }]

            embed_list = discord_responder.embed_message(
                Embed=discord.Embed,
                color=discord.Color(client_data.embed_color),
                icon_url=(ctx.bot.user.avatar_url.BASE +
                          ctx.bot.user.avatar_url._url),
                title=f"{discord_user_obj.display_name} {player_obj.name}",
                bot_prefix=ctx.prefix,
                bot_user_name=ctx.bot.user.name,
                thumbnail=player_obj.league_icons,
                field_list=field_dict_list,
                image_url=None,
                author_display_name=ctx.author.display_name,
                author_avatar_url=(ctx.author.avatar_url.BASE +
                                   ctx.author.avatar_url._url)
            )
            for embed in embed_list:
                await ctx.send(embed=embed)

            continue

        # get discord clan and rank roles
        db_clan_role_obj = db_responder.read_clan_role_from_tag(
            ctx.guild.id, player_obj.clan_tag)
        db_rank_role_obj = (db_responder.read_rank_role_from_guild_and_clash(
            ctx.guild.id, player_obj.role))

        if not db_clan_role_obj and not db_rank_role_obj:
            field_dict_list = [{
                "name": f"clan and rank roles not claimed",
                "value": f"please claim proper roles"
            }]

            embed_list = discord_responder.embed_message(
                Embed=discord.Embed,
                color=discord.Color(client_data.embed_color),
                icon_url=(ctx.bot.user.avatar_url.BASE +
                          ctx.bot.user.avatar_url._url),
                title=f"{discord_user_obj.display_name} {player_obj.name}",
                bot_prefix=ctx.prefix,
                bot_user_name=ctx.bot.user.name,
                thumbnail=player_obj.league_icons,
                field_list=field_dict_list,
                image_url=None,
                author_display_name=ctx.author.display_name,
                author_avatar_url=(ctx.author.avatar_url.BASE +
                                   ctx.author.avatar_url._url)
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
        add_role_obj = discord.utils.get(ctx.guild.roles, id=add_role_id)
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
        remove_role_obj = discord.utils.get(
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
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=f"{discord_user_obj.display_name}",
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=field_dict_list,
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
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
            Embed=discord.Embed,
            color=discord.Color(client_data.embed_color),
            icon_url=(ctx.bot.user.avatar_url.BASE +
                      ctx.bot.user.avatar_url._url),
            title=f"{discord_user_obj.display_name}",
            bot_prefix=ctx.prefix,
            bot_user_name=ctx.bot.user.name,
            thumbnail=None,
            field_list=field_dict_list,
            image_url=None,
            author_display_name=ctx.author.display_name,
            author_avatar_url=(ctx.author.avatar_url.BASE +
                               ctx.author.avatar_url._url)
        )
        for embed in embed_list:
            await ctx.send(embed=embed)


@client.command(
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
                Embed=discord.Embed,
                color=discord.Color(client_data.embed_color),
                icon_url=(ctx.bot.user.avatar_url.BASE +
                          ctx.bot.user.avatar_url._url),
                title=f"{discord_user_obj.display_name}",
                bot_prefix=ctx.prefix,
                bot_user_name=ctx.bot.user.name,
                thumbnail=None,
                field_list=field_dict_list,
                image_url=None,
                author_display_name=ctx.author.display_name,
                author_avatar_url=(ctx.author.avatar_url.BASE +
                                   ctx.author.avatar_url._url)
            )
            for embed in embed_list:
                await ctx.send(embed=embed)
            continue

        # getting a list of all claimed players
        player_obj_list = []
        for db_obj in db_player_obj_list:
            player_obj = clash_responder.get_player(
                db_obj.player_tag, razbot_data.header)
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
                ctx.guild.id, player_obj.clan_tag)
            # clan not found
            if not db_clan_obj:
                field_dict_list = [{
                    "name": f"{player_obj.clan_name} {player_obj.clan_tag}",
                    "value": f"not claimed in {ctx.guild.name} server"
                }]

                embed_list = discord_responder.embed_message(
                    Embed=discord.Embed,
                    color=discord.Color(client_data.embed_color),
                    icon_url=(ctx.bot.user.avatar_url.BASE +
                              ctx.bot.user.avatar_url._url),
                    title=f"{discord_user_obj.display_name} {player_obj.name}",
                    bot_prefix=ctx.prefix,
                    bot_user_name=ctx.bot.user.name,
                    thumbnail=player_obj.league_icons,
                    field_list=field_dict_list,
                    image_url=None,
                    author_display_name=ctx.author.display_name,
                    author_avatar_url=(ctx.author.avatar_url.BASE +
                                       ctx.author.avatar_url._url)
                )
                for embed in embed_list:
                    await ctx.send(embed=embed)

                continue

            # get discord clan and rank roles
            db_clan_role_obj = db_responder.read_clan_role_from_tag(
                ctx.guild.id, player_obj.clan_tag)
            db_rank_role_obj = (db_responder.read_rank_role_from_guild_and_clash(
                ctx.guild.id, player_obj.role))

            if not db_clan_role_obj and not db_rank_role_obj:
                field_dict_list = [{
                    "name": f"clan and rank roles not claimed",
                    "value": f"please claim proper roles"
                }]

                embed_list = discord_responder.embed_message(
                    Embed=discord.Embed,
                    color=discord.Color(client_data.embed_color),
                    icon_url=(ctx.bot.user.avatar_url.BASE +
                              ctx.bot.user.avatar_url._url),
                    title=f"{discord_user_obj.display_name} {player_obj.name}",
                    bot_prefix=ctx.prefix,
                    bot_user_name=ctx.bot.user.name,
                    thumbnail=player_obj.league_icons,
                    field_list=field_dict_list,
                    image_url=None,
                    author_display_name=ctx.author.display_name,
                    author_avatar_url=(ctx.author.avatar_url.BASE +
                                       ctx.author.avatar_url._url)
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
            add_role_obj = discord.utils.get(ctx.guild.roles, id=add_role_id)
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
            remove_role_obj = discord.utils.get(
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
                Embed=discord.Embed,
                color=discord.Color(client_data.embed_color),
                icon_url=(ctx.bot.user.avatar_url.BASE +
                          ctx.bot.user.avatar_url._url),
                title=f"{discord_user_obj.display_name}",
                bot_prefix=ctx.prefix,
                bot_user_name=ctx.bot.user.name,
                thumbnail=None,
                field_list=field_dict_list,
                image_url=None,
                author_display_name=ctx.author.display_name,
                author_avatar_url=(ctx.author.avatar_url.BASE +
                                   ctx.author.avatar_url._url)
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
                Embed=discord.Embed,
                color=discord.Color(client_data.embed_color),
                icon_url=(ctx.bot.user.avatar_url.BASE +
                          ctx.bot.user.avatar_url._url),
                title=f"{discord_user_obj.display_name}",
                bot_prefix=ctx.prefix,
                bot_user_name=ctx.bot.user.name,
                thumbnail=None,
                field_list=field_dict_list,
                image_url=None,
                author_display_name=ctx.author.display_name,
                author_avatar_url=(ctx.author.avatar_url.BASE +
                                   ctx.author.avatar_url._url)
            )
            for embed in embed_list:
                await ctx.send(embed=embed)


# CLIENT

# client user
@client.command(
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
@client.command(
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
        player_obj = clash_responder.get_player(
            player_tag, razbot_data.header)
    if not player_obj:
        # player tag was not valid
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
    if db_player_obj:
        # player has already been claimed
        await ctx.send(f"{player_obj.name} {player_obj.tag} "
                       f"has already been claimed")
        return

    # authenticate player api key
    player_verified = clash_responder.verify_token(
        api_key, player_obj.tag, razbot_data.header)
    if not player_verified:
        # api key could not be verified
        await ctx.send(f"verification for "
                       f"player tag {player_obj.tag} has failed")
        return

        # check if not claimed
        db_player_obj = db_responder.read_player_from_tag(player_obj.tag)

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


@client.command(
    aliases=['showplayers', 'showclaimedplayers',
             'showplayersclaim', 'showplayerlist'],
    brief='client',
    description=(
        'Shows players claimed by a discord user')
)
async def showplayerclaim(ctx):
    async with ctx.typing():
        db_player_obj_list = db_responder.read_player_list(ctx.author.id)

    # if the user is found, but has no claimed players
    if len(db_player_obj_list) == 0:
        await ctx.send(f"{ctx.author.mention} does not have any "
                       f"claimed players")

        return

    message = f"{ctx.author.mention} has claimed "
    for db_player_obj in db_player_obj_list:
        player_obj = clash_responder.get_player(
            db_player_obj.player_tag, razbot_data.header)
        if db_player_obj.active:
            message += f"{player_obj.name} {player_obj.tag} (active), "
        else:
            message += f"{player_obj.name} {player_obj.tag}, "
    # cuts the last two characters from the string ', '
    message = message[:-2]
    await ctx.send(message)


@client.command(
    aliases=['updateactiveplayer', 'updateplayer'],
    brief='client',
    description=(
        "updates the user's active player")
)
async def updateplayeractive(ctx, player_tag):
    async with ctx.typing():
        player_obj = clash_responder.get_player(player_tag, razbot_data.header)

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


@client.command(
    aliases=['removeplayer'],
    brief='client',
    description=(
        "deletes the user's requested player claim")
)
async def deleteplayer(ctx, player_tag):
    async with ctx.typing():
        player_obj = clash_responder.get_player(
            player_tag, razbot_data.header)

    # player not found
    if not player_obj:
        await ctx.send(f"player with tag {player_tag} not found")
        return

    db_user_obj = db_responder.read_user(ctx.author.id)

    # db user not found
    if not db_user_obj:
        await ctx.send(f"{ctx.author.mention} has not been claimed")
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
    clash_updated_player_obj = clash_responder.get_player(
        db_updated_player_obj.player_tag, razbot_data.header)

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
@client.command(
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
# todo pull the clan tag from the db player to player tag to player.clan_tag
# ? simplify this...
@client.command(
    aliases=['clanclaim'],
    brief='client',
    description=(
        'This will claim the clan your '
        'active player is currently a member of'),
    hidden=True
)
async def claimclan(ctx, clan_tag):
    async with ctx.typing():
        clan_obj = clash_responder.get_clan(clan_tag, razbot_data.header)

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
        player_obj = clash_responder.get_player(
            db_player_obj.player_tag, razbot_data.header)

        # player in clan
        if player_obj.clan_tag == clan_obj.tag:
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


@client.command(
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

    message = f"{ctx.guild.name} has claimed "
    for item in db_clan_obj_list:
        clan = clash_responder.get_clan(
            item.clan_tag, razbot_data.header)
        message += f"{clan.name} {clan.tag}, "

    # cuts the last two characters from the string ', '
    message = message[:-2]

    await ctx.send(message)


@client.command(
    aliases=['removeclan', 'deleteclanclaim',
             'deleteclaimclan', 'deleteclaimedclan'],
    brief='client',
    description=(
        "deletes the requested clan claim"),
    hidden=True
)
async def deleteclan(ctx, clan_tag):
    async with ctx.typing():
        clan_obj = clash_responder.get_clan(clan_tag, razbot_data.header)

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


# client clan role
@client.command(
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
        clan_obj = clash_responder.get_clan(clan_tag, razbot_data.header)

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

    # confirm role has not been claimed
    db_clan_role_obj = db_responder.read_clan_role(role.id)
    # clan role has been claimed
    if db_clan_role_obj:
        await ctx.send(f"{role.mention} has already been claimed")
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


@client.command(
    aliases=['removeclanroleclaim'],
    brief='client',
    description=(
        "This will remove the claimed clan's discord role, "
        "the role will not be deleted from discord."),
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
@client.command(
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

    # confirm role has not been claimed
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
                   f"for rank {db_rank_role_obj.model_name}")


@client.command(
    aliases=['removerankroleclaim'],
    brief='client',
    description=(
        "This will remove the claimed rank's discord role, "
        "the role will not be deleted from discord."),
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
@client.command(
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
@client.command(
    aliases=['removeuser'],
    brief='clientsuperuser',
    description=('delete a claimed user'),
    hidden=True
)
async def removeuserclaim(ctx, user_id):

    db_author_obj = db_responder.read_user(ctx.author.id)
    if not db_author_obj:
        # author is not claimed
        await ctx.send(f"{ctx.author.mention} is not claimed")
        return

    if not db_author_obj.super_user:
        # author is not super user
        await ctx.send(f"{ctx.author.mention} is not super user")
        return

    # confirm user is claimed
    db_user_obj = db_responder.read_user(user_id)
    if not db_user_obj:
        # user isn't claimed
        await ctx.send(f"user with id {user_id} is not claimed")
        return

    deleted_user_obj = db_responder.delete_user(user_id)
    if deleted_user_obj:
        # user could not be deleted
        await ctx.send(f"user with id {user_id} could not be deleted")

    else:
        # user was deleted properly
        await ctx.send(f"user with id {user_id} was deleted")


# client events
@client.event
async def on_member_join(ctx):
    # get uninitiated role from db
    db_role_obj = db_responder.read_rank_role_from_guild_and_clash(
        ctx.guild.id, 'uninitiated')
    if db_role_obj:
        discord_role_obj = discord.utils.get(
            ctx.guild.roles, id=db_role_obj.discord_role_id)
        if discord_role_obj:
            await ctx.add_roles(discord_role_obj)


@client.event
async def on_member_remove(member):
    print(f'{member} has left {member.guild.name} id {member.guild.id}')


@client.event
async def on_reaction_add(reaction, user):
    # if the reactor is clash discord
    if user.id == razbot_data.discord_id:
        return

    # if the author of the reacted message is not clash discord
    if reaction.message.author.id != razbot_data.discord_id:
        return

    # if there are no embedded messages
    if len(reaction.message.embeds) == 0:
        return

    # if clash discord embedded message is not a help message
    if 'help' not in reaction.message.embeds[0].title:
        return

    ctx = await client.get_context(reaction.message)

    db_guild_obj = db_responder.read_guild(ctx.guild.id)
    db_player_obj = db_responder.read_player_active(user.id)

    if db_player_obj:
        player_obj = clash_responder.get_player(
            db_player_obj.player_tag, razbot_data.header)
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
        Embed=discord.Embed,
        color=discord.Color(client_data.embed_color),
        icon_url=(ctx.bot.user.avatar_url.BASE +
                  ctx.bot.user.avatar_url._url),
        title=embed_title,
        bot_prefix=ctx.bot.command_prefix,
        bot_user_name=ctx.bot.user.name,
        thumbnail=None,
        field_list=field_dict_list,
        image_url=None,
        author_display_name=user.display_name,
        author_avatar_url=(user.avatar_url.BASE +
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


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"command '{ctx.invoked_with}' could not be found")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"command '{ctx.invoked_with}' "
                       f"requires more information")
    elif hasattr(error.original, "text"):
        await ctx.send(f"there was an error that I have not accounted for, "
                       f"please let Razgriz know, "
                       f"error text: `{error.original.text}`")
    else:
        await ctx.send(f"there was an error that I have not accounted for, "
                       f"please let Razgriz know")

client.run(razbot_data.token)
