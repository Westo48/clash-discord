import discord
from discord.ext import commands
from discord.utils import get
from ClashResponder import *
from DiscordResponder import *


# todo make another .py file for client clan class and methods
class ClientClan(object):
    def __init__(
        self, tag, name, emoji_id
    ):
        self.tag = tag
        self.name = name
        self.emoji_id = emoji_id


client = commands.Bot(command_prefix='!')

leader_role = '👑Leaders👑'

time_zone = (-5)
raz_tag = '#RGQ8RGU9'
header = {
    'Accept': 'application/json',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjkyNWJjYzg1LWFhZDktNGM2NC05M2Y2LWM4MWEwZGVhOGUwNiIsImlhdCI6MTU3NDYyMjY3Nywic3ViIjoiZGV2ZWxvcGVyLzdjZmJkOWFjLTFlYzAtNDI3OS1jODM2LTU0YzMxN2FlZmE4NiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjEwOC4yMTEuOTUuMjU0Il0sInR5cGUiOiJjbGllbnQifV19.gdc-4-OEZzsYBLk8HfqZBH-idvlK1vX9nim91XEqLgwNAyarfZquxfkZDKPsswUGyiXRIFV7Am3RB7iWtd9T5w'
}
client_clans = [
    (ClientClan('#28LRPVP8C', '6ers', 753096212969816144)),
    (ClientClan('#88UUULPU', 'Regis', 753096189213278298))
]
bot_categories = [
    {
        'name': 'Discord',
        'brief': 'discord',
        'emoji': ':computer:'
    },
    {
        'name': 'Misc',
        'brief': 'misc',
        'emoji': ':iphone:'
    },
    {
        'name': 'Player',
        'brief': 'player',
        'emoji': ':sunglasses:'
    },
    {
        'name': 'Clan',
        'brief': 'clan',
        'emoji': ':fire:'
    },
    {
        'name': 'War',
        'brief': 'war',
        'emoji': ':crossed_swords:'
    },
    {
        'name': 'CWL Group',
        'brief': 'cwlgroup',
        'emoji': ':shield:'
    },
    {
        'name': 'CWL War',
        'brief': 'cwlwar',
        'emoji': ':dagger:'
    }
]
guild_emoji_dict = {
    'legacy': 753096212969816144,
    'regis': 753096189213278298,
    'legends': 753096689405001728,
    'titan': 753096677661081649,
    'master': 753096714977542144,
    'crystal': 753096731234664548,
    '9': 753340589600276567,
    '10': 753340591248638013,
    '11': 753340591009694288,
    '12': 753340591462416526,
    '13': 753340591101706300,
}
testing_channel_id = 756197533818028184


@client.event
async def on_ready():
    print('RazBot is ready')


@client.command(
    brief='discord',
    description='Returns the help text you see before you'
)
async def helpme(ctx):
    embed = discord.Embed(
        colour=discord.Colour.blue()
    )
    embed.set_author(
        name="[!] RazClashBot", icon_url="https://cdn.discordapp.com/avatars/649107156989378571/053f201109188da026d0a980dd4136e0.webp")
    # embed.set_image(
    #     url="https://i.imgur.com/rwgo8fJ.jpg")
    embed.set_thumbnail(
        url="https://i.imgur.com/JBt2Kwt.gif")

    user_clan = find_user_clan(
        player_name_string(ctx.author.display_name),
        client_clans, ctx.author.roles, header
    )

    for item in bot_categories:
        brief = item['brief']

        if (user_clan != ''
                and brief == 'clan'):
            clan_emoji = ctx.bot.get_emoji(user_clan.emoji_id)
            emoji = f"<:{clan_emoji.name}:{clan_emoji.id}>"
        else:
            emoji = item['emoji']

        embed.add_field(
            name="__**"+item['name'] + "**__",
            value=emoji,
            inline=False
        )
        for command in ctx.bot.all_commands.items():
            if (
                command[1].brief == brief
                and command[1].description != ''
                and command[0] == command[1].name
                and not command[1].hidden
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
        name="[!] RazClashBot", icon_url="https://cdn.discordapp.com/avatars/649107156989378571/053f201109188da026d0a980dd4136e0.webp")
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

