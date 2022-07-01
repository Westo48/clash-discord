import disnake
import coc
from asyncio.tasks import sleep
from disnake.ext import commands
from cogs import (
    help as help_cog,
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
from linkAPI.client import LinkApiClient
from responders.ClientResponder import (
    get_client_email,
    get_client_password,
    get_linkapi_username,
    get_linkapi_password,
    get_client_test_guilds,
    get_client_token
)

client_data = ClashDiscord_Client_Data.ClashDiscord_Data()

coc_client = coc.login(
    email=get_client_email(),
    password=get_client_password()
)

linkapi_client = LinkApiClient(
    get_linkapi_username(),
    get_linkapi_password()
)

intents = disnake.Intents.default()
intents.members = True

bot = commands.InteractionBot(
    intents=intents,
    test_guilds=get_client_test_guilds())

# only load Misc if there are test guilds
# only if it is in dev
if get_client_test_guilds() is not None:
    bot.add_cog(misc_cog.Misc(
        bot, coc_client, client_data))

bot.add_cog(help_cog.Help(
    bot, coc_client, client_data))
bot.add_cog(player_cog.Player(
    bot, coc_client, client_data))
bot.add_cog(clan_cog.Clan(
    bot, coc_client, client_data))
bot.add_cog(war_cog.War(
    bot, coc_client, client_data))
bot.add_cog(cwl_cog.CWL(
    bot, coc_client, client_data))
bot.add_cog(discord_cog.Discord(
    bot, coc_client, client_data))
bot.add_cog(announce_cog.Announce(
    bot, coc_client, client_data))
bot.add_cog(client_cog.Client(
    bot, coc_client, client_data, linkapi_client))
bot.add_cog(admin_cog.Admin(
    bot, coc_client, client_data, linkapi_client))
bot.add_cog(superuser_cog.SuperUser(
    bot, coc_client, client_data, linkapi_client))
bot.add_cog(events_cog.Events(
    bot, coc_client, client_data, linkapi_client))

if __name__ == "__main__":
    bot.run(get_client_token())
