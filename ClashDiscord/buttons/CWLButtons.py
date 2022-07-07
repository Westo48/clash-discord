from disnake.ui import Button
from disnake import ButtonStyle, MessageInteraction
from coc.clans import Clan
from coc.wars import ClanWar, ClanWarLeagueGroup

from data import ClashDiscord_Client_Data as ClientData

from responders.CWLResponder import (
    cwl_info_scoreboard)
from responders.ClashResponder import (
    cwl_current_round)
from responders.DiscordResponder import (
    embed_message,
    get_emoji)


class CWLInfoBtn(Button):
    def __init__(
        self,
        client_data: ClientData.ClashDiscord_Data,
        coc_client,
        clan: Clan,
        group: ClanWarLeagueGroup,
        war: ClanWar,
        btn_name: str = "CWL Info",
        btn_style: ButtonStyle = ButtonStyle.primary
    ):
        super().__init__(
            label=btn_name,
            style=btn_style)
        self.client_data = client_data
        self.coc_client = coc_client
        self.clan = clan
        self.group = group
        self.war = war

    async def callback(
            self,
            inter: MessageInteraction):

        await inter.response.defer()

        if self.group is None:
            embed_description = f"could not find war"

            embed_list = embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author)

            await inter.edit_original_message(embeds=embed_list)
            return

        if self.clan is None:
            embed_description = f"could not find clan"

            embed_list = embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author)

            await inter.edit_original_message(embeds=embed_list)
            return

        btn_name = self.label

        self.label = f"Please Wait"

        await inter.edit_original_message(view=self.view)

        league_emoji = get_emoji(
            f"Clan War {self.clan.war_league.name}",
            inter.client.emojis,
            self.client_data.emojis)

        embed_title = f"CWL {league_emoji} {self.clan.war_league.name} Group"

        # get current round number
        round_number = cwl_current_round(
            self.group, self.war)

        embed_description = f"Round {round_number}/{self.group.number_of_rounds}"

        field_dict_list = cwl_info_scoreboard(
            self.war, inter.client.emojis, self.client_data.emojis)

        embed_list = embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=embed_title,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            thumbnail=self.clan.badge.small,
            field_list=field_dict_list,
            author=inter.author)

        self.label = btn_name

        # edit the original message with the updated embeds
        await inter.edit_original_message(
            embeds=embed_list, view=self.view)


# * class CWLLineupBtn
