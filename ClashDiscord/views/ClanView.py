from disnake.ui import View
from coc.clans import Clan
from data import ClashDiscord_Client_Data as ClientData
from buttons.ClanButtons import (
    ClanInfoBtn,
    ClanLineupBtn,
    ClanWarPreferenceBtn,
    ClanSuperTroopBtn)


class ClanView(View):

    def __init__(
            self,
            client_data: ClientData.ClashDiscord_Data,
            coc_client,
            clan: Clan):
        super().__init__(timeout=None)

        # * INFO
        self.add_item(ClanInfoBtn(
            client_data=client_data,
            coc_client=coc_client,
            clan=clan,
            btn_name=f"{clan.name} Info"))

        # * LINEUP
        self.add_item(ClanLineupBtn(
            client_data=client_data,
            coc_client=coc_client,
            clan=clan,
            btn_name=f"{clan.name} Lineup"))

        # * WAR PREFERENCE
        self.add_item(ClanWarPreferenceBtn(
            client_data=client_data,
            coc_client=coc_client,
            clan=clan,
            btn_name=f"{clan.name} War Preference"))

        # * SUPER TROOP
        self.add_item(ClanSuperTroopBtn(
            client_data=client_data,
            coc_client=coc_client,
            player=clan,
            btn_name=f"{clan.name} Super Troops"))
