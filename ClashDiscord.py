import discord
from discord.ext import commands
from discord.utils import get
from ClashResponder import *


client = commands.Bot(command_prefix='!')


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


@client.command(description='Enter your player name and hero/troop/spell you are looking for. If your name has a space in it replace that space with -')
async def trooplvl(ctx, player_name, *, troop_name):
    await ctx.send(f'{troop_level_response(player_name, troop_name)}')


@client.command(description='enter your player name and get all your player troop levels', hidden=True)
async def alltrooplvl(ctx, player_name):
    for line in all_troop_level_response(player_name):
        await ctx.send(f'{line}')


@client.command(desctiption='enter your player name and troop to see if you will be able to donate specified troop', aliases=['donation', 'donate'])
async def donationchecker(ctx, player_name, *, troop_name):
    await ctx.send(f'{donation_response(player_name, troop_name)}')


@client.command(description='enter the TH you are looking for and the amount of gold/elixir in TH or one storage')
async def warweight(ctx, THlvl, *, amount):
    await ctx.send(f'{war_weight(THlvl, amount)}')


@client.command(aliases=['war', 'scoreboard'])
async def waroverview(ctx):
    await ctx.send(f'{war_response()}')


@client.command()
async def wartime(ctx):
    await ctx.send(f'{war_response()}')


@client.command(aliases=['warmembers', 'warmember', 'warmem', 'warmemstar', 'warmemstars'], description='overview of all members in war', hidden=True)
async def warmemberstars(ctx):
    for line in all_attacks_response():
        await ctx.send(f'{line}')


@client.command(aliases=['noatk'])
async def noattack(ctx):
    await ctx.send(f'{no_attack_response()}')


@client.command(aliases=['allatk'], description='showing all attacks for every member', hidden=True)
async def allattacks(ctx):
    for line in all_attacks_response():
        await ctx.send(f'{line}')


# cwl war

@client.command(aliases=['cwltime'], description='shows time remaining in the current clan war league')
async def cwlwartime(ctx):
    await ctx.send(f'{cwl_war_response()}')


@client.command(aliases=['cwlwar'], description='shows the overview of the current war league')
async def cwlwaroverview(ctx):
    await ctx.send(f'{cwl_war_response()}')


@client.command(aliases=['cwlnoatk'])
async def cwlnoattack(ctx):
    await ctx.send(f'{cwl_no_attack_response()}')


@client.command(aliases=['cwlallatk'], description='showing all attacks for every member', hidden=True)
async def cwlallattack(ctx):
    for line in cwl_all_attacks_response():
        await ctx.send(line)


# Discord

# todo get players to set nickname and use member.nick for that
# todo set player nicknames to reflect CoC name
@client.command(pass_context=True, aliases=['roleme'], description='this will give you your MightyHeroes role here in Discord')
async def role(ctx, player_name):
    new_role = member_role_response(player_name)
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
