from disnake.ui import Button
from disnake import ButtonStyle, MessageInteraction
from coc.wars import ClanWar

from data import ClashDiscord_Client_Data as ClientData

from responders.WarResponder import (
    war_clan_scoreboard,
    war_scoreboard,
    war_lineup_overview,
    war_lineup_clan,
    war_no_attack)
from responders.DiscordResponder import embed_message


class WarInfoBtn(Button):
    def __init__(
        self,
        discord_emojis: list,
        client_data: ClientData.ClashDiscord_Data,
        coc_client,
        war: ClanWar,
        btn_name: str = "War Info",
        btn_style: ButtonStyle = ButtonStyle.primary
    ):
        super().__init__(
            label=btn_name,
            style=btn_style)
        self.discord_emojis = discord_emojis
        self.client_data = client_data
        self.coc_client = coc_client
        self.war = war

    async def callback(
            self,
            inter: MessageInteraction):

        await inter.response.defer()

        if self.war is None:
            embed_description = f"could not find war"

            embed_list = embed_message(
                icon_url=inter.me.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author)

            await inter.edit_original_message(embeds=embed_list)
            return

        btn_name = self.label

        self.label = f"Please Wait"

        await inter.edit_original_message(view=self.view)

        field_dict_list = war_scoreboard(
            self.war, self.discord_emojis, self.client_data.emojis)

        embed_list = embed_message(
            icon_url=inter.me.avatar.url,
            title=f"{self.war.clan.name} vs. {self.war.opponent.name}",
            bot_user_name=inter.me.display_name,
            thumbnail=self.war.clan.badge.small,
            field_list=field_dict_list,
            author=inter.author)

        self.label = btn_name

        # edit the original message with the updated embeds
        await inter.edit_original_message(
            embeds=embed_list, view=self.view)


class WarLineupCountBtn(Button):
    def __init__(
        self,
        discord_emojis: list,
        client_data: ClientData.ClashDiscord_Data,
        coc_client,
        war: ClanWar,
        btn_name: str = "War Lineup Count",
        btn_style: ButtonStyle = ButtonStyle.primary
    ):
        super().__init__(
            label=btn_name,
            style=btn_style)
        self.discord_emojis = discord_emojis
        self.client_data = client_data
        self.coc_client = coc_client
        self.war = war

    async def callback(
            self,
            inter: MessageInteraction):

        await inter.response.defer()

        if self.war is None:
            embed_description = f"could not find war"

            embed_list = embed_message(
                icon_url=inter.me.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author)

            await inter.edit_original_message(embeds=embed_list)
            return

        btn_name = self.label

        self.label = f"Please Wait"

        await inter.edit_original_message(view=self.view)

        embed_title = f"{self.war.clan.name} vs. {self.war.opponent.name}"
        field_dict_list = war_lineup_overview(
            self.war, self.discord_emojis, self.client_data.emojis)

        embed_list = embed_message(
            icon_url=inter.me.avatar.url,
            title=embed_title,
            bot_user_name=inter.me.display_name,
            thumbnail=self.war.clan.badge.small,
            field_list=field_dict_list,
            author=inter.author)

        self.label = btn_name

        # edit the original message with the updated embeds
        await inter.edit_original_message(
            embeds=embed_list, view=self.view)


