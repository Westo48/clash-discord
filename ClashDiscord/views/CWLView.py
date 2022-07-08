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
            client_data: ClientData.ClashDiscord_Data,
            coc_client,
            clan: Clan,
            group: ClanWarLeagueGroup):
        super().__init__(timeout=None)

        # * INFO
        self.add_item(CWLInfoBtn(
            client_data=client_data,
            coc_client=coc_client,
            clan=clan,
            group=group,
            btn_name=f"{clan.name} CWL Info"))

        # * CWL LINEUP
        self.add_item(CWLLineupBtn(
            client_data=client_data,
            coc_client=coc_client,
            clan=clan,
            group=group,
            btn_name=f"{clan.name} CWL Lineup"))

        # * CWL GROUP SCOREBOARD
        self.add_item(CWLGroupScoreboardBtn(
            client_data=client_data,
            coc_client=coc_client,
            clan=clan,
            group=group,
            btn_name=f"{clan.name} CWL Group Scoreboard"))

        # * CWL ROUND SCOREBOARD
        self.add_item(CWLRoundScoreboardBtn(
            client_data=client_data,
            coc_client=coc_client,
            clan=clan,
            group=group,
            btn_name=f"{clan.name} CWL Rounds Scoreboard"))

        # * CWL CLAN SCOREBOARD
        self.add_item(CWLClanScoreboardBtn(
            client_data=client_data,
            coc_client=coc_client,
            clan=clan,
            group=group,
            btn_name=f"{clan.name} CWL Clan Scoreboard"))

        # * CWL MISSING ATTACKS
        self.add_item(CWLMissingAttacksBtn(
            client_data=client_data,
            coc_client=coc_client,
            clan=clan,
            group=group,
            btn_name=f"{clan.name} CWL Missing Attacks"))
