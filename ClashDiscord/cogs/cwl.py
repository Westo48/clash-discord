import disnake
from disnake.ext import commands
from coc.utils import get
from responders import (
    DiscordResponder as discord_responder,
    ClashResponder as clash_responder,
    RazBotDB_Responder as db_responder
)
from utils import discord_utils


class CWL(commands.Cog):
    def __init__(self, bot, coc_client, client_data):
        self.bot = bot
        self.coc_client = coc_client
        self.client_data = client_data

    @commands.slash_command()
    async def cwl(self, inter):
        """
            parent for cwl commands
        """

        # defer for every command
        await inter.response.defer()

    @cwl.sub_command()
    async def lineup(
        self,
        inter,
        option: str = discord_utils.command_param_dict['war_lineup'],
        clan_role: disnake.Role = discord_utils.command_param_dict['clan_role']
    ):
        """
            returns the CWL group lineup

            Parameters
            ----------
            clan_role (optional): clan role to use linked clan
        """

        # role not mentioned
        if clan_role is None:
            db_player_obj = db_responder.read_player_active(inter.author.id)

            verification_payload = await discord_responder.cwl_group_verification(
                db_player_obj, inter.author, self.coc_client)
        # role has been mentioned
        else:
            verification_payload = await discord_responder.clan_role_cwl_group_verification(
                clan_role, self.coc_client)

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

        cwl_group_obj = verification_payload['cwl_group_obj']

        if option == "overview":
            await inter.edit_original_message(
                content=discord_responder.cwl_lineup(cwl_group_obj))

            return

        elif option == "clan":
            for clan in cwl_group_obj.clans:
                field_dict_list = await discord_responder.war_lineup_member(
                    clan, self.coc_client, inter.client.emojis, self.client_data.emojis)

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    title=f"{clan.name} {clan.tag} CWL Lineup",
                    bot_user_name=inter.me.display_name,
                    thumbnail=clan.badge,
                    field_list=field_dict_list,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(embed_list, inter)

            return

        elif option == "member":
            for clan in cwl_group_obj.clans:
                field_dict_list = await discord_responder.war_lineup_member(
                    clan, self.coc_client, inter.client.emojis, self.client_data.emojis)

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    title=f"{clan.name} {clan.tag} CWL Lineup",
                    bot_user_name=inter.me.display_name,
                    thumbnail=clan.badge,
                    field_list=field_dict_list,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(embed_list, inter)

            return

        else:
            field_dict_list = [{
                'name': "incorrect option selected",
                'value': "please select a different option"
            }]

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)

    @cwl.sub_command_group()
    async def score(self, inter):
        """
            parent for cwl score commands
        """

        pass

    @score.sub_command()
    async def user(
        self,
        inter,
        user: disnake.User = discord_utils.command_param_dict['user']
    ):
        """
            returns specified user's active player's cwl score

            Parameters
            ----------
            user (optional): user to search for active player
        """

        # setting user to author if not specified
        if user is None:
            user = inter.author

        db_player_obj = db_responder.read_player_active(user.id)

        verification_payload = await discord_responder.cwl_group_verification(
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

        player_obj = verification_payload['player_obj']
        cwl_group_obj = verification_payload['cwl_group_obj']

        field_dict_list = await discord_responder.cwl_member_score(
            player_obj, cwl_group_obj, player_obj.clan.tag)
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{player_obj.name} CWL score",
            bot_user_name=inter.me.display_name,
            thumbnail=player_obj.league.icon,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)

    @score.sub_command()
    async def clan(
        self,
        inter,
        clan_role: disnake.Role = discord_utils.command_param_dict['clan_role']
    ):
        """
            *leadership*
            returns all member scores for the specified clan

            Parameters
            ----------
            clan_role (optional): clan role to use linked clan
        """

        # role not mentioned
        if clan_role is None:
            db_player_obj = db_responder.read_player_active(inter.author.id)

            verification_payload = (
                await discord_responder.cwl_group_leadership_verification(
                    db_player_obj, inter.author, inter.guild.id, self.coc_client)
            )
        # role has been mentioned
        else:
            verification_payload = (
                await discord_responder.clan_role_cwl_group_leadership_verification(
                    clan_role, inter.author, inter.guild.id, self.coc_client))

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
        clan_obj = verification_payload['clan_obj']
        cwl_group_obj = verification_payload['cwl_group_obj']

        field_dict_list = await discord_responder.cwl_clan_score(
            clan_obj, cwl_group_obj)
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{clan_obj.name} CWL scores",
            bot_user_name=inter.me.display_name,
            thumbnail=player_obj.clan.badge,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
