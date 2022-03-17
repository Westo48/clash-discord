import disnake
from disnake import (
    ApplicationCommandInteraction
)
from disnake.ext import commands
from responders import (
    DiscordResponder as discord_responder,
    ClashResponder as clash_responder,
    RazBotDB_Responder as db_responder
)
from utils import discord_utils


class Announce(commands.Cog):
    def __init__(self, bot, coc_client, client_data):
        self.bot = bot
        self.coc_client = coc_client
        self.client_data = client_data

    @commands.slash_command()
    async def announce(self, inter):
        """
            parent for discord commands
        """

        await inter.response.defer(ephemeral=True)

    @announce.sub_command()
    async def message(
        self,
        inter: ApplicationCommandInteraction,
        channel: disnake.TextChannel = discord_utils.command_param_dict['channel'],
        message: str = discord_utils.command_param_dict['message']
    ):
        """
            *leadership* 
            announces message to specified channel

            Parameters
            ----------
            channel: channel to announce the message
            message: message to send the specified channel
        """

        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = (
            await discord_responder.player_leadership_verification(
                db_player_obj, inter.author, inter.guild.id, self.coc_client))
        if not verification_payload['verified']:
            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                field_list=verification_payload['field_dict_list'],
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.xx(embed_list, inter)
            return

        embed_title = f"**ANNOUNCEMENT**"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            title=embed_title,
            description=message,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url)

        if channel is None:
            channel = inter.channel

        await discord_responder.send_embed_list(
            inter, embed_list, channel=channel)

    @announce.sub_command()
    async def player(
        self,
        inter: ApplicationCommandInteraction,
        channel: disnake.TextChannel = discord_utils.command_param_dict['channel'],
        message: str = discord_utils.command_param_dict['message'],
        tag: str = discord_utils.command_param_dict['required_tag']
    ):
        """
            announces message to specified channel, 
            pings user with the specified player tag

            Parameters
            ----------
            channel: channel to announce the message
            message: message to send the specified channel
            tag: player tag to find and ping user
        """

        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = (
            await discord_responder.player_verification(
                db_player_obj, inter.author, self.coc_client))
        if not verification_payload['verified']:
            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                field_list=verification_payload['field_dict_list'],
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url)

            await discord_responder.send_embed_list(inter, embed_list)
            return

        player = await clash_responder.get_player(tag, self.coc_client)

        if player is None:
            field_dict_list = [{
                "name": f"player with tag {tag} not found",
                "value": f"please check the tag and try again"
            }]
            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                field_list=field_dict_list,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        embed_title = f"**{player.name} {player.tag}**"

        embed_thumbnail = discord_responder.get_town_hall_url(player)

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            title=embed_title,
            description=message,
            thumbnail=embed_thumbnail,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url)

        content = discord_responder.user_player_ping(
            player, inter.guild.members)

        if channel is None:
            channel = inter.channel

        await discord_responder.send_embed_list(
            inter, embed_list, content=content, channel=channel)

    @announce.sub_command()
    async def donate(
        self,
        inter: ApplicationCommandInteraction,
        channel: disnake.TextChannel = discord_utils.command_param_dict['channel'],
        message: str = discord_utils.command_param_dict['message'],
        unit_name: str = commands.Param(
            name=discord_utils.command_param_dict['unit_name'].name,
            description=discord_utils.command_param_dict['unit_name'].description,
            autocomplete=discord_utils.autocomp_unit
        ),
        clan_role: disnake.Role = discord_utils.command_param_dict['clan_role'],
    ):
        """
            announces message to specified channel, 
            pings all that can donate the requested unit

            Parameters
            ----------
            unit_name: name of unit to search clan donations
            channel: channel to announce the message
            message: message to send the specified channel
            clan_role (optional): clan role to use linked clan
        """

        # role not mentioned
        if clan_role is None:
            db_player_obj = db_responder.read_player_active(inter.author.id)

            verification_payload = (
                await discord_responder.clan_verification(
                    db_player_obj, inter.author, self.coc_client)
            )
        # role has been mentioned
        else:
            verification_payload = (
                await discord_responder.clan_role_verification(
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

        clan = verification_payload['clan_obj']

        donator_list = await clash_responder.donation(
            clan, unit_name, self.coc_client)

        # unit is either hero, pet or is an incorrect unit
        if donator_list is None:
            await inter.edit_original_message(
                content=f"{unit_name} is not a valid donatable unit")
            return

        formatted_unit_name = clash_responder.find_unit_name(unit_name)

        unit_emoji = discord_responder.get_emoji(
            formatted_unit_name, inter.client.emojis, self.client_data.emojis)

        content_list = []

        # nobody in the clan can donate the requested unit
        if len(donator_list) == 0:
            message = f"{clan.name} is unable to donate {unit_emoji}"
            content = None

        else:
            content = ""
            for donor in donator_list:
                member_message = discord_responder.user_player_ping(
                    donor.player_obj, inter.guild.members)
                member_message += ", "
                # making sure the proposed content will not exceed the 2K limit
                if len(content+member_message) >= 2000:
                    # cuts the last two characters from the string ', '
                    content = content[:-2]

                    # add the content to the list
                    content_list.append(content)

                    # reset content
                    content = ""

                content += member_message

            # cuts the last two characters from the string ', '
            content = content[:-2]

            content_list.append(content)

        embed_title = f"{unit_emoji} **{formatted_unit_name} DONORS**"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            title=embed_title,
            description=message,
            thumbnail=clan.badge.small,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url)

        if channel is None:
            channel = inter.channel

        await discord_responder.send_embed_list(
            inter, embed_list, channel=channel)

        for content in content_list:
            # making sure the content isn't empty
            if content != "":
                await discord_responder.send_embed_list(
                    inter, content=content, channel=channel)

    @announce.sub_command()
    async def supertroop(
        self,
        inter: ApplicationCommandInteraction,
        channel: disnake.TextChannel = discord_utils.command_param_dict['channel'],
        message: str = discord_utils.command_param_dict['message'],
        super_troop: str = commands.Param(
            name=discord_utils.command_param_dict['super_troop'].name,
            description=discord_utils.command_param_dict['super_troop'].description,
            autocomplete=discord_utils.autocomp_supertroop
        ),
        clan_role: disnake.Role = discord_utils.command_param_dict['clan_role']
    ):
        """
            announces message to specified channel, 
            pings all that have the requested super troop active

            Parameters
            ----------
            channel: channel to announce the message
            message: message to send the specified channel
            super_troop: name of unit to search clan donations
            clan_role (optional): clan role to use linked clan
        """

        # role not mentioned
        if clan_role is None:
            db_player_obj = db_responder.read_player_active(inter.author.id)

            verification_payload = (
                await discord_responder.clan_verification(
                    db_player_obj, inter.author, self.coc_client))
        # role has been mentioned
        else:
            verification_payload = (
                await discord_responder.clan_role_verification(
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

        clan = verification_payload['clan_obj']

        super_troop_name = clash_responder.find_super_troop_name(super_troop)

        if super_troop_name is None:
            await inter.edit_original_message(
                content=f"{super_troop} is not super troop")
            return

        donator_list = await clash_responder.active_super_troop_search(
            clan, super_troop_name, self.coc_client)

        # unit is either hero, pet or is an incorrect unit
        if donator_list is None:
            await inter.edit_original_message(
                content=f"{super_troop} is not a super troop")
            return

        unit_emoji = discord_responder.get_emoji(
            super_troop_name, inter.client.emojis, self.client_data.emojis)

        content_list = []
        # nobody in the clan can donate the requested unit
        if len(donator_list) == 0:
            message = f"{clan.name} is unable to donate {unit_emoji}"
            content = None

        else:
            content = ""
            for donor in donator_list:
                member_message = discord_responder.user_player_ping(
                    donor, inter.guild.members)
                member_message += ", "
                # making sure the proposed content will not exceed the 2K limit
                if len(content+member_message) >= 2000:
                    # cuts the last two characters from the string ', '
                    content = content[:-2]

                    # add the content to the list
                    content_list.append(content)

                    # reset content
                    content = ""

                content += member_message

            # cuts the last two characters from the string ', '
            content = content[:-2]

            content_list.append(content)

        embed_title = f"{unit_emoji} **{super_troop_name} DONORS**"
        embed_description = message

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            title=embed_title,
            description=embed_description,
            thumbnail=clan.badge.small,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url)

        if channel is None:
            channel = inter.channel

        await discord_responder.send_embed_list(
            inter, embed_list, channel=channel)

        for content in content_list:
            # making sure the content isn't empty
            if content != "":
                await discord_responder.send_embed_list(
                    inter, content=content, channel=channel)

    @announce.sub_command()
    async def war(
        self,
        inter: ApplicationCommandInteraction,
        channel: disnake.TextChannel = discord_utils.command_param_dict['channel'],
        message: str = discord_utils.command_param_dict['message'],
        clan_role: disnake.Role = discord_utils.command_param_dict['clan_role'],
        war_selection: str = discord_utils.command_param_dict['war_selection']
    ):
        """
            *leadership* 
            announces message to specified channel, 
            pings all in current war

            Parameters
            ----------
            channel: channel to announce the message
            message: message to send the specified channel
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

            await discord_responder.send_embed_list(inter, embed_list)
            return

        war = verification_payload['war_obj']

        content_list = []
        content = ""
        for war_member in war.clan.members:
            member_message = discord_responder.user_player_ping(
                war_member, inter.guild.members)
            member_message += ", "
            # making sure the proposed content will not exceed the 2K limit
            if len(content+member_message) >= 2000:
                # cuts the last two characters from the string ', '
                content = content[:-2]

                # add the content to the list
                content_list.append(content)

                # reset content
                content = ""

            content += member_message

        # cuts the last two characters from the string ', '
        content = content[:-2]

        content_list.append(content)

        embed_title = f"**WAR ANNOUNCEMENT**"
        embed_description = message

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            title=embed_title,
            description=embed_description,
            thumbnail=war.clan.badge.small,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url)

        if channel is None:
            channel = inter.channel

        await discord_responder.send_embed_list(
            inter, embed_list, channel=channel)

        for content in content_list:
            # making sure the content isn't empty
            if content != "":
                await discord_responder.send_embed_list(
                    inter, content=content, channel=channel)

    @announce.sub_command()
    async def warnoattack(
        self,
        inter: ApplicationCommandInteraction,
        channel: disnake.TextChannel = discord_utils.command_param_dict['channel'],
        message: str = discord_utils.command_param_dict['message'],
        missed_attacks: int = discord_utils.command_param_dict['missed_attacks'],
        clan_role: disnake.Role = discord_utils.command_param_dict['clan_role'],
        war_selection: str = discord_utils.command_param_dict['war_selection']
    ):
        """
            *leadership* 
            announces message to channel, 
            pings all in war missing attacks

            Parameters
            ----------
            channel: channel to announce the message
            message: message to send the specified channel
            missed_attacks (optional): specified missed attack count
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

            await discord_responder.send_embed_list(inter, embed_list)
            return

        war = verification_payload['war_obj']

        if missed_attacks is None:
            embed_title = "**MISSING WAR ATTACKS**"
        else:
            if missed_attacks == 1:
                embed_title = "**MISSING 1 ATTACK**"
            else:
                embed_title = "**MISSING 2 ATTACKS**"

        war_member_no_attack_list = clash_responder.war_no_attack(
            war, missed_attacks)

        content_list = []
        content = ""
        for war_member in war_member_no_attack_list:
            member_message = discord_responder.user_player_ping(
                war_member, inter.guild.members)
            member_message += ", "
            # making sure the proposed content will not exceed the 2K limit
            if len(content+member_message) >= 2000:
                # cuts the last two characters from the string ', '
                content = content[:-2]

                # add the content to the list
                content_list.append(content)

                # reset content
                content = ""

            content += member_message

        # cuts the last two characters from the string ', '
        content = content[:-2]

        content_list.append(content)

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            title=embed_title,
            description=message,
            thumbnail=war.clan.badge.small,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url)

        if channel is None:
            channel = inter.channel

        await discord_responder.send_embed_list(
            inter, embed_list, channel=channel)

        for content in content_list:
            # making sure the content isn't empty
            if content != "":
                await discord_responder.send_embed_list(
                    inter, content=content, channel=channel)
