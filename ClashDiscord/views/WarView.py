from disnake.ui import View
from coc.wars import ClanWar
from data import ClashDiscord_Client_Data as ClientData
from buttons.WarButtons import (
    WarInfoBtn,
    WarLineupClanBtn,
    WarLineupCountBtn,
    WarMissingAttacksBtn,
    WarClanScoreboardBtn)


class WarView(View):

    def __init__(
            self,
            discord_emojis: list,
            client_data: ClientData.ClashDiscord_Data,
            coc_client,
            war: ClanWar):
        super().__init__(timeout=None)

        # * INFO
        self.add_item(WarInfoBtn(
            discord_emojis=discord_emojis,
            client_data=client_data,
            coc_client=coc_client,
            war=war,
            btn_name=f"{war.clan.name} War Info"))

        # * CLAN LINEUP
        self.add_item(WarLineupClanBtn(
            discord_emojis=discord_emojis,
            client_data=client_data,
            coc_client=coc_client,
            war=war,
            btn_name=f"{war.clan.name} War Clan Lineup"))

        # * COUNT LINEUP
        self.add_item(WarLineupCountBtn(
            discord_emojis=discord_emojis,
            client_data=client_data,
            coc_client=coc_client,
            war=war,
            btn_name=f"{war.clan.name} War Lineup Count"))

        # * WAR CLAN SCOREBOARD
        self.add_item(WarClanScoreboardBtn(
            discord_emojis=discord_emojis,
            client_data=client_data,
            coc_client=coc_client,
            war=war,
            btn_name=f"{war.clan.name} War Scoreboard"))

        # * WAR MISSING ATTACKS
        self.add_item(WarMissingAttacksBtn(
            discord_emojis=discord_emojis,
            client_data=client_data,
            coc_client=coc_client,
            war=war,
            btn_name=f"{war.clan.name} War Missing Attacks"))