class WarLineupClanBtn(Button):
    def __init__(
        self,
        discord_emojis: list,
        client_data: ClientData.ClashDiscord_Data,
        coc_client,
        war: ClanWar,
        btn_name: str = "War Clan Lineup",
        btn_style: ButtonStyle = ButtonStyle.primary
    ):
        super().__init__(
            label=btn_name,
            style=btn_style)
        self.discord_emojis = discord_emojis
        self.client_data = client_data
        self.coc_client = coc_client
        self.war = war

    async def callback(
            self,
            inter: MessageInteraction):

        await inter.response.defer()

        if self.war is None:
            embed_description = f"could not find war"

            embed_list = embed_message(
                icon_url=inter.me.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author)

            await inter.edit_original_message(embeds=embed_list)
            return

        btn_name = self.label

        self.label = f"Please Wait"

        await inter.edit_original_message(view=self.view)

        embed_title = f"{self.war.clan.name} vs. {self.war.opponent.name}"
        field_dict_list = war_lineup_clan(
            self.war, self.discord_emojis, self.client_data.emojis)

        embed_list = embed_message(
            icon_url=inter.me.avatar.url,
            title=embed_title,
            bot_user_name=inter.me.display_name,
            thumbnail=self.war.clan.badge.small,
            field_list=field_dict_list,
            author=inter.author)

        self.label = btn_name

        # edit the original message with the updated embeds
        await inter.edit_original_message(
            embeds=embed_list, view=self.view)


class WarMissingAttacksBtn(Button):
    def __init__(
        self,
        discord_emojis: list,
        client_data: ClientData.ClashDiscord_Data,
        coc_client,
        war: ClanWar,
        btn_name: str = "War Missing Attacks",
        btn_style: ButtonStyle = ButtonStyle.primary
    ):
        super().__init__(
            label=btn_name,
            style=btn_style)
        self.discord_emojis = discord_emojis
        self.client_data = client_data
        self.coc_client = coc_client
        self.war = war

    async def callback(
            self,
            inter: MessageInteraction):

        await inter.response.defer()

        if self.war is None:
            embed_description = f"could not find war"

            embed_list = embed_message(
                icon_url=inter.me.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author)

            await inter.edit_original_message(embeds=embed_list)
            return

        btn_name = self.label

        self.label = f"Please Wait"

        await inter.edit_original_message(view=self.view)

        embed_title = f"{self.war.clan.name} vs. {self.war.opponent.name}"

        # setting missed_attacks to None
        field_dict_list = war_no_attack(
            self.war, None,
            self.discord_emojis, self.client_data.emojis)

        embed_list = embed_message(
            icon_url=inter.me.avatar.url,
            title=embed_title,
            bot_user_name=inter.me.display_name,
            thumbnail=self.war.clan.badge.small,
            field_list=field_dict_list,
            author=inter.author)

        self.label = btn_name

        # edit the original message with the updated embeds
        await inter.edit_original_message(
            embeds=embed_list, view=self.view)


class WarClanScoreboardBtn(Button):
    def __init__(
        self,
        discord_emojis: list,
        client_data: ClientData.ClashDiscord_Data,
        coc_client,
        war: ClanWar,
        btn_name: str = "War Scoreboard",
        btn_style: ButtonStyle = ButtonStyle.primary
    ):
        super().__init__(
            label=btn_name,
            style=btn_style)
        self.discord_emojis = discord_emojis
        self.client_data = client_data
        self.coc_client = coc_client
        self.war = war

    async def callback(
            self,
            inter: MessageInteraction):

        await inter.response.defer()

        if self.war is None:
            embed_description = f"could not find war"

            embed_list = embed_message(
                icon_url=inter.me.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author)

            await inter.edit_original_message(embeds=embed_list)
            return

        btn_name = self.label

        self.label = f"Please Wait"

        await inter.edit_original_message(view=self.view)

        field_dict_list = war_clan_scoreboard(
            war=self.war,
            discord_emoji_list=self.discord_emojis,
            client_emoji_list=self.client_data.emojis,
            bot_name=inter.me.display_name)

        embed_title = f"{self.war.clan.name} vs. {self.war.opponent.name}"

        embed_list = embed_message(
            icon_url=inter.me.avatar.url,
            title=embed_title,
            bot_user_name=inter.me.display_name,
            thumbnail=self.war.clan.badge.small,
            field_list=field_dict_list,
            author=inter.author)

        self.label = btn_name

        # edit the original message with the updated embeds
        await inter.edit_original_message(
            embeds=embed_list, view=self.view)


# * Scoreboard
# placeholder for upcoming war scoreboard command
