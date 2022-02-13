import disnake
from disnake.ext import commands
from responders import (
    DiscordResponder as discord_responder,
    ClashResponder as clash_responder
)
from utils import discord_utils


class Misc(commands.Cog):
    def __init__(self, bot, coc_client, client_data):
        self.bot = bot
        self.coc_client = coc_client
        self.client_data = client_data

    @commands.slash_command()
    async def misc(self, inter):
        pass

    @misc.sub_command()
    async def hellothere(self, inter):
        """
            GENERAL KENOBI
        """
        await inter.response.send_message(content=f'General Kenobi')

    @misc.sub_command()
    async def ping(self, inter):
        """
            gets the bot ping

            Parameters
            ----------
            inter: disnake interaction object
        """

        await inter.response.defer()

        await inter.edit_original_message(
            content=f"pong {round(inter.bot.latency, 3) * 1000}ms")