'''
@client.command(brief='discord')
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour=discord.Colour.blue()
    )
    embed.set_author(
        name="[!] RazClashBot", icon_url="https://cdn.discordapp.com/avatars/649107156989378571/053f201109188da026d0a980dd4136e0.webp")
    # embed.set_image(
    #     url="https://i.imgur.com/rwgo8fJ.jpg")
    embed.set_thumbnail(
        url="https://i.imgur.com/MFZp1Fy.gif")

    embed.add_field(
        name="Discord Commands", value=":computer:", inline=False)
    embed.add_field(
        name="role",
        value="Grabs your nickname and gives you the role in the "
        "clan you are in. (CURRENTLY ONLY AN EXAMPLE)",
        inline=False
    )
    embed.add_field(
        name="Hello There",
        value="Funsies command (CURRENTLY ONLY FOR EXAMPLE)",
        inline=False
    )

    embed.add_field(
        name="Player Commands", value=":sunglasses:", inline=False)
    embed.add_field(
        name=f"{ctx.bot.all_commands['trooplvl'].name} <troop name>",
        value=ctx.bot.all_commands['trooplvl'].description,
        inline=False
    )

    embed.add_field(
        name="Clan", value="Clan commands", inline=False)
    embed.add_field(
        name=f"{ctx.bot.all_commands['donationchecker'].name} <troop name> | [donation, donate]",
        value=ctx.bot.all_commands['donationchecker'].description,
        inline=False
    )

    embed.add_field(
        name="War",
        value=":crossed_swords:",
        inline=False
    )
    embed.add_field(
        name=f"{ctx.bot.all_commands['waroverview'].name} | [war]",
        value=ctx.bot.all_commands['waroverview'].description,
        inline=False
    )
    embed.add_field(
        name=ctx.bot.all_commands['wartime'].name,
        value=ctx.bot.all_commands['wartime'].description,
        inline=False
    )
    embed.add_field(
        name=f"{ctx.bot.all_commands['warnoattack'].name} | [warnoatk]",
        value=ctx.bot.all_commands['warnoattack'].description,
        inline=False
    )
    embed.add_field(
        name=f"{ctx.bot.all_commands['warnoattackalert'].name} | [warnoatkalert]",
        value=ctx.bot.all_commands['warnoattackalert'].description,
        inline=False
    )

    embed.add_field(
        name="CWL Group",
        value=":shield:",
        inline=False
    )
    embed.add_field(
        name="WIP",
        value="This section is still a work in progress",
        inline=False
    )

    embed.add_field(
        name="CWL War",
        value=":dagger:",
        inline=False
    )
    embed.add_field(
        name=f"{ctx.bot.all_commands['cwlwaroverview'].name} | [cwlwar]",
        value=ctx.bot.all_commands['cwlwaroverview'].description,
        inline=False
    )
    embed.add_field(
        name=ctx.bot.all_commands['cwlwartime'].name,
        value=ctx.bot.all_commands['cwlwartime'].description,
        inline=False
    )
    embed.add_field(
        name=f"{ctx.bot.all_commands['cwlwarnoattack'].name} | [cwlwarnoatk]",
        value=ctx.bot.all_commands['cwlwarnoattack'].description,
        inline=False
    )
    embed.add_field(
        name=ctx.bot.all_commands['cwlmemberscore'].name,
        value=ctx.bot.all_commands['cwlmemberscore'].description,
        inline=False
    )
    embed.add_field(
        name=ctx.bot.all_commands['cwlclanmatescore'].name,
        value=ctx.bot.all_commands['cwlclanmatescore'].description,
        inline=False
    )

    embed.set_footer(
        text="If you have a question mention Razgriz. "
        "Please note this is still a work in progress "
        "and there will be bugs to work out.")

    await ctx.send(embed=embed)
'''


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
        name="[!] RazClashBot", icon_url="https://cdn.discordapp.com/avatars/649107156989378571/053f201109188da026d0a980dd4136e0.webp")
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
    if player.th_weapon_lvl != 0:
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
        embed.add_field(
            name='**League**',
            value=f'{player.name} is not in a league',
            inline=True
        )
    else:
        embed.set_thumbnail(url=player.league_icons['medium'])
        embed.add_field(
            name='**League**',
            value=player.league_name,
            inline=True
        )
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
        embed.add_field(
            name='**VS Trophies**',
            value=player.vs_trophies,
            inline=True
        )
        embed.add_field(
            name='**Best VS Trophies**',
            value=player.best_vs_trophies,
            inline=True
        )

    for troop in player.troops:
        if troop.name == 'Barbarian King':
            embed.add_field(
                name='**Barbarian King**',
                value=troop.lvl,
                inline=True
            )
        elif troop.name == 'Archer Queen':
            embed.add_field(
                name='**Archer Queen**',
                value=troop.lvl,
                inline=True
            )
        elif troop.name == 'Grand Warden':
            embed.add_field(
                name='**Grand Warden**',
                value=troop.lvl,
                inline=True
            )
        elif troop.name == 'Royal Champion':
            embed.add_field(
                name='**Royal Champion**',
                value=troop.lvl,
                inline=True
            )
        else:
            break

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
    description='Enter troop/hero/spell to see its '
                'current, th max, and max level.'
)
async def trooplvl(ctx, *, troop_name):
    player_name = player_name_string(ctx.author.display_name)
    user_clan = find_user_clan(
        player_name, client_clans, ctx.author.roles, header)
    if user_clan != '':
        await ctx.send(response_troop_lvl(
            player_name, troop_name, user_clan.tag, header))
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
    if user_clan != '':
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
    if user_clan != '':
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
    if user_clan != '':
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
    if user_clan != '':
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
    if user_clan != '':
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
    if user_clan != '':
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
    if user_clan != '':
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
    if user_clan != '':
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
    if user_clan != '':
        for line in response_war_all_member_standing(user_clan.tag, time_zone, header):
            await ctx.send(f'{line}')
    else:
        await ctx.send(f"Couldn't find {ctx.author.display_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


# CWL Group
# todo cwl_group overview, scoreboard, cwl_clan_noatk


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
    if user_clan != '':
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
    if user_clan != '':
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
    if user_clan != '':
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
    if user_clan != '':
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
    if user_clan != '':
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
    if user_clan != '':
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
    if user_clan != '':
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
    if user_clan != '':
        clan_emoji = ctx.bot.get_emoji(user_clan.emoji_id)
        await ctx.send(f"<:{clan_emoji.name}:{clan_emoji.id}>")


"""
@client.command(
    aliases=['roleme'],
    brief='discord',
    description=('This will give you your clan role '
                 'here in Discord.')
)
async def role(ctx):
    author = ctx.message.author
    player = response_player(author.display_name, heroes_tag, header)

    # player is found in the clan
    if player != '':
        new_role, old_role = role_switch(player.role, author.roles)

        if old_role != '':
            await author.remove_roles(
                discord.utils.get(author.guild.roles, name=old_role))
        if new_role != '':
            await author.add_roles(
                discord.utils.get(author.guild.roles, name=new_role))

        await ctx.send(f'{author.display_name} now has the role {new_role}')
    else:
        await author.edit(nick=None)
        await ctx.send(f"Couldn't find {author.display_name} in the clan.")
"""


'''
@client.command(
    aliases=['nick'],
    brief='discord',
    description=(
        'This will check the clan with the given name '
        'and set your nickname to the corresponding name '
        'and reset your role')
)
async def nickname(ctx, *, player_name):
    author = ctx.author
    player = response_player(
        player_name, heroes_tag, header)

    # player is found in the clan
    if player != '':
        # gets the new role and current (old) role
        new_role, old_role = role_switch(player.role, author.roles)
        # if the user already has the correct name
        if player.name == author.display_name:
            # don't change the user's nickname
            # getting the user's roles in place
            if old_role != '':
                await author.remove_roles(
                    discord.utils.get(author.guild.roles, name=old_role))
            if new_role != '':
                await author.add_roles(
                    discord.utils.get(author.guild.roles, name=new_role))
            await ctx.send(f'Your nickname does not need to be changed. '
                           f'Your role has been set to {new_role}')

        # if the user doesn't have to correct name & player name is available
        elif nickname_available(player.name, ctx.guild.members):
            # getting the user's roles in place
            if old_role != '':
                await author.remove_roles(
                    discord.utils.get(author.guild.roles, name=old_role))
            if new_role != '':
                await author.add_roles(
                    discord.utils.get(author.guild.roles, name=new_role))

            await author.edit(nick=player.name)
            await ctx.send(f'Your nickname has been changed to {player.name} '
                           f'and your role has been changed to {new_role}')

        # if the name isn't available and it isn't you that has the name
        else:
            await ctx.send(f'Someone in the channel already has the name '
                           f'{player.name}')
    else:
        new_role, old_role = role_switch('Uninitiated', author.roles)
        # getting the user's roles in place
        if old_role != '':
            await author.remove_roles(
                discord.utils.get(author.guild.roles, name=old_role))
        if new_role != '':
            await author.add_roles(
                discord.utils.get(author.guild.roles, name=new_role))

        await author.edit(nick=None)
        channel = channel_changer(ctx, welcome_channel_id)
        await channel.send(f"Couldn't find {player_name} in the clan."
                           f"Your role and nickname have been reset.")
'''

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
            # leave Uninitiated members alone
            if role_check('Uninitiated', member.roles):
                pass
            # all initiated members
            else:
                player = response_player(
                    member.display_name, heroes_tag, header)

                # the player is found in the given clan
                if player != '':
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

"""
@client.event
async def on_member_join(member):
    member_role = discord.utils.get(member.guild.roles, name='Uninitiated')
    await member.add_roles(member_role)
"""


@client.event
async def on_member_remove(member):
    print(f'{member} has left the server')


client.run('NjQ5MTA3MTU2OTg5Mzc4NTcx.Xd3-Jg.OM20CTzSqwFPjrl0PMQQRocG87w')
