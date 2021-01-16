import discord
from discord.ext import commands
from discord.utils import get
from ClashResponder import *
from DiscordResponder import *


intents = discord.Intents.all()

client = commands.Bot(command_prefix='!', intents=intents)
client.remove_command('help')

# todo make another .py file for client clan class and methods
# had emoji id as well


class ClientClan(object):
    def __init__(
        self, name,  tag, emoji_name, emoji_id
    ):
        self.name = name
        self.tag = tag
        self.emoji_name = emoji_name
        self.emoji_id = emoji_id


class ClientRole(object):
    def __init__(
        self, name, tag, is_clash_role
    ):
        self.name = name
        self.tag = tag
        self.is_clash_role = is_clash_role


client_roles = {
    'TheMightyHeroes': ClientRole('TheMightyHeroes', 799031143633518604, True),
    'wild side': ClientRole('sild side', 799031364984242216, True),
    'admin': ClientRole('admin', 798606035539591169, False),
    'bot': ClientRole('bot', 798610168018632784, False),
    'dev': ClientRole('dev', 798610076528672808, False),
    'leader': ClientRole('leader', 798605886300880936, True),
    'co-leader': ClientRole('co-leader', 798608772783800361, True),
    'elder': ClientRole('elder', 798608564494139443, True),
    'member': ClientRole('member', 798608480033964093, True),
    'community': ClientRole('community', 798616833628438549, False),
    'underground': ClientRole('underground', 798729981336354836, False),
    'uninitiated': ClientRole('uninitiated', 798610698337779713, False)
}
leader_role = 'leader'
time_zone = (-5)
raz_tag = '#RGQ8RGU9'
heroes_tag = '#JJRJGVR0'
header = {
    'Accept': 'application/json',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjkyNWJjYzg1LWFhZDktNGM2NC05M2Y2LWM4MWEwZGVhOGUwNiIsImlhdCI6MTU3NDYyMjY3Nywic3ViIjoiZGV2ZWxvcGVyLzdjZmJkOWFjLTFlYzAtNDI3OS1jODM2LTU0YzMxN2FlZmE4NiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjEwOC4yMTEuOTUuMjU0Il0sInR5cGUiOiJjbGllbnQifV19.gdc-4-OEZzsYBLk8HfqZBH-idvlK1vX9nim91XEqLgwNAyarfZquxfkZDKPsswUGyiXRIFV7Am3RB7iWtd9T5w'
}
client_clans = [
    (ClientClan('TheMightyHeroes', '#JJRJGVR0',
                "the_mighty_heroes", 798999641269207090)),
    (ClientClan('wild side', '#2QQRLQV',
                "wild_side", 799045915268743228))
]
bot_categories = [
    {
        'name': 'DISCORD',
        'brief': 'discord',
        'description': 'Discord based commands',
        'emoji': ':computer:'
    },
    # {
    #     'name': 'MISC',
    #     'brief': 'misc',
    #     'description': 'Misc commands',
    #     'emoji': ':iphone:'
    # },
    {
        'name': 'PLAYER',
        'brief': 'player',
        'description': 'Player based commands',
        'emoji': ':sunglasses:'
    },
    {
        'name': 'CLAN',
        'brief': 'clan',
        'description': 'Clan based commands',
        'emoji': ':fire:'
    },
    {
        'name': 'WAR',
        'brief': 'war',
        'description': 'War based commands',
        'emoji': ':crossed_swords:'
    },
    {
        'name': 'CWL GROUP',
        'brief': 'cwlgroup',
        'description': 'CWL Group based commands',
        'emoji': ':shield:'
    },
    {
        'name': 'CWL WAR',
        'brief': 'cwlwar',
        'description': 'CWL War based commands',
        'emoji': ':dagger:'
    }
]
guild_emoji_dict = {
    'the_mighty_heroes': 798999641269207090,
    'wild_side': 799045915268743228,
    'unranked': 798985793313701908,
    'bronze': 798985819754332161,
    'silver': 798985849365725234,
    'gold': 798985865786294303,
    'crystal': 798985900084297768,
    'master': 798985913127534635,
    'champion': 798985927266795611,
    'titan': 798985986947285002,
    'legend': 798986001971281960,
    '1': 798988715170070598,
    '2': 798988734979637348,
    '3': 798988750478639114,
    '4': 798988788923629590,
    '5': 798988789120761917,
    '6': 798988853930754069,
    '7': 798988873257451550,
    '8': 798988892895313930,
    '9': 798983538581045328,
    '10': 798984308265320449,
    '11': 798984326258753597,
    '12': 798984348299690034,
    '13': 798984362606460939,
}
welcome_channel_id = 798605437662134302
testing_channel_id = 798642365648732212
general_channel_id = 798603935022710847


