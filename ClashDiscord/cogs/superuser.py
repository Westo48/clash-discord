import disnake
from disnake.ext import commands
from responders import (
    DiscordResponder as discord_responder,
    ClashResponder as clash_responder,
    RazBotDB_Responder as db_responder,
    linkApiResponder as link_responder
)
from utils import discord_utils
from linkAPI.client import LinkApiClient
from linkAPI.errors import *


class SuperUser(commands.Cog):
    def __init__(self, bot, coc_client, client_data, linkapi_client: LinkApiClient):
        self.bot = bot
        self.coc_client = coc_client
        self.client_data = client_data
        self.linkapi_client = linkapi_client

    # super user administration
    @commands.slash_command()
    async def superuser(self, inter):
        """
            parent for client super user commands
        """

        pass

    @superuser.sub_command()
    async def guild(
        self,
        inter,
        option: str = discord_utils.command_param_dict['superuser_guild'],
        guild_id: str = discord_utils.command_param_dict['guild_id']
    ):
        """
            *super user* 
            super user guild commands

            Parameters
            ----------
            option (optional): options for superuser guild commands
            guild_id (optional): guild id for removal
        """

        await inter.response.defer()

        db_author_obj = db_responder.read_user(inter.author.id)
        # author is not claimed
        if not db_author_obj:
            embed_description = f"{inter.author.mention} is not claimed"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        # author is not super user
        if not db_author_obj.super_user:
            embed_description = f"{inter.author.mention} is not super user"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        # initializing embed default values
        embed_title = None
        embed_description = None
        field_dict_list = []

        if option == "show":
            embed_title = f"**ClashDiscord Guilds**"
            embed_description = f"Guild Count: {len(inter.client.guilds)}"

            for guild in inter.client.guilds:
                field_dict_list.append({
                    'name': f"{guild.name}",
                    'value': f"{guild.id}"
                })

        elif option == "remove":
            if guild_id is None:
                embed_description = (
                    f"guild id not specified, "
                    f"please provide guild id to remove a guild")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            guild_id = int(guild_id)

            # confirm guild is claimed
            db_guild_obj = db_responder.read_guild(guild_id)

            # guild isn't claimed
            if not db_guild_obj:
                embed_description = f"guild with id {guild_id} is not claimed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            deleted_guild_obj = db_responder.delete_guild(guild_id)

            # guild was deleted properly
            if deleted_guild_obj is None:
                embed_description = f"guild with id {guild_id} was deleted"

            # guild could not be deleted
            else:
                embed_description = f"guild with id {guild_id} could not be deleted"

        elif option == "leave":
            if guild_id is None:
                embed_description = (
                    f"guild id not specified, "
                    f"please provide guild id to leave a guild")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            guild_id = int(guild_id)

            # confirm bot is in guild
            guild = disnake.utils.get(inter.bot.guilds, id=guild_id)

            # bot isn't in guild
            if guild is None:
                embed_description = (f"{inter.me.display_name} "
                                     f"is not in guild {guild_id}")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            await guild.leave()
            left_guild = disnake.utils.get(inter.bot.guilds, id=guild.id)

            # guild was left properly
            if left_guild is None:
                embed_description = (f"{inter.me.display_name} left "
                                     f"guild {guild.name} id {guild.id}")

            # guild could not be left
            else:
                embed_description = (f"{inter.me.display_name} could not leave "
                                     f"guild {guild.name} id {guild.id}")

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
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(inter, embed_list)

    @superuser.sub_command()
    async def admin(
        self,
        inter,
        option: str = discord_utils.command_param_dict['superuser_admin'],
        user: disnake.User = discord_utils.command_param_dict['user']
    ):
        """
            *super user* 
            super user admin commands

            Parameters
            ----------
            option (optional): options for superuser admin commands
            user (optional): user for admin toggle and user removal
        """

        # defer for every superuser admin command
        await inter.response.defer(ephemeral=True)

        db_author_obj = db_responder.read_user(inter.author.id)
        # author is not claimed
        if not db_author_obj:
            embed_description = f"{inter.author.mention} is not claimed"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        # author is not super user
        if not db_author_obj.super_user:
            embed_description = f"{inter.author.mention} is not super user"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        # initializing embed default values
        embed_title = None
        embed_description = None
        field_dict_list = []

        if option == "show":
            db_admin_users = db_responder.read_user_admin_all()

            if len(db_admin_users) == 0:
                embed_description = f"{inter.me.display_name} has no admin users"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            embed_title = f"{inter.me.display_name} admin users"

            # initialize admin user field dict list
            field_dict_list = []
            for admin_user in db_admin_users:
                # get the discord member in the server of the admin user
                member = disnake.utils.get(
                    inter.guild.members, id=admin_user.discord_id)

                # member not found in server
                if member is None:
                    field_dict_list.append({
                        "name": "admin user id",
                        "value": f"{admin_user.discord_id}",
                        "inline": False
                    })

                # member found in server
                else:
                    field_dict_list.append({
                        "name": "admin user",
                        "value": f"{member.mention}",
                        "inline": False
                    })

        elif option == "toggle":
            if user is None:
                embed_description = (
                    f"user not specified, "
                    f"please provide user to toggle admin status")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # confirm user is claimed
            db_user_obj = db_responder.read_user(user.id)
            # user isn't claimed
            if not db_user_obj:
                embed_description = f"{user.mention} is not claimed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            updated_user_obj = db_responder.update_toggle_user_admin(user.id)
            # upated user not found
            if updated_user_obj is None:
                embed_description = f"{user.mention} could not be updated"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # user was updated and is now an admin
            if updated_user_obj.admin:
                embed_description = f"{user.mention} is now an admin"

            # user was updated and is now not an admin
            else:
                embed_description = f"{user.mention} is no longer an admin"

        elif option == "toggle":
            if user is None:
                embed_description = (
                    f"user not specified, "
                    f"please provide user to remove user")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # confirm user is claimed
            db_user_obj = db_responder.read_user(user.id)
            # user isn't claimed
            if not db_user_obj:
                embed_description = f"{user.mention} is not claimed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            deleted_user_obj = db_responder.delete_user(user.id)

            # user was deleted properly
            if deleted_user_obj is None:
                embed_description = f"{user.mention} was deleted"

            # user could not be deleted
            else:
                embed_description = f"{user.mention} could not be deleted"

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
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(inter, embed_list)

    @superuser.sub_command()
    async def player(
        self,
        inter,
        option: str = discord_utils.command_param_dict['superuser_player'],
        player_tag: str = discord_utils.command_param_dict['required_tag'],
        user: disnake.User = discord_utils.command_param_dict['required_user']
    ):
        """
            *super user* 
            super user player commands

            Parameters
            ----------
            option (optional): options for superuser player commands
            player_tag: player tag create or remove link
            user: user to create or remove player link
        """

        # defer for every superuser player command
        await inter.response.defer(ephemeral=True)

        db_author_obj = db_responder.read_user(inter.author.id)
        # author is not claimed
        if not db_author_obj:
            embed_description = f"{inter.author.mention} is not claimed"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        # author is not super user
        if not db_author_obj.super_user:
            embed_description = f"{inter.author.mention} is not super user"

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

        # initializing embed default values
        embed_title = None
        embed_description = None
        field_dict_list = []

        if option == "claim":
            # confirm user has been claimed
            db_user_obj = db_responder.read_user(user.id)
            if not db_user_obj:
                # user has not been claimed
                db_user_obj = db_responder.claim_user(user.id)
                if not db_user_obj:
                    # user could not be claimed
                    await inter.edit_original_message(
                        content=f"{user.mention} user couldn't be claimed")
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

            # add player link to link API
            try:
                link_responder.add_secure_link(
                    linkapi_client=self.linkapi_client,
                    player_tag=player_obj.tag,
                    discord_user_id=db_user_obj.discord_id
                )
            except ConflictError:
                embed_description = (
                    f"player could not be linked to LinkAPI database, "
                    f"please let {self.client_data.author} know"
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

            # player linked in LinkAPI correctly
            # user claimed
            # player is valid
            # player hasn't been claimed
            db_player_obj = db_responder.claim_player(
                user.id, player_obj.tag)

            # failed to claim
            if db_player_obj is None:
                embed_description = (f"Could not claim {player_obj.name} "
                                     f"{player_obj.tag} for {user.mention}")

            # succesfully claimed
            else:
                embed_description = (f"{player_obj.name} {player_obj.tag} "
                                     f"is now claimed by {user.mention}")

        elif option == "remove":
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
                    author_avatar_url=inter.author.avatar.url)

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_del_player_obj = db_responder.delete_player(
                user.id, player_obj.tag)

            # player was not deleted
            if db_del_player_obj:
                embed_description = (
                    f"{player_obj.name} {player_obj.tag} "
                    f"could not be deleted "
                    f"from {user.mention} player list")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url)

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_active_player_obj = db_responder.read_player_active(user.id)

            # active player found
            # no need to change the active player
            if db_active_player_obj:
                embed_description = (
                    f"{player_obj.name} {player_obj.tag} "
                    f"has been deleted "
                    f"from {user.mention} player list")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url)

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
                    f"{user.mention} has no more claimed players")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url)

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
                    f"{user.mention} has no active players")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url)

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
                    f"could not find player in clash of clans")

            # player deleted
            # active player updated
            # clash player found
            else:
                embed_description = (
                    f"{player_obj.name} {player_obj.tag} "
                    f"has been deleted, "
                    f"{user.mention} active is now set to "
                    f"{clash_updated_player_obj.name} "
                    f"{clash_updated_player_obj.tag}")

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
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url)

        await discord_responder.send_embed_list(inter, embed_list)
