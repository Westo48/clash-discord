from disnake.ui import Button
from disnake import ButtonStyle, MessageInteraction
from coc.clans import Clan
from coc.wars import ClanWar, ClanWarLeagueGroup

from data import ClashDiscord_Client_Data as ClientData

from responders.CWLResponder import (
    cwl_info_scoreboard,
    cwl_scoreboard_group,
    cwl_scoreboard_round,
    cwl_scoreboard_clan,
    cwl_clan_noatk,
    cwl_lineup)
from responders.ClashResponder import (
    cwl_current_round)
from responders.AuthResponder import war_verification_clan
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

    async def callback(
            self,
            inter: MessageInteraction):

        await inter.response.defer()

        if self.group is None:
            embed_description = f"could not find CWL group"

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

        verification_payload = await war_verification_clan(
            clan=self.clan,
            war_selection=None,
            coc_client=self.coc_client)

        if not verification_payload['verified']:
            embed_list = embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                field_list=verification_payload['field_dict_list'],
                author=inter.author)

            await inter.edit_original_message(embeds=embed_list)
            return

        war = verification_payload['war']

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
            self.group, war)

        embed_description = f"Round {round_number}/{self.group.number_of_rounds}"

        field_dict_list = cwl_info_scoreboard(
            war, inter.client.emojis, self.client_data.emojis)

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


class CWLLineupBtn(Button):
    def __init__(
        self,
        client_data: ClientData.ClashDiscord_Data,
        coc_client,
        clan: Clan,
        group: ClanWarLeagueGroup,
        btn_name: str = "CWL Lineup",
        btn_style: ButtonStyle = ButtonStyle.primary
    ):
        super().__init__(
            label=btn_name,
            style=btn_style)
        self.client_data = client_data
        self.coc_client = coc_client
        self.clan = clan
        self.group = group

    async def callback(
            self,
            inter: MessageInteraction):

        await inter.response.defer()

        if self.group is None:
            embed_description = f"could not find CWL group"

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

        embed_title = (
            f"CWL {league_emoji} {self.clan.war_league.name} "
            "Group Lineup")

        field_dict_list = cwl_lineup(
            cwl_group=self.group,
            discord_emoji_list=inter.client.emojis,
            client_emoji_list=self.client_data.emojis)

        embed_list = embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=embed_title,
            field_list=field_dict_list,
            bot_user_name=inter.me.display_name,
            thumbnail=self.clan.badge.small,
            author=inter.author)

        self.label = btn_name

        # edit the original message with the updated embeds
        await inter.edit_original_message(
            embeds=embed_list, view=self.view)


class CWLGroupScoreboardBtn(Button):
    def __init__(
        self,
        client_data: ClientData.ClashDiscord_Data,
        coc_client,
        clan: Clan,
        group: ClanWarLeagueGroup,
        btn_name: str = "CWL Group Scoreboard",
        btn_style: ButtonStyle = ButtonStyle.primary
    ):
        super().__init__(
            label=btn_name,
            style=btn_style)
        self.client_data = client_data
        self.coc_client = coc_client
        self.clan = clan
        self.group = group

    async def callback(
            self,
            inter: MessageInteraction):

        await inter.response.defer()

        if self.group is None:
            embed_description = f"could not find CWL group"

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

        field_dict_list = await cwl_scoreboard_group(
            self.group,
            inter.client.emojis,
            self.client_data.emojis,
            self.coc_client)

        embed_list = embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=embed_title,
            bot_user_name=inter.me.display_name,
            thumbnail=self.clan.badge.small,
            field_list=field_dict_list,
            author=inter.author)

        self.label = btn_name

        # edit the original message with the updated embeds
        await inter.edit_original_message(
            embeds=embed_list, view=self.view)


