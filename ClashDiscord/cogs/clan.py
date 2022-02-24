import disnake
from disnake.ext import commands
from responders import (
    DiscordResponder as discord_responder,
    ClashResponder as clash_responder,
    RazBotDB_Responder as db_responder
)
from utils import discord_utils


class Clan(commands.Cog):
    def __init__(self, bot, coc_client, client_data):
        self.bot = bot
        self.coc_client = coc_client
        self.client_data = client_data

    @commands.slash_command()
    async def clan(self, inter):
        """
            parent for clan commands
        """

        # defer for every command
        await inter.response.defer()

    @clan.sub_command()
    async def info(
        self,
        inter,
        clan_role: disnake.Role = discord_utils.command_param_dict['clan_role'],
        tag: str = discord_utils.command_param_dict['tag']
    ):
        """
            get clan information

            Parameters
            ----------
            clan_role (optional): clan role to use linked clan
            tag (optional): tag to search
        """

        # role not mentioned
        if clan_role is None:
            db_player_obj = db_responder.read_player_active(inter.author.id)

            verification_payload = await discord_responder.clan_verification(
                db_player_obj, inter.author, self.coc_client)
        # role has been mentioned
        else:
            verification_payload = await discord_responder.clan_role_verification(
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

        clan = verification_payload['clan_obj']

        # clan tag selected
        if tag is not None:
            clan = await clash_responder.get_clan(tag, self.coc_client)

            if clan is None:
                embed_description = f"could not find clan with tag {tag}"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    bot_user_name=inter.me.display_name,
                    description=embed_description,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

        field_dict_list = discord_responder.clan_info(
            clan, inter.client.emojis, self.client_data.emojis
        )

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{clan.name} {clan.tag}",
            bot_user_name=inter.me.display_name,
            thumbnail=clan.badge.small,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(inter, embed_list)

    @clan.sub_command()
    async def lineup(
        self,
        inter,
        option: str = discord_utils.command_param_dict['clan_lineup'],
        clan_role: disnake.Role = discord_utils.command_param_dict['clan_role'],
        tag: str = discord_utils.command_param_dict['tag']
    ):
        """
            *leadership* 
            get clan town hall lineup information 
            *default option is overview*

            Parameters
            ----------
            option (optional): options for lineup returns
            clan_role (optional): clan role to use linked clan
            tag (optional): tag to search
        """

        # role not mentioned
        if clan_role is None:
            db_player_obj = db_responder.read_player_active(inter.author.id)

            verification_payload = (
                await discord_responder.clan_leadership_verification(
                    db_player_obj, inter.author, inter.guild.id, self.coc_client))
        # role has been mentioned
        else:
            verification_payload = (
                await discord_responder.clan_role_player_leadership_verification(
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

        clan = verification_payload['clan_obj']

        # clan tag selected
        if tag is not None:
            clan = await clash_responder.get_clan(tag, self.coc_client)

            if clan is None:
                embed_description = f"could not find clan with tag {tag}"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    bot_user_name=inter.me.display_name,
                    description=embed_description,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

        if option == "overview":
            embed_title = f"{clan.name} lineup"
            field_dict_list = await discord_responder.clan_lineup(
                clan, self.coc_client, inter.client.emojis, self.client_data.emojis)
        elif option == "member":
            embed_title = f"{clan.name} lineup"
            field_dict_list = await discord_responder.clan_lineup_member(
                clan, self.coc_client, inter.client.emojis, self.client_data.emojis)
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
            thumbnail=clan.badge.small,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(inter, embed_list)

    @clan.sub_command()
    async def warpreference(
        self,
        inter,
        option: str = discord_utils.command_param_dict['clan_warpreference'],
        clan_role: disnake.Role = discord_utils.command_param_dict['clan_role'],
        tag: str = discord_utils.command_param_dict['tag']
    ):
        """
            *leadership* 
            rundown of clan's war preference 
            *default option is overview*

            Parameters
            ----------
            option (optional): options for clan warpreference returns
            clan_role (optional): clan role to use linked clan
            tag (optional): tag to search
        """

        # role not mentioned
        if clan_role is None:
            db_player_obj = db_responder.read_player_active(inter.author.id)

            verification_payload = (
                await discord_responder.clan_leadership_verification(
                    db_player_obj, inter.author, inter.guild.id, self.coc_client))
        # role has been mentioned
        else:
            verification_payload = (
                await discord_responder.clan_role_player_leadership_verification(
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

        clan = verification_payload['clan_obj']

        # clan tag selected
        if tag is not None:
            clan = await clash_responder.get_clan(tag, self.coc_client)

            if clan is None:
                embed_description = f"could not find clan with tag {tag}"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    bot_user_name=inter.me.display_name,
                    description=embed_description,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

        # initializing embed default values
        embed_title = None
        embed_description = None
        field_dict_list = []

        if option == "overview":
            embed_title = f"{clan.name} war preference"
            field_dict_list = await discord_responder.war_preference_clan(
                clan, self.coc_client, inter.client.emojis, self.client_data.emojis)

        elif option == "member":
            embed_title = f"{clan.name} war preference"
            embed_description = await discord_responder.war_preference_member(
                clan, self.coc_client, inter.client.emojis, self.client_data.emojis)

        else:
            field_dict_list = [{
                'name': "incorrect option selected",
                'value': "please select a different option"
            }]

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=embed_title,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            thumbnail=clan.badge.small,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(inter, embed_list)

    @clan.sub_command()
    async def donate(
        self,
        inter,
        unit_name: str = commands.Param(
            name=discord_utils.command_param_dict['unit_name'].name,
            description=discord_utils.command_param_dict['unit_name'].description,
            autocomplete=discord_utils.autocomp_unit
        ),
        clan_role: disnake.Role = discord_utils.command_param_dict['clan_role'],
        tag: str = discord_utils.command_param_dict['tag']
    ):
        """
            search the clan for available donors for a specified unit

            Parameters
            ----------
            unit_name: name of unit to search clan donations
            clan_role (optional): clan role to use linked clan
            tag (optional): tag to search
        """

        # role not mentioned
        if clan_role is None:
            db_player_obj = db_responder.read_player_active(inter.author.id)

            verification_payload = await discord_responder.clan_verification(
                db_player_obj, inter.author, self.coc_client)
        # role has been mentioned
        else:
            verification_payload = await discord_responder.clan_role_verification(
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

        clan = verification_payload['clan_obj']

        # clan tag selected
        if tag is not None:
            clan = await clash_responder.get_clan(tag, self.coc_client)

            if clan is None:
                embed_description = f"could not find clan with tag {tag}"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    bot_user_name=inter.me.display_name,
                    description=embed_description,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

        donator_list = await clash_responder.donation(
            clan, unit_name, self.coc_client)

        field_dict_list = discord_responder.donation(
            clan, donator_list, unit_name,
            inter.client.emojis, self.client_data.emojis
        )

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{clan.name} {clan.tag}",
            bot_user_name=inter.me.display_name,
            thumbnail=clan.badge.small,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(inter, embed_list)

    @clan.sub_command()
    async def supertroop(
        self,
        inter,
        super_troop: str = commands.Param(
            name=discord_utils.command_param_dict['super_troop'].name,
            description=discord_utils.command_param_dict['super_troop'].description,
            default=discord_utils.command_param_dict['super_troop'].default,
            autocomplete=discord_utils.autocomp_supertroop
        ),
        clan_role: disnake.Role = discord_utils.command_param_dict['clan_role'],
        tag: str = discord_utils.command_param_dict['tag']
    ):
        """
            shows all active super troops in the clan

            Parameters
            ----------
            super_troop (optional): super troop name to search clan donations
            clan_role (optional): clan role to use linked clan
            tag (optional): tag to search
        """

        # role not mentioned
        if clan_role is None:
            db_player_obj = db_responder.read_player_active(inter.author.id)

            verification_payload = await discord_responder.clan_verification(
                db_player_obj, inter.author, self.coc_client)
        # role has been mentioned
        else:
            verification_payload = await discord_responder.clan_role_verification(
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

        clan = verification_payload['clan_obj']

        # clan tag selected
        if tag is not None:
            clan = await clash_responder.get_clan(tag, self.coc_client)

            if clan is None:
                embed_description = f"could not find clan with tag {tag}"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    bot_user_name=inter.me.display_name,
                    description=embed_description,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

        # super troop not specified for search
        if super_troop is None:
            embed_title = f"{clan.name} active super troops"

            field_dict_list = await discord_responder.clan_super_troop_active(
                clan, inter.client.emojis, self.client_data.emojis, self.coc_client)

        # super troop specified for search
        else:
            super_troop_name = clash_responder.find_super_troop_name(
                super_troop)

            # super troop was not found
            if super_troop_name is None:
                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=f"{super_troop} is not a viable request",
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            donor_list = await clash_responder.active_super_troop_search(
                clan, super_troop_name, self.coc_client)

            embed_title = f"{clan.name} {clan.tag}"

            field_dict_list = discord_responder.super_troop_search(
                clan, donor_list, super_troop_name,
                inter.client.emojis, self.client_data.emojis
            )

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=embed_title,
            bot_user_name=inter.me.display_name,
            thumbnail=clan.badge.small,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(inter, embed_list)
