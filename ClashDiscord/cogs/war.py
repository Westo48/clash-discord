import disnake
from disnake.ext import commands
from responders import (
    DiscordResponder as discord_responder,
    ClashResponder as clash_responder,
    RazBotDB_Responder as db_responder
)
from utils import discord_utils


class War(commands.Cog):
    def __init__(self, bot, coc_client, client_data):
        self.bot = bot
        self.coc_client = coc_client
        self.client_data = client_data

    @commands.slash_command()
    async def war(self, inter):
        """
            parent for war commands
        """

        # defer for every command
        await inter.response.defer()

    @war.sub_command()
    async def info(
        self,
        inter,
        clan_role: disnake.Role = discord_utils.command_param_dict['clan_role'],
        war_selection: str = discord_utils.command_param_dict['war_selection']
    ):
        """
            war info

            Parameters
            ----------
            clan_role (optional): clan role to use linked clan
            war_selection (optional): cwl war selection
        """

        # role not mentioned
        if clan_role is None:
            db_player_obj = db_responder.read_player_active(inter.author.id)

            verification_payload = await discord_responder.war_verification(
                db_player_obj, war_selection, inter.author, self.coc_client)
        # role has been mentioned
        else:
            verification_payload = await discord_responder.clan_role_war_verification(
                clan_role, war_selection, self.coc_client)

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

        war_obj = verification_payload['war_obj']

        field_dict_list = discord_responder.war_scoreboard(
            war_obj, inter.client.emojis, self.client_data.emojis)

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
            bot_user_name=inter.me.display_name,
            thumbnail=war_obj.clan.badge,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)

    @war.sub_command()
    async def noattack(
        self,
        inter,
        missed_attacks: int = discord_utils.command_param_dict['missed_attacks'],
        clan_role: disnake.Role = discord_utils.command_param_dict['clan_role'],
        war_selection: str = discord_utils.command_param_dict['war_selection']
    ):
        """
            list of players that missed attacks in the current war

            Parameters
            ----------
            missed_attacks (optional): specified missed attack count
            clan_role (optional): clan role to use linked clan
            war_selection (optional): cwl war selection
        """

        # role not mentioned
        if clan_role is None:
            db_player_obj = db_responder.read_player_active(inter.author.id)

            verification_payload = await discord_responder.war_verification(
                db_player_obj, war_selection, inter.author, self.coc_client)

        # role has been mentioned
        else:
            verification_payload = await discord_responder.clan_role_war_verification(
                clan_role, war_selection, self.coc_client)

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

        war_obj = verification_payload['war_obj']

        field_dict_list = discord_responder.war_no_attack(
            war_obj, missed_attacks)

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
            bot_user_name=inter.me.display_name,
            thumbnail=war_obj.clan.badge,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)

    @war.sub_command()
    async def stars(
        self,
        inter,
        option: str = discord_utils.command_param_dict['war_stars'],
        clan_role: disnake.Role = discord_utils.command_param_dict['clan_role'],
        war_selection: str = discord_utils.command_param_dict['war_selection']
    ):
        """
            *leadership*
            overview of all members in war

            Parameters
            ----------
            clan_role (optional): clan role to use linked clan
            war_selection (optional): cwl war selection
        """

        # role not mentioned
        if clan_role is None:
            db_player_obj = db_responder.read_player_active(inter.author.id)

            verification_payload = (
                await discord_responder.war_leadership_verification(
                    db_player_obj, war_selection,
                    inter.author, inter.guild.id, self.coc_client))
        # role has been mentioned
        else:
            verification_payload = (
                await discord_responder.clan_role_war_leadership_verification(
                    clan_role, war_selection,
                    inter.author, inter.guild.id, self.coc_client))

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

        war_obj = verification_payload['war_obj']

        if option == "stars":
            embed_title = f"{war_obj.clan.name} vs. {war_obj.opponent.name}"
            field_dict_list = discord_responder.war_clan_stars(
                war_obj, inter.client.emojis, self.client_data.emojis)
        elif option == "attacks":
            embed_title = f"{war_obj.clan.name} vs. {war_obj.opponent.name}"
            field_dict_list = discord_responder.war_all_attacks(
                war_obj, inter.client.emojis, self.client_data.emojis)
        else:
            embed_title = None
            field_dict_list = [{
                'name': "incorrect option selected",
                'value': "please select a different option"
            }]

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=embed_title,
            bot_user_name=inter.me.display_name,
            thumbnail=war_obj.clan.badge,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)

    @war.sub_command_group()
    async def score(self, inter):
        """
            parent for war score commands
        """

        pass

    @score.sub_command()
    async def user(
        self,
        inter,
        user: disnake.User = discord_utils.command_param_dict['user'],
        war_selection: str = discord_utils.command_param_dict['war_selection']
    ):
        """
            your war member score

            Parameters
            ----------
            user (optional): user to search for active player
            war_selection (optional): cwl war selection
        """

        # setting user to author if not specified
        if user is None:
            user = inter.author

        db_player_obj = db_responder.read_player_active(user.id)

        verification_payload = await discord_responder.war_verification(
            db_player_obj, war_selection, user, self.coc_client)
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

        player_obj = verification_payload['player_obj']
        war_obj = verification_payload['war_obj']

        field_dict_list = discord_responder.war_member_score(
            war_obj, player_obj)
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{player_obj.name} war score",
            bot_user_name=inter.me.display_name,
            thumbnail=player_obj.clan.badge,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)

    @score.sub_command()
    async def clan(
        self,
        inter,
        clan_role: disnake.Role = discord_utils.command_param_dict['clan_role'],
        war_selection: str = discord_utils.command_param_dict['war_selection']
    ):
        """
            *leadership*
            every clanmate's war member score

            Parameters
            ----------
            clan_role (optional): clan role to use linked clan
            war_selection (optional): cwl war selection
        """

        # role not mentioned
        if clan_role is None:
            db_player_obj = db_responder.read_player_active(inter.author.id)

            verification_payload = (
                await discord_responder.war_leadership_verification(
                    db_player_obj, war_selection,
                    inter.author, inter.guild.id, self.coc_client))
        # role has been mentioned
        else:
            verification_payload = (
                await discord_responder.clan_role_war_leadership_verification(
                    clan_role, war_selection,
                    inter.author, inter.guild.id, self.coc_client))

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

        war_obj = verification_payload['war_obj']

        field_dict_list = discord_responder.war_clan_score(
            war_obj)
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{war_obj.clan.name} vs. {war_obj.opponent.name}",
            bot_user_name=inter.me.display_name,
            thumbnail=war_obj.clan.badge,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)

    @war.sub_command()
    async def lineup(
        self,
        inter,
        option: str = discord_utils.command_param_dict['war_lineup'],
        clan_role: disnake.Role = discord_utils.command_param_dict['clan_role'],
        war_selection: str = discord_utils.command_param_dict['war_selection']
    ):
        """
            town hall lineup overview for war

            Parameters
            ----------
            clan_role (optional): clan role to use linked clan
            war_selection (optional): cwl war selection
        """

        # role not mentioned
        if clan_role is None:
            db_player_obj = db_responder.read_player_active(inter.author.id)

            verification_payload = await discord_responder.war_verification(
                db_player_obj, war_selection, inter.author, self.coc_client)
        # role has been mentioned
        else:
            verification_payload = await discord_responder.clan_role_war_verification(
                clan_role, war_selection, self.coc_client)

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

        war_obj = verification_payload['war_obj']

        if option == "overview":
            await inter.edit_original_message(
                content=discord_responder.war_lineup_overview(war_obj))

            return

        elif option == "clan":
            embed_title = f"{war_obj.clan.name} vs. {war_obj.opponent.name}"
            field_dict_list = discord_responder.war_lineup_clan(
                war_obj, inter.client.emojis, self.client_data.emojis)

        elif option == "member":
            embed_title = f"{war_obj.clan.name} vs. {war_obj.opponent.name}"
            field_dict_list = await discord_responder.war_lineup_member(
                war_obj.opponent, self.coc_client,
                inter.client.emojis, self.client_data.emojis)
        else:
            embed_title = None
            field_dict_list = [{
                'name': "incorrect option selected",
                'value': "please select a different option"
            }]

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=embed_title,
            bot_user_name=inter.me.display_name,
            thumbnail=war_obj.clan.badge,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
