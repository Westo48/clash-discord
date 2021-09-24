import discord
from asyncio.tasks import sleep
from discord.ext import commands
from discord.utils import get
import RazBot_Data
import ClashResponder as clash_responder
from DiscordResponder import *
import RazBotDB_Responder as db_responder

razbot_data = RazBot_Data.RazBot_Data()

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
    is_leader = role_check('leader', ctx.author.roles)

    embed = discord.Embed(
        colour=discord.Colour.blue()
    )
    embed.set_author(
        name=f"[{ctx.prefix}] {ctx.bot.user.name}", icon_url="https://cdn.discordapp.com/avatars/649107156989378571/053f201109188da026d0a980dd4136e0.webp")

    embed.set_thumbnail(
        url=(
            "https://media0.giphy.com/media/dYzd7l6IdYY6I/giphy.gif?cid="
            "790b7611d2ac327de00b11cbd7fae83d4c62107b53baa86f&"
            "rid=giphy.gif&ct=g"
        )
    )

    for category in razbot_data.bot_categories:
        brief = category.brief

        embed.add_field(
            name=f"__**{category.name.upper()}**__",
            value=f"{category.emoji}-----------------",
            inline=False
        )

        for command in ctx.bot.all_commands.items():
            if (
                command[1].brief == brief
                and command[1].description != ''
                and command[0] == command[1].name
                and (not command[1].hidden or is_leader)
            ):
                embed_name = "**" + command[1].name + "**"
                if command[1].signature != '':
                    embed_name += f" {command[1].signature}"
                if len(command[1].aliases) != 0:
                    embed_name += f" | {command[1].aliases}"
                embed.add_field(
                    name=embed_name,
                    value=command[1].description,
                    inline=False
                )

    embed.set_footer(
        text="If you have a question mention Razgriz. "
        "Please note this is still a work in progress "
        "and there will be bugs to work out.")

    await ctx.send(embed=embed)


@client.command(
    brief='discord'
)
async def embedtest(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour=discord.Colour.teal(),
        title='Test title'
    )
    embed.set_author(
        name="[{ctx.prefix}] RazClashBot", icon_url="https://cdn.discordapp.com/avatars/649107156989378571/053f201109188da026d0a980dd4136e0.webp")
    # embed.set_image(
    #     url="https://i.imgur.com/rwgo8fJ.jpg")
    embed.set_thumbnail(
        url="https://i.imgur.com/MFZp1Fy.gif")

    embed.add_field(
        name="Testing", value=":computer:", inline=False)

    embed.add_field(
        name=f"{ctx.bot.all_commands['waroverview'].name} | {ctx.bot.all_commands['waroverview'].aliases}",
        value=ctx.bot.all_commands['waroverview'].description,
        inline=False
    )

    embed.set_footer(
        text="This is the embed testing command")

    await ctx.send(embed=embed)


@client.command(
    brief='misc', description='Misc Command'
)
async def hellothere(ctx):
    await ctx.send(f'General Kenobi')


@client.command(
    brief='misc'
)
async def ping(ctx):
    async with ctx.typing():
        await ctx.send(f'pong {round(ctx.bot.latency, 3) * 1000}ms')


# Player

@client.command(
    brief='player',
    description="Enter a player's tag and get a player's information"
)
async def player(ctx, *, player_tag):
    player = clash_responder.get_player(player_tag, razbot_data.header)

    if player:
        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title=player.name,
        )
        embed.set_author(
            name=f"[{ctx.prefix}] {ctx.bot.user.name}", icon_url="https://cdn.discordapp.com/avatars/649107156989378571/053f201109188da026d0a980dd4136e0.webp")
        embed.add_field(
            name='**Exp Lvl**',
            value=player.xp_lvl,
            inline=True
        )
        embed.add_field(
            name='**TH Lvl**',
            value=player.th_lvl,
            inline=True
        )
        if player.th_weapon_lvl:
            embed.add_field(
                name='**TH Weapon Lvl**',
                value=player.th_weapon_lvl,
                inline=True
            )
        embed.add_field(
            name='**Trophies**',
            value=player.trophies,
            inline=True
        )
        embed.add_field(
            name='**Best Trophies**',
            value=player.best_trophies,
            inline=True
        )
        if player.legend_trophies:
            embed.add_field(
                name='**Legend Trophies**',
                value=player.legend_trophies,
                inline=True
            )
            embed.add_field(
                name='**Best Rank | Trophies**',
                value=f"{player.best_legend_rank} | {player.best_legend_trophies}",
                inline=True
            )
            if player.previous_legend_rank:
                embed.add_field(
                    name='**Previous Rank | Trophies**',
                    value=f"{player.previous_legend_rank} | {player.previous_legend_trophies}",
                    inline=True
                )
            if player.current_legend_rank:
                embed.add_field(
                    name='**Current Rank | Trophies**',
                    value=f"{player.current_legend_rank} | {player.current_legend_trophies}",
                    inline=True
                )

        if not player.league_id:
            embed.set_thumbnail(
                url='https://api-assets.clashofclans.com/leagues/72/e--YMyIexEQQhE4imLoJcwhYn6Uy8KqlgyY3_kFV6t4.png')
        else:
            embed.set_thumbnail(url=player.league_icons['medium'])
        embed.add_field(
            name='**War Stars**',
            value=player.war_stars,
            inline=True
        )
        if player.clan_lvl:
            embed.add_field(
                name='**Clan**',
                value=f"[{player.clan_name}](https://link.clashofclans.com/en?action=OpenClanProfile&tag={player.clan_tag[1:]})",
                inline=True
            )

            if player.role == 'leader':
                role_name = 'Leader'
            elif player.role == 'coLeader':
                role_name = 'Co-Leader'
            elif player.role == 'admin':
                role_name = 'Elder'
            else:
                role_name = 'Member'
            embed.add_field(
                name='**Clan Role**',
                value=role_name,
                inline=True
            )
        else:
            embed.add_field(
                name='**Clan**',
                value=f"{player.name} is not in a clan",
                inline=True
            )

        hero_title = ''
        hero_value = ''
        for hero in player.heroes:
            if hero.name == 'Barbarian King':
                hero_title = 'BK'
                hero_value = f'{hero.lvl}'
            elif hero.name == 'Archer Queen':
                hero_title += ' | AQ'
                hero_value += f' | {hero.lvl}'
            elif hero.name == 'Grand Warden':
                hero_title += ' | GW'
                hero_value += f' | {hero.lvl}'
            elif hero.name == 'Royal Champion':
                hero_title += ' | RC'
                hero_value += f' | {hero.lvl}'
            else:
                break
        if hero_title != '':
            embed.add_field(
                name=f'**{hero_title}**',
                value=hero_value,
                inline=True
            )

        pet_title = ''
        pet_value = ''
        for troop in player.troops:
            if troop.name == 'L.A.S.S.I':
                pet_title = 'LA'
                pet_value = f'{troop.lvl}'
            elif troop.name == 'Mighty Yak':
                pet_title += ' | MY'
                pet_value += f' | {troop.lvl}'
            elif troop.name == 'Electro Owl':
                pet_title += ' | EO'
                pet_value += f' | {troop.lvl}'
            elif troop.name == 'Unicorn':
                pet_title += ' | UC'
                pet_value += f' | {troop.lvl}'
        if pet_title != '':
            embed.add_field(
                name=f'**{pet_title}**',
                value=pet_value,
                inline=True
            )

        embed.add_field(
            name='**Link**',
            value=f"[{player.name}](https://link.clashofclans.com/en?action=OpenPlayerProfile&tag={player.tag[1:]})",
            inline=True
        )

        # todo set footer to display user called and timestamp
        embed.set_footer(
            text=ctx.author.display_name,
            icon_url=ctx.author.avatar_url.BASE+ctx.author.avatar_url._url
        )

        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Could not find player with tag {player_tag}")


