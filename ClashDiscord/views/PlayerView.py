from disnake.ui import View
from coc.players import Player
from data import ClashDiscord_Client_Data as ClientData
from buttons.PlayerButtons import (
    PlayerInfoBtn,
    PlayerUnitsBtn,
    PlayerSuperTroopBtn)


class PlayerView(View):

    def __init__(
            self,
            client_data: ClientData.ClashDiscord_Data,
            coc_client,
            player: Player):
        super().__init__(timeout=None)

        # * INFO
        self.add_item(PlayerInfoBtn(
            client_data=client_data,
            coc_client=coc_client,
            player=player,
            btn_name=f"{player.name} Info"))

        # * UNITS
        self.add_item(PlayerUnitsBtn(
            client_data=client_data,
            coc_client=coc_client,
            player=player,
            btn_name=f"{player.name} Units"))

        # * SUPER TROOP
        self.add_item(PlayerSuperTroopBtn(
            client_data=client_data,
            coc_client=coc_client,
            player=player,
            btn_name=f"{player.name} Super Troops"))
