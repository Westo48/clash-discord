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
    async def info(
        self,
        inter: disnake.ApplicationCommandInteraction,
        clan_role: disnake.Role = discord_utils.command_param_dict['clan_role']
    ):
        """
            CWL info

            Parameters
            ----------
            clan_role (optional): clan role to use linked clan
        """

        # getting the cwl group

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

            await discord_responder.send_embed_list(inter, embed_list)
            return

        cwl_group = verification_payload['cwl_group_obj']

        # get the clan object from player or clan
        if "clan_obj" in verification_payload:
            clan = verification_payload['clan_obj']

        elif "player_obj" in verification_payload:
            clan = await verification_payload['player_obj'].get_detailed_clan()

        # getting the war

        war_selection = None
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

            await discord_responder.send_embed_list(inter, embed_list)
            return

        cwl_war = verification_payload['war_obj']

        league_emoji = discord_responder.get_emoji(
            f"Clan War {clan.war_league.name}",
            inter.client.emojis,
            self.client_data.emojis)

        embed_title = f"CWL {league_emoji} {clan.war_league.name} Group"

        # get current round number
        round_number = clash_responder.cwl_current_round(
            cwl_group, cwl_war)

        embed_description = f"Round {round_number}/{cwl_group.number_of_rounds}"

        field_dict_list = discord_responder.cwl_info_scoreboard(
            cwl_war, inter.client.emojis, self.client_data.emojis)

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            thumbnail=clan.badge.small,
            title=embed_title,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url)

        await discord_responder.send_embed_list(inter, embed_list)

    @cwl.sub_command()
    async def lineup(
        self,
        inter,
        option: str = discord_utils.command_param_dict['war_lineup'],
        clan_role: disnake.Role = discord_utils.command_param_dict['clan_role']
    ):
        """
            CWL town hall lineup 
            *default option is clan*

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

            await discord_responder.send_embed_list(inter, embed_list)
            return

        cwl_group_obj = verification_payload['cwl_group_obj']

        if option == "overview":
            await inter.edit_original_message(
                content=discord_responder.cwl_lineup(cwl_group_obj))

            return

        elif option == "clan":
            for clan in cwl_group_obj.clans:
                embed_description = discord_responder.cwl_lineup_clan(
                    clan, self.coc_client, inter.client.emojis, self.client_data.emojis)

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    title=f"{clan.name} {clan.tag} CWL Lineup",
                    bot_user_name=inter.me.display_name,
                    thumbnail=clan.badge.small,
                    description=embed_description,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)

            return

        elif option == "member":
            for clan in cwl_group_obj.clans:
                field_dict_list = await discord_responder.cwl_lineup_member(
                    clan, self.coc_client, inter.client.emojis, self.client_data.emojis)

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    title=f"{clan.name} {clan.tag} CWL Lineup",
                    bot_user_name=inter.me.display_name,
                    thumbnail=clan.badge.small,
                    field_list=field_dict_list,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)

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

        await discord_responder.send_embed_list(inter, embed_list)

    @cwl.sub_command()
    async def scoreboard(
        self,
        inter,
        option: str = discord_utils.command_param_dict['cwl_scoreboard'],
        clan_role: disnake.Role = discord_utils.command_param_dict['clan_role']
    ):
        """
            CWL scoreboard

            Parameters
            ----------
            option (optional): options for cwl scoreboard returns
            clan_role (optional): clan role to use linked clan
        """

        # role not mentioned
        if clan_role is None:
            db_player_obj = db_responder.read_player_active(inter.author.id)

            verification_payload = await discord_responder.cwl_group_verification(
                db_player_obj, inter.author, self.coc_client)
        # role has been mentioned
        else:
            verification_payload = await (
                discord_responder.clan_role_cwl_group_verification(
                    clan_role, self.coc_client))

        if not verification_payload['verified']:
            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                field_list=verification_payload['field_dict_list'],
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        cwl_group = verification_payload['cwl_group_obj']

        # get the clan object from player or clan
        if "clan_obj" in verification_payload:
            clan = verification_payload['clan_obj']

        elif "player_obj" in verification_payload:
            clan = await verification_payload['player_obj'].get_detailed_clan()

        # initializing embed default values
        embed_title = None
        embed_description = None
        field_dict_list = []

        if option == "group":
            league_emoji = discord_responder.get_emoji(
                f"Clan War {clan.war_league.name}",
                inter.client.emojis,
                self.client_data.emojis)
            embed_title = f"CWL {league_emoji} {clan.war_league.name} Group"

            field_dict_list = await discord_responder.cwl_scoreboard_group(
                cwl_group, inter.client.emojis, self.client_data.emojis, self.coc_client)

        elif option == "rounds":
            embed_list = []
            league_emoji = discord_responder.get_emoji(
                f"Clan War {clan.war_league.name}",
                inter.client.emojis,
                self.client_data.emojis)
            embed_title = f"CWL {league_emoji} {clan.war_league.name} Group"

            embed_list.extend(discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                title=embed_title,
                description=embed_description,
                thumbnail=clan.badge.small,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            ))

            round_index = 0

            for cwl_round in cwl_group.rounds:

                # checking if war has ended
                war = await self.coc_client.get_league_war(cwl_round[0])
                if war.state != "warEnded":
                    break

                field_dict_list = await discord_responder.cwl_scoreboard_round(
                    cwl_group, cwl_round, round_index,
                    inter.client.emojis, self.client_data.emojis,
                    self.coc_client)

                # update round index
                round_index += 1
                embed_title = f"**Round: {round_index}**"

                embed_list.extend(discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    bot_user_name=inter.me.display_name,
                    title=embed_title,
                    description=embed_description,
                    field_list=field_dict_list,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                ))

            if len(embed_list) == 1:
                field_dict_list = [{
                    "name": f"no rounds have ended",
                    "value": f"please wait till after the first round is over"
                }]

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    bot_user_name=inter.me.display_name,
                    title=embed_title,
                    description=embed_description,
                    field_list=field_dict_list,
                    thumbnail=clan.badge.small,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

            await discord_responder.send_embed_list(
                inter, embed_list=embed_list)

            return

        elif option == "clan":
            league_emoji = discord_responder.get_emoji(
                f"Clan War {clan.war_league.name}",
                inter.client.emojis,
                self.client_data.emojis)
            embed_title = f"CWL {league_emoji} {clan.war_league.name} Group"
            embed_description = f"{clan.name} {clan.tag}"

            round_index = 0

            for cwl_round in cwl_group.rounds:

                # checking if war has ended
                war = await self.coc_client.get_league_war(cwl_round[0])
                if war.state != "warEnded":
                    break

                # update round index
                round_index += 1

            if round_index == 0:
                field_dict_list = [{
                    "name": f"no rounds have ended",
                    "value": f"please wait till after the first round is over"
                }]

            else:
                field_dict_list = await discord_responder.cwl_scoreboard_clan(
                    inter, cwl_group, clan, self.coc_client,
                    inter.client.emojis, self.client_data.emojis
                )

        else:
            field_dict_list = [{
                'name': "incorrect option selected",
                'value': "please select a different option"
            }]

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            title=embed_title,
            description=embed_description,
            field_list=field_dict_list,
            thumbnail=clan.badge.small,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(inter, embed_list)

    @cwl.sub_command()
    async def noattack(
        self,
        inter,
        clan_role: disnake.Role = discord_utils.command_param_dict['clan_role']
    ):
        """
            *leadership*
            lists players that missed attacks in cwl

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

            await discord_responder.send_embed_list(inter, embed_list)
            return

        player_obj = verification_payload['player_obj']
        clan_obj = verification_payload['clan_obj']
        cwl_group_obj = verification_payload['cwl_group_obj']

        field_dict_list = await discord_responder.cwl_clan_noatk(
            clan_obj, cwl_group_obj, self.coc_client,
            inter.client.emojis, self.client_data.emojis)

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{clan_obj.name} CWL missed attacks",
            bot_user_name=inter.me.display_name,
            thumbnail=player_obj.clan.badge.small,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(inter, embed_list)

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
        user: disnake.User = discord_utils.command_param_dict['user'],
        tag: str = discord_utils.command_param_dict['tag']
    ):
        """
            user's player cwl score

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

            await discord_responder.send_embed_list(inter, embed_list)
            return

        player_obj = verification_payload['player_obj']
        cwl_group_obj = verification_payload['cwl_group_obj']

        # player tag specified
        if tag is not None:
            player_obj = await clash_responder.get_player(tag, self.coc_client)

            if player_obj is None:
                embed_description = f"could not find player with tag {tag}"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    bot_user_name=inter.me.display_name,
                    description=embed_description,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

        embed_thumbnail = discord_responder.get_town_hall_url(player_obj)
        field_dict_list = await discord_responder.cwl_member_score(
            player_obj, cwl_group_obj, player_obj.clan.tag)
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{player_obj.name} CWL score",
            bot_user_name=inter.me.display_name,
            thumbnail=embed_thumbnail,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(inter, embed_list)

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

            await discord_responder.send_embed_list(inter, embed_list)
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
            thumbnail=player_obj.clan.badge.small,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(inter, embed_list)