@client.command(
    brief='player',
    description='Enter unit to see its current, th max, and max level.'
)
async def trooplvl(ctx, *, troop_name):
    db_player_obj = db_responder.read_player_active(ctx.author.id)
    if db_player_obj:
        player_obj = clash_responder.get_player(
            db_player_obj.player_tag, razbot_data.header)
        if player_obj:
            await ctx.send(clash_responder.response_troop_lvl(
                player_obj, troop_name, razbot_data.header))
        else:
            await ctx.send(f"Couldn't find player from tag "
                           f"{db_player_obj.player_tag}")
    else:
        await ctx.send(f"{ctx.author.mention} does not have an active player")


@client.command(
    brief='player',
    description='Get all your troop levels.',
    hidden=True
)
async def alltrooplvl(ctx):
    db_player_obj = db_responder.read_player_active(ctx.author.id)
    if db_player_obj:
        player_obj = clash_responder.get_player(
            db_player_obj.player_tag, razbot_data.header)
        if player_obj:
            for line in clash_responder.response_all_troop_level(player_obj):
                await ctx.send(line)
        else:
            await ctx.send(f"Couldn't find player from tag "
                           f"{db_player_obj.player_tag}")
    else:
        await ctx.send(f"{ctx.author.mention} does not have an active player")


# Clan


@client.command(
    brief='clan',
    description="Enter a clan's tag and get a clan's information"
)
async def clan(ctx, *, clan_tag):
    clan_obj = Clan.get(clan_tag, razbot_data.header)

    if clan_obj:
        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title=clan_obj.name,
        )
        embed.set_author(
            name=f"[{ctx.prefix}] RazClashBot", icon_url="https://cdn.discordapp.com/avatars/649107156989378571/053f201109188da026d0a980dd4136e0.webp")

        embed.set_thumbnail(url=clan_obj.clan_icons['small'])

        embed.add_field(
            name='**Description**',
            value=clan_obj.description,
            inline=False
        )
        embed.add_field(
            name='**Clan Lvl**',
            value=clan_obj.clan_lvl,
            inline=True
        )
        embed.add_field(
            name='**Clan War League**',
            value=clan_obj.war_league_name,
            inline=True
        )
        embed.add_field(
            name='**Total Points**',
            value=clan_obj.clan_points,
            inline=True
        )
        embed.add_field(
            name='**Link**',
            value=f"[{clan_obj.name}](https://link.clashofclans.com/en?action=OpenClanProfile&tag={clan_obj.tag[1:]})",
            inline=True
        )

        # todo set footer to display user called and timestamp
        embed.set_footer(
            text=ctx.author.display_name,
            icon_url=ctx.author.avatar_url.BASE+ctx.author.avatar_url._url
        )

        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Could not find clan with tag {clan_tag}")


@client.command(
    aliases=['donation', 'donate'],
    brief='clan',
    description='Enter a troop name to see who in the clan '
                'is best suited to donate that troop.'
)
async def donationchecker(ctx, *, unit_name):
    db_player_obj = db_responder.read_player_active(ctx.author.id)
    if db_player_obj:
        player_obj = clash_responder.get_player(
            db_player_obj.player_tag, razbot_data.header)
        if player_obj:
            if player_obj.clan_tag:
                clan_obj = Clan.get(player_obj.clan_tag, razbot_data.header)
                if clan_obj:
                    donators = clash_responder.response_donation(
                        unit_name, clan_obj, razbot_data.header)

                    # if the requested unit is not a hero
                    if donators:
                        member_string = ''

                        # setting the string of members that can donate
                        for donator in donators:
                            member_string += f'{donator.player.name}, '

                        # cuts the last two characters from the string ', '
                        member_string = member_string[:-2]

                        # if donators can donate max
                        if ((donators[0].unit.lvl + clan_obj.donation_upgrade) >=
                                donators[0].unit.max_lvl):
                            message = (
                                f'{member_string} can donate level '
                                f'{donators[0].unit.max_lvl} {donators[0].unit.name}, '
                                f'which is max.'
                            )
                        # if donators cannot donate max
                        else:
                            message = (
                                f'{member_string} can donate level'
                                f'{donators[0].unit.lvl + clan_obj.donation_upgrade} '
                                f'{donators[0].unit.name}, max is '
                                f'{donators[0].unit.max_lvl}'
                            )

                    # if the requested unit is a hero
                    else:
                        message = f'{unit_name} is not a valid donatable unit.'

                    await ctx.send(message)
                else:
                    await ctx.send(f"Couldn't find clan from tag "
                                   f"{player_obj.clan_tag}")
            else:
                await ctx.send(f"{player_obj.name} is not in a clan")
        else:
            await ctx.send(f"Couldn't find player from tag "
                           f"{db_player_obj.player_tag}")
    else:
        await ctx.send(f"{ctx.author.mention} does not have an active player")


# War
# todo warmember gets a war overview for a specific war member

@client.command(
    aliases=['war'],
    brief='war',
    description='Returns an overview of the current war'
)
async def waroverview(ctx):
    db_player_obj = db_responder.read_player_active(ctx.author.id)
    if db_player_obj:
        player_obj = clash_responder.get_player(
            db_player_obj.player_tag, razbot_data.header)
        if player_obj:
            if player_obj.clan_tag:
                await ctx.send(
                    clash_responder.response_war_overview(
                        player_obj.clan_tag, razbot_data.header))
            else:
                await ctx.send(f"{player_obj.name} is not in a clan")
        else:
            await ctx.send(f"Couldn't find player from tag "
                           f"{db_player_obj.player_tag}")
    else:
        await ctx.send(f"{ctx.author.mention} does not have an active player")


@client.command(
    brief='war',
    description='Returns the time remaining in the current war')
async def wartime(ctx):
    db_player_obj = db_responder.read_player_active(ctx.author.id)
    if db_player_obj:
        player_obj = clash_responder.get_player(
            db_player_obj.player_tag, razbot_data.header)
        if player_obj:
            if player_obj.clan_tag:
                await ctx.send(clash_responder.response_war_time(
                    player_obj.clan_tag, razbot_data.header))
            else:
                await ctx.send(f"{player_obj.name} is not in a clan")
        else:
            await ctx.send(f"Couldn't find player from tag "
                           f"{db_player_obj.player_tag}")
    else:
        await ctx.send(f"{ctx.author.mention} does not have an active player")


