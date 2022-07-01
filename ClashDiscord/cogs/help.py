import disnake
from disnake import (
    ApplicationCommandInteraction
)
from disnake.ext import commands
from responders import (
    DiscordResponder as discord_responder,
    HelpResponder as help_responder,
    help_main as help_main_responder,
    ClashResponder as clash_responder,
    RazBotDB_Responder as db_responder
)
from utils import discord_utils


class Help(commands.Cog):
    def __init__(self, bot, coc_client, client_data):
        self.bot = bot
        self.coc_client = coc_client
        self.client_data = client_data

    @commands.slash_command()
    async def help(
        self,
        inter: ApplicationCommandInteraction
    ):
        """
            returns help menu
        """

        await inter.response.defer()

        help_dict = help_main_responder.help_main(
            bot=inter.bot,
            inter=inter,
            client_data=self.client_data)

        field_dict_list = help_dict['field_dict_list']
        view = help_dict['view']

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{inter.me.display_name} help menu",
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author=inter.author
        )

        await inter.send(embeds=embed_list, view=view)
