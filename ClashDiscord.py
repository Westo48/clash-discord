import discord
from discord.ext import commands
from discord.utils import get
from ClashResponder import *
from DiscordResponder import *


client = commands.Bot(command_prefix='!')
raz_tag = '#RGQ8RGU9'
heroes_tag = '#JJRJGVR0'
time_zone = (-5)
header = {
    'Accept': 'application/json',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjkyNWJjYzg1LWFhZDktNGM2NC05M2Y2LWM4MWEwZGVhOGUwNiIsImlhdCI6MTU3NDYyMjY3Nywic3ViIjoiZGV2ZWxvcGVyLzdjZmJkOWFjLTFlYzAtNDI3OS1jODM2LTU0YzMxN2FlZmE4NiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjEwOC4yMTEuOTUuMjU0Il0sInR5cGUiOiJjbGllbnQifV19.gdc-4-OEZzsYBLk8HfqZBH-idvlK1vX9nim91XEqLgwNAyarfZquxfkZDKPsswUGyiXRIFV7Am3RB7iWtd9T5w'
}

welcome_channel_id = 671865539831791636
testing_channel_id = 649146862099759124


@client.event
async def on_ready():
    print('RazBot is ready')


@client.command()
async def helpme(ctx):
    await ctx.send(f'Here are some helpful functions: !ping, !hellothere, !trooplvl, !waroverview, !scoreboard, !war, !noatk, !cwl')


@client.command()
async def hellothere(ctx):
    await ctx.send(f'General Kenobi')


@client.command()
async def ping(ctx):
    await ctx.send(f'pong {round(client.latency) * 1000}ms')


# Player

@client.command(description=('Enter troop/hero/spell to see its '
                             'current, th max, and max level.'))
async def trooplvl(ctx, *, troop_name):
    await ctx.send(response_troop_lvl(ctx.author.display_name, troop_name, heroes_tag, header))


@client.command(description='Get all your troop levels.', hidden=True)
async def alltrooplvl(ctx):
    for line in response_all_troop_level(ctx.author.display_name, heroes_tag, header):
        await ctx.send(line)


# Clan

@client.command(
    aliases=['donation', 'donate'],
    desctiption='Enter a troop name to see who in the clan '
    'is best suited to donate that troop.'
)
async def donationchecker(ctx, *, troop_name):
    await ctx.send(response_donation(troop_name, heroes_tag, header))


# War
# todo warmember gets a war overview for a specific war member

@client.command(aliases=['war', 'scoreboard'])
async def waroverview(ctx):
    await ctx.send(response_war_overview(heroes_tag, time_zone, header))


@client.command()
async def wartime(ctx):
    await ctx.send(response_war_time(heroes_tag, time_zone, header))


@client.command(aliases=['noatk'])
async def noattack(ctx):
    await ctx.send(response_war_no_attack(heroes_tag, time_zone, header))


@client.command(
    aliases=['warmembers', 'warstars', 'warmemstar', 'warmemstars'],
    description='overview of all members in war',
    hidden=True
)
async def warmemberstars(ctx):
    for line in response_war_members_overview(heroes_tag, time_zone, header):
        await ctx.send(line)


@client.command(
    aliases=['allatk'],
    description='showing all attacks for every member',
    hidden=True
)
async def allattacks(ctx):
    for line in response_war_all_attacks(heroes_tag, time_zone, header):
        await ctx.send(f'{line}')


@client.command(
    aliases=['warmemberscore'],
    description='showing every member score',
    hidden=True
)
async def warallmemberscore(ctx):
    for line in response_war_all_member_standing(heroes_tag, time_zone, header):
        await ctx.send(f'{line}')


@client.command(
    description=('enter the amount of storages (not including the TH) '
                 'you are looking for and the amount of gold/elixir '
                 'in TH or one storage')
)
async def warweight(ctx, storages, *, amount):
    return (int(storages) + 1) * int(amount)


# CWL Group
# todo cwl_group overview, scoreboard


# CWL War
# todo cwlwar war_time_prep, war_overview_prep, war_overview_round,

@client.command(
    aliases=['cwlwar'],
    description='shows the overview of the current war league'
)
async def cwlwaroverview(ctx):
    await ctx.send(response_cwl_war_overview(heroes_tag, time_zone, header))


@client.command(
    aliases=['cwltime'],
    description='shows time remaining in the current clan war league'
)
async def cwlwartime(ctx):
    await ctx.send(response_cwl_war_time(heroes_tag, time_zone, header))


@client.command(aliases=['cwlnoatk'])
async def cwlnoattack(ctx):
    await ctx.send(response_cwl_war_no_attack(heroes_tag, time_zone, header))


@client.command(
    aliases=['cwlallatk'],
    description='showing all attacks for every member',
    hidden=True
)
async def cwlallattack(ctx):
    for line in response_cwl_war_all_attacks(heroes_tag, time_zone, header):
        await ctx.send(line)


@client.command(
    aliases=['cwlscore', 'cwlbonus'],
    description='Lists each member and their score in CWL',
    hidden=True
)
async def cwlclanscore(ctx):
    for line in response_cwl_clan_standing(heroes_tag, header):
        await ctx.send(line)


@client.command(aliases=['cwlmemberbonus'],
                description='Lists each score you have in CWL.')
async def cwlmemberscore(ctx):
    await ctx.send(
        response_cwl_member_standing(ctx.author.display_name, heroes_tag, header))


@client.command(aliases=['cwlclanmatebonus'],
                description='Lists each score the member has in CWL.')
async def cwlclanmatescore(ctx, *, player_name):
    await ctx.send(
        response_cwl_member_standing(player_name, heroes_tag, header))


# Discord

@client.command(
    aliases=['roleme'],
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


@client.command(
    aliases=['nick'], description=(
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


@client.command(
    aliases=['member_check'],
    description=('Checks for people not in your clan. '
                 'Does not change any current member roles.'),
    hidden=True
)
# todo only be able to run this if author is admin
# ! this is kind of a giant mess right now... don't use this
# ? testing
async def all_member_roles(ctx):
    members = ctx.guild.members
    for member in members:
        # if the member is not initiated then leave them be
        if role_check('Uninitiated', member.roles):
            pass
        # makes the player Uninitiated if they do not have a nickname set
        elif member.nick == None:
            new_role, old_role = role_switch('Uninitiated', member.roles)
            if old_role != '':
                await member.remove_roles(
                    discord.utils.get(member.guild.roles, name=old_role))
            if new_role != '':
                await member.add_roles(
                    discord.utils.get(member.guild.roles, name=new_role))
        else:
            player = response_player(member.nick, heroes_tag, header)
            if player != '':
                # makes the player Uninitiated if they are not in the clan
                new_role, old_role = role_switch('Uninitiated', member.roles)
            else:
                new_role, old_role = role_switch(player.role, member.roles)

            if old_role != '':
                await member.remove_roles(
                    discord.utils.get(member.guild.roles, name=old_role))
            if new_role != '':
                await member.add_roles(
                    discord.utils.get(member.guild.roles, name=new_role))


@client.event
async def on_member_join(member):
    member_role = discord.utils.get(member.guild.roles, name='Uninitiated')
    await member.add_roles(member_role)


@client.event
async def on_member_remove(member):
    print(f'{member} has left the server')


client.run('NjQ5MTA3MTU2OTg5Mzc4NTcx.Xd3-Jg.OM20CTzSqwFPjrl0PMQQRocG87w')