@client.command(
    aliases=['warnoatk'],
    brief='war',
    description='Returns a list of players that have/did not use '
                'all possible attacks in the current war'
)
async def warnoattack(ctx):
    db_player_obj = db_responder.read_player_active(ctx.author.id)
    if db_player_obj:
        player_obj = clash_responder.get_player(
            db_player_obj.player_tag, razbot_data.header)
        if player_obj:
            if player_obj.clan_tag:
                await ctx.send(clash_responder.response_war_no_attack(
                    player_obj.clan_tag, razbot_data.header))
            else:
                await ctx.send(f"{player_obj.name} is not in a clan")
        else:
            await ctx.send(f"Couldn't find player from tag "
                           f"{db_player_obj.player_tag}")
    else:
        await ctx.send(f"{ctx.author.mention} does not have an active player")


@client.command(
    aliases=['warnoatkalert'],
    brief='war',
    description='Returns a list of players that '
                'have/did not use all possible attacks '
                'and mentions them if found',
    hidden=True
)
async def warnoattackalert(ctx):
    db_player_obj = db_responder.read_player_active(ctx.author.id)
    if db_player_obj:
        player_obj = clash_responder.get_player(
            db_player_obj.player_tag, razbot_data.header)
        if player_obj:
            if player_obj.clan_tag:
                no_atk_list = clash_responder.war_no_attack_members(
                    player_obj.clan_tag, razbot_data.header)
                if len(no_atk_list) == 0:
                    await ctx.send('Nobody needs to attack.')
                else:
                    message = ''
                    for player in no_atk_list:
                        member = find_channel_member(
                            player.name, ctx.channel.members)
                        if member != '':
                            message += f'{member.mention}, '
                        else:
                            message += f'{player.name}, '
                    message = message[:-2]
                    message += ' needs to attack.'
                    await ctx.send(message)
            else:
                await ctx.send(f"{player_obj.name} is not in a clan")
        else:
            await ctx.send(f"Couldn't find player from tag "
                           f"{db_player_obj.player_tag}")
    else:
        await ctx.send(f"{ctx.author.mention} does not have an active player")


@client.command(
    aliases=['warclan', 'warstars'],
    brief='war',
    description='overview of all members in war',
    hidden=True
)
async def warclanstars(ctx):
    db_player_obj = db_responder.read_player_active(ctx.author.id)
    if db_player_obj:
        player_obj = clash_responder.get_player(
            db_player_obj.player_tag, razbot_data.header)
        if player_obj:
            if player_obj.clan_tag:
                for line in clash_responder.response_war_members_overview(
                        player_obj.clan_tag, razbot_data.header):
                    await ctx.send(line)
            else:
                await ctx.send(f"{player_obj.name} is not in a clan")
        else:
            await ctx.send(f"Couldn't find player from tag "
                           f"{db_player_obj.player_tag}")
    else:
        await ctx.send(f"{ctx.author.mention} does not have an active player")


@client.command(
    aliases=['warallatk'],
    brief='war',
    description='showing all attacks for every member',
    hidden=True
)
async def warallattacks(ctx):
    db_player_obj = db_responder.read_player_active(ctx.author.id)
    if db_player_obj:
        player_obj = clash_responder.get_player(
            db_player_obj.player_tag, razbot_data.header)
        if player_obj:
            if player_obj.clan_tag:
                for line in clash_responder.response_war_all_attacks(
                        player_obj.clan_tag, razbot_data.header):
                    await ctx.send(f'{line}')
            else:
                await ctx.send(f"{player_obj.name} is not in a clan")
        else:
            await ctx.send(f"Couldn't find player from tag "
                           f"{db_player_obj.player_tag}")
    else:
        await ctx.send(f"{ctx.author.mention} does not have an active player")


@client.command(
    aliases=['warscore'],
    brief='war',
    description='showing every member score',
    hidden=True
)
async def warclanscore(ctx):
    db_player_obj = db_responder.read_player_active(ctx.author.id)
    if db_player_obj:
        player_obj = clash_responder.get_player(
            db_player_obj.player_tag, razbot_data.header)
        if player_obj:
            if player_obj.clan_tag:
                for line in clash_responder.response_war_all_member_standing(
                        player_obj.clan_tag, razbot_data.header):
                    await ctx.send(f'{line}')
            else:
                await ctx.send(f"{player_obj.name} is not in a clan")
        else:
            await ctx.send(f"Couldn't find player from tag "
                           f"{db_player_obj.player_tag}")
    else:
        await ctx.send(f"{ctx.author.mention} does not have an active player")


# CWL Group
# todo cwl_group overview, scoreboard, cwl_clan_noatk

@client.command(
    aliases=['cwlgroup'],
    brief='cwlgroup',
    description='Returns the CWL group lineup',
    hidden=False
)
async def cwllineup(ctx):
    db_player_obj = db_responder.read_player_active(ctx.author.id)
    if db_player_obj:
        player_obj = clash_responder.get_player(
            db_player_obj.player_tag, razbot_data.header)
        if player_obj:
            if player_obj.clan_tag:

                cwl_group = clash_responder.get_cwl_group(
                    player_obj.clan_tag, razbot_data.header)

                if cwl_group:
                    cwl_lineup = clash_responder.response_cwl_lineup(cwl_group)
                    message = (
                        "```\n"
                        "CWL Group Lineup\n"
                        "14 | 13 | 12 | 11 | 10 | 9  | 8\n"
                        "-------------------------------\n"
                    )
                    for clan_dict in cwl_lineup:
                        lineup_message = f"{clan_dict['clan'].name}\n"
                        for key in clan_dict:
                            if key != 'clan' and key > 6:
                                if key >= 8:
                                    lineup_message += f"{clan_dict[key]}"
                                    # if it is a double digit number
                                    if clan_dict[key] >= 10:
                                        lineup_message += " | "
                                    # if it is a single digit number add an extra space
                                    else:
                                        lineup_message += "  | "
                        # removes the last 4 characters '  | ' of the string
                        lineup_message = lineup_message[:-4]
                        lineup_message += "\n\n"
                        message += lineup_message
                    message += "```"
                    await ctx.send(message)
                else:
                    await ctx.send(f"{player_obj.clan_name} is not in CWL")
            else:
                await ctx.send(f"{player_obj.name} is not in a clan")
        else:
            await ctx.send(f"Couldn't find player from tag "
                           f"{db_player_obj.player_tag}")
    else:
        await ctx.send(f"{ctx.author.mention} does not have an active player")


# CWL War
# todo cwlwar war_time_prep, war_overview_prep, war_overview_round,

