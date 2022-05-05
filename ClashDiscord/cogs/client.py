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

        field_dict_list.extend(discord_responder.client_info(
            inter.client, self.client_data))

        db_guild = db_responder.read_guild(inter.guild.id)

        field_dict_list.extend(discord_responder.client_guild_info(
            inter.guild, db_guild))

        db_players = db_responder.read_player_list(inter.author.id)

        field_dict_list.extend(await discord_responder.client_player_info(
            inter.author, db_players, self.coc_client))

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=f"{inter.me.display_name} client overview",
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
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
                embed_description = f"{inter.author.mention} has already been claimed"

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
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
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
            many of ClashDiscord commands

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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            message = f"{inter.author.mention} has claimed "
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

        elif option == "update":
            if player_tag is None:
                embed_description = (
                    f"player tag not specified, "
                    f"please provide player tag to update a player")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            player_obj = await clash_responder.get_player(player_tag, self.coc_client)

            # if player with tag not found
            if not player_obj:
                embed_description = f"player with tag {player_tag} not found"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_player_obj = db_responder.read_player(
                inter.author.id, player_obj.tag)

            # if requested player is not claimed
            if not db_player_obj:
                embed_description = (
                    f"{inter.author.mention} "
                    f"has not claimed "
                    f"{player_obj.name} {player_obj.tag}"
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

            # if requested player is the active player
            if db_player_obj.active:
                embed_description = (
                    f"{player_obj.name} {player_obj.tag} "
                    f"is already your active player "
                    f"{inter.author.mention}"
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

            else:
                db_player_obj = db_responder.update_player_active(
                    inter.author.id, player_obj.tag)

                embed_description = (
                    f"{player_obj.name} {player_obj.tag} is now "
                    f"your active player {inter.author.mention}"
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

        elif option == "remove":
            if player_tag is None:
                embed_description = (
                    f"player tag not specified, "
                    f"please provide player tag to remove a player")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            player_obj = await clash_responder.get_player(player_tag, self.coc_client)

            # player not found
            if not player_obj:
                embed_description = f"player with tag {player_tag} not found"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            db_player_obj = db_responder.read_player(
                inter.author.id, player_obj.tag)

            # db player not found
            if not db_player_obj:
                embed_description = (f"{player_obj.name} {player_obj.tag} "
                                     f"is not claimed by {inter.author.mention}")

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
                inter.author.id, player_obj.tag)

            # player was not deleted
            if db_del_player_obj:
                embed_description = (
                    f"{player_obj.name} {player_obj.tag} "
                    f"could not be deleted "
                    f"from {inter.author.mention} player list"
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

            # delete link api link
            self.linkapi_client.delete_link(
                player_tag=player_obj.tag)

            db_active_player_obj = db_responder.read_player_active(
                inter.author.id)

            # active player found
            # no need to change the active player
            if db_active_player_obj:
                embed_description = (
                    f"{player_obj.name} {player_obj.tag} "
                    f"has been deleted "
                    f"from {inter.author.mention} player list"
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
                inter.author.id)

            # no additional players claimed
            if len(db_player_obj_list) == 0:
                embed_description = (
                    f"{player_obj.name} {player_obj.tag} "
                    f"has been deleted, "
                    f"{inter.author.mention} has no more claimed players"
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
                inter.author.id, db_player_obj_list[0].player_tag)

            # update not successful
            if not db_updated_player_obj:
                embed_description = (
                    f"{player_obj.name} {player_obj.tag} "
                    f"has been deleted, could not update active player, "
                    f"{inter.author.mention} has no active players"
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
            if not clash_updated_player_obj:
                embed_description = (
                    f"{player_obj.name} {player_obj.tag} "
                    f"has been deleted, "
                    f"{inter.author.mention} active is now set to "
                    f"{db_updated_player_obj.player_tag}, "
                    f"could not find player in clash of clans"
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

            # player deleted
            # active player updated
            # clash player found
            embed_description = (
                f"{player_obj.name} {player_obj.tag} "
                f"has been deleted, "
                f"{inter.author.mention} active is now set to "
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
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(inter, embed_list)

    @client.sub_command()
    async def guild(
        self,
        inter,
        option: str = discord_utils.command_param_dict['client_guild']
    ):
        """
            claim a discord guild and set yourself 
            as the guild admin for ClashDiscord

            Parameters
            ----------
            option (optional): options for client guild returns
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
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
            *ClashDiscord server admin* 
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

        if option == "claim":
            if clan_tag is None:
                embed_description = (
                    f"player tag not specified, "
                    f"please provide player tag to remove a player")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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

            clan_obj = await clash_responder.get_clan(clan_tag, self.coc_client)

            # clan not found
            if not clan_obj:
                embed_description = f"couldn't find clan {clan_tag}"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
                )

                await discord_responder.send_embed_list(inter, embed_list)
                return

            embed_description = f"{clan_obj.name} has been claimed"

        elif option == "show":
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

        elif option == "remove":
            if clan_tag is None:
                embed_description = (
                    f"player tag not specified, "
                    f"please provide player tag to remove a player")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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

            clan_obj = await clash_responder.get_clan(clan_tag, self.coc_client)

            # clan not found
            if not clan_obj:
                embed_description = f"couldn't find clan {clan_tag}"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(inter, embed_list)

    @client.sub_command()
    async def role(
        self,
        inter,
        option: str = discord_utils.command_param_dict['client_role'],
        role: disnake.Role = discord_utils.command_param_dict['client_role_mention']
    ):
        """
            *ClashDiscord server admin* 
            client role commands

            Parameters
            ----------
            option (optional): options for client role returns
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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
                        author_display_name=inter.author.display_name,
                        author_avatar_url=inter.author.avatar.url
                    )

                    await discord_responder.send_embed_list(inter, embed_list)
                    return

                # clan role deleted
                embed_description = f"{role.mention} claim was removed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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
                        author_display_name=inter.author.display_name,
                        author_avatar_url=inter.author.avatar.url
                    )

                    await discord_responder.send_embed_list(inter, embed_list)
                    return

                # rank role deleted
                embed_description = f"{role.mention} claim was removed"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(inter, embed_list)

    @client.sub_command()
    async def clanrole(
        self,
        inter,
        option: str = discord_utils.command_param_dict['client_clan_rank_role'],
        role: disnake.Role = discord_utils.command_param_dict['client_role_mention'],
        clan_tag: str = discord_utils.command_param_dict['tag']
    ):
        """
            *ClashDiscord server admin* 
            client clan role commands

            Parameters
            ----------
            option (optional): options for client clan role returns
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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

            db_clan_obj = db_responder.read_clan(inter.guild.id, clan_obj.tag)

            # clan not claimed by guild
            if not db_clan_obj:
                embed_description = (f"{clan_obj.name} has not been claimed by "
                                     f"{inter.guild.name}")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    description=embed_description,
                    bot_user_name=inter.me.display_name,
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(inter, embed_list)

    @client.sub_command()
    async def rankrole(
        self,
        inter,
        option: str = discord_utils.command_param_dict['client_clan_rank_role'],
        role: disnake.Role = discord_utils.command_param_dict['client_role_mention'],
        rank_name: str = discord_utils.command_param_dict['rank_name']
    ):
        """
            *ClashDiscord server admin* 
            client rank role commands

            Parameters
            ----------
            option (optional): options for client rank role returns
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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
                    author_display_name=inter.author.display_name,
                    author_avatar_url=inter.author.avatar.url
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
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(inter, embed_list)
