import disnake
from disnake.ext import commands
from responders import (
    DiscordResponder as discord_responder,
    ClashResponder as clash_responder,
    RazBotDB_Responder as db_responder,
    linkApiResponder as link_responder,
    AuthResponder as auth_responder
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
    async def player(
        self,
        inter,
        user: disnake.User = discord_utils.command_param_dict['required_user'],
        option: str = discord_utils.command_param_dict['admin_player'],
        player_tag: str = discord_utils.command_param_dict['client_player_tag']
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

            embed_description = verification_payload["embed_description"]

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

        # options that do not require player tag
        if option == "show":
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

        # options that require a player tag

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
                link_responder.add_link(
                    linkapi_client=self.linkapi_client,
                    player_tag=player_obj.tag,
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

            # player linked in LinkAPI correctly
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
                    author=inter.author
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
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # delete link api link
            try:
                self.linkapi_client.delete_link(
                    player_tag=player_obj.tag)
            except LoginError as arg:
                print(arg)
            # error not found can be ignored
            # failure to delete something that isn't there isn't a problem
            except NotFoundError:
                pass

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
                    author=inter.author
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
                    author=inter.author
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
                    author=inter.author
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
                    f"{clash_updated_player_obj.tag}")

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

            embed_description = verification_payload["embed_description"]

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