@client.command(
    aliases=['cwlwar'],
    brief='cwlwar',
    description='Returns an overview of the current CWL war'
)
async def cwlwaroverview(ctx):
    db_player_obj = db_responder.read_player_active(ctx.author.id)
    if db_player_obj:
        player_obj = clash_responder.get_player(
            db_player_obj.player_tag, razbot_data.header)
        if player_obj:
            if player_obj.clan_tag:
                await ctx.send(clash_responder.response_cwl_war_overview(
                    player_obj.clan_tag, razbot_data.header))
            else:
                await ctx.send(f"{player_obj.name} is not in a clan")
        else:
            await ctx.send(f"Couldn't find player from tag "
                           f"{db_player_obj.player_tag}")
    else:
        await ctx.send(f"{ctx.author.mention} does not have an active player")


@client.command(
    brief='cwlwar',
    description='Returns the time remaining in the current CWL war'
)
async def cwlwartime(ctx):
    db_player_obj = db_responder.read_player_active(ctx.author.id)
    if db_player_obj:
        player_obj = clash_responder.get_player(
            db_player_obj.player_tag, razbot_data.header)
        if player_obj:
            if player_obj.clan_tag:
                await ctx.send(clash_responder.response_cwl_war_time(
                    player_obj.clan_tag, razbot_data.header))
            else:
                await ctx.send(f"{player_obj.name} is not in a clan")
        else:
            await ctx.send(f"Couldn't find player from tag "
                           f"{db_player_obj.player_tag}")
    else:
        await ctx.send(f"{ctx.author.mention} does not have an active player")


@client.command(
    aliases=['cwlwarnoatk'],
    brief='cwlwar',
    description='Returns a list of players that have/did not use '
                'all possible attacks in the current CWL war'
)
async def cwlwarnoattack(ctx):
    db_player_obj = db_responder.read_player_active(ctx.author.id)
    if db_player_obj:
        player_obj = clash_responder.get_player(
            db_player_obj.player_tag, razbot_data.header)
        if player_obj:
            if player_obj.clan_tag:
                await ctx.send(clash_responder.response_cwl_war_no_attack(
                    player_obj.clan_tag, razbot_data.header))
            else:
                await ctx.send(f"{player_obj.name} is not in a clan")
        else:
            await ctx.send(f"Couldn't find player from tag "
                           f"{db_player_obj.player_tag}")
    else:
        await ctx.send(f"{ctx.author.mention} does not have an active player")


@client.command(
    aliases=['cwlwarallatk'],
    brief='cwlwar',
    description='showing all attacks for every member in the current war',
    hidden=True
)
async def cwlwarallattack(ctx):
    db_player_obj = db_responder.read_player_active(ctx.author.id)
    if db_player_obj:
        player_obj = clash_responder.get_player(
            db_player_obj.player_tag, razbot_data.header)
        if player_obj:
            if player_obj.clan_tag:
                for line in clash_responder.response_cwl_war_all_attacks(
                        player_obj.clan_tag, razbot_data.header):
                    await ctx.send(line)
            else:
                await ctx.send(f"{player_obj.name} is not in a clan")
        else:
            await ctx.send(f"Couldn't find player from tag "
                           f"{db_player_obj.player_tag}")
    else:
        await ctx.send(f"{ctx.author.mention} does not have an active player")


@client.command(
    aliases=['cwlscore'],
    brief='cwlwar',
    description='Lists each member and their score in CWL',
    hidden=True
)
async def cwlclanscore(ctx):
    db_player_obj = db_responder.read_player_active(ctx.author.id)
    if db_player_obj:
        player_obj = clash_responder.get_player(
            db_player_obj.player_tag, razbot_data.header)
        if player_obj:
            if player_obj.clan_tag:
                for line in clash_responder.response_cwl_clan_standing(
                        player_obj.clan_tag, razbot_data.header):
                    await ctx.send(line)
            else:
                await ctx.send(f"{player_obj.name} is not in a clan")
        else:
            await ctx.send(f"Couldn't find player from tag "
                           f"{db_player_obj.player_tag}")
    else:
        await ctx.send(f"{ctx.author.mention} does not have an active player")


@client.command(
    brief='cwlwar',
    description='Lists each score you have in CWL'
)
async def cwlmemberscore(ctx):
    db_player_obj = db_responder.read_player_active(ctx.author.id)
    if db_player_obj:
        player_obj = clash_responder.get_player(
            db_player_obj.player_tag, razbot_data.header)
        if player_obj:
            if player_obj.clan_tag:
                await ctx.send(clash_responder.response_cwl_member_standing(
                    player_obj, razbot_data.header))
            else:
                await ctx.send(f"{player_obj.name} is not in a clan")
        else:
            await ctx.send(f"Couldn't find player from tag "
                           f"{db_player_obj.player_tag}")
    else:
        await ctx.send(f"{ctx.author.mention} does not have an active player")


@client.command(
    brief='cwlwar',
    description='Lists each score the specified member has in CWL'
)
async def cwlclanmatescore(ctx):
    if len(ctx.message.mentions) > 0:
        # if a user has been mentioned
        discord_member = ctx.message.mentions[0]
        db_player_obj = db_responder.read_player_active(discord_member.id)
        if db_player_obj:
            player_obj = clash_responder.get_player(
                db_player_obj.player_tag, razbot_data.header)
            if player_obj:
                if player_obj.clan_tag:
                    await ctx.send(
                        clash_responder.response_cwl_member_standing(
                            player_obj, razbot_data.header))
                else:
                    await ctx.send(f"{player_obj.name} is not in a clan")
            else:
                await ctx.send(f"Couldn't find player from tag "
                               f"{db_player_obj.player_tag}")
        else:
            await ctx.send(f"{discord_member.mention} does not have "
                           f"an active player")
    else:
        await ctx.send(f"You have to mention a member")


# Discord

@client.command(
    aliases=['mentionraz'],
    brief='testing',
    description=('This will send a message to mention Razgriz'),
    hidden=True
)
async def mentionrazgriz(ctx):
    found = False
    for member in ctx.channel.members:
        if player_name_string(member.display_name) == 'Razgriz':
            mention = member.mention
            await ctx.send(f'Hello {mention}')
            found = True
            break
    if not found:
        await ctx.send("Couldn't find 'Razgriz' in the channel.")


@client.command(
    aliases=['emoji'],
    brief='testing',
    description=('emoji testing'),
    hidden=True
)
async def emojitesting(ctx):
    await ctx.send(f"this is currently not in use, only for emoji testing")


