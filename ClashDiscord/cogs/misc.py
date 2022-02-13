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

    # misc link
    @misc.sub_command_group()
    async def link(inter):
        """
            group for misc link commands
        """

        pass

    @link.sub_command()
    async def clashofstats(
        self,
        inter,
        tag: str = discord_utils.command_param_dict['required_tag']
    ):
        """
            gets a clash of stats link

            Parameters
            ----------
            tag (optional): tag to search
        """

        await inter.response.defer()

        player = await clash_responder.get_player(tag, self.coc_client)

        if player is None:
            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=f"could not find player with tag {tag}",
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(embed_list, inter)
            return

        await inter.edit_original_message(
            content=(discord_responder.link_clash_of_stats(player)))

    @link.sub_command()
    async def chocolateclash(
        self,
        inter,
        tag: str = discord_utils.command_param_dict['required_tag']
    ):
        """
            gets a ChocolateClash link

            Parameters
            ----------
            tag (optional): tag to search
        """

        await inter.response.defer()

        player = await clash_responder.get_player(tag, self.coc_client)

        if player is None:
            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=f"could not find player with tag {tag}",
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(embed_list, inter)
            return

        await inter.edit_original_message(
            content=discord_responder.link_chocolate_clash(player))
