from disnake.ui import Button
from disnake import ButtonStyle, MessageInteraction
from coc.players import Player

from data import ClashDiscord_Client_Data as ClientData
from responders.PlayerResponder import (
    player_info,
    unit_lvl_all,
    active_super_troops)
from responders.ClashResponder import (
    player_active_super_troops)
from responders.DiscordResponder import (
    embed_message,
    get_town_hall_url)


class PlayerInfoBtn(Button):
    def __init__(
        self,
        client_data: ClientData.ClashDiscord_Data,
        coc_client,
        player: Player,
        btn_name: str = "Info",
        btn_style: ButtonStyle = ButtonStyle.primary
    ):
        super().__init__(
            label=btn_name,
            style=btn_style)
        self.client_data = client_data
        self.coc_client = coc_client
        self.player = player

    async def callback(
            self,
            inter: MessageInteraction):

        await inter.response.defer()

        if self.player is None:
            embed_description = f"could not find player"

            embed_list = embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author)

            await inter.edit_original_message(embeds=embed_list)
            return

        embed_thumbnail = get_town_hall_url(self.player)

        field_dict_list = player_info(
            self.player, inter.client.emojis, self.client_data.emojis)

        embed_list = embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{self.player.name} {self.player.tag}",
            bot_user_name=inter.me.display_name,
            thumbnail=embed_thumbnail,
            field_list=field_dict_list,
            author=inter.author)

        # edit the original message with the updated embeds
        await inter.edit_original_message(embeds=embed_list)


class PlayerUnitsBtn(Button):
    def __init__(
        self,
        client_data: ClientData.ClashDiscord_Data,
        coc_client,
        player: Player,
        btn_name: str = "Units",
        btn_style: ButtonStyle = ButtonStyle.primary
    ):
        super().__init__(
            label=btn_name,
            style=btn_style)
        self.client_data = client_data
        self.coc_client = coc_client
        self.player = player

    async def callback(
            self,
            inter: MessageInteraction):

        await inter.response.defer()

        if self.player is None:
            embed_description = f"could not find player"

            embed_list = embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author)

            await inter.edit_original_message(embeds=embed_list)
            return

        title_string = f"{self.player.name} units"
        embed_thumbnail = get_town_hall_url(self.player)

        field_dict_list = unit_lvl_all(
            self.player, inter.client.emojis, self.client_data.emojis
        )

        embed_list = embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=title_string,
            bot_user_name=inter.me.display_name,
            thumbnail=embed_thumbnail,
            field_list=field_dict_list,
            author=inter.author)

        # edit the original message with the updated embeds
        await inter.edit_original_message(embeds=embed_list)


class PlayerSuperTroopBtn(Button):
    def __init__(
        self,
        client_data: ClientData.ClashDiscord_Data,
        coc_client,
        player: Player,
        btn_name: str = "Super Troop",
        btn_style: ButtonStyle = ButtonStyle.primary
    ):
        super().__init__(
            label=btn_name,
            style=btn_style)
        self.client_data = client_data
        self.coc_client = coc_client
        self.player = player

    async def callback(
            self,
            inter: MessageInteraction):

        await inter.response.defer()

        if self.player is None:
            embed_description = f"could not find player"

            embed_list = embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author)

            await inter.edit_original_message(embeds=embed_list)
            return

        active_super_troop_list = player_active_super_troops(
            self.player)

        embed_thumbnail = get_town_hall_url(self.player)

        field_dict_list = active_super_troops(
            self.player, active_super_troop_list,
            inter.client.emojis, self.client_data.emojis
        )
        embed_list = embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{self.player.name} Active Super Troops",
            bot_user_name=inter.me.display_name,
            thumbnail=embed_thumbnail,
            field_list=field_dict_list,
            author=inter.author)

        # edit the original message with the updated embeds
        await inter.edit_original_message(embeds=embed_list)
