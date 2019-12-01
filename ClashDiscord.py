import discord
from discord.ext import commands
from Time_Calculator import *
from Clash_Responder import *

client = commands.Bot(command_prefix='!')

RazgrizTag = 'RGQ8RGU9'
TheMightyHeroesTag = 'JJRJGVR0'
headers = {
    'Accept': 'application/json',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjkyNWJjYzg1LWFhZDktNGM2NC05M2Y2LWM4MWEwZGVhOGUwNiIsImlhdCI6MTU3NDYyMjY3Nywic3ViIjoiZGV2ZWxvcGVyLzdjZmJkOWFjLTFlYzAtNDI3OS1jODM2LTU0YzMxN2FlZmE4NiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjEwOC4yMTEuOTUuMjU0Il0sInR5cGUiOiJjbGllbnQifV19.gdc-4-OEZzsYBLk8HfqZBH-idvlK1vX9nim91XEqLgwNAyarfZquxfkZDKPsswUGyiXRIFV7Am3RB7iWtd9T5w'
}


@client.event
async def on_ready():
    print('RazBot is ready')


@client.command()
async def helpme(ctx):
    await ctx.send(f'Here are some helpful functions: !ping, !hellothere, !waroverview, !scoreboard, !war, !wartime, !noattack, !noatk')


@client.command()
async def hellothere(ctx):
    await ctx.send(f'General Kenobi')


@client.command()
async def ping(ctx):
    await ctx.send(f'pong {round(client.latency) * 1000}ms')


@client.command(aliases=['war', 'scoreboard'])
async def waroverview(ctx):
    await ctx.send(f'{curr_war_overview(TheMightyHeroesTag)}')


@client.command()
async def wartime(ctx):
    await ctx.send(f'{war_time(TheMightyHeroesTag)}')


@client.command(aliases=['noatk'])
async def noattack(ctx):
    await ctx.send(f'{no_atk(TheMightyHeroesTag)}')


@client.command(aliases=['allatk'],description='showing all attacks for every member', hidden=True)
async def allattacks(ctx):
    for message_line in all_attacks(TheMightyHeroesTag):
        await ctx.send(f'{message_line}')


@client.event
async def on_member_join(member):
    print(f'{member} has joined the server')


@client.event
async def on_member_remove(member):
    print(f'{member} has left the server')


client.run('NjQ5MTA3MTU2OTg5Mzc4NTcx.Xd3-7g.YMM0SYwbNfzDdUvYi6ibbh3g_Ck')
