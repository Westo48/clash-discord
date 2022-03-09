import disnake
from disnake.ext import commands
from responders import (
    DiscordResponder as discord_responder,
    ClashResponder as clash_responder,
    RazBotDB_Responder as db_responder
)
from utils import discord_utils


class Admin(commands.Cog):
    def __init__(self, bot, coc_client, client_data):
        self.bot = bot
        self.coc_client = coc_client
        self.client_data = client_data

    @commands.slash_command()
    async def admin(self, inter):
        """
            parent for client admin commands
        """

        # defer for every command
        await inter.response.defer()

    @admin.sub_command_group()
    async def player(self, inter):
        """
            group for player commands
        """

        pass

    @player.sub_command()
    async def claim(
        self,
        inter,
        player_tag: str = discord_utils.command_param_dict['required_tag'],
        user: disnake.User = discord_utils.command_param_dict['required_user']
    ):
        """
            *admin* 
            claim a player for the mentioned user

            Parameters
            ----------
            player_tag: player tag link user to
            user: user to link player to
        """

        verification_payload = (
            discord_responder.guild_admin_verification(inter))

        if not verification_payload['verified']:

            embed_list = verification_payload["embed_list"]

            await discord_responder.send_embed_list(inter, embed_list)

            return

        # confirm user has been claimed
        db_user_obj = db_responder.read_user(user.id)
        if not db_user_obj:
            # user has not been claimed
            db_user_obj = db_responder.claim_user(user.id)
            if not db_user_obj:
                # user could not be claimed
                embed_description = f"{user.mention} user couldn't be claimed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

        db_author = verification_payload["db_author"]

        # admin is not a super user and author is not the user
        if (not db_author.super_user
                and db_author.discord_id != db_user_obj.discord_id):
            # admin users are not allowed to update admins or super users
            if db_user_obj.admin or db_user_obj.super_user:
                embed_description = (f"admins are not allowed to update "
                                     f"admins or super users")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

        # confirm valid player_tag
        player_obj = await clash_responder.get_player(
            player_tag, self.coc_client)

        # player tag was not valid
        if not player_obj:
            embed_description = f"player with tag {player_tag} was not found"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        # confirm player has not been claimed
        db_player_obj = db_responder.read_player_from_tag(player_obj.tag)
        # player has already been claimed
        if db_player_obj:
            embed_description = (f"{player_obj.name} {player_obj.tag} "
                                 f"has already been claimed")

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        # user claimed
        # player is valid
        # player hasn't been claimed
        db_player_obj = db_responder.claim_player(
            user.id, player_obj.tag)

        # succesfully claimed
        if db_player_obj:
            embed_description = (f"{player_obj.name} {player_obj.tag} "
                                 f"is now claimed by {user.mention}")
        # failed to claim
        else:
            embed_description = (f"Could not claim {player_obj.name} "
                                 f"{player_obj.tag} for {user.mention}")

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(inter, embed_list)

    @player.sub_command()
    async def show(
        self,
        inter,
        user: disnake.User = discord_utils.command_param_dict['required_user']
    ):
        """
            *admin* 
            shows players claimed by the mentioned user

            Parameters
            ----------
            user: user to show player tags
        """

        verification_payload = (
            discord_responder.guild_admin_verification(inter))

        if not verification_payload['verified']:

            embed_list = verification_payload["embed_list"]

            await discord_responder.send_embed_list(inter, embed_list)

            return

        # confirm db user exists
        db_user_obj = db_responder.read_user(user.id)
        if db_user_obj is None:
            embed_description = f"{user.mention} has not been claimed"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        db_author = verification_payload["db_author"]

        # admin is not a super user and author is not the user
        if (not db_author.super_user
                and db_author.discord_id != db_user_obj.discord_id):
            # admin users are not allowed to update admins or super users
            if db_user_obj.admin or db_user_obj.super_user:
                embed_description = (f"admins are not allowed to update "
                                     f"admins or super users")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

        db_player_obj_list = db_responder.read_player_list(user.id)

        # user has no claimed players
        if len(db_player_obj_list) == 0:
            embed_description = (f"{user.mention} does not have any "
                                 f"claimed players")

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        message = f"{user.mention} has claimed "
        for db_player_obj in db_player_obj_list:
            player_obj = await clash_responder.get_player(
                db_player_obj.player_tag, self.coc_client)
            if db_player_obj.active:
                message += f"{player_obj.name} {player_obj.tag} (active), "
            else:
                message += f"{player_obj.name} {player_obj.tag}, "
        # cuts the last two characters from the string ', '
        message = message[:-2]
        await inter.edit_original_message(content=message)

    @player.sub_command()
    async def remove(
        self,
        inter,
        player_tag: str = discord_utils.command_param_dict['required_tag'],
        user: disnake.User = discord_utils.command_param_dict['required_user']
    ):
        """
            *admin* 
            remove a player for the mentioned user

            Parameters
            ----------
            player_tag: player tag to remove
            user: user to remove player from
        """

        verification_payload = (
            discord_responder.guild_admin_verification(inter))

        if not verification_payload['verified']:

            embed_list = verification_payload["embed_list"]

            await discord_responder.send_embed_list(inter, embed_list)

            return

        # confirm db user exists
        db_user_obj = db_responder.read_user(user.id)
        if db_user_obj is None:
            embed_description = f"{user.mention} has not been claimed"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        db_author = verification_payload["db_author"]

        # admin is not a super user and author is not the user
        if (not db_author.super_user
                and db_author.discord_id != db_user_obj.discord_id):
            # admin users are not allowed to update admins or super users
            if db_user_obj.admin or db_user_obj.super_user:
                embed_description = (f"admins are not allowed to update "
                                     f"admins or super users")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

        # confirm valid player_tag
        player_obj = await clash_responder.get_player(
            player_tag, self.coc_client)

        # player tag was not valid
        if not player_obj:
            embed_description = f"player with tag {player_tag} was not found"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        db_player_obj = db_responder.read_player(user.id, player_obj.tag)

        # db player not found
        if not db_player_obj:
            embed_description = (f"{player_obj.name} {player_obj.tag} "
                                 f"is not claimed by {user.mention}")

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        db_del_player_obj = db_responder.delete_player(
            user.id, player_obj.tag)

        # player was not deleted
        if db_del_player_obj:
            embed_description = (
                f"{player_obj.name} {player_obj.tag} "
                f"could not be deleted "
                f"from {user.mention} player list"
            )

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        db_active_player_obj = db_responder.read_player_active(user.id)

        # active player found
        # no need to change the active player
        if db_active_player_obj:
            embed_description = (
                f"{player_obj.name} {player_obj.tag} "
                f"has been deleted "
                f"from {user.mention} player list"
            )

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        # no active player found
        # check if there are any other players
        db_player_obj_list = db_responder.read_player_list(
            user.id)

        # no additional players claimed
        if len(db_player_obj_list) == 0:
            embed_description = (
                f"{player_obj.name} {player_obj.tag} "
                f"has been deleted, "
                f"{user.mention} has no more claimed players"
            )

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        # additional players claimed by user
        # update the first as the new active
        db_updated_player_obj = db_responder.update_player_active(
            user.id, db_player_obj_list[0].player_tag)

        # update not successful
        if not db_updated_player_obj:
            embed_description = (
                f"{player_obj.name} {player_obj.tag} "
                f"has been deleted, could not update active player, "
                f"{user.mention} has no active players"
            )

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        # update was successful
        clash_updated_player_obj = await clash_responder.get_player(
            db_updated_player_obj.player_tag, self.coc_client)

        # clash player not found
        if clash_updated_player_obj is None:
            embed_description = (
                f"{player_obj.name} {player_obj.tag} "
                f"has been deleted, "
                f"{user.mention} active is now set to "
                f"{db_updated_player_obj.player_tag}, "
                f"could not find player in clash of clans"
            )

        # player deleted
        # active player updated
        # clash player found
        else:
            embed_description = (
                f"{player_obj.name} {player_obj.tag} "
                f"has been deleted, "
                f"{user.mention} active is now set to "
                f"{clash_updated_player_obj.name} "
                f"{clash_updated_player_obj.tag}"
            )

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(inter, embed_list)
