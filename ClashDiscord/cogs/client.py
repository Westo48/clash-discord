import disnake
from disnake.ext import commands
from responders import (
    DiscordResponder as discord_responder,
    ClashResponder as clash_responder,
    RazBotDB_Responder as db_responder,
    linkApiResponder as link_responder,
    ClientResponder as client_responder
)
from utils import discord_utils
from linkAPI.client import LinkApiClient
from linkAPI.errors import *


class Client(commands.Cog):
    def __init__(self, bot, coc_client, client_data, linkapi_client: LinkApiClient):
        self.bot = bot
        self.coc_client = coc_client
        self.client_data = client_data
        self.linkapi_client = linkapi_client

    @commands.slash_command()
    async def client(self, inter):
        """
            parent for client commands
        """

        # defer for every command
        await inter.response.defer()

    @client.sub_command()
    async def info(self, inter):
        """
            overview for the client
        """

        field_dict_list = []

        field_dict_list.extend(client_responder.client_info(
            inter.client, self.client_data))

        db_guild = db_responder.read_guild(inter.guild.id)

        field_dict_list.extend(client_responder.client_guild_info(
            inter.guild, db_guild))

        db_players = db_responder.read_player_list(inter.author.id)

        field_dict_list.extend(await client_responder.client_player_info(
            inter.author, db_players, self.coc_client))

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{inter.me.display_name} client overview",
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author=inter.author
        )

        await discord_responder.send_embed_list(inter, embed_list)

    @client.sub_command()
    async def user(
        self,
        inter,
        option: str = discord_utils.command_param_dict['client_user']
    ):
        """
            claim your discord user

            Parameters
            ----------
            option (optional): options for client user returns
        """

        # initializing embed default values
        embed_title = None
        embed_description = None
        field_dict_list = []

        if option == "claim":
            user = db_responder.claim_user(inter.author.id)

            # user wasn't claimed and now is
            if user:
                embed_description = f"{inter.author.mention} is now claimed"

            # user was already claimed
            else:
                embed_description = (f"{inter.author.mention} "
                                     f"has already been claimed")

        elif option == "remove":
            db_user = db_responder.read_user(inter.author.id)

            # user not found
            if not db_user:
                embed_description = (f"claimed user for "
                                     f"{inter.author.mention} not found")

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
            removed_user = db_responder.delete_user(inter.author.id)

            # user could not be deleted
            if removed_user:
                embed_description = (
                    f"could not delete user "
                    f"{inter.author.mention}, please let "
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
                    inter.author.id)
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
                f"user {inter.author.mention} removed properly")

        else:
            embed_title = None
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

    @client.sub_command()
    async def player(
        self,
        inter,
        option: str = discord_utils.command_param_dict['client_player'],
        player_tag: str = discord_utils.command_param_dict['client_player_tag'],
        api_key: str = discord_utils.command_param_dict['api_key']
    ):
        """
            client player commands, 
            a player must be claimed to view and run 
            many of ClashCommander commands

            Parameters
            ----------
            option (optional): options for client player returns
            player_tag: player tag to search
            api_key: api key provided from in game
        """

        # initializing embed default values
        embed_title = None
        embed_description = None
        field_dict_list = []

        if option == "claim":
            if player_tag is None or api_key is None:
                embed_description = (
                    f"player tag and api key not specified, "
                    f"please provide player tag and api key to claim a player")

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

            # confirm user has been claimed
            db_user_obj = db_responder.read_user(inter.author.id)
            if not db_user_obj:
                db_user_obj = db_responder.claim_user(inter.author.id)

                # user could not be claimed
                if not db_user_obj:
                    embed_description = f"{inter.author.mention} user couldn't be claimed"

                    embed_list = discord_responder.embed_message(
                        icon_url=inter.bot.user.avatar.url,
                        description=embed_description,
                        bot_user_name=inter.me.display_name,
                        author=inter.author
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
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # authenticate player api key
            player_verified = await clash_responder.verify_token(
                api_key, player_obj.tag, self.coc_client)
            # api key could not be verified
            if not player_verified:
                embed_description = (f"verification for "
                                     f"player tag {player_obj.tag} has failed")

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
            # player is authenticated

            # claim player in db
            db_player_obj = db_responder.claim_player(
                inter.author.id, player_obj.tag)

            # succesfully claimed
            if db_player_obj:
                embed_description = (
                    f"{player_obj.name} {player_obj.tag} "
                    f"is now claimed by {inter.author.mention}")
            # failed to claim
            else:
                embed_description = (
                    f"Could not claim {player_obj.name} "
                    f"{player_obj.tag} for {inter.author.mention}")

        elif option == "show":
            db_player_obj_list = db_responder.read_player_list(inter.author.id)

            # user has no claimed players
            if len(db_player_obj_list) == 0:
                embed_description = (f"{inter.author.mention} does not have any "
                                     f"claimed players")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            message = f"{inter.author.mention} has claimed "
            for db_player_obj in db_player_obj_list:
                player_obj = await clash_responder.get_player(
                    db_player_obj.player_tag, self.coc_client)

                # player not found in clash
                if player_obj is None:
                    message += f"**{db_player_obj.player_tag} not found in clash please remove**, "
                    continue

                if db_player_obj.active:
                    message += f"{player_obj.name} {player_obj.tag} (active), "
                else:
                    message += f"{player_obj.name} {player_obj.tag}, "

            # cuts the last two characters from the string ', '
            message = message[:-2]

            await inter.send(message)

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
                inter.author.id, player.tag)

            # if requested player is not claimed
            if not db_player:
                embed_description = (
                    f"{inter.author.mention} "
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
                    f"is already your active player "
                    f"{inter.author.mention}"
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
                    inter.author.id, player.tag)

                embed_description = (
                    f"{player.name} {player.tag} is now "
                    f"your active player {inter.author.mention}"
                )

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

        elif option == "remove":
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

            db_player = db_responder.read_player(
                inter.author.id, player_tag)

            # db player not found
            if not db_player:
                embed_description = (f"{player_title} is not claimed by "
                                     f"{inter.author.mention}")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_del_player = db_responder.delete_player(
                inter.author.id, player_tag)

            # player was not deleted
            if db_del_player:
                embed_description = (
                    f"{player_title} could not be deleted "
                    f"from {inter.author.mention} player list"
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
            self.linkapi_client.delete_link(
                player_tag=player_tag)

            db_active_player = db_responder.read_player_active(
                inter.author.id)

            # active player found
            # no need to change the active player
            if db_active_player:
                embed_description = (
                    f"{player_title} has been deleted "
                    f"from {inter.author.mention} player list"
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
                inter.author.id)

            # no additional players claimed
            if len(db_player_list) == 0:
                embed_description = (
                    f"{player_title} has been deleted, "
                    f"{inter.author.mention} has no more claimed players")

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
                inter.author.id, db_player_list[0].player_tag)

            # update not successful
            if not db_updated_player:
                embed_description = (
                    f"{player_title} has been deleted, "
                    f"could not update active player, "
                    f"{inter.author.mention} has no active players"
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
            if not clash_updated_player:
                embed_description = (
                    f"{player_title} has been deleted, "
                    f"{inter.author.mention} active is now set to "
                    f"{db_updated_player.player_tag}, "
                    f"could not find player in clash of clans"
                )

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # player deleted
            # active player updated
            # clash player found
            embed_description = (
                f"{player_title} has been deleted, "
                f"{inter.author.mention} active is now set to "
                f"{clash_updated_player.name} "
                f"{clash_updated_player.tag}"
            )

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)

        elif option == "sync":
            # confirm user has been claimed
            db_user_obj = db_responder.read_user(inter.author.id)

            if not db_user_obj:
                db_user_obj = db_responder.claim_user(inter.author.id)

                # user could not be claimed
                if not db_user_obj:
                    embed_description = f"{inter.author.mention} user couldn't be claimed"

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
                f"data for {inter.author.mention} has been properly synced")

        else:
            field_dict_list = [{
                'name': "incorrect option selected",
                'value': "please select a different option"
            }]

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=embed_title,
            description=embed_description,
            field_list=field_dict_list,
            bot_user_name=inter.me.display_name,
            author=inter.author
        )

        await discord_responder.send_embed_list(inter, embed_list)

    @client.sub_command()
    async def clan(
        self,
        inter,
        option: str = discord_utils.command_param_dict['client_clan'],
        clan_tag: str = discord_utils.command_param_dict['tag']
    ):
        """
            *ClashCommander server admin* 
            client clan commands

            Parameters
            ----------
            option (optional): options for client clan returns
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            # user is not guild admin and is not super user
            if (not db_guild_obj.admin_user_id == inter.author.id
                    and not db_user_obj.super_user):
                embed_description = f"{inter.author.mention} is not guild's admin"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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
