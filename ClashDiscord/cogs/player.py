import disnake
from disnake.ui import View, Button
from disnake.ext import commands
from views.PlayerView import PlayerView
from views import ViewModels
from buttons.ButtonModels import (
    LinkButton)
from responders import (
    DiscordResponder as discord_responder,
    ClashResponder as clash_responder,
    RazBotDB_Responder as db_responder,
    AuthResponder as auth_responder,
    PlayerResponder as player_responder
)
from utils import discord_utils


class Player(commands.Cog):
    def __init__(self, bot, coc_client, client_data):
        self.bot = bot
        self.coc_client = coc_client
        self.client_data = client_data

    @commands.slash_command()
    async def player(self, inter):
        """
            parent for player commands
        """

        # defer for every command
        await inter.response.defer()

    @player.sub_command()
    async def info(
        self,
        inter,
        user: disnake.User = discord_utils.command_param_dict['user'],
        tag: str = discord_utils.command_param_dict['tag']
    ):
        """
            get player information

            Parameters
            ----------
            user (optional): user to search for active player
            tag (optional): tag to search
        """

        # setting user to author if not specified
        if user is None:
            user = inter.author

        db_player_obj = db_responder.read_player_active(user.id)

        verification_payload = await auth_responder.player_verification(
            db_player_obj, user, self.coc_client)
        if not verification_payload['verified']:
            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                field_list=verification_payload['field_dict_list'],
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        player = verification_payload['player_obj']

        # player tag selected
        if tag is not None:
            player = await clash_responder.get_player(tag, self.coc_client)

            if player is None:
                embed_description = f"could not find player with tag {tag}"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    bot_user_name=inter.me.display_name,
                    description=embed_description,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

        embed_thumbnail = discord_responder.get_town_hall_url(player)

        field_dict_list = player_responder.player_info(
            player, inter.client.emojis, self.client_data.emojis)

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{player.name} {player.tag}",
            bot_user_name=inter.me.display_name,
            thumbnail=embed_thumbnail,
            field_list=field_dict_list,
            author=inter.author)

        view = PlayerView(
            client_data=self.client_data,
            coc_client=self.coc_client,
            player=player)

        await inter.send(embeds=embed_list, view=view)

    @player.sub_command()
    async def recruit(
        self,
        inter,
        user: disnake.User = discord_utils.command_param_dict['user'],
        tag: str = discord_utils.command_param_dict['tag']
    ):
        """
            get player recruitment information

            Parameters
            ----------
            user (optional): user to search for active player
            tag (optional): tag to search
        """

        # setting user to author if not specified
        if user is None:
            user = inter.author

        db_player_obj = db_responder.read_player_active(user.id)

        verification_payload = await auth_responder.player_verification(
            db_player_obj, user, self.coc_client)
        if not verification_payload['verified']:
            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                field_list=verification_payload['field_dict_list'],
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        player = verification_payload['player_obj']

        # player tag selected
        if tag is not None:
            player = await clash_responder.get_player(tag, self.coc_client)

            if player is None:
                embed_description = f"could not find player with tag {tag}"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    bot_user_name=inter.me.display_name,
                    description=embed_description,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

        embed_thumbnail = discord_responder.get_town_hall_url(player)

        player_field_dict_list = player_responder.player_info(
            player, inter.client.emojis, self.client_data.emojis)

        embed_list = []

        embed_list.extend(discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{player.name} {player.tag}",
            bot_user_name=inter.me.display_name,
            thumbnail=embed_thumbnail,
            field_list=player_field_dict_list,
            author=inter.author
        ))

        unit_field_dict_list = player_responder.unit_lvl_all(
            player, inter.client.emojis, self.client_data.emojis)

        embed_list.extend(discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{player.name} units",
            bot_user_name=inter.me.display_name,
            thumbnail=embed_thumbnail,
            field_list=unit_field_dict_list,
            author=inter.author
        ))

        button_list: list[Button] = []

        url = player_responder.link_clash_of_stats(player)

        # clash of stats player link
        button_list.append(LinkButton(
            btn_name=f"{player.name} Clash of Stats",
            url=url))

        url = player_responder.link_chocolate_clash(player)

        # chocolate clash player link
        button_list.append(LinkButton(
            btn_name=f"{player.name} Chocolate Clash",
            url=url))

        player_button_links: View = ViewModels.ButtonListView(
            buttons=button_list)

        await inter.send(
            embeds=embed_list, view=player_button_links)

    @player.sub_command()
    async def units(
        self,
        inter,
        user: disnake.User = discord_utils.command_param_dict['user'],
        tag: str = discord_utils.command_param_dict['tag']
    ):
        """
            get all unit levels for a player

            Parameters
            ----------
            user (optional): user to search for active player
            tag (optional): tag to search
        """

        # setting user to author if not specified
        if user is None:
            user = inter.author

        db_player_obj = db_responder.read_player_active(user.id)

        verification_payload = await auth_responder.player_verification(
            db_player_obj, user, self.coc_client)
        if not verification_payload['verified']:
            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                field_list=verification_payload['field_dict_list'],
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        player = verification_payload['player_obj']

        # player tag selected
        if tag is not None:
            player = await clash_responder.get_player(tag, self.coc_client)

            if player is None:
                embed_description = f"could not find player with tag {tag}"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    bot_user_name=inter.me.display_name,
                    description=embed_description,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

        title_string = f"{player.name} units"
        embed_thumbnail = discord_responder.get_town_hall_url(player)

        field_dict_list = player_responder.unit_lvl_all(
            player, inter.client.emojis, self.client_data.emojis
        )

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=title_string,
            bot_user_name=inter.me.display_name,
            thumbnail=embed_thumbnail,
            field_list=field_dict_list,
            author=inter.author)

        view = PlayerView(
            client_data=self.client_data,
            coc_client=self.coc_client,
            player=player)

        await inter.send(embeds=embed_list, view=view)

    @player.sub_command()
    async def supertroops(
        self,
        inter,
        user: disnake.User = discord_utils.command_param_dict['user'],
        tag: str = discord_utils.command_param_dict['tag']
    ):
        """
            check to see player's active super troops

            Parameters
            ----------
            user (optional): user to search for active player
            tag (optional): tag to search
        """

        # setting user to author if not specified
        if user is None:
            user = inter.author

        db_player_obj = db_responder.read_player_active(user.id)

        verification_payload = await auth_responder.player_verification(
            db_player_obj, user, self.coc_client)
        if not verification_payload['verified']:
            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                field_list=verification_payload['field_dict_list'],
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        player = verification_payload['player_obj']

        # player tag selected
        if tag is not None:
            player = await clash_responder.get_player(tag, self.coc_client)

            if player is None:
                embed_description = f"could not find player with tag {tag}"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    bot_user_name=inter.me.display_name,
                    description=embed_description,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

        active_super_troop_list = clash_responder.player_active_super_troops(
            player)

        embed_thumbnail = discord_responder.get_town_hall_url(player)

        field_dict_list = player_responder.active_super_troops(
            player, active_super_troop_list,
            inter.client.emojis, self.client_data.emojis
        )
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{player.name} Active Super Troops",
            bot_user_name=inter.me.display_name,
            thumbnail=embed_thumbnail,
            field_list=field_dict_list,
            author=inter.author)

        view = PlayerView(
            client_data=self.client_data,
            coc_client=self.coc_client,
            player=player)

        await inter.send(embeds=embed_list, view=view)
