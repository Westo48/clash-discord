import disnake
from disnake.ext import commands
from responders import (
    DiscordResponder as discord_responder,
    RazBotDB_Responder as db_responder
)
from responders.ClientResponder import (
    client_user_profile,
    client_player_list
)
from utils import discord_utils


class User(commands.Cog):
    def __init__(self, bot, coc_client, client_data):
        self.bot = bot
        self.coc_client = coc_client
        self.client_data = client_data

    @commands.slash_command()
    async def user(self, inter):
        """
            parent for user commands
        """

        # defer for every command
        await inter.response.defer()

    @user.sub_command()
    async def profile(
        self,
        inter,
        user: disnake.User = discord_utils.command_param_dict['user']
    ):
        """
            show the user's clash profile of linked accounts

            Parameters
            ----------
            user (optional): user to run command for
        """

        # setting user to author if not specified
        if user is None:
            user = inter.author

        # initializing embed default values
        embed_title = None
        embed_description = None
        field_dict_list = []

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

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=embed_title,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author=inter.author)

        await discord_responder.send_embed_list(inter, embed_list)

    @user.sub_command()
    async def player_list(
        self,
        inter,
        user: disnake.User = discord_utils.command_param_dict['user']
    ):
        """
            show the list of players a user has

            Parameters
            ----------
            user (optional): user to run command for
        """

        # setting user to author if not specified
        if user is None:
            user = inter.author

        # initializing embed default values
        embed_title = None
        embed_description = None
        field_dict_list = []

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
