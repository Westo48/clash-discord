import discord
from discord.ext import commands
from Clash_Responder import *

RazgrizTag = 'RGQ8RGU9'
TheMightyHeroesTag = 'JJRJGVR0'


client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print('RazBot is ready')

# todo add methods to this command
@client.command()
async def helpme(ctx):
    await ctx.send(f'Here are some helpful functions: !ping, !hellothere, !trooplvl, !waroverview, !scoreboard, !war, !wartime, !noattack, !noatk')


@client.command()
async def hellothere(ctx):
    await ctx.send(f'General Kenobi')


@client.command()
async def ping(ctx):
    await ctx.send(f'pong {round(client.latency) * 1000}ms')


@client.command(description='Enter your player name and hero/troop/spell you are looking for. If your name has a space in it replace that space with -')
async def trooplvl(ctx, player, *, troop):
    await ctx.send(f'{user_troop_levels(player, troop)}')


@client.command(description='enter your player name and get all your player troop levels', hidden=True)
async def alltrooplvl(ctx, player):
    for message_line in all_user_levels(player):
        await ctx.send(f'{message_line}')


@client.command(desctiption='enter your player name and troop to see if you will be able to donate specified troop', aliases=['donation', 'donate'])
async def donationchecker(ctx, player, *, troop):
    await ctx.send(f'{donation_checker(player, troop)}')


@client.command(description='enter the TH you are looking for and the amount of gold/elixir in TH or one storage')
async def warweight(ctx, THlvl, *, amount):
    await ctx.send(f'{war_weight(THlvl, amount)}')


@client.command(aliases=['war', 'scoreboard'])
async def waroverview(ctx):
    await ctx.send(f'{curr_war_overview(TheMightyHeroesTag)}')


@client.command()
async def wartime(ctx):
    await ctx.send(f'{curr_war_time(TheMightyHeroesTag)}')

# todo make war members call
@client.command(aliases=['warmembers', 'warmember', 'warmem', 'warmemstar', 'warmemstars'], description='overview of all members in war', hidden=True)
async def warmemberstars(ctx):
    for message_line in all_attack_stars(TheMightyHeroesTag):
        await ctx.send(f'{message_line}')


@client.command(aliases=['noatk'])
async def noattack(ctx):
    await ctx.send(f'{curr_no_atk(TheMightyHeroesTag)}')


@client.command(aliases=['allatk'], description='showing all attacks for every member', hidden=True)
async def allattacks(ctx):
    for message_line in all_attacks(TheMightyHeroesTag):
        await ctx.send(f'{message_line}')


# cwl war

@client.command(aliases=['cwltime'], description='shows time remaining in the current clan war league')
async def cwlwartime(ctx):
    await ctx.send(f'{cwl_war_time(TheMightyHeroesTag)}')


@client.command(aliases=['cwlwar'], description='shows the overview of the current war league')
async def cwlwaroverview(ctx):
    await ctx.send(f'{cwl_curr_war_overview(TheMightyHeroesTag)}')


@client.event
async def on_member_join(member):
    print(f'{member} has joined the server')


@client.event
async def on_member_remove(member):
    print(f'{member} has left the server')


client.run('NjQ5MTA3MTU2OTg5Mzc4NTcx.Xd3-7g.YMM0SYwbNfzDdUvYi6ibbh3g_Ck')