# ! for all claimed players
# todo uninitiated setup
@client.command(
    aliases=['roleme'],
    brief='discord',
    description=('This will give you your clan role '
                 'here in Discord.')
)
async def role(ctx):

    db_guild_obj = db_responder.read_guild(ctx.guild.id)
    if not db_guild_obj:
        # if guild is not claimed
        await ctx.send(f"{ctx.guild.name} has not been claimed")
        return

    db_user_obj = db_responder.read_user(ctx.author.id)
    if not db_user_obj:
        # if user is not claimed
        await ctx.send(f"{ctx.author.mention} has not been claimed")
        return

    db_player_obj = db_responder.read_player_list(ctx.author.id)
    if len(db_player_obj) == 0:
        # if player is not claimed
        await ctx.send(f"{ctx.author.mention} has no claimed players")
        return

    player_obj_list = []
    for db_obj in db_player_obj:
        player_obj = clash_responder.get_player(
            db_obj.player_tag, razbot_data.header)
        if player_obj:
            player_obj_list.append(player_obj)
        else:
            # player was not found from tag
            await ctx.send(f"Couldn't find player from tag "
                           f"{db_player_obj.player_tag}")
            return

    # get needed roles
    needed_role_list = []
    for player_obj in player_obj_list:
        # get discord roles for the clan and role in the clan
        if player_obj.clan_tag:
            db_clan_role_obj = db_responder.read_clan_role_from_tag(
                ctx.guild.id, player_obj.clan_tag)
            # adding the role id to the list
            needed_role_list.append(db_clan_role_obj.discord_role_id)
            db_rank_role_obj = (
                db_responder.read_rank_role_from_guild_and_clash(
                    ctx.guild.id, player_obj.role))
            # adding the role id to the list
            needed_role_list.append(db_rank_role_obj.discord_role_id)

    # get rid of duplicates
    needed_role_list = list(dict.fromkeys(needed_role_list))

    # get current roles
    current_discord_role_list = []
    for current_role in ctx.author.roles:
        current_discord_role_list.append(current_role.id)

    # get current roles that match db roles
    current_db_role_list = db_responder.read_rank_role_list(
        current_discord_role_list)

    # getting the list of role id's
    current_role_list = []
    for current_role in current_db_role_list:
        current_role_list.append(current_role.discord_role_id)

    add_role_id_list, remove_role_id_list = role_add_remove_list(
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
                f"Could not find role for id {add_role_id}, "
                f"please ensure claimed roles and discord roles match"
            )

    # add roles
    for add_role_obj in add_role_obj_list:
        await ctx.author.add_roles(add_role_obj)

    # get objects of roles to remove from id's
    remove_role_obj_list = []
    for remove_role_id in remove_role_id_list:
        # returns None if role is not found
        remove_role_obj = discord.utils.get(ctx.guild.roles, id=remove_role_id)
        if remove_role_obj:
            # role was found in guild.roles
            remove_role_obj_list.append(remove_role_obj)
        else:
            await ctx.send(
                f"Could not find role for id {remove_role_id}, "
                f"please ensure claimed roles and discord roles match"
            )

    # remove roles
    for remove_role_obj in remove_role_obj_list:
        await ctx.author.remove_roles(remove_role_obj)

    await ctx.send(f"Roles have been updated")

# CLIENT

# client user


@client.command(
    aliases=['claim_user', 'userclaim'],
    brief='discord',
    description=(
        'This will claim a discord user')
)
async def claimuser(ctx):
    user = db_responder.claim_user(ctx.author.id)
    # if user wasn't claimed and now is
    if user:
        await ctx.send(f"{ctx.author.mention} is now claimed")
    # if user was already claimed
    else:
        await ctx.send(f"{ctx.author.mention} has already been claimed")


# client player
# todo claim user if user isn't set up
@client.command(
    aliases=['playerclaim'],
    brief='discord',
    description=(
        'This will verify and claim a player')
)
async def claimplayer(ctx, player_tag, *, api_key):

    # confirm valid player_tag
    clash_player_obj = clash_responder.get_player(
        player_tag, razbot_data.header)

    # verifying player
    if clash_player_obj:
        player_verified = clash_responder.verify_token(
            api_key, clash_player_obj.tag, razbot_data.header)

        if player_verified:
            # check if not claimed
            claimed_player = db_responder.read_player_from_tag(
                clash_player_obj.tag)

            if claimed_player:
                # already claimed
                await ctx.send(f"{clash_player_obj.name} has already been claimed")
            else:
                # verified and not claimed
                player_obj = db_responder.claim_player(
                    ctx.author.id, clash_player_obj.tag)

                if player_obj:
                    # if succesfully claimed
                    await ctx.send(f"{clash_player_obj.name} tag {clash_player_obj.tag} "
                                   f"is now claimed by {ctx.author.mention}")
                else:
                    # if failed to claim
                    await ctx.send(
                        f"Could not claim {clash_player_obj.name} "
                        f"tag {clash_player_obj.tag} for {ctx.author.mention}"
                    )

        else:
            # player verification failed
            await ctx.send(f"Verification for "
                           f"player tag {clash_player_obj.tag} has failed")
    else:
        # invalid player_tag
        await ctx.send(f"Couldn't find a player with player tag {player_tag}")


# todo remove the user search
# todo simply use "no claimed players found ad mention user"
@client.command(
    aliases=['showplayers', 'showclaimedplayers',
             'showplayersclaim', 'showplayerlist'],
    brief='discord',
    description=(
        'Shows players claimed by a discord user')
)
async def showplayerclaim(ctx):
    user = db_responder.read_user(ctx.author.id)
    # if user is found
    if user:
        player_list = db_responder.read_player_list(ctx.author.id)
        # if the user is found, but has no claimed players
        if len(player_list) == 0:
            await ctx.send(f"{ctx.author.mention} does not have any "
                           "claimed players")
        else:
            message = f"{ctx.author.mention} has claimed "
            for item in player_list:
                player = clash_responder.get_player(
                    item.player_tag, razbot_data.header)
                if item.active:
                    message += f"{player.name} (active), "
                else:
                    message += f"{player.name}, "
            # cuts the last two characters from the string ', '
            message = message[:-2]
            await ctx.send(message)
    # if user is not found
    else:
        await ctx.send(f"{ctx.author.mention} has not been claimed")