class CWLRoundScoreboardBtn(Button):
    def __init__(
        self,
        client_data: ClientData.ClashDiscord_Data,
        coc_client,
        clan: Clan,
        group: ClanWarLeagueGroup,
        btn_name: str = "CWL Rounds Scoreboard",
        btn_style: ButtonStyle = ButtonStyle.primary
    ):
        super().__init__(
            label=btn_name,
            style=btn_style)
        self.client_data = client_data
        self.coc_client = coc_client
        self.clan = clan
        self.group = group

    async def callback(
            self,
            inter: MessageInteraction):

        await inter.response.defer()

        if self.group is None:
            embed_description = f"could not find CWL group"

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

        embed_list = []
        league_emoji = get_emoji(
            f"Clan War {self.clan.war_league.name}",
            inter.client.emojis,
            self.client_data.emojis)
        embed_title = f"CWL {league_emoji} {self.clan.war_league.name} Group"

        embed_list.extend(embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            title=embed_title,
            thumbnail=self.clan.badge.small,
            author=inter.author
        ))

        round_index = 0

        for cwl_round in self.group.rounds:

            # checking if war has ended
            war = await self.coc_client.get_league_war(cwl_round[0])
            if war.state != "warEnded":
                break

            field_dict_list = await cwl_scoreboard_round(
                self.group, cwl_round, round_index,
                inter.client.emojis, self.client_data.emojis,
                self.coc_client)

            # update round index
            round_index += 1
            embed_title = f"**Round: {round_index}**"

            embed_list.extend(embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                title=embed_title,
                field_list=field_dict_list,
                author=inter.author
            ))

        if len(embed_list) == 1:
            field_dict_list = [{
                "name": f"no rounds have ended",
                "value": f"please wait till after the first round is over"
            }]

            embed_list = embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                title=embed_title,
                field_list=field_dict_list,
                thumbnail=self.clan.badge.small,
                author=inter.author
            )

        self.label = btn_name

        # edit the original message with the updated embeds
        await inter.edit_original_message(
            embeds=embed_list, view=self.view)


class CWLClanScoreboardBtn(Button):
    def __init__(
        self,
        client_data: ClientData.ClashDiscord_Data,
        coc_client,
        clan: Clan,
        group: ClanWarLeagueGroup,
        btn_name: str = "CWL Clan Scoreboard",
        btn_style: ButtonStyle = ButtonStyle.primary
    ):
        super().__init__(
            label=btn_name,
            style=btn_style)
        self.client_data = client_data
        self.coc_client = coc_client
        self.clan = clan
        self.group = group

    async def callback(
            self,
            inter: MessageInteraction):

        await inter.response.defer()

        if self.group is None:
            embed_description = f"could not find CWL group"

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
        embed_description = f"**{self.clan.name} {self.clan.tag}**"

        round_index = 0

        for cwl_round in self.group.rounds:

            # checking if war has ended
            war = await self.coc_client.get_league_war(cwl_round[0])
            if war.state != "warEnded":
                break

            # update round index
            round_index += 1

        if round_index == 0:
            field_dict_list = [{
                "name": f"no rounds have ended",
                "value": f"please wait till after the first round is over"
            }]

        else:
            field_dict_list = await cwl_scoreboard_clan(
                inter, self.group, self.clan, self.coc_client,
                inter.client.emojis, self.client_data.emojis)

        embed_list = embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            title=embed_title,
            description=embed_description,
            field_list=field_dict_list,
            thumbnail=self.clan.badge.small,
            author=inter.author)

        self.label = btn_name

        # edit the original message with the updated embeds
        await inter.edit_original_message(
            embeds=embed_list, view=self.view)


class CWLMissingAttacksBtn(Button):
    def __init__(
        self,
        client_data: ClientData.ClashDiscord_Data,
        coc_client,
        clan: Clan,
        group: ClanWarLeagueGroup,
        btn_name: str = "CWL Missing Attacks",
        btn_style: ButtonStyle = ButtonStyle.primary
    ):
        super().__init__(
            label=btn_name,
            style=btn_style)
        self.client_data = client_data
        self.coc_client = coc_client
        self.clan = clan
        self.group = group

    async def callback(
            self,
            inter: MessageInteraction):

        await inter.response.defer()

        if self.group is None:
            embed_description = f"could not find CWL group"

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

        embed_title = f"{self.clan.name} CWL Missed Attacks"

        field_dict_list = await cwl_clan_noatk(
            self.clan, self.group, self.coc_client,
            inter.client.emojis, self.client_data.emojis)

        embed_list = embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=embed_title,
            bot_user_name=inter.me.display_name,
            thumbnail=self.clan.badge.small,
            field_list=field_dict_list,
            author=inter.author)

        self.label = btn_name

        # edit the original message with the updated embeds
        await inter.edit_original_message(
            embeds=embed_list, view=self.view)
