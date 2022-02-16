import disnake
from disnake.ext import commands
from responders import (
    DiscordResponder as discord_responder,
    ClashResponder as clash_responder,
    RazBotDB_Responder as db_responder
)
from utils import discord_utils


class Discord(commands.Cog):
    def __init__(self, bot, coc_client, client_data):
        self.bot = bot
        self.coc_client = coc_client
        self.client_data = client_data

    @commands.slash_command()
    async def discord(self, inter):
        """
            parent for discord commands
        """

        pass

    @discord.sub_command()
    async def help(self, inter):
        """
            returns help menu
        """

        await inter.response.defer()

        db_guild_obj = db_responder.read_guild(inter.guild.id)
        db_player_obj = db_responder.read_player_active(inter.author.id)

        if db_player_obj:
            player_obj = await clash_responder.get_player(
                db_player_obj.player_tag, self.coc_client)
        else:
            player_obj = None

        help_dict = discord_responder.help_main(
            db_guild_obj, inter.author.id, player_obj, self.client_data.bot_categories)
        field_dict_list = help_dict['field_dict_list']
        emoji_list = help_dict['emoji_list']

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{inter.me.display_name} help menu",
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)

        original_message = await inter.original_message()

        for emoji in emoji_list:
            await original_message.add_reaction(emoji)

    # discord announce
    @discord.sub_command_group()
    async def announce(self, inter):
        """
            group for discord announce commands
        """

        await inter.response.defer(ephemeral=True)

    @announce.sub_command(
        description=("*leadership* "
                     "announces message to specified channel")
    )
    async def message(
        self,
        inter,
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

            await discord_responder.send_embed_list(embed_list, inter)
            return

        message = "**ANNOUNCEMENT**\n\n" + message

        try:
            await channel.send(content=message)
        except:
            field_dict_list = [{
                "name": "message could not be sent",
                "value": f"please ensure bot is in channel {channel.mention}"
            }]
            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                field_list=field_dict_list,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(embed_list, inter)
            return

        field_dict_list = [{
            "name": "message sent",
            "value": f"channel {channel.mention}"
        }]
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)

    @announce.sub_command()
    async def player(
        self,
        inter,
        channel: disnake.TextChannel = discord_utils.command_param_dict['channel'],
        message: str = discord_utils.command_param_dict['message'],
        tag: str = discord_utils.command_param_dict['required_tag']
    ):
        """
            *leadership* 
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

            await discord_responder.send_embed_list(embed_list, inter)
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

            await discord_responder.send_embed_list(embed_list, inter)
            return

        message = f"**{player.name} {player.tag}**\n\n" + message
        message += "\n\n"

        message += discord_responder.user_player_ping(
            player, inter.guild.members)

        try:
            await channel.send(content=message)
        except:
            field_dict_list = [{
                "name": "message could not be sent",
                "value": f"please ensure bot is in channel {channel.mention}"
            }]
            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                field_list=field_dict_list,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )
            await discord_responder.send_embed_list(embed_list, inter)

            return

        field_dict_list = [{
            "name": "message sent",
            "value": f"channel {channel.mention}"
        }]
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )
        await discord_responder.send_embed_list(embed_list, inter)

    @announce.sub_command()
    async def donate(
        self,
        inter,
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

            await discord_responder.send_embed_list(embed_list, inter)
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

        message = f"{unit_emoji} **DONORS**\n\n" + message
        message += "\n\n"

        # nobody in the clan can donate the requested unit
        if len(donator_list) == 0:
            message += f"{clan.name} is unable to donate {unit_emoji}"

        else:

            for donor in donator_list:
                donor_ping = discord_responder.user_player_ping(
                    donor.player_obj, inter.guild.members)
                message += (f"{donor_ping}, ")

            # cuts the last two characters from the string ', '
            message = message[:-2]

        try:
            await channel.send(content=(message))
        except:
            field_dict_list = [{
                "name": "message could not be sent",
                "value": f"please ensure bot is in channel {channel.mention}"
            }]
            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                field_list=field_dict_list,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )
            await discord_responder.send_embed_list(embed_list, inter)

            return

        field_dict_list = [{
            "name": "message sent",
            "value": f"channel {channel.mention}"
        }]
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )
        await discord_responder.send_embed_list(embed_list, inter)

    @announce.sub_command()
    async def supertroop(
        self,
        inter,
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

            await discord_responder.send_embed_list(embed_list, inter)
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

        message = f"{unit_emoji} **DONORS**\n\n" + message
        message += "\n\n"

        # nobody in the clan can donate the requested unit
        if len(donator_list) == 0:
            message += f"{clan.name} is unable to donate {unit_emoji}"

        else:

            for donor in donator_list:
                donor_ping = discord_responder.user_player_ping(
                    donor, inter.guild.members)
                message += (f"{donor_ping}, ")

            # cuts the last two characters from the string ', '
            message = message[:-2]

        try:
            await channel.send(content=message)
        except:
            field_dict_list = [{
                "name": "message could not be sent",
                "value": f"please ensure bot is in channel {channel.mention}"
            }]
            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                field_list=field_dict_list,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )
            await discord_responder.send_embed_list(embed_list, inter)

            return

        field_dict_list = [{
            "name": "message sent",
            "value": f"channel {channel.mention}"
        }]
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )
        await discord_responder.send_embed_list(embed_list, inter)

    @announce.sub_command()
    async def war(
        self,
        inter,
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

            await discord_responder.send_embed_list(embed_list, inter)
            return

        war = verification_payload['war_obj']

        message = "**WAR ANNOUNCEMENT**\n\n" + message
        message += "\n\n"

        for war_member in war.clan.members:
            member_message = discord_responder.user_player_ping(
                war_member, inter.guild.members)
            message += (f"{member_message}, ")

        # cuts the last two characters from the string ', '
        message = message[:-2]

        try:
            await channel.send(content=message)
        except:
            field_dict_list = [{
                "name": "message could not be sent",
                "value": f"please ensure bot is in channel {channel.mention}"
            }]
            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                field_list=field_dict_list,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )
            await discord_responder.send_embed_list(embed_list, inter)

            return

        field_dict_list = [{
            "name": "message sent",
            "value": f"channel {channel.mention}"
        }]
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )
        await discord_responder.send_embed_list(embed_list, inter)

    @announce.sub_command()
    async def warnoattack(
        self,
        inter,
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

            await discord_responder.send_embed_list(embed_list, inter)
            return

        war = verification_payload['war_obj']

        if missed_attacks is None:
            message = "**MISSING WAR ATTACKS**\n\n" + message
        else:
            if missed_attacks == 1:
                message = "**MISSING 1 ATTACK**\n\n" + message
            else:
                message = "**MISSING 2 ATTACKS**\n\n" + message

        message += "\n\n"

        war_member_no_attack_list = clash_responder.war_no_attack(
            war, missed_attacks)

        for war_member in war_member_no_attack_list:
            member_message = discord_responder.user_player_ping(
                war_member, inter.guild.members)
            message += (f"{member_message}, ")

        # cuts the last two characters from the string ', '
        message = message[:-2]

        try:
            await channel.send(content=message)
        except:
            field_dict_list = [{
                "name": "message could not be sent",
                "value": f"please ensure bot is in channel {channel.mention}"
            }]
            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                field_list=field_dict_list,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )
            await discord_responder.send_embed_list(embed_list, inter)

            return

        field_dict_list = [{
            "name": "message sent",
            "value": f"channel {channel.mention}"
        }]
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )
        await discord_responder.send_embed_list(embed_list, inter)

    # discord role
    @discord.sub_command_group()
    async def role(self, inter):
        """
            group for discord role commands
        """

        await inter.response.defer()

    @role.sub_command()
    async def me(self, inter):
        """
            update your roles
        """

        db_guild_obj = db_responder.read_guild(inter.guild.id)

        # if guild is not claimed
        if not db_guild_obj:
            await inter.edit_original_message(
                content=f"{inter.guild.name} has not been claimed")
            return

        embed_dict_list = await discord_responder.update_roles(
            inter.author, inter.guild, self.coc_client)

        for embed_dict in embed_dict_list:

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                title=embed_dict["title"],
                bot_user_name=inter.me.display_name,
                thumbnail=embed_dict["thumbnail"],
                field_list=embed_dict["field_dict_list"],
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(embed_list, inter)

    @role.sub_command()
    async def member(
        self,
        inter,
        user: disnake.User = discord_utils.command_param_dict['user']
    ):
        """
            *leadership* 
            update mentioned user's roles

            Parameters
            ----------
            user: user to update roles
        """

        db_guild_obj = db_responder.read_guild(inter.guild.id)

        # if guild is not claimed
        if not db_guild_obj:
            await inter.edit_original_message(
                content=f"{inter.guild.name} has not been claimed")
            return

        # getting author's db player obj for leadership verification
        db_player_obj = db_responder.read_player_active(inter.author.id)

        verification_payload = await discord_responder.player_leadership_verification(
            db_player_obj, inter.author, inter.guild.id, self.coc_client)

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

        embed_dict_list = await discord_responder.update_roles(
            user, inter.guild, self.coc_client)

        for embed_dict in embed_dict_list:

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                title=embed_dict["title"],
                bot_user_name=inter.me.display_name,
                thumbnail=embed_dict["thumbnail"],
                field_list=embed_dict["field_dict_list"],
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(embed_list, inter)

    @role.sub_command()
    async def all(self, inter):
        """
            *ClashDiscord server admin* 
            update roles for every member in the server
        """

        db_guild_obj = db_responder.read_guild(inter.guild.id)

        if not db_guild_obj:
            # if guild is not claimed
            await inter.edit_original_message(
                content=f"{inter.guild.name} has not been claimed")
            return

        db_user_obj = db_responder.read_user(inter.author.id)

        # if user is not claimed
        if not db_user_obj:
            await inter.edit_original_message(
                content=f"{inter.author.mention} has not been claimed")
            return

        # if author is not guild admin and is not super user
        if (not db_guild_obj.admin_user_id == inter.author.id
                and not db_user_obj.super_user):

            await inter.edit_original_message(
                content=f"{inter.author.mention} is not guild's admin")
            return

        # telling the user that the bot is updating roles
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description="updating roles",
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)

        for user in inter.guild.members:
            if user.bot:
                continue

            embed_dict_list = await discord_responder.update_roles(
                user, inter.guild, self.coc_client)

            for embed_dict in embed_dict_list:

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    title=embed_dict["title"],
                    bot_user_name=inter.me.display_name,
                    thumbnail=embed_dict["thumbnail"],
                    field_list=embed_dict["field_dict_list"],
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(embed_list, inter)

        # telling the user that the bot is done updating roles
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description="update complete",
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)

    @discord.sub_command()
    async def emoji(
        self,
        inter,
        coc_name: str = commands.Param(
            name=discord_utils.command_param_dict['coc_name'].name,
            description=discord_utils.command_param_dict['coc_name'].description,
            autocomplete=discord_utils.autocomp_emoji_name
        )
    ):
        """
            sends specified emoji

            Parameters
            ----------
            coc_name: name of emoji to search for
        """

        await inter.response.defer(ephemeral=True)

        await inter.edit_original_message(content="getting emoji")

        emoji = discord_responder.get_emoji(
            coc_name, inter.client.emojis, self.client_data.emojis)

        if emoji is None:
            await inter.edit_original_message(
                content=f"{coc_name} emoji not found")
            return

        await inter.send(content=emoji)

        await inter.edit_original_message(content=f"{emoji} emoji sent")

    @discord.sub_command()
    async def user(
        self,
        inter,
        option: str = discord_utils.command_param_dict['discord_user'],
        tag: str = discord_utils.command_param_dict['discord_user_tag'],
        clan_role: disnake.Role = discord_utils.command_param_dict['clan_role']
    ):
        """
            returns the user linked to a requested player 
            *default option is clan*

            Parameters
            ----------
            option (optional): options for discord user returns
            tag (optional): player tag to search
            clan_role (optional): clan role to use linked clan
        """

        await inter.response.defer()

        if option == "player":
            # player selected and no tag specified
            if tag is None:
                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=f"tag not specified, please provide player tag",
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(embed_list, inter)
                return

            player_obj = await clash_responder.get_player(tag, self.coc_client)

            # player with given tag not found
            if player_obj is None:
                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=f"could not find player with tag {tag}",
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(embed_list, inter)
                return

            embed_title = None
            field_dict_list = []
            embed_thumbnail = player_obj.league.icon

            field_dict_list.append(
                discord_responder.find_user_from_tag(
                    player_obj, inter.guild.members))

        elif option == "clan":
            # role not mentioned
            if clan_role is None:
                db_player_obj = db_responder.read_player_active(
                    inter.author.id)

                verification_payload = (
                    await discord_responder.clan_leadership_verification(
                        db_player_obj, inter.author, inter.guild.id, self.coc_client))

            # role mentioned
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

                await discord_responder.send_embed_list(embed_list, inter)
                return

            clan_obj = verification_payload['clan_obj']

            embed_title = f"{clan_obj.name} {clan_obj.tag} linked users"
            field_dict_list = []
            embed_thumbnail = clan_obj.badge

            # finding the user for each member in the clan
            for member_obj in clan_obj.members:
                field_dict_list.append(discord_responder.find_user_from_tag(
                    member_obj, inter.guild.members))

        else:
            embed_title = None
            embed_thumbnail = None
            field_dict_list = [{
                'name': "incorrect option selected",
                'value': "please select a different option"
            }]

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            title=embed_title,
            thumbnail=embed_thumbnail,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