@client.command(
    aliases=['showplayer', 'activeplayer'],
    brief='player',
    description="Get information about your active player"
)
async def showactiveplayer(ctx):
    user = db_responder.read_user(ctx.author.id)
    # if user is found
    if user:
        # if the user is found
        db_player_obj = db_responder.read_player_active(ctx.author.id)
        if db_player_obj:
            # active player is found
            player = clash_responder.get_player(
                db_player_obj.player_tag, razbot_data.header)

            if player:
                # if player is found
                embed = discord.Embed(
                    colour=discord.Colour.blue(),
                    title=player.name,
                )
                embed.set_author(
                    name=f"[{ctx.prefix}] {ctx.bot.user.name}", icon_url="https://cdn.discordapp.com/avatars/649107156989378571/053f201109188da026d0a980dd4136e0.webp")
                embed.add_field(
                    name='**Exp Lvl**',
                    value=player.xp_lvl,
                    inline=True
                )
                embed.add_field(
                    name='**TH Lvl**',
                    value=player.th_lvl,
                    inline=True
                )
                if player.th_weapon_lvl:
                    embed.add_field(
                        name='**TH Weapon Lvl**',
                        value=player.th_weapon_lvl,
                        inline=True
                    )
                embed.add_field(
                    name='**Trophies**',
                    value=player.trophies,
                    inline=True
                )
                embed.add_field(
                    name='**Best Trophies**',
                    value=player.best_trophies,
                    inline=True
                )
                if player.legend_trophies:
                    embed.add_field(
                        name='**Legend Trophies**',
                        value=player.legend_trophies,
                        inline=True
                    )
                    embed.add_field(
                        name='**Best Rank | Trophies**',
                        value=f"{player.best_legend_rank} | {player.best_legend_trophies}",
                        inline=True
                    )
                    if player.previous_legend_rank:
                        embed.add_field(
                            name='**Previous Rank | Trophies**',
                            value=f"{player.previous_legend_rank} | {player.previous_legend_trophies}",
                            inline=True
                        )
                    if player.current_legend_rank:
                        embed.add_field(
                            name='**Current Rank | Trophies**',
                            value=f"{player.current_legend_rank} | {player.current_legend_trophies}",
                            inline=True
                        )

                if not player.league_id:
                    embed.set_thumbnail(
                        url='https://api-assets.clashofclans.com/leagues/72/e--YMyIexEQQhE4imLoJcwhYn6Uy8KqlgyY3_kFV6t4.png')
                else:
                    embed.set_thumbnail(url=player.league_icons['medium'])
                embed.add_field(
                    name='**War Stars**',
                    value=player.war_stars,
                    inline=True
                )
                if player.clan_lvl:
                    embed.add_field(
                        name='**Clan**',
                        value=f"[{player.clan_name}](https://link.clashofclans.com/en?action=OpenClanProfile&tag={player.clan_tag[1:]})",
                        inline=True
                    )

                    if player.role == 'leader':
                        role_name = 'Leader'
                    elif player.role == 'coLeader':
                        role_name = 'Co-Leader'
                    elif player.role == 'admin':
                        role_name = 'Elder'
                    else:
                        role_name = 'Member'
                    embed.add_field(
                        name='**Clan Role**',
                        value=role_name,
                        inline=True
                    )
                else:
                    embed.add_field(
                        name='**Clan**',
                        value=f"{player.name} is not in a clan",
                        inline=True
                    )

                hero_title = ''
                hero_value = ''
                for hero in player.heroes:
                    if hero.name == 'Barbarian King':
                        hero_title = 'BK'
                        hero_value = f'{hero.lvl}'
                    elif hero.name == 'Archer Queen':
                        hero_title += ' | AQ'
                        hero_value += f' | {hero.lvl}'
                    elif hero.name == 'Grand Warden':
                        hero_title += ' | GW'
                        hero_value += f' | {hero.lvl}'
                    elif hero.name == 'Royal Champion':
                        hero_title += ' | RC'
                        hero_value += f' | {hero.lvl}'
                    else:
                        break
                if hero_title != '':
                    embed.add_field(
                        name=f'**{hero_title}**',
                        value=hero_value,
                        inline=True
                    )

                pet_title = ''
                pet_value = ''
                for troop in player.troops:
                    if troop.name == 'L.A.S.S.I':
                        pet_title = 'LA'
                        pet_value = f'{troop.lvl}'
                    elif troop.name == 'Mighty Yak':
                        pet_title += ' | MY'
                        pet_value += f' | {troop.lvl}'
                    elif troop.name == 'Electro Owl':
                        pet_title += ' | EO'
                        pet_value += f' | {troop.lvl}'
                    elif troop.name == 'Unicorn':
                        pet_title += ' | UC'
                        pet_value += f' | {troop.lvl}'
                if pet_title != '':
                    embed.add_field(
                        name=f'**{pet_title}**',
                        value=pet_value,
                        inline=True
                    )

                embed.add_field(
                    name='**Link**',
                    value=f"[{player.name}](https://link.clashofclans.com/en?action=OpenPlayerProfile&tag={player.tag[1:]})",
                    inline=True
                )

                # todo set footer to display user called and timestamp
                embed.set_footer(
                    text=ctx.author.display_name,
                    icon_url=ctx.author.avatar_url.BASE+ctx.author.avatar_url._url
                )

                await ctx.send(embed=embed)
            else:
                # if player is not found
                await ctx.send(f"Could not find player with tag {db_player_obj.player_tag}")

        else:
            await ctx.send(f"{ctx.author.mention} does not "
                           f"have an active player")
    else:
        # if user is not found
        await ctx.send(f"{ctx.author.mention} has not been claimed")


@client.command(
    aliases=['updateactiveplayer'],
    brief='discord',
    description=(
        "updates the user's active player")
)
async def updateplayeractive(ctx, player_tag):

    player_obj = clash_responder.get_player(player_tag, razbot_data.header)

    user = db_responder.read_user(ctx.author.id)
    # if user is found
    if user:
        db_player_obj = db_responder.read_player(ctx.author.id, player_obj.tag)
        if db_player_obj:
            if db_player_obj.active:
                await ctx.send(f"{player_obj.name} is already your active player {ctx.author.mention}")
            else:
                db_player_obj = db_responder.update_player_active(
                    ctx.author.id, player_obj.tag)
                await ctx.send(f"{player_obj.name} is now your active player {ctx.author.mention}")
        else:
            await ctx.send(f"{ctx.author.mention} has not claimed {player_obj.name}")
    # if user is not found
    else:
        await ctx.send(f"{ctx.author.mention} has not been claimed")


@client.command(
    aliases=['removeplayer'],
    brief='discord',
    description=(
        "deletes the requested user's player")
)
async def deleteplayer(ctx, player_tag):

    player_obj = clash_responder.get_player(player_tag, razbot_data.header)
    if player_obj:
        # if player is found in clash
        author = ctx.author
        user = db_responder.read_user(author.id)
        # if user is found
        if user:
            if db_responder.read_player(author.id, player_obj.tag):
                # if the player is claimed by user
                db_player_obj = db_responder.delete_player(
                    author.id, player_obj.tag)
                # if player was not deleted
                if db_player_obj:
                    await ctx.send(f"{player_obj.name} could not be deleted "
                                   f"from {author.mention} player list")
                # if player was deleted
                else:
                    # check if there is a active player
                    active_player_data = db_responder.read_player_active(
                        author.id)

                    if active_player_data:
                        # if there is a active player
                        # then no need to change the active
                        await ctx.send(f"{player_obj.name} has been deleted "
                                       f"from {author.mention} player list")
                    else:
                        # if there is no active player
                        # check if there are any other players
                        player_list = db_responder.read_player_list(
                            author.id)
                        if len(player_list) == 0:
                            # no additional players claimed by user
                            await ctx.send(
                                f"{player_obj.name} has been deleted "
                                f"{author.mention} has no more claimed players"
                            )
                        else:
                            # if there are additional players claimed by user
                            # update the first as the new active
                            updated_active_player = db_responder.update_player_active(
                                author.id, player_list[0].player_tag)
                            if updated_active_player:
                                # if update was successful
                                clash_updated_active_player = clash_responder.get_player(
                                    updated_active_player.player_tag, razbot_data.header)
                                await ctx.send(
                                    f"{player_obj.name} has been deleted "
                                    f"{author.mention} active is now set to "
                                    f"{clash_updated_active_player.name}"
                                )
            else:
                # if player is not claimed by user
                await ctx.send(f"{player_obj.name} is not claimed by"
                               f" {author.mention}")

        # if user is not found
        else:
            await ctx.send(f"{author.mention} has not been claimed")
    else:
        # if player is not found in clash
        await ctx.send(f"{player_tag} was not found")


