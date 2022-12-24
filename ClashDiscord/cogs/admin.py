import disnake
from disnake.ext import commands
from responders import (
    DiscordResponder as discord_responder,
    ClashResponder as clash_responder,
    RazBotDB_Responder as db_responder,
    linkApiResponder as link_responder,
    AuthResponder as auth_responder
)
from responders.ClientResponder import (
    client_player_list,
    client_user_profile
)
from utils import discord_utils
from linkAPI.client import LinkApiClient
from linkAPI.errors import *


class Admin(commands.Cog):
    def __init__(self, bot, coc_client, client_data, linkapi_client: LinkApiClient):
        self.bot = bot
        self.coc_client = coc_client
        self.client_data = client_data
        self.linkapi_client = linkapi_client

    @commands.slash_command()
    async def admin(self, inter):
        """
            parent for client admin commands
        """

        # defer for every command
        await inter.response.defer()

    @admin.sub_command()
    async def user(
        self,
        inter,
        user: disnake.User = discord_utils.command_param_dict['required_user'],
        option: str = discord_utils.command_param_dict['admin_user'],
        player_tag: str = discord_utils.command_param_dict['client_player_tag']
    ):
        """
            *admin* 
            admin user commands

            Parameters
            ----------
            player_tag: clash of clans player tag
            option (optional): options for player commands
            user (optional): user to run command for
        """

        # authenticating admin authorization
        verification_payload = (
            auth_responder.guild_admin_verification(inter))

        if not verification_payload['verified']:

            embed_description = verification_payload["embed_list"]

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author=inter.author
            )

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
                    author=inter.author
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
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

        # admin authentication authorized

        # initializing embed default values
        embed_title = None
        embed_description = None
        field_dict_list = []

        if option == "profile":
            db_player_list = db_responder.read_player_list(user.id)

            # user has no claimed players
            if len(db_player_list) == 0:
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

            embed_title = f"{user.display_name} Profile"
            embed_description = f"Player Count: {len(db_player_list)}"

            field_dict_list = await client_user_profile(
                db_player_list=db_player_list,
                user=user,
                discord_emoji_list=inter.client.emojis,
                client_emoji_list=self.client_data.emojis,
                coc_client=self.coc_client)

        elif option == "player list":
            db_player_list = db_responder.read_player_list(user.id)

            # user has no claimed players
            if len(db_player_list) == 0:
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

            message = await client_player_list(
                db_player_list=db_player_list,
                user=user,
                coc_client=self.coc_client)

            await inter.edit_original_message(content=message)
            return

        elif option == "sync":
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

        elif option == "update":
            if player_tag is None:
                embed_description = (
                    f"player tag not specified, "
                    f"please provide player tag to update a player")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            player = await clash_responder.get_player(player_tag, self.coc_client)

            # if player with tag not found
            if not player:
                embed_description = f"player with tag {player_tag} not found"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_player = db_responder.read_player(
                user.id, player.tag)

            # if requested player is not claimed
            if not db_player:
                embed_description = (
                    f"{user.mention} "
                    f"has not claimed "
                    f"{player.name} {player.tag}"
                )

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # if requested player is the active player
            if db_player.active:
                embed_description = (
                    f"{player.name} {player.tag} "
                    f"is already active player for {user.mention}"
                    f""
                )

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            else:
                db_player = db_responder.update_player_active(
                    user.id, player.tag)

                embed_description = (
                    f"{player.name} {player.tag} is now "
                    f"active player for {user.mention}"
                )

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
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
            title=embed_title,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author=inter.author)

        await discord_responder.send_embed_list(inter, embed_list)

    @admin.sub_command()
    async def player(
        self,
        inter,
        option: str = discord_utils.command_param_dict['admin_player'],
        user: disnake.User = discord_utils.command_param_dict['required_user'],
        player_tag: str = discord_utils.command_param_dict['required_player_tag']
    ):
        """
            *admin* 
            admin player commands

            Parameters
            ----------
            user: user to run command for
            option (optional): options for player commands
            player_tag (optional): player tag create or remove link
        """

        # authenticating admin authorization
        verification_payload = (
            auth_responder.guild_admin_verification(inter))

        if not verification_payload['verified']:

            embed_description = verification_payload["embed_list"]

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)

            return

        # admin authentication authorized

        # user not supplied
        if not user:
            embed_description = f"please supply a valid user"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        # confirm admin is not editing an admin

        # confirm user has been claimed
        db_user = db_responder.read_user(user.id)
        if not db_user:
            # user has not been claimed
            db_user = db_responder.claim_user(user.id)
            if not db_user:
                # user could not be claimed
                embed_description = f"{user.mention} user couldn't be claimed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

        db_author = verification_payload["db_author"]

        # admin is not a super user and author is not the user
        if (not db_author.super_user
                and db_author.discord_id != db_user.discord_id):
            # admin users are not allowed to update admins or super users
            if db_user.admin or db_user.super_user:
                embed_description = (f"admins are not allowed to update "
                                     f"admins or super users")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

        # action approved

        # initializing embed default values
        embed_title = None
        embed_description = None
        field_dict_list = []

        if option == "claim":
            # confirm valid player_tag
            player = await clash_responder.get_player(
                player_tag, self.coc_client)

            # player tag was not valid
            if not player:
                embed_description = f"player with tag {player_tag} was not found"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # confirm player has not been claimed
            db_player = db_responder.read_player_from_tag(player.tag)

            # player has already been claimed
            if db_player:
                embed_description = (f"{player.name} {player.tag} "
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
                link_responder.add_link(
                    linkapi_client=self.linkapi_client,
                    player_tag=player.tag,
                    discord_user_id=db_user.discord_id
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

            # player linked in LinkAPI correctly
            # user claimed
            # player is valid
            # player hasn't been claimed
            db_player = db_responder.claim_player(
                user.id, player.tag)

            # succesfully claimed
            if db_player:
                embed_description = (f"{player.name} {player.tag} "
                                     f"is now claimed by {user.mention}")
            # failed to claim
            else:
                embed_description = (f"Could not claim {player.name} "
                                     f"{player.tag} for {user.mention}")

        elif option == "remove":
            # player tag is a required parameter
            # player tag not specified
            if player_tag is None:
                embed_description = (
                    f"player tag not specified, "
                    f"please provide player tag to remove a player")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            player = await clash_responder.get_player(player_tag, self.coc_client)

            # player not found
            if not player:
                # format player tag
                # remove spaces
                player_tag = player_tag.replace(" ", "")
                # adding "#" if it isn't already in the player tag
                if "#" not in player_tag:
                    player_tag = f"#{player_tag}"

                player_title = player_tag.upper()

            else:
                player_tag = player.tag
                player_title = f"{player.name} {player.tag}"

            db_player = db_responder.read_player(user.id, player_tag)

            # db player not found
            if not db_player:
                embed_description = (
                    f"{player_title} is not claimed "
                    f"by {user.mention}")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_del_player = db_responder.delete_player(
                user.id, player_tag)

            # player was not deleted
            if db_del_player:
                embed_description = (
                    f"{player_title} "
                    f"could not be deleted "
                    f"from {user.mention} player list"
                )

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # delete link api link
            try:
                self.linkapi_client.delete_link(
                    player_tag=player_tag)
            except LoginError as arg:
                print(arg)
            # error not found can be ignored
            # failure to delete something that isn't there isn't a problem
            except NotFoundError:
                pass

            db_active_player = db_responder.read_player_active(user.id)

            # active player found
            # no need to change the active player
            if db_active_player:
                embed_description = (
                    f"{player_title} has been deleted "
                    f"from {user.mention} player list"
                )

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # no active player found
            # check if there are any other players
            db_player_list = db_responder.read_player_list(
                user.id)

            # no additional players claimed
            if len(db_player_list) == 0:
                embed_description = (
                    f"{player_title} has been deleted, "
                    f"{user.mention} has no more claimed players"
                )

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # additional players claimed by user
            # update the first as the new active
            db_updated_player = db_responder.update_player_active(
                user.id, db_player_list[0].player_tag)

            # update not successful
            if not db_updated_player:
                embed_description = (
                    f"{player_title} has been deleted, "
                    f"could not update active player, "
                    f"{user.mention} has no active players"
                )

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # update was successful
            clash_updated_player = await clash_responder.get_player(
                db_updated_player.player_tag, self.coc_client)

            # clash player not found
            if clash_updated_player is None:
                embed_description = (
                    f"{player_title} has been deleted, "
                    f"{user.mention} active is now set to "
                    f"{db_updated_player.player_tag}, "
                    f"could not find player in clash of clans"
                )

            # player deleted
            # active player updated
            # clash player found
            else:
                embed_description = (
                    f"{player_title} has been deleted, "
                    f"{user.mention} active is now set to "
                    f"{clash_updated_player.name} "
                    f"{clash_updated_player.tag}")

        else:
            field_dict_list = [{
                'name': "incorrect option selected",
                'value': "please select a different option"
            }]

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author=inter.author)

        await discord_responder.send_embed_list(inter, embed_list)

    @admin.sub_command()
    async def missing(
        self,
        inter,
        clan_role: disnake.Role = discord_utils.command_param_dict['clan_role']
    ):
        """
            *admin* 
            show who has not been linked from a clan

            Parameters
            ----------
            clan_role (optional): clan role to use linked clan
        """

        verification_payload = (
            auth_responder.guild_admin_verification(inter))

        if not verification_payload['verified']:

            embed_description = verification_payload["embed_list"]

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)

            return

        # role not mentioned
        if clan_role is None:
            db_player_obj = db_responder.read_player_active(
                inter.author.id)

            verification_payload = (
                await auth_responder.clan_verification(
                    db_player_obj, inter.author, self.coc_client))

        # role mentioned
        else:
            verification_payload = (
                await auth_responder.clan_role_player_verification(
                    clan_role, inter.author, inter.guild.id, self.coc_client))

        if not verification_payload['verified']:
            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                field_list=verification_payload['field_dict_list'],
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        clan_obj = verification_payload['clan_obj']

        embed_title = f"{clan_obj.name} {clan_obj.tag} missing linked users"
        field_dict_list = []
        embed_thumbnail = clan_obj.badge.small

        member_dict_list = []

        # finding the user for each member in the clan
        for member_obj in clan_obj.members:
            member_dict_list.append(discord_responder.find_user_from_tag(
                member_obj, inter.guild.members))

        # selecting all those who aren't linked
        for member_dict in member_dict_list:
            if "not found" in member_dict["value"]:
                field_dict_list.append(member_dict)

        if len(field_dict_list) == 0:
            field_dict_list.append({
                "name": f"all {len(clan_obj.members)} members linked",
                "value": "no additional members need to be linked"
            })

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=embed_title,
            thumbnail=embed_thumbnail,
            field_list=field_dict_list,
            bot_user_name=inter.me.display_name,
            author=inter.author
        )

        await discord_responder.send_embed_list(inter, embed_list)

    @admin.sub_command()
    async def clan(
        self,
        inter,
        option: str = discord_utils.command_param_dict['admin_clan'],
        clan_tag: str = discord_utils.command_param_dict['tag']
    ):
        """
            *ClashCommander server admin* 
            admin clan commands

            Parameters
            ----------
            option (optional): options for admin clan returns
            clan_tag (optional): tag for clan to claim
        """

        # initializing embed default values
        embed_title = None
        embed_description = None
        field_dict_list = []

        if option == "show":
            db_guild_obj = db_responder.read_guild(inter.guild.id)

            # guild not claimed
            if not db_guild_obj:
                embed_description = f"{inter.guild.name} has not been claimed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_user_obj = db_responder.read_user(inter.author.id)

            # user not claimed
            if not db_user_obj:
                embed_description = f"{inter.author.mention} has not been claimed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # user is not guild admin and is not super user
            if (not db_guild_obj.admin_user_id == inter.author.id
                    and not db_user_obj.super_user):
                embed_description = f"{inter.author.mention} is not server's admin"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_clan_obj_list = db_responder.read_clan_list_from_guild(
                inter.guild.id)

            # guild has no claimed clans
            if len(db_clan_obj_list) == 0:
                embed_description = f"{inter.guild.name} does not have any claimed clans"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            embed_title = f"{inter.guild.name} claimed clans"

            field_dict_list = []
            for db_clan in db_clan_obj_list:
                clan = await clash_responder.get_clan(
                    db_clan.clan_tag, self.coc_client)

                field_dict_list.append({
                    "name": clan.name,
                    "value": clan.tag
                })

        elif option == "claim":
            if clan_tag is None:
                embed_description = (
                    f"player tag not specified, "
                    f"please provide player tag to remove a player")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_guild_obj = db_responder.read_guild(inter.guild.id)

            # guild not claimed
            if not db_guild_obj:
                embed_description = f"{inter.guild.name} has not been claimed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_user_obj = db_responder.read_user(inter.author.id)

            # user not claimed
            if not db_user_obj:
                embed_description = f"{inter.author.mention} has not been claimed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # user is not guild admin and is not super user
            if (not db_guild_obj.admin_user_id == inter.author.id
                    and not db_user_obj.super_user):
                embed_description = f"{inter.author.mention} is not server's admin"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            clan_obj = await clash_responder.get_clan(clan_tag, self.coc_client)

            # clan not found
            if not clan_obj:
                embed_description = f"couldn't find clan {clan_tag}"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            claimed_clan_obj = db_responder.read_clan(
                inter.guild.id, clan_obj.tag)

            # already claimed
            if claimed_clan_obj:
                embed_description = (
                    f"{clan_obj.name} has already been claimed for "
                    f"{inter.guild.name}"
                )

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_clan_obj = db_responder.claim_clan(inter.guild.id, clan_obj.tag)

            # clan not claimed
            if not db_clan_obj:
                embed_description = f"couldn't claim {clan_obj.name}"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            embed_description = f"{clan_obj.name} has been claimed"

        elif option == "remove":
            if clan_tag is None:
                embed_description = (
                    f"player tag not specified, "
                    f"please provide player tag to remove a player")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_guild_obj = db_responder.read_guild(inter.guild.id)

            # guild not claimed
            if not db_guild_obj:
                embed_description = f"{inter.guild.name} has not been claimed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_user_obj = db_responder.read_user(inter.author.id)

            # user not claimed
            if not db_user_obj:
                embed_description = f"{inter.author.mention} has not been claimed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # user is not guild admin and is not super user
            if (not db_guild_obj.admin_user_id == inter.author.id
                    and not db_user_obj.super_user):
                embed_description = f"{inter.author.mention} is not server's admin"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            clan_obj = await clash_responder.get_clan(clan_tag, self.coc_client)

            # clan not found
            if not clan_obj:
                embed_description = f"couldn't find clan {clan_tag}"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_clan_obj = db_responder.read_clan(inter.guild.id, clan_obj.tag)
            # clan not claimed by guild
            if not db_clan_obj:
                embed_description = (f"{clan_obj.name} has not been claimed by "
                                     f"{inter.guild.name}")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_clan_deletion = db_responder.delete_clan(
                inter.guild.id, clan_obj.tag)
            # clan was found after deletion
            if db_clan_deletion:
                embed_description = f"{clan_obj.name} could not be deleted"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            embed_description = (f"{clan_obj.name} has been deleted "
                                 f"from {inter.guild.name}")

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

    @admin.sub_command()
    async def role(
        self,
        inter,
        option: str = discord_utils.command_param_dict['admin_role'],
        role: disnake.Role = discord_utils.command_param_dict['role_mention']
    ):
        """
            *ClashCommander server admin* 
            admin role commands

            Parameters
            ----------
            option (optional): options for admin role returns
            role (optional): mentioned discord role
        """

        # initializing embed default values
        embed_title = None
        embed_description = None
        field_dict_list = []

        if option == "show":
            db_user_obj = db_responder.read_user(inter.author.id)

            db_guild_obj = db_responder.read_guild(inter.guild.id)
            # guild not claimed
            if not db_guild_obj:
                embed_description = f"{inter.guild.name} has not been claimed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # user not claimed
            if not db_user_obj:
                embed_description = f"{inter.author.mention} has not been claimed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # user is not guild admin and is not super user
            if (not db_guild_obj.admin_user_id == inter.author.id
                    and not db_user_obj.super_user):
                embed_description = f"{inter.author.mention} is not server's admin"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            embed_title = f"{inter.guild.name} claimed roles"
            field_dict_list = []

            db_clan_role_list = db_responder.read_guild_clan_role(
                inter.guild.id)

            db_rank_role_list = db_responder.read_guild_rank_role(
                inter.guild.id)

            if len(db_clan_role_list) != 0:
                for db_role in db_clan_role_list:
                    discord_role = disnake.utils.get(
                        inter.guild.roles, id=db_role.discord_role_id)

                    # discord role is claimed, but not found in server
                    if not discord_role:
                        deleted_db_role = db_responder.delete_clan_role(
                            db_role.discord_role_id)

                        field_dict_list.append({
                            'name': f"clan tag {db_role.clan_tag}",
                            'value': f"role {db_role.discord_role_id} *deleted*"
                        })
                        continue

                    clan = await clash_responder.get_clan(
                        db_role.clan_tag, self.coc_client)

                    if not clan:
                        field_dict_list.append({
                            'name': f"clan tag {db_role.clan_tag}",
                            'value': f"role {discord_role.mention}"
                        })
                        continue

                    field_dict_list.append({
                        'name': f"clan {clan.name} tag {db_role.clan_tag}",
                        'value': f"role {discord_role.mention}"
                    })

            if len(db_rank_role_list) != 0:
                for db_role in db_rank_role_list:
                    discord_role = disnake.utils.get(
                        inter.guild.roles, id=db_role.discord_role_id)

                    # discord role is claimed, but not found in server
                    if not discord_role:
                        deleted_db_role = db_responder.delete_rank_role(
                            db_role.discord_role_id)

                        field_dict_list.append({
                            'name': f"rank {db_role.model_name}",
                            'value': f"role {db_role.discord_role_id} *deleted*"
                        })
                        continue

                    field_dict_list.append({
                        'name': f"rank {db_role.model_name}",
                        'value': f"role {discord_role.mention}"
                    })

            # guild has no claimed rank roles
            if (len(db_clan_role_list) == 0 and
                    len(db_rank_role_list) == 0):
                field_dict_list.append({
                    'name': f"server has no claimed roles",
                    'value': f"please claim a clan or rank role"
                })

        elif option == "remove":
            if role is None:
                embed_description = (
                    f"role not specified, "
                    f"please provide role to remove a linked role")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_user_obj = db_responder.read_user(inter.author.id)
            db_guild_obj = db_responder.read_guild(inter.guild.id)

            # guild not claimed
            if not db_guild_obj:
                embed_description = f"{inter.guild.name} has not been claimed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # user not claimed
            if not db_user_obj:
                embed_description = f"{inter.author.mention} has not been claimed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # user is not guild admin and is not super user
            if (not db_guild_obj.admin_user_id == inter.author.id
                    and not db_user_obj.super_user):
                embed_description = f"{inter.author.mention} is not server's admin"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_clan_role_obj = db_responder.read_clan_role(role.id)

            # claimed role is clan role
            if db_clan_role_obj:
                # delete clan role
                db_clan_role_deletion = db_responder.delete_clan_role(role.id)
                # clan role found after deletion
                if db_clan_role_deletion:
                    embed_description = f"{role.mention} claim could not be removed"

                    embed_list = discord_responder.embed_message(
                        icon_url=inter.bot.user.avatar.url,
                        description=embed_description,
                        bot_user_name=inter.me.display_name,
                        author=inter.author
                    )

                    await discord_responder.send_embed_list(inter, embed_list)
                    return

                # clan role deleted
                embed_description = f"{role.mention} claim was removed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_rank_role_obj = db_responder.read_rank_role(role.id)

            # claimed role is rank role
            if db_rank_role_obj:
                # delete rank role
                db_rank_role_deletion = db_responder.delete_rank_role(role.id)
                # rank role found after deletion
                if db_rank_role_deletion:
                    embed_description = f"{role.mention} claim could not be removed"

                    embed_list = discord_responder.embed_message(
                        icon_url=inter.bot.user.avatar.url,
                        description=embed_description,
                        bot_user_name=inter.me.display_name,
                        author=inter.author
                    )

                    await discord_responder.send_embed_list(inter, embed_list)
                    return

                # rank role deleted
                embed_description = f"{role.mention} claim was removed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            embed_description = f"{role.mention} is not claimed"

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

    @admin.sub_command()
    async def clanrole(
        self,
        inter,
        option: str = discord_utils.command_param_dict['admin_clan_rank_role'],
        role: disnake.Role = discord_utils.command_param_dict['role_mention'],
        clan_tag: str = discord_utils.command_param_dict['tag']
    ):
        """
            *ClashCommander server admin* 
            admin clan role commands

            Parameters
            ----------
            option (optional): options for admin clan role returns
            role (optional): role object to claim and link to claimed clan
            clan_tag (optional): clan tag to link to role
        """

        # initializing embed default values
        embed_title = None
        embed_description = None
        field_dict_list = []

        if option == "claim":
            if role is None or clan_tag is None:
                embed_description = (
                    f"role and clan tag not specified, "
                    f"please provide role and clan tag to link a clan role")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            clan_obj = await clash_responder.get_clan(clan_tag, self.coc_client)

            # clan not found
            if not clan_obj:
                embed_description = f"couldn't find clan {clan_tag}"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_guild_obj = db_responder.read_guild(inter.guild.id)

            # guild not claimed
            if not db_guild_obj:
                embed_description = f"{inter.guild.name} has not been claimed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_user_obj = db_responder.read_user(inter.author.id)

            # user not claimed
            if not db_user_obj:
                embed_description = f"{inter.author.mention} has not been claimed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # user is not guild admin and is not super user
            if (not db_guild_obj.admin_user_id == inter.author.id
                    and not db_user_obj.super_user):
                embed_description = f"{inter.author.mention} is not server's admin"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_clan_obj = db_responder.read_clan(inter.guild.id, clan_obj.tag)

            # clan not claimed by guild
            if not db_clan_obj:
                embed_description = (f"{clan_obj.name} has not been claimed by "
                                     f"{inter.guild.name}")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # confirm clan role has not been claimed
            db_clan_role_obj = db_responder.read_clan_role(role.id)

            # clan role has been claimed
            if db_clan_role_obj:
                embed_description = (f"{role.mention} has already been claimed "
                                     f"for clan {db_clan_role_obj.clan_tag}")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # confirm rank role has not been claimed
            db_rank_role_obj = db_responder.read_rank_role(role.id)

            # rank role has been claimed
            if db_rank_role_obj:
                embed_description = (f"{role.mention} has already been claimed "
                                     f"for rank {db_rank_role_obj.model_name}")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # claim clan role
            claimed_clan_role_obj = db_responder.claim_clan_role(
                role.id, inter.guild.id, clan_obj.tag)

            # clan role could not be claimed
            if not claimed_clan_role_obj:
                embed_description = (f"could not claim {role.mention} "
                                     f"for clan {clan_obj.tag}")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            embed_description = f"{role.mention} has been claimed for clan {clan_obj.tag}"

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

    @admin.sub_command()
    async def rankrole(
        self,
        inter,
        option: str = discord_utils.command_param_dict['admin_clan_rank_role'],
        role: disnake.Role = discord_utils.command_param_dict['role_mention'],
        rank_name: str = discord_utils.command_param_dict['rank_name']
    ):
        """
            *ClashCommander server admin* 
            admin rank role commands

            Parameters
            ----------
            option (optional): options for admin rank role returns
            rank_name: requested rank to link to role
        """

        # initializing embed default values
        embed_title = None
        embed_description = None
        field_dict_list = []

        if option == "claim":
            if role is None or rank_name is None:
                embed_description = (
                    f"role and rank name not specified, "
                    f"please provide role and rank name to link a rank role")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # validate given role name with model
            rank_role_model_obj = db_responder.read_rank_role_model(rank_name)

            # rank role name invalid
            if not rank_role_model_obj:
                embed_description = f"{rank_name} is not a valid rank"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_guild_obj = db_responder.read_guild(inter.guild.id)
            # guild not claimed
            if not db_guild_obj:
                embed_description = f"{inter.guild.name} has not been claimed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_user_obj = db_responder.read_user(inter.author.id)
            # user not claimed
            if not db_user_obj:
                embed_description = f"{inter.author.mention} has not been claimed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # user is not guild admin and is not super user
            if (not db_guild_obj.admin_user_id == inter.author.id
                    and not db_user_obj.super_user):
                embed_description = f"{inter.author.mention} is not server's admin"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # confirm clan role has not been claimed
            db_clan_role_obj = db_responder.read_clan_role(role.id)
            # clan role has been claimed
            if db_clan_role_obj:
                embed_description = (f"{role.mention} has already been claimed for clan "
                                     f"{db_clan_role_obj.clan_tag}")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # confirm rank role has not been claimed
            db_rank_role_obj = db_responder.read_rank_role(role.id)
            # rank role has been claimed
            if db_rank_role_obj:
                embed_description = (f"{role.mention} has already been claimed for rank "
                                     f"{db_rank_role_obj.model_name}")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # claim rank role
            claimed_rank_role_obj = db_responder.claim_rank_role(
                role.id, inter.guild.id, rank_name)
            # rank role could not be claimed
            if claimed_rank_role_obj is None:
                embed_description = (f"could not claim {role.mention} for rank "
                                     f"{db_rank_role_obj.model_name}")

            # rank role was claimed and found
            else:
                embed_description = (f"{role.mention} has been claimed for rank "
                                     f"{claimed_rank_role_obj.model_name}")

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

    @admin.sub_command()
    async def server(
        self,
        inter,
        option: str = discord_utils.command_param_dict['admin_server']
    ):
        """
            claim a discord server and set yourself 
            as the server admin for ClashCommander

            Parameters
            ----------
            option (optional): options for client server returns
        """

        # initializing embed default values
        embed_title = None
        embed_description = None
        field_dict_list = []

        if option == "claim":
            # getting db user object
            db_user_obj = db_responder.read_user(inter.author.id)

            # user not found
            if not db_user_obj:
                embed_description = f"{inter.author.mention} has not been claimed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_guild_obj = db_responder.read_guild(inter.guild.id)

            # guild already claimed
            if db_guild_obj:
                embed_description = f"{inter.guild.name} has already been claimed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_claimed_guild = db_responder.claim_guild(
                inter.author.id, inter.guild.id)

            # guild already claimed or could not be claimed
            if not db_claimed_guild:
                embed_description = f"{inter.guild.name} could not be claimed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            field_dict_list = [{
                "name": f"{inter.guild.name} is now claimed",
                "value": f"admin user {inter.author.mention}"
            }]

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