@client.event
async def on_ready():
    print('RazBot is ready')


@client.command(
    aliases=['helpme'],
    brief='discord',
    description='Returns the help text you see before you'
)
# todo allow leader or co-leader
# todo hide clan help if user is not in a clan
async def help(ctx):
    is_leader = role_check(leader_role, ctx.author.roles)

    embed = discord.Embed(
        colour=discord.Colour.blue()
    )
    embed.set_author(
        name=f"[{ctx.prefix}] RazClashBot", icon_url="https://cdn.discordapp.com/avatars/649107156989378571/053f201109188da026d0a980dd4136e0.webp")

    embed.set_thumbnail(
        url="https://i.imgur.com/nwnXABb.gif")

    user_clan = find_user_clan(
        player_name_string(ctx.author.display_name),
        client_clans, ctx.author.roles, header
    )

    for item in bot_categories:
        brief = item['brief']

        if (user_clan
                and brief == 'clan'):
            clan_emoji = ctx.bot.get_emoji(user_clan.emoji_id)
            emoji = f"<:{clan_emoji.name}:{clan_emoji.id}>"
        else:
            emoji = item['emoji']

        embed.add_field(
            name=f"__**{item['name']}**__",
            value=f"{emoji}-----------------",
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


@client.command(brief='discord')
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


@client.command(brief='misc', description='Misc Command')
async def hellothere(ctx):
    await ctx.send(f'General Kenobi')


@client.command(brief='misc')
async def ping(ctx):
    await ctx.send(f'pong {round(client.latency) * 1000}ms')


# Player

@client.command(
    brief='player',
    description="Enter a player's tag and get a player's information"
)
async def player(ctx, *, player_tag):
    if '#' not in player_tag:
        player_tag = '#'+player_tag

    player = Player.get(player_tag, header)

    if player.tag == 0:
        await ctx.send(f"Could not find player with tag {player_tag}")
        return

    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title=player.name,
    )
    embed.set_author(
        name=f"[{ctx.prefix}] RazClashBot", icon_url="https://cdn.discordapp.com/avatars/649107156989378571/053f201109188da026d0a980dd4136e0.webp")
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
    if player.league_id == 0:
        embed.set_thumbnail(
            url='https://api-assets.clashofclans.com/leagues/72/e--YMyIexEQQhE4imLoJcwhYn6Uy8KqlgyY3_kFV6t4.png')
    else:
        embed.set_thumbnail(url=player.league_icons['medium'])
    embed.add_field(
        name='**War Stars**',
        value=player.war_stars,
        inline=True
    )
    if player.clan_lvl == 0:
        embed.add_field(
            name='**Clan**',
            value=f"{player.name} is not in a clan",
            inline=True
        )
    else:
        embed.add_field(
            name='**Clan**',
            value=f"[{player.clan_name}](https://link.clashofclans.com/en?action=OpenClanProfile&tag={player.clan_tag[1:]})",
            inline=True
        )
        embed.add_field(
            name='**Clan Role**',
            value=player.role,
            inline=True
        )
    embed.add_field(
        name='**Donations | Received**',
        value=f"{player.donations} | {player.donations_received}",
        inline=True
    )
    embed.add_field(
        name='**Attack | Defense**',
        value=f"{player.attack_wins} | {player.defense_wins}",
        inline=True
    )
    if player.builder_hall_lvl == 0:
        embed.add_field(
            name='**BH Lvl**',
            value=f"{player.name} has not unlocked their Builder Hall",
            inline=True
        )
    else:
        embed.add_field(
            name='**BH Lvl**',
            value=player.builder_hall_lvl,
            inline=True
        )

    hero_title = ''
    hero_value = ''
    for troop in player.troops:
        if troop.name == 'Barbarian King':
            hero_title = 'BK'
            hero_value = f'{troop.lvl}'
        elif troop.name == 'Archer Queen':
            hero_title += ' | AQ'
            hero_value += f' | {troop.lvl}'
        elif troop.name == 'Grand Warden':
            hero_title += ' | GW'
            hero_value += f' | {troop.lvl}'
        elif troop.name == 'Royal Champion':
            hero_title += ' | RC'
            hero_value += f' | {troop.lvl}'
        else:
            break
    if hero_title != '':
        embed.add_field(
            name=f'**{hero_title}**',
            value=hero_value,
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

'''
    PAT - #8V0L0GJ8
    :exp: Expirence Level
    218
    :classical_building: Townhall Level
    13
    :trophy: Trophies
    2925
    :chart_with_upwards_trend: Highest Trophies
    5144
    :medal: League
    Master League II
    :star: War Stars
    1707
    :european_castle: Clan
    FewGoodMen
    #LL82022R
    :clipboard: Role in Clan
    Elder
    :outbox_tray: Donations | Recieved :inbox_tray:
    1600 | 385
    :crossed_swords: Attack- | Defense Wins :shield:
    60 | 43
    :hammer_pick: Builderhall Level
    7
    :crossed_swords: Versus Battle Wins
    693
    :trophy: Versus Trophies
    2693
    :chart_with_upwards_trend: Highest Versus Trophies
    2723
    :crossed_swords::bow_and_arrow: Total Hero Level
    158
    :link: Open Ingame
    Click me!
    [named links](https://discordapp.com)
    https://clashofclans.com/clans/search/#clanTag=28LRPVP8C


    Semi RH | 6ers | Leader•09/20/2020

'''


@client.command(
    brief='player',
    description='Enter unit to see its current, th max, and max level.'
)
async def trooplvl(ctx, *, troop_name):
    player_name = player_name_string(ctx.author.display_name)
    user_clan = find_user_clan(
        player_name, client_clans, ctx.author.roles, header)
    if user_clan != '':
        await ctx.send(response_troop_lvl(
            ctx.author.display_name, troop_name, heroes_tag, header))
    else:
        await ctx.send(f"Couldn't find {ctx.author.display_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


@client.command(
    brief='player',
    description='Get all your troop levels.',
    hidden=True
)
async def alltrooplvl(ctx):
    player_name = player_name_string(ctx.author.display_name)
    user_clan = find_user_clan(
        player_name, client_clans, ctx.author.roles, header)
    if user_clan:
        for line in response_all_troop_level(ctx.author.display_name, user_clan.tag, header):
            await ctx.send(line)
    else:
        await ctx.send(f"Couldn't find {ctx.author.display_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


# Clan

@client.command(
    aliases=['donation', 'donate'],
    brief='clan',
    description='Enter a troop name to see who in the clan '
                'is best suited to donate that troop.'
)
async def donationchecker(ctx, *, troop_name):
    player_name = player_name_string(ctx.author.display_name)
    user_clan = find_user_clan(
        player_name, client_clans, ctx.author.roles, header)
    if user_clan:
        await ctx.send(response_donation(troop_name, user_clan.tag, header))
    else:
        await ctx.send(f"Couldn't find {ctx.author.display_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


# War
# todo warmember gets a war overview for a specific war member

@client.command(
    aliases=['war'],
    brief='war',
    description='Returns an overview of the current war'
)
async def waroverview(ctx):
    player_name = player_name_string(ctx.author.display_name)
    user_clan = find_user_clan(
        player_name, client_clans, ctx.author.roles, header)
    if user_clan:
        await ctx.send(response_war_overview(user_clan.tag, time_zone, header))
    else:
        await ctx.send(f"Couldn't find {ctx.author.display_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


@client.command(brief='war',
                description='Returns the time remaining in the current war')
async def wartime(ctx):
    player_name = player_name_string(ctx.author.display_name)
    user_clan = find_user_clan(
        player_name, client_clans, ctx.author.roles, header)
    if user_clan:
        await ctx.send(response_war_time(user_clan.tag, time_zone, header))
    else:
        await ctx.send(f"Couldn't find {ctx.author.display_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


@client.command(
    aliases=['warnoatk'],
    brief='war',
    description='Returns a list of players that have/did not use '
                'all possible attacks in the current war'
)
async def warnoattack(ctx):
    player_name = player_name_string(ctx.author.display_name)
    user_clan = find_user_clan(
        player_name, client_clans, ctx.author.roles, header)
    if user_clan:
        await ctx.send(response_war_no_attack(user_clan.tag, time_zone, header))
    else:
        await ctx.send(f"Couldn't find {ctx.author.display_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


@client.command(
    aliases=['warnoatkalert'],
    brief='war',
    description='Returns a list of players that '
                'have/did not use all possible attacks '
                'and mentions them if found'
)
async def warnoattackalert(ctx):
    player_name = player_name_string(ctx.author.display_name)
    user_clan = find_user_clan(
        player_name, client_clans, ctx.author.roles, header)
    if user_clan:
        no_atk_list = war_no_attack_members(
            user_clan.tag, time_zone, header)
        if len(no_atk_list) == 0:
            await ctx.send('Nobody needs to attack.')
        else:
            message = ''
            for player in no_atk_list:
                member = find_channel_member(player.name, ctx.channel.members)
                if member != '':
                    message += f'{member.mention}, '
                else:
                    message += f'{player.name}, '
            message = message[:-2]
            message += ' needs to attack.'
            await ctx.send(message)
    else:
        await ctx.send(f"Couldn't find {ctx.author.display_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


@client.command(
    aliases=['warclan', 'warstars'],
    brief='war',
    description='overview of all members in war',
    hidden=True
)
async def warclanstars(ctx):
    player_name = player_name_string(ctx.author.display_name)
    user_clan = find_user_clan(
        player_name, client_clans, ctx.author.roles, header)
    if user_clan:
        for line in response_war_members_overview(user_clan.tag, time_zone, header):
            await ctx.send(line)
    else:
        await ctx.send(f"Couldn't find {ctx.author.display_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


@client.command(
    aliases=['warallatk'],
    brief='war',
    description='showing all attacks for every member',
    hidden=True
)
async def warallattacks(ctx):
    player_name = player_name_string(ctx.author.display_name)
    user_clan = find_user_clan(
        player_name, client_clans, ctx.author.roles, header)
    if user_clan:
        for line in response_war_all_attacks(user_clan.tag, time_zone, header):
            await ctx.send(f'{line}')
    else:
        await ctx.send(f"Couldn't find {ctx.author.display_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


@client.command(
    aliases=['warscore'],
    brief='war',
    description='showing every member score',
    hidden=True
)
async def warclanscore(ctx):
    player_name = player_name_string(ctx.author.display_name)
    user_clan = find_user_clan(
        player_name, client_clans, ctx.author.roles, header)
    if user_clan:
        for line in response_war_all_member_standing(user_clan.tag, time_zone, header):
            await ctx.send(f'{line}')
    else:
        await ctx.send(f"Couldn't find {ctx.author.display_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


# CWL Group
# todo cwl_group overview, scoreboard, cwl_clan_noatk

@client.command(
    aliases=['cwlgroup'],
    brief='cwlgroup',
    description='Returns the CWL group lineup',
    hidden=False
)
async def cwllineup(ctx):
    player_name = player_name_string(ctx.author.display_name)
    user_clan = find_user_clan(
        player_name, client_clans, ctx.author.roles, header)
    if user_clan:
        cwl_group = CWLGroup.get(user_clan.tag, header)
        cwl_lineup = response_cwl_lineup(cwl_group)
        message = (
            "```\n"
            "CWL Group Lineup\n"
            "13 | 12 | 11 | 10 | 9  | 8  | 7\n"
            "-------------------------------\n"
        )
        for clan_dict in cwl_lineup:
            lineup_message = f"{clan_dict['clan'].name}\n"
            for key in clan_dict:
                if key != 'clan' and key > 6:
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
        await ctx.send(f"Couldn't find {ctx.author.display_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


# CWL War
# todo cwlwar war_time_prep, war_overview_prep, war_overview_round,

@client.command(
    aliases=['cwlwar'],
    brief='cwlwar',
    description='Returns an overview of the current CWL war'
)
async def cwlwaroverview(ctx):
    player_name = player_name_string(ctx.author.display_name)
    user_clan = find_user_clan(
        player_name, client_clans, ctx.author.roles, header)
    if user_clan:
        await ctx.send(response_cwl_war_overview(user_clan.tag, time_zone, header))
    else:
        await ctx.send(f"Couldn't find {ctx.author.display_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


@client.command(brief='cwlwar',
                description='Returns the time remaining in the current CWL war'
                )
async def cwlwartime(ctx):
    player_name = player_name_string(ctx.author.display_name)
    user_clan = find_user_clan(
        player_name, client_clans, ctx.author.roles, header)
    if user_clan:
        await ctx.send(response_cwl_war_time(user_clan.tag, time_zone, header))
    else:
        await ctx.send(f"Couldn't find {ctx.author.display_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


@client.command(
    aliases=['cwlwarnoatk'],
    brief='cwlwar',
    description='Returns a list of players that have/did not use '
                'all possible attacks in the current CWL war'
)
async def cwlwarnoattack(ctx):
    player_name = player_name_string(ctx.author.display_name)
    user_clan = find_user_clan(
        player_name, client_clans, ctx.author.roles, header)
    if user_clan:
        await ctx.send(response_cwl_war_no_attack(user_clan.tag, time_zone, header))
    else:
        await ctx.send(f"Couldn't find {ctx.author.display_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


@client.command(
    aliases=['cwlwarallatk'],
    brief='cwlwar',
    description='showing all attacks for every member in the current war',
    hidden=True
)
async def cwlwarallattack(ctx):
    player_name = player_name_string(ctx.author.display_name)
    user_clan = find_user_clan(
        player_name, client_clans, ctx.author.roles, header)
    if user_clan:
        for line in response_cwl_war_all_attacks(user_clan.tag, time_zone, header):
            await ctx.send(line)
    else:
        await ctx.send(f"Couldn't find {ctx.author.display_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


@client.command(
    aliases=['cwlscore'],
    brief='cwlwar',
    description='Lists each member and their score in CWL',
    hidden=True
)
async def cwlclanscore(ctx):
    player_name = player_name_string(ctx.author.display_name)
    user_clan = find_user_clan(
        player_name, client_clans, ctx.author.roles, header)
    if user_clan:
        for line in response_cwl_clan_standing(user_clan.tag, header):
            await ctx.send(line)
    else:
        await ctx.send(f"Couldn't find {ctx.author.display_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


@client.command(brief='cwlwar',
                description='Lists each score you have in CWL.')
async def cwlmemberscore(ctx):
    player_name = player_name_string(ctx.author.display_name)
    user_clan = find_user_clan(
        player_name, client_clans, ctx.author.roles, header)
    if user_clan:
        await ctx.send(
            response_cwl_member_standing(player_name, user_clan.tag, header))
    else:
        await ctx.send(f"Couldn't find {ctx.author.display_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


@client.command(brief='cwlwar',
                description='Lists each score the specified member has in CWL.')
async def cwlclanmatescore(ctx, *, player_name):
    user_clan = find_user_clan(
        player_name, client_clans, ctx.author.roles, header)
    if user_clan:
        await ctx.send(
            response_cwl_member_standing(player_name, user_clan.tag, header))
    else:
        await ctx.send(f"Couldn't find {player_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


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
    user_clan = find_user_clan(
        player_name_string(ctx.author.display_name),
        client_clans, ctx.author.roles, header
    )
    if user_clan:
        clan_emoji = ctx.bot.get_emoji(user_clan.emoji_id)
        await ctx.send(f"<:{clan_emoji.name}:{clan_emoji.id}>")


@client.command(
    aliases=['roleme'],
    brief='discord',
    description=('This will give you your clan role '
                 'here in Discord.')
)
# ! set up multiple responses for added roles
# ? reset nickname if they are not found in the clan
async def role(ctx):
    author = ctx.message.author
    # if they have the community role
    if role_check(client_roles['community'].name, author.roles):
        await ctx.send(f"You do not need new roles, you have the community role.")
    # if they do not have the community role
    else:
        # check all listed clans for the requested player name
        for clan in client_clans:
            player = response_player(
                author.display_name, clan.tag, header)
            if player:
                break

        # player is found in the clan
        if player:
            # gets the roles to add and remove
            add_roles, remove_roles = role_switch(
                player, author.roles, client_clans)

            # getting the user's roles in place
            for role in remove_roles:
                await author.remove_roles(
                    discord.utils.get(author.guild.roles, name=role))
            for role in add_roles:
                await author.add_roles(
                    discord.utils.get(author.guild.roles, name=role))

            if len(add_roles) > 0:
                await ctx.send(f'{author.display_name} now has the role(s) {add_roles}')
            else:
                await ctx.send(f'{author.display_name} did not change roles')

        else:
            await author.edit(nick=None)
            await ctx.send(f"Couldn't find {author.display_name} in the clan.")


@client.command(
    aliases=['nick'],
    brief='discord',
    description=(
        'This will check the clan with the given name '
        'and set your nickname to the corresponding name '
        'and reset your role')
)
# ! set up multiple responses for added roles
async def nickname(ctx, *, player_name):
    author = ctx.author
    # check all listed clans for the requested player name
    for clan in client_clans:
        player = response_player(
            player_name, clan.tag, header)
        if player:
            break

    # player is found in a clan
    if player:
        # gets the roles to add and remove
        add_roles, remove_roles = role_switch(
            player, author.roles, client_clans)
        # if the user already has the correct name
        if player.name == author.display_name:
            # don't change the user's nickname
            # getting the user's roles in place
            for role in remove_roles:
                await author.remove_roles(
                    discord.utils.get(author.guild.roles, name=role))
            for role in add_roles:
                await author.add_roles(
                    discord.utils.get(author.guild.roles, name=role))

            if len(add_roles) > 0:
                await ctx.send(f'Your nickname does not need to be changed. '
                               f'Your role has been set to {add_roles[-1]}')
            else:
                await ctx.send(f'Your nickname does not need to be changed. '
                               f'No roles have been added.')

        # if the user doesn't have to correct name & player name is available
        elif nickname_available(player.name, ctx.guild.members):
            # getting the user's roles in place
            for role in remove_roles:
                await author.remove_roles(
                    discord.utils.get(author.guild.roles, name=role))
            for role in add_roles:
                await author.add_roles(
                    discord.utils.get(author.guild.roles, name=role))

            await author.edit(nick=player.name)
            await ctx.send(f'Your nickname has been changed to {player.name} '
                           f'and your role has been changed to {add_roles[-1]}')

        # if the name isn't available and it isn't you that has the name
        else:
            await ctx.send(f'Someone in the channel already has the name '
                           f'{player.name}')
    else:
        # set the display_name to the requested name
        # give them community role
        add_roles, remove_roles = role_switch(None, author.roles, client_clans)
        # getting the user's roles in place
        for role in remove_roles:
            await author.remove_roles(
                discord.utils.get(author.guild.roles, name=role))
        for role in add_roles:
            await author.add_roles(
                discord.utils.get(author.guild.roles, name=role))

        await author.edit(nick=player_name)
        await ctx.send(
            f"Couldn't find {player_name} in the clans. "
            f"Your role is set to community "
            f"and nickname has been changed to {player_name}."
        )


"""
@client.command(
    aliases=['member_check'],
    brief = 'discord',
    description = 'Checks for people not in your clan. '
                 'Does not change any current member roles.',
    hidden=True
)
async def all_member_roles(ctx):
    # todo only be able to run this if author is admin
    # admin check
    if role_check('Admin', ctx.author.roles):
        # for each member in the clan
        message_list = []
        for member in ctx.guild.members:
            # leave uninitiated members alone
            if role_check('uninitiated', member.roles):
                pass
            # all initiated members
            else:
                player = response_player(
                    member.display_name, heroes_tag, header)

                # the player is found in the given clan
                if player:
                    # gets the new role and current (old) role
                    new_role, old_role = role_switch(player.role, member.roles)

                    # role hasn't changed
                    if new_role == old_role:
                        pass

                    # role has changed
                    else:
                        # setting the roles for the specified member
                        if old_role != '':
                            await member.remove_roles(
                                discord.utils.get(ctx.guild.roles, name=old_role))
                        if new_role != '':
                            await member.add_roles(
                                discord.utils.get(ctx.guild.roles, name=new_role))

                        message_list.append(f'{member.display_name} now has '
                                            'the role {new_role}')

                # the player is not found in the given clan
                else:
                    await member.edit(nick=None)
                    message_list.append(f"Couldn't find {member.name} "
                                        "in the clan.")

        for line in message_list:
            await ctx.send(line)
"""


@client.event
async def on_member_join(member):
    member_role = discord.utils.get(member.guild.roles, name='uninitiated')
    await member.add_roles(member_role)


@client.event
async def on_member_remove(member):
    print(f'{member} has left the server')


client.run('NjQ5MTA3MTU2OTg5Mzc4NTcx.Xd3-Jg.OM20CTzSqwFPjrl0PMQQRocG87w')
