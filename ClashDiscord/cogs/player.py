import disnake
from disnake.ext import commands
from responders import (
    DiscordResponder as discord_responder,
    ClashResponder as clash_responder,
    RazBotDB_Responder as db_responder
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

    # player info
    @player.sub_command_group()
    async def info(self, inter):
        """
            group for player info commands
        """

        pass

    @info.sub_command()
    async def overview(
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

        verification_payload = await discord_responder.player_verification(
            db_player_obj, user, self.coc_client)
        if not verification_payload['verified']:
            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                field_list=verification_payload['field_dict_list'],
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(embed_list, inter)
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(embed_list, inter)
                return

        field_dict_list = discord_responder.player_info(
            player, inter.client.emojis, self.client_data.emojis)

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{player.name} {player.tag}",
            bot_user_name=inter.me.display_name,
            thumbnail=player.league.icon,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)

    @info.sub_command()
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

        verification_payload = await discord_responder.player_verification(
            db_player_obj, user, self.coc_client)
        if not verification_payload['verified']:
            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                field_list=verification_payload['field_dict_list'],
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(embed_list, inter)
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(embed_list, inter)
                return

        player_field_dict_list = discord_responder.player_info(
            player, inter.client.emojis, self.client_data.emojis)

        embed_list = []

        embed_list.extend(discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{player.name} {player.tag}",
            bot_user_name=inter.me.display_name,
            thumbnail=player.league.icon,
            field_list=player_field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        ))

        unit_field_dict_list = discord_responder.unit_lvl_all(
            player, inter.client.emojis, self.client_data.emojis)

        embed_list.extend(discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{player.name} units",
            bot_user_name=inter.me.display_name,
            thumbnail=player.league.icon,
            field_list=unit_field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        ))

        await discord_responder.send_embed_list(embed_list, inter)

        player_links = ""

        player_links += discord_responder.link_clash_of_stats(player)

        player_links += "\n\n"

        player_links += discord_responder.link_chocolate_clash(player)

        await inter.send(content=player_links)

    # player unit
    @player.sub_command_group()
    async def unit(self, inter):
        """
            group for player unit commands
        """

        pass

    @unit.sub_command()
    async def find(
        self,
        inter,
        unit_name: str = commands.Param(
            name=discord_utils.command_param_dict['unit_name'].name,
            description=discord_utils.command_param_dict['unit_name'].description,
            autocomplete=discord_utils.autocomp_unit
        ),
        user: disnake.User = discord_utils.command_param_dict['user'],
        tag: str = discord_utils.command_param_dict['tag']
    ):
        """
            get information about a specified player

            Parameters
            ----------
            unit_name: name of the unit you would like information on
            user (optional): user to search for active player
            tag (optional): tag to search
        """

        # setting user to author if not specified
        if user is None:
            user = inter.author

        db_player_obj = db_responder.read_player_active(user.id)

        verification_payload = await discord_responder.player_verification(
            db_player_obj, user, self.coc_client)
        if not verification_payload['verified']:
            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                field_list=verification_payload['field_dict_list'],
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(embed_list, inter)
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(embed_list, inter)
                return

        unit_obj = clash_responder.find_player_unit(player, unit_name)
        field_dict_list = [discord_responder.unit_lvl(
            player, unit_obj, unit_name,
            inter.client.emojis, self.client_data.emojis)]
        # unit_obj not found
        # set title to player name
        if not unit_obj:
            title_string = player.name
        # unit_obj found
        # set title to player_name unit_name
        else:
            title_string = f"{player.name} {unit_obj.name}"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=title_string,
            bot_user_name=inter.me.display_name,
            thumbnail=player.league.icon,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)

    @unit.sub_command()
    async def all(
        self,
        inter,
        unit_type: str = discord_utils.command_param_dict['unit_type'],
        user: disnake.User = discord_utils.command_param_dict['user'],
        tag: str = discord_utils.command_param_dict['tag']
    ):
        """
            get all unit levels

            Parameters
            ----------
            unit_type (optional): type of unit to return information for
            user (optional): user to search for active player
            tag (optional): tag to search
        """

        # setting user to author if not specified
        if user is None:
            user = inter.author

        db_player_obj = db_responder.read_player_active(user.id)

        verification_payload = await discord_responder.player_verification(
            db_player_obj, user, self.coc_client)
        if not verification_payload['verified']:
            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                field_list=verification_payload['field_dict_list'],
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(embed_list, inter)
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(embed_list, inter)
                return

        if unit_type == "all":
            field_dict_list = discord_responder.unit_lvl_all(
                player, inter.client.emojis, self.client_data.emojis
            )
        elif unit_type == "hero":
            field_dict_list = discord_responder.hero_lvl_all(
                player, inter.client.emojis, self.client_data.emojis
            )
        elif unit_type == "pet":
            field_dict_list = discord_responder.pet_lvl_all(
                player, inter.client.emojis, self.client_data.emojis
            )
        elif unit_type == "troop":
            field_dict_list = discord_responder.troop_lvl_all(
                player, inter.client.emojis, self.client_data.emojis
            )
        elif unit_type == "spell":
            field_dict_list = discord_responder.spell_lvl_all(
                player, inter.client.emojis, self.client_data.emojis
            )
        elif unit_type == "siege":
            field_dict_list = discord_responder.siege_lvl_all(
                player, inter.client.emojis, self.client_data.emojis
            )

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{player.name} units",
            bot_user_name=inter.me.display_name,
            thumbnail=player.league.icon,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)

    # player supertroop
    @player.sub_command_group()
    async def supertroop(self, inter):
        """
            group for player supertroop commands
        """

        pass

    @supertroop.sub_command()
    async def active(
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

        verification_payload = await discord_responder.player_verification(
            db_player_obj, user, self.coc_client)
        if not verification_payload['verified']:
            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                field_list=verification_payload['field_dict_list'],
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(embed_list, inter)
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(embed_list, inter)
                return

        active_super_troop_list = clash_responder.player_active_super_troops(
            player)

        field_dict_list = discord_responder.active_super_troops(
            player, active_super_troop_list,
            inter.client.emojis, self.client_data.emojis
        )
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{player.name} super troops",
            bot_user_name=inter.me.display_name,
            thumbnail=player.league.icon,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
