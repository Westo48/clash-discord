import disnake
import coc
from asyncio.tasks import sleep
from disnake.ext import commands
from cogs import (
    misc as misc_cog,
    player as player_cog,
    clan as clan_cog,
    war as war_cog,
    cwl as cwl_cog,
    discord as discord_cog,
    announce as announce_cog,
    client as client_cog,
    admin as admin_cog,
    superuser as superuser_cog,
    events as events_cog
)
from data import ClashDiscord_Client_Data
import responders.ClashResponder as clash_responder
import responders.DiscordResponder as discord_responder
import responders.RazBotDB_Responder as db_responder
from utils import discord_utils

client_data = ClashDiscord_Client_Data.ClashDiscord_Data()

coc_client = coc.login(
    email=discord_responder.get_client_email(),
    password=discord_responder.get_client_password()
)

intents = disnake.Intents.all()

bot = commands.Bot(
    command_prefix=client_data.prefix,
    intents=intents,
    test_guilds=discord_responder.get_client_test_guilds())
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f"RazBot is ready")


bot.add_cog(misc_cog.Misc(bot, coc_client, client_data))
bot.add_cog(player_cog.Player(bot, coc_client, client_data))
bot.add_cog(clan_cog.Clan(bot, coc_client, client_data))
bot.add_cog(war_cog.War(bot, coc_client, client_data))
bot.add_cog(cwl_cog.CWL(bot, coc_client, client_data))
bot.add_cog(discord_cog.Discord(bot, coc_client, client_data))
bot.add_cog(announce_cog.Announce(bot, coc_client, client_data))
bot.add_cog(client_cog.Client(bot, coc_client, client_data))
bot.add_cog(admin_cog.Admin(bot, coc_client, client_data))
bot.add_cog(superuser_cog.SuperUser(bot, coc_client, client_data))
bot.add_cog(events_cog.Events(bot, coc_client, client_data))

if __name__ == "__main__":
    bot.run(discord_responder.get_client_token())