# client guild
@client.command(
    aliases=['claim_guild', 'guildclaim'],
    brief='discord',
    description=(
        'This will claim a discord guild')
)
async def claimguild(ctx):
    # getting db user object
    user_obj = db_responder.read_user(ctx.author.id)
    if user_obj:
        if user_obj.admin or user_obj.super_user:
            # only for admin or super user use
            guild_obj = db_responder.claim_guild(ctx.author.id, ctx.guild.id)
            # if guild wasn't claimed and now is
            if guild_obj:
                await ctx.send(f"{ctx.guild.name} is now claimed "
                               f"by admin user {ctx.author.mention}")
            # if guild was already claimed
            else:
                await ctx.send(f"{ctx.guild.name} has already been claimed")
        else:
            await ctx.send(f"{ctx.author.mention} is not an admin")
    else:
        await ctx.send(f"{ctx.author.mention} has not been claimed")


# client clan
# todo pull the clan tag from the db player to player tag to player.clan_tag
# ? simplify this...
@client.command(
    aliases=['clanclaim'],
    brief='discord',
    description=(
        'This will claim the clan your '
        'active player is currently a member of')
)
async def claimclan(ctx, clan_tag):
    clan_obj = clash_responder.get_clan(clan_tag, razbot_data.header)
    if clan_obj:
        # if clan is found
        claimed_clan_obj = db_responder.read_clan(ctx.guild.id, clan_tag)
        if claimed_clan_obj:
            # already claimed
            await ctx.send(f"{clan_obj.name} has already been claimed")
        else:
            # getting db user object
            user_obj = db_responder.read_user(ctx.author.id)
            # getting db guild object
            guild_obj = db_responder.read_guild(ctx.guild.id)
            if user_obj:
                # ? consolidate if user and if guild into one
                # if user has been claimed
                if guild_obj:
                    if (guild_obj.admin_user_id == ctx.author.id
                            or user_obj.super_user):
                        # if user is guild admin or super user
                        db_player_obj = db_responder.read_player_active(
                            ctx.author.id)
                        if db_player_obj:
                            # if active player is found
                            player_obj = clash_responder.get_player(
                                db_player_obj.player_tag, razbot_data.header)
                            if player_obj.clan_tag == clan_obj.tag:
                                # if player is in requested clan
                                db_clan_obj = db_responder.claim_clan(
                                    ctx.guild.id, clan_obj.tag)
                                if db_clan_obj:
                                    # if clan has been claimed and returned
                                    await ctx.send(
                                        f"{clan_obj.name} has been claimed")
                                else:
                                    await ctx.send(f"Couldn't claim {clan_obj.name}")
                            else:
                                await ctx.send(f"{ctx.author.mention} is not in {clan_obj.name}")
                        else:
                            await ctx.send(f"{ctx.author.mention} has no active player")
                    else:
                        await ctx.send(f"{ctx.author.mention} is not guild's admin")
                else:
                    await ctx.send(f"{ctx.guild.name} has not been claimed")
            else:
                await ctx.send(f"{ctx.author.mention} has not been claimed")
    else:
        await ctx.send(f"Couldn't find clan {clan_tag}")


@client.command(
    aliases=['showclaimclan', 'showclan', 'showclans', 'showclaimedclan',
             'showclaimedclans', 'showclansclaim', 'showclanlist'],
    brief='discord',
    description=(
        'Shows clans claimed by a discord guild')
)
async def showclanclaim(ctx):
    db_guild_obj = db_responder.read_guild(ctx.guild.id)

    if db_guild_obj:
        # if guild is found
        db_clan_obj_list = db_responder.read_clan_list_from_guild(ctx.guild.id)
        if len(db_clan_obj_list) == 0:
            # if guild is found, but has no claimed clans
            await ctx.send(f"{ctx.guild.name} does not have any "
                           f"claimed clans")
        else:
            message = f"{ctx.guild.name} has claimed "
            for item in db_clan_obj_list:
                clan = clash_responder.get_clan(
                    item.clan_tag, razbot_data.header)
                message += f"{clan.name} {clan.tag}, "
            # cuts the last two characters from the string ', '
            message = message[:-2]
            await ctx.send(message)
    else:
        # if guild is not found in db
        await ctx.send(f"{ctx.guild.name} has not been claimed")


@client.command(
    aliases=['removeclan', 'deleteclanclaim',
             'deleteclaimclan', 'deleteclaimedclan'],
    brief='discord',
    description=(
        "deletes the requested user's clan")
)
async def deleteclan(ctx, clan_tag):
    clan_obj = clash_responder.get_clan(clan_tag, razbot_data.header)
    if clan_obj:
        # clan has been found in clash
        db_user_obj = db_responder.read_user(ctx.author.id)
        if db_user_obj:
            # user is found in db
            db_guild_obj = db_responder.read_guild(ctx.guild.id)
            if db_guild_obj:
                # guild is found in db
                if (db_guild_obj.admin_user_id == ctx.author.id
                        or db_user_obj.super_user):
                    # author is guild admin or user is super user
                    db_clan_obj = db_responder.read_clan(
                        ctx.guild.id, clan_obj.tag)
                    if db_clan_obj:
                        # clan is found in db
                        db_clan_found = db_responder.delete_clan(
                            ctx.guild.id, clan_obj.tag)
                        if db_clan_found:
                            await ctx.send(f"{clan_obj.name} could "
                                           f"not be deleted")
                        else:
                            await ctx.send(f"{clan_obj.name} has been "
                                           f"deleted from {ctx.guild.name}")
                    else:
                        # clan is not found in db
                        await ctx.send(f"{clan_obj.name} has "
                                       f"not been claimed")
                else:
                    await ctx.send(f"{ctx.author.mention} is not guild's admin")
            else:
                # guild is not found in db
                await ctx.send(f"{ctx.guild.name} has not been claimed")
        else:
            # user is not found in db
            await ctx.send(f"{ctx.author.mention} has not been claimed")
    else:
        # clan is not found in clash
        await ctx.send(f"{clan_tag} was not found")


