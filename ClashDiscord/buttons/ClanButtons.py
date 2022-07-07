from disnake.ui import Button
from disnake import ButtonStyle, MessageInteraction
from coc.clans import Clan

from data import ClashDiscord_Client_Data as ClientData

from responders.ClanResponder import (
    clan_info,
    clan_lineup,
    war_preference_member,
    clan_super_troop_active)
from responders.DiscordResponder import embed_message


class ClanInfoBtn(Button):
    def __init__(
        self,
        client_data: ClientData.ClashDiscord_Data,
        coc_client,
        clan: Clan,
        btn_name: str = "Info",
        btn_style: ButtonStyle = ButtonStyle.primary
    ):
        super().__init__(
            label=btn_name,
            style=btn_style)
        self.client_data = client_data
        self.coc_client = coc_client
        self.clan = clan

    async def callback(
            self,
            inter: MessageInteraction):

        await inter.response.defer()

        if self.clan is None:
            embed_description = f"could not find clan"

            embed_list = embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author)

            await inter.edit_original_message(embeds=embed_list)
            return

        field_dict_list = clan_info(
            self.clan,
            inter.client.emojis,
            self.client_data.emojis)

        embed_list = embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{self.clan.name} {self.clan.tag}",
            bot_user_name=inter.me.display_name,
            thumbnail=self.clan.badge.small,
            field_list=field_dict_list,
            author=inter.author)

        # edit the original message with the updated embeds
        await inter.edit_original_message(embeds=embed_list)


class ClanLineupBtn(Button):
    def __init__(
        self,
        client_data: ClientData.ClashDiscord_Data,
        coc_client,
        clan: Clan,
        btn_name: str = "Lineup",
        btn_style: ButtonStyle = ButtonStyle.primary
    ):
        super().__init__(
            label=btn_name,
            style=btn_style)
        self.client_data = client_data
        self.coc_client = coc_client
        self.clan = clan

    async def callback(
            self,
            inter: MessageInteraction):

        await inter.response.defer()

        if self.clan is None:
            embed_description = f"could not find clan"

            embed_list = embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author)

            await inter.edit_original_message(embeds=embed_list)
            return

        embed_title = f"{self.clan.name} Lineup"
        embed_description = await clan_lineup(
            self.clan,
            self.coc_client,
            inter.client.emojis,
            self.client_data.emojis)

        embed_list = embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=embed_title,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            thumbnail=self.clan.badge.small,
            author=inter.author)

        # edit the original message with the updated embeds
        await inter.edit_original_message(embeds=embed_list)


class ClanWarPreferenceBtn(Button):
    def __init__(
        self,
        client_data: ClientData.ClashDiscord_Data,
        coc_client,
        clan: Clan,
        btn_name: str = "War Preference",
        btn_style: ButtonStyle = ButtonStyle.primary
    ):
        super().__init__(
            label=btn_name,
            style=btn_style)
        self.client_data = client_data
        self.coc_client = coc_client
        self.clan = clan

    async def callback(
            self,
            inter: MessageInteraction):

        await inter.response.defer()

        if self.clan is None:
            embed_description = f"could not find clan"

            embed_list = embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author)

            await inter.edit_original_message(embeds=embed_list)
            return

        embed_title = f"{self.clan.name} War Preference"
        embed_description = await war_preference_member(
            self.clan,
            self.coc_client,
            inter.client.emojis,
            self.client_data.emojis)

        embed_list = embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=embed_title,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            thumbnail=self.clan.badge.small,
            author=inter.author)

        # edit the original message with the updated embeds
        await inter.edit_original_message(embeds=embed_list)


class ClanSuperTroopBtn(Button):
    def __init__(
        self,
        client_data: ClientData.ClashDiscord_Data,
        coc_client,
        clan: Clan,
        btn_name: str = "Super Troops",
        btn_style: ButtonStyle = ButtonStyle.primary
    ):
        super().__init__(
            label=btn_name,
            style=btn_style)
        self.client_data = client_data
        self.coc_client = coc_client
        self.clan = clan

    async def callback(
            self,
            inter: MessageInteraction):

        await inter.response.defer()

        if self.clan is None:
            embed_description = f"could not find clan"

            embed_list = embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author)

            await inter.edit_original_message(embeds=embed_list)
            return

        embed_title = f"{self.clan.name} active super troops"

        field_dict_list = await clan_super_troop_active(
            self.clan,
            inter.client.emojis,
            self.client_data.emojis,
            self.coc_client)

        embed_list = embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=embed_title,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            thumbnail=self.clan.badge.small,
            author=inter.author)

        # edit the original message with the updated embeds
        await inter.edit_original_message(embeds=embed_list)
