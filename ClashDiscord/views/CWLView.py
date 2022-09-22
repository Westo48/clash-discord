from disnake.ui import View
from coc.clans import Clan
from coc.wars import (
    ClanWarLeagueGroup)
from data import ClashDiscord_Client_Data as ClientData
from buttons.CWLButtons import (
    CWLInfoBtn,
    CWLLineupBtn,
    CWLGroupScoreboardBtn,
    CWLRoundScoreboardBtn,
    CWLClanScoreboardBtn,
    CWLMissingAttacksBtn)


class CWLView(View):

    def __init__(
            self,
            discord_emojis: list,
            client_data: ClientData.ClashDiscord_Data,
            coc_client,
            clan: Clan,
            group: ClanWarLeagueGroup):
        super().__init__(timeout=None)

        # * INFO
        self.add_item(CWLInfoBtn(
            discord_emojis=discord_emojis,
            client_data=client_data,
            coc_client=coc_client,
            clan=clan,
            group=group,
            btn_name=f"{clan.name} CWL Info"))

        # * CWL LINEUP
        self.add_item(CWLLineupBtn(
            discord_emojis=discord_emojis,
            client_data=client_data,
            coc_client=coc_client,
            clan=clan,
            group=group,
            btn_name=f"{clan.name} CWL Lineup"))

        # * CWL GROUP SCOREBOARD
        self.add_item(CWLGroupScoreboardBtn(
            discord_emojis=discord_emojis,
            client_data=client_data,
            coc_client=coc_client,
            clan=clan,
            group=group,
            btn_name=f"{clan.name} CWL Group Scoreboard"))

        # * CWL ROUND SCOREBOARD
        self.add_item(CWLRoundScoreboardBtn(
            discord_emojis=discord_emojis,
            client_data=client_data,
            coc_client=coc_client,
            clan=clan,
            group=group,
            btn_name=f"{clan.name} CWL Rounds Scoreboard"))

        # * CWL CLAN SCOREBOARD
        self.add_item(CWLClanScoreboardBtn(
            discord_emojis=discord_emojis,
            client_data=client_data,
            coc_client=coc_client,
            clan=clan,
            group=group,
            btn_name=f"{clan.name} CWL Clan Scoreboard"))

        # * CWL MISSING ATTACKS
        self.add_item(CWLMissingAttacksBtn(
            discord_emojis=discord_emojis,
            client_data=client_data,
            coc_client=coc_client,
            clan=clan,
            group=group,
            btn_name=f"{clan.name} CWL Missing Attacks"))
