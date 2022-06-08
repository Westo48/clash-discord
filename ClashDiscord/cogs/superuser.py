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
    async def user(
        self,
        inter,
        user: disnake.User = discord_utils.command_param_dict['required_user'],
        option: str = discord_utils.command_param_dict['superuser_user'],
    ):
        """
            *super user* 
            superuser user commands

            Parameters
            ----------
            user: user to run command for
            option (optional): options for superuser user commands
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
                author=inter.author
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
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        # initializing embed default values
        embed_title = None
        embed_description = None
        field_dict_list = []

        if option == "players":
            db_player_obj_list = db_responder.read_player_list(user.id)

            # user has no claimed players
            if len(db_player_obj_list) == 0:
                embed_description = (f"{user.mention} does not have any "
                                     f"claimed players")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
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

            await inter.send(message)

            return

        elif option == "sync":
            try:
                # confirm user has been claimed
                db_user_obj = db_responder.read_user(user.id)

                link_responder.sync_link(
                    linkapi_client=self.linkapi_client,
                    discord_user_id=db_user_obj.discord_id
                )
            except ConflictError as arg:
                embed_description = (f"{inter.author.mention}: {arg}\n\n"
                                     f"please let {self.client_data.author} know")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # player data has been synced correctly
            embed_description = (
                f"data for {user.mention} has been properly synced")

        if option == "claim":
            db_user = db_responder.claim_user(user.id)

            # user wasn't claimed and now is
            if db_user:
                embed_description = f"{user.mention} is now claimed"

            # user was already claimed
            else:
                embed_description = (f"{user.mention} "
                                     f"has already been claimed")

        elif option == "remove":
            db_user = db_responder.read_user(user.id)

            # user not found
            if not db_user:
                embed_description = (f"claimed user for "
                                     f"{user.mention} not found")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    title=embed_title,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    field_list=field_dict_list,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # user found

            # delete user claim
            removed_user = db_responder.delete_user(user.id)

            # user could not be deleted
            if removed_user:
                embed_description = (
                    f"could not delete user "
                    f"{user.mention}, please let "
                    f"{self.client_data.author} know")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    title=embed_title,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    field_list=field_dict_list,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            player_links = []

            # get all player links for this user
            try:
                player_links = self.linkapi_client.get_discord_user_link(
                    user.id)
            except LoginError as arg:
                print(arg)
            # pass this error as nothing needs to be deleted
            except NotFoundError:
                pass

            # delete each link for the user
            for link in player_links:
                try:
                    self.linkapi_client.delete_link(player_tag=link.player_tag)
                except LoginError as arg:
                    print(arg)
                # pass this error as nothing needs to be deleted
                except NotFoundError:
                    pass

            embed_description = (
                f"user {user.mention} removed properly")
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
            author=inter.author)

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
                author=inter.author
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
                author=inter.author
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
                    author=inter.author
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
                    author=inter.author
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
                    author=inter.author
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
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # user was updated and is now an admin
            if updated_user_obj.admin:
                embed_description = f"{user.mention} is now an admin"

            # user was updated and is now not an admin
            else:
                embed_description = f"{user.mention} is no longer an admin"

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
            author=inter.author
        )

        await discord_responder.send_embed_list(inter, embed_list)

    @superuser.sub_command()
    async def player(
        self,
        inter,
        user: disnake.User = discord_utils.command_param_dict['required_user'],
        option: str = discord_utils.command_param_dict['superuser_player'],
        player_tag: str = discord_utils.command_param_dict['client_player_tag']
    ):
        """
            *super user* 
            super user player commands

            Parameters
            ----------
            user: user to run command for
            option (optional): options for superuser player commands
            player_tag (optional): player tag create or remove link
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
                author=inter.author
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
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        # initializing embed default values
        embed_title = None
        embed_description = None
        field_dict_list = []

        # commands that do not require player tag
        if option == "sync":
            # confirm user has been claimed
            db_user_obj = db_responder.read_user(user.id)

            if not db_user_obj:
                db_user_obj = db_responder.claim_user(user.id)

                # user could not be claimed
                if not db_user_obj:
                    embed_description = f"{user.mention} user couldn't be claimed"

                    embed_list = discord_responder.embed_message(
                        icon_url=inter.bot.user.avatar.url,
                        description=embed_description,
                        bot_user_name=inter.me.display_name,
                        author=inter.author
                    )

                    await discord_responder.send_embed_list(inter, embed_list)
                    return

            try:
                link_responder.sync_link(
                    linkapi_client=self.linkapi_client,
                    discord_user_id=db_user_obj.discord_id
                )
            except ConflictError as arg:
                embed_description = (f"{inter.author.mention}: {arg}\n\n"
                                     f"please let {self.client_data.author} know")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # player data has been synced correctly
            embed_description = (
                f"data for {user.mention} has been properly synced")

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                title=embed_title,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                field_list=field_dict_list,
                author=inter.author)

            await discord_responder.send_embed_list(inter, embed_list)
            return

        # player tag not supplied
        if not player_tag:
            embed_description = f"please enter a valid player tag"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author=inter.author
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
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

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
                    author=inter.author
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
                embed_description = (f"{inter.author.mention}: {arg}\n\n"
                                     f"please let {self.client_data.author} know")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
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
                    author=inter.author)

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
                    author=inter.author)

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # delete link api link
            self.linkapi_client.delete_link(
                player_tag=player_obj.tag)

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
                    author=inter.author)

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
                    author=inter.author)

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
                    author=inter.author)

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
            author=inter.author)

        await discord_responder.send_embed_list(inter, embed_list)

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
                author=inter.author
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
                author=inter.author
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
                    author=inter.author
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
                    author=inter.author
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
                    author=inter.author
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
                    author=inter.author
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
            author=inter.author
        )

        await discord_responder.send_embed_list(inter, embed_list)

    @superuser.sub_command()
    async def count(
        self, inter,
        option: str = discord_utils.command_param_dict['superuser_count'],
    ):
        """
            *super user* 
            super user count commands

            Parameters
            ----------
            option (optional): options for superuser count commands
        """

        # defer for every superuser count command
        await inter.response.defer(ephemeral=True)

        db_author_obj = db_responder.read_user(inter.author.id)

        # author is not claimed
        if not db_author_obj:
            embed_description = f"{inter.author.mention} is not claimed"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author=inter.author
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
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        # initializing embed default values
        embed_title = None
        embed_description = None
        field_dict_list = []

        if option == "user":
            user_count = db_responder.read_user_count()

            embed_title = f"{inter.me.display_name} User Count"
            embed_description = f"{user_count} users"

        elif option == "player":
            player_count = db_responder.read_player_count()

            embed_title = f"{inter.me.display_name} Player Count"
            embed_description = f"{player_count} players"

        elif option == "guild":
            guild_count = db_responder.read_guild_count()

            embed_title = f"{inter.me.display_name} Guild Count"
            embed_description = f"{guild_count} guilds"

        elif option == "clan":
            clan_count = db_responder.read_clan_count()

            embed_title = f"{inter.me.display_name} Clan Count"
            embed_description = f"{clan_count} clans"

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
            author=inter.author)

        await discord_responder.send_embed_list(inter, embed_list)
