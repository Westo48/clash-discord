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

            await discord_responder.send_embed_list(inter, embed_list)

    @role.sub_command()
    async def member(
        self,
        inter,
        user: disnake.User = discord_utils.command_param_dict['required_user']
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

            await discord_responder.send_embed_list(inter, embed_list)
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

            await discord_responder.send_embed_list(inter, embed_list)

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

        await discord_responder.send_embed_list(inter, embed_list)

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

                await discord_responder.send_embed_list(inter, embed_list)

        # telling the user that the bot is done updating roles
        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description="update complete",
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(inter, embed_list)

    @discord.sub_command()
    async def emoji(
        self,
        inter: ApplicationCommandInteraction,
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

        emoji = discord_responder.get_emoji(
            coc_name, inter.client.emojis, self.client_data.emojis)

        if emoji is None:
            await inter.edit_original_message(
                content=f"{coc_name} emoji not found")
            return

        message_sent = await discord_responder.send_embed_list(
            inter, content=emoji, channel=inter.channel)

        if message_sent:
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

                await discord_responder.send_embed_list(inter, embed_list)
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

                await discord_responder.send_embed_list(inter, embed_list)
                return

            embed_title = None
            field_dict_list = []
            embed_thumbnail = player_obj.league.icon.small

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

                await discord_responder.send_embed_list(inter, embed_list)
                return

            clan_obj = verification_payload['clan_obj']

            embed_title = f"{clan_obj.name} {clan_obj.tag} linked users"
            field_dict_list = []
            embed_thumbnail = clan_obj.badge.small

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

        await discord_responder.send_embed_list(inter, embed_list)