# client clan role
@client.command(
    aliases=['clanroleclaim'],
    brief='discord',
    description=(
        "This will claim a clan's discord role")
)
async def claimclanrole(ctx, clan_tag):

    if len(ctx.message.role_mentions) > 0:
        # if the role has been mentioned
        role = ctx.message.role_mentions[0]
        # get the clash of clans clan object
        clan_obj = clash_responder.get_clan(clan_tag, razbot_data.header)
        if clan_obj:
            # if clan is found
            db_clan_obj = db_responder.read_clan(ctx.guild.id, clan_tag)
            if db_clan_obj:
                # claimed by guild
                # getting db user object
                user_obj = db_responder.read_user(ctx.author.id)
                # getting db guild object
                guild_obj = db_responder.read_guild(ctx.guild.id)
                if user_obj:
                    # ? consolidate if user and if guild into one
                    # if user has been claimed
                    if guild_obj:
                        # if guild has been claimed
                        if (guild_obj.admin_user_id == ctx.author.id
                                or user_obj.super_user):
                            # if user is guild admin or super user
                            # confirm role has not been claimed
                            clan_role_obj = db_responder.read_clan_role(
                                role.id)
                            if clan_role_obj:
                                # clan role has been claimed
                                await ctx.send(f"{role.mention} has already been claimed")
                            else:
                                # clan role has not been claimed
                                # claim clan role
                                db_clan_role_obj = db_responder.claim_clan_role(
                                    role.id, ctx.guild.id, clan_obj.tag)
                                if db_clan_role_obj:
                                    # if clan role has been claimed and returned
                                    await ctx.send(
                                        f"{role.mention} has been claimed")
                                else:
                                    await ctx.send(f"Couldn't claim requested discord role")
                        else:
                            await ctx.send(f"{ctx.author.mention} is not guild's admin")
                    else:
                        await ctx.send(f"{ctx.guild.name} has not been claimed")
                else:
                    await ctx.send(f"{ctx.author.mention} has not been claimed")
            else:
                await ctx.send(f"{clan_obj.name} is not claimed "
                               f"within {ctx.guild.name}")
        else:
            await ctx.send(f"Couldn't find clan {clan_tag}")
    else:
        await ctx.send(f"You have to mention the role")


@client.command(
    aliases=['removeclanroleclaim'],
    brief='discord',
    description=(
        "This will remove the claimed clan's discord role, "
        "the role will not be deleted from discord.")
)
async def removeclaimclanrole(ctx):
    if len(ctx.message.role_mentions) > 0:
        # if the role has been mentioned
        role = ctx.message.role_mentions[0]
        # getting db user object
        user_obj = db_responder.read_user(ctx.author.id)
        # getting db guild object
        guild_obj = db_responder.read_guild(ctx.guild.id)
        if user_obj:
            # ? consolidate if user and if guild into one
            # if user has been claimed
            if guild_obj:
                # if guild has been claimed
                if (guild_obj.admin_user_id == ctx.author.id
                        or user_obj.super_user):
                    # if user is guild admin or super user
                    # get clan role from db
                    clan_role_obj = db_responder.read_clan_role(role.id)
                    if clan_role_obj:
                        # clan role has been claimed in db
                        # remove the clan role from db
                        db_clan_role_found = db_responder.delete_clan_role(
                            role.id)
                        if db_clan_role_found:
                            # clan role was found after deletion
                            await ctx.send(f"{role.mention} "
                                           f"could not be deleted from database")
                        else:
                            # clan role wasn't found after deletion
                            await ctx.send(f"{role.mention} "
                                           f"was deleted from database")
                    else:
                        await ctx.send(f"{role.mention} is not claimed")
                else:
                    await ctx.send(f"{ctx.author.mention} is not guild's admin")
            else:
                await ctx.send(f"{ctx.guild.name} has not been claimed")
        else:
            await ctx.send(f"{ctx.author.mention} has not been claimed")
    else:
        await ctx.send(f"You have to mention the role")


# client rank role
@client.command(
    aliases=['rankroleclaim'],
    brief='discord',
    description=(
        "This will claim a rank's discord role")
)
async def claimrankrole(ctx, rank_role_name):
    if len(ctx.message.role_mentions) > 0:
        # if the role has been mentioned
        role = ctx.message.role_mentions[0]
        # validate given role name with model
        rank_role_model_obj = db_responder.read_rank_role_model(
            rank_role_name)
        if rank_role_model_obj:
            # getting db user object
            user_obj = db_responder.read_user(ctx.author.id)
            # getting db guild object
            guild_obj = db_responder.read_guild(ctx.guild.id)
            if user_obj:
                # ? consolidate if user and if guild into one
                # if user has been claimed
                if guild_obj:
                    # if guild has been claimed
                    if (guild_obj.admin_user_id == ctx.author.id
                            or user_obj.super_user):
                        # user is guild admin or super user
                        # confirm role has not been claimed
                        rank_role_obj = db_responder.read_rank_role(role.id)
                        if rank_role_obj:
                            # rank role has been claimed
                            await ctx.send(f"{role.mention} has already been claimed")
                        else:
                            # rank role has not been claimed
                            # claim rank role
                            db_rank_role_obj = db_responder.claim_rank_role(
                                role.id, ctx.guild.id, rank_role_name)
                            if db_rank_role_obj:
                                # if rank role has been claimed and returned
                                await ctx.send(
                                    f"{role.mention} has been claimed")
                            else:
                                await ctx.send(f"Couldn't claim requested discord role")
                    else:
                        await ctx.send(f"{ctx.author.mention} is not guild's admin")
                else:
                    await ctx.send(f"{ctx.guild.name} has not been claimed")
            else:
                await ctx.send(f"{ctx.author.mention} has not been claimed")
        else:
            await ctx.send(f"Invalid rank name given")
    else:
        await ctx.send(f"You have to mention the role")


@client.command(
    aliases=['removerankroleclaim'],
    brief='discord',
    description=(
        "This will remove the claimed rank's discord role, "
        "the role will not be deleted from discord.")
)
async def removeclaimrankrole(ctx):
    if len(ctx.message.role_mentions) > 0:
        # if the role has been mentioned
        role = ctx.message.role_mentions[0]
        # getting db user object
        user_obj = db_responder.read_user(ctx.author.id)
        # getting db guild object
        guild_obj = db_responder.read_guild(ctx.guild.id)
        if user_obj:
            # ? consolidate if user and if guild into one
            # if user has been claimed
            if guild_obj:
                # if guild has been claimed
                if (guild_obj.admin_user_id == ctx.author.id
                        or user_obj.super_user):
                    # if user is guild admin or super user
                    # get rank role from db
                    rank_role_obj = db_responder.read_rank_role(role.id)
                    if rank_role_obj:
                        # rank role has been claimed in db
                        # remove the rank role from db
                        db_rank_role_found = db_responder.delete_rank_role(
                            role.id)
                        if db_rank_role_found:
                            # rank role was found after deletion
                            await ctx.send(f"{role.mention} "
                                           f"could not be deleted from database")
                        else:
                            # rank role wasn't found after deletion
                            await ctx.send(f"{role.mention} "
                                           f"was deleted from database")
                    else:
                        await ctx.send(f"{role.mention} is not claimed")
                else:
                    await ctx.send(f"{ctx.author.mention} is not guild's admin")
            else:
                await ctx.send(f"{ctx.guild.name} has not been claimed")
        else:
            await ctx.send(f"{ctx.author.mention} has not been claimed")
    else:
        await ctx.send(f"You have to mention the role")


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
    print(f'{member} has left the server')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"command '{ctx.invoked_with}' could not be found")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"command '{ctx.invoked_with}' "
                       f"requires more information")
    else:
        await ctx.send(f"there was an error that I have not accounted for, "
                       f"please let Razgriz know")

client.run(razbot_data.token)
