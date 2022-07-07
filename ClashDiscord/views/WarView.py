from disnake.ui import View
from coc.wars import ClanWar
from data import ClashDiscord_Client_Data as ClientData
from buttons.WarButtons import (
    WarInfoBtn,
    WarClanLineupBtn,
    WarNoAttackBtn)


class WarView(View):

    def __init__(
            self,
            client_data: ClientData.ClashDiscord_Data,
            coc_client,
            war: ClanWar):
        super().__init__(timeout=None)

        # * INFO
        self.add_item(WarInfoBtn(
            client_data=client_data,
            coc_client=coc_client,
            war=war,
            btn_name=f"{war.clan.name} War Info"))

        # * OVERVIEW LINEUP

        # * CLAN LINEUP
        self.add_item(WarClanLineupBtn(
            client_data=client_data,
            coc_client=coc_client,
            war=war,
            btn_name=f"{war.clan.name} War Clan Lineup"))

        # * WAR NOATTACK
        self.add_item(WarNoAttackBtn(
            client_data=client_data,
            coc_client=coc_client,
            war=war,
            btn_name=f"{war.clan.name} War No Attack"))

        # * SCOREBOARD
