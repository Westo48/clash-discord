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


class Help(commands.Cog):
    def __init__(self, bot, coc_client, client_data):
        self.bot = bot
        self.coc_client = coc_client
        self.client_data = client_data

    @commands.slash_command()
    async def help(
            self,
            inter: ApplicationCommandInteraction):
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
            author=inter.author
        )

        await discord_responder.send_embed_list(inter, embed_list)

        original_message = await inter.original_message()

        for emoji in emoji_list:
            await original_message.add_reaction(emoji)
