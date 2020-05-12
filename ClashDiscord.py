import discord
from discord.ext import commands
from discord.utils import get
from ClashResponder import *


client = commands.Bot(command_prefix='!')
raz_tag = '#RGQ8RGU9'
heroes_tag = '#JJRJGVR0'
time_zone = (-5)
header = {
    'Accept': 'application/json',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjkyNWJjYzg1LWFhZDktNGM2NC05M2Y2LWM4MWEwZGVhOGUwNiIsImlhdCI6MTU3NDYyMjY3Nywic3ViIjoiZGV2ZWxvcGVyLzdjZmJkOWFjLTFlYzAtNDI3OS1jODM2LTU0YzMxN2FlZmE4NiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjEwOC4yMTEuOTUuMjU0Il0sInR5cGUiOiJjbGllbnQifV19.gdc-4-OEZzsYBLk8HfqZBH-idvlK1vX9nim91XEqLgwNAyarfZquxfkZDKPsswUGyiXRIFV7Am3RB7iWtd9T5w'
}


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

@client.command(description='Enter your player name and hero/troop/spell you are looking for. If your name has a space in it replace that space with -')
async def trooplvl(ctx, player_name, *, troop_name):
    await ctx.send(response_troop_lvl(player_name, troop_name, heroes_tag, header))


@client.command(description='enter your player name and get all your player troop levels', hidden=True)
async def alltrooplvl(ctx, *, player_name):
    for line in response_all_troop_level(player_name, heroes_tag, header):
        await ctx.send(line)


# Clan

@client.command(desctiption='enter your player name and troop to see if you will be able to donate specified troop', aliases=['donation', 'donate'])
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


@client.command(aliases=['warmembers', 'warstars', 'warmemstar', 'warmemstars'], description='overview of all members in war', hidden=True)
async def warmemberstars(ctx):
    for line in response_war_members_overview(heroes_tag, time_zone, header):
        await ctx.send(line)


@client.command(aliases=['allatk'], description='showing all attacks for every member', hidden=True)
async def allattacks(ctx):
    for line in response_war_all_attacks(heroes_tag, time_zone, header):
        await ctx.send(f'{line}')


@client.command(description='enter the amount of storages (not including the TH) you are looking for and the amount of gold/elixir in TH or one storage')
async def warweight(ctx, storages, *, amount):
    return (int(storages) + 1) * int(amount)


# CWL Group
# todo cwl_group overview, scoreboard


# CWL War
# todo cwlwar war_time_prep, war_overview_prep, war_overview_round,

@client.command(aliases=['cwlwar'], description='shows the overview of the current war league')
async def cwlwaroverview(ctx):
    await ctx.send(response_cwl_war_overview(heroes_tag, time_zone, header))


@client.command(aliases=['cwltime'], description='shows time remaining in the current clan war league')
async def cwlwartime(ctx):
    await ctx.send(response_cwl_war_time(heroes_tag, time_zone, header))


@client.command(aliases=['cwlnoatk'])
async def cwlnoattack(ctx):
    await ctx.send(response_cwl_war_no_attack(heroes_tag, time_zone, header))


@client.command(aliases=['cwlallatk'], description='showing all attacks for every member', hidden=True)
async def cwlallattack(ctx):
    for line in response_cwl_war_all_attacks(heroes_tag, time_zone, header):
        await ctx.send(line)


# Discord

# todo get players to set nickname and use member.nick for that
# todo set player nicknames to reflect CoC name
@client.command(pass_context=True, aliases=['roleme'], description='this will give you your MightyHeroes role here in Discord')
async def role(ctx, player_name):
    new_role = response_member_role(player_name, heroes_tag, header)
    if new_role == 'leader':
        new_role = 'Leader'
    elif new_role == 'coLeader':
        new_role = 'Co-Leader'
    elif new_role == 'admin':
        new_role = 'Elder'
    elif new_role == 'member':
        new_role = 'Member'
    else:
        new_role = 'Uninitiated'

    member = ctx.message.author
    old_role = ''
    for item in member.roles:
        if item.name == 'Leader':
            old_role = 'Leader'
            break
        if item.name == 'Co-Leader':
            old_role = 'Co-Leader'
            break
        if item.name == 'Elder':
            old_role = 'Elder'
            break
        if item.name == 'Member':
            old_role = 'Member'
            break
        if item.name == 'Uninitiated':
            old_role = 'Uninitiated'
            break

    member_role_remove = discord.utils.get(member.guild.roles, name=old_role)
    member_role = discord.utils.get(member.guild.roles, name=new_role)
    await member.remove_roles(member_role_remove)
    await member.add_roles(member_role)
    await ctx.send(f'{member.name} now has the role {new_role}')


# todo have this event set that member's role to 'Uninitiated'
@client.event
async def on_member_join(member):
    member_role = discord.utils.get(member.guild.roles, name='Uninitiated')
    await member.add_roles(member_role)


@client.event
async def on_member_remove(member):
    print(f'{member} has left the server')


client.run('NjQ5MTA3MTU2OTg5Mzc4NTcx.Xd3-7g.YMM0SYwbNfzDdUvYi6ibbh3g_Ck')
