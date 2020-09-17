import discord
from discord.ext import commands
from discord.utils import get
from ClashResponder import *
from DiscordResponder import *


class ClientClan(object):
    def __init__(
        self, tag, name
    ):
        self.tag = tag
        self.name = name


client = commands.Bot(command_prefix='!')
raz_tag = '#RGQ8RGU9'
heroes_tag = '#JJRJGVR0'
client_clans = [
    (ClientClan('#28LRPVP8C', '6ers')),
    (ClientClan('#JJRJGVR0', 'TheMightyHeroes'))

]
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
    player_name = player_name_string(ctx.author.display_name)
    user_clan = find_user_clan(
        player_name, client_clans, ctx.author.roles, header)
    if user_clan != '':
        await ctx.send(response_troop_lvl(
            player_name, troop_name, user_clan.tag, header))
    else:
        await ctx.send(f"Couldn't find {ctx.author.display_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


@client.command(description='Get all your troop levels.', hidden=True)
async def alltrooplvl(ctx):
    user_clan = find_user_clan(client_clans, ctx.author.roles)
    if user_clan != '':
        for line in response_all_troop_level(ctx.author.display_name, user_clan.tag, header):
            await ctx.send(line)
    else:
        await ctx.send(f"Couldn't find {ctx.author.display_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


# Clan

@client.command(
    aliases=['donation', 'donate'],
    desctiption='Enter a troop name to see who in the clan '
    'is best suited to donate that troop.'
)
async def donationchecker(ctx, *, troop_name):
    user_clan = find_user_clan(client_clans, ctx.author.roles)
    if user_clan != '':
        await ctx.send(response_donation(troop_name, user_clan.tag, header))
    else:
        await ctx.send(f"Couldn't find {ctx.author.display_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


# War
# todo warmember gets a war overview for a specific war member

@client.command(aliases=['war', 'scoreboard'])
async def waroverview(ctx):
    user_clan = find_user_clan(client_clans, ctx.author.roles)
    if user_clan != '':
        await ctx.send(response_war_overview(user_clan.tag, time_zone, header))
    else:
        await ctx.send(f"Couldn't find {ctx.author.display_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


@client.command()
async def wartime(ctx):
    user_clan = find_user_clan(client_clans, ctx.author.roles)
    if user_clan != '':
        await ctx.send(response_war_time(user_clan.tag, time_zone, header))
    else:
        await ctx.send(f"Couldn't find {ctx.author.display_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


@client.command(aliases=['noatk'])
async def noattack(ctx):
    user_clan = find_user_clan(client_clans, ctx.author.roles)
    if user_clan != '':
        await ctx.send(response_war_no_attack(user_clan.tag, time_zone, header))
    else:
        await ctx.send(f"Couldn't find {ctx.author.display_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


@client.command(
    aliases=['warmembers', 'warstars', 'warmemstar', 'warmemstars'],
    description='overview of all members in war',
    hidden=True
)
async def warmemberstars(ctx):
    user_clan = find_user_clan(client_clans, ctx.author.roles)
    if user_clan != '':
        for line in response_war_members_overview(user_clan.tag, time_zone, header):
            await ctx.send(line)
    else:
        await ctx.send(f"Couldn't find {ctx.author.display_name}'s clan. "
                       "Please ensure a clan role has been given to the user.")


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
# todo cwl_group overview, scoreboard, cwl_clan_noatk


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


@client.event
async def on_member_join(member):
    member_role = discord.utils.get(member.guild.roles, name='Uninitiated')
    await member.add_roles(member_role)


@client.event
async def on_member_remove(member):
    print(f'{member} has left the server')


client.run('NjQ5MTA3MTU2OTg5Mzc4NTcx.Xd3-Jg.OM20CTzSqwFPjrl0PMQQRocG87w')
