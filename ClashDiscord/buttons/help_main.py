import disnake
from disnake.ext.commands import InteractionBot

from data import ClashDiscord_Client_Data as ClientData
from responders import (
    DiscordResponder as discord_responder,
    help_main as help_main_responder
)


class HelpMainBtn(disnake.ui.Button):
    def __init__(
        self, bot: InteractionBot,
        client_data: ClientData.ClashDiscord_Data
    ):
        super().__init__(
            label="Back", style=disnake.ButtonStyle.primary)
        self.bot = bot
        self.client_data = client_data

    async def callback(
            self,
            inter: disnake.MessageInteraction):

        await inter.response.defer()

        help_dict = help_main_responder.help_main(
            bot=self.bot, inter=inter,
            client_data=self.client_data)

        field_dict_list = help_dict['field_dict_list']
        view = help_dict['view']

        embed_list = discord_responder.embed_message(
            icon_url=self.bot.user.avatar.url,
            title=f"{inter.me.display_name} help menu",
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author=inter.author
        )

        # edit the original message with the updated embeds
        await inter.edit_original_message(embeds=embed_list, view=view)
