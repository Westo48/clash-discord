import disnake
from disnake.ext import commands
from linkAPI.client import LinkApiClient
from linkAPI.errors import ConflictError
from responders import (
    DiscordResponder as discord_responder,
    ClashResponder as clash_responder,
    RazBotDB_Responder as db_responder,
    linkApiResponder as link_responder
)
from utils import discord_utils


class Events(commands.Cog):
    def __init__(self, bot, coc_client, client_data, linkapi_client: LinkApiClient):
        self.bot = bot
        self.coc_client = coc_client
        self.client_data = client_data
        self.linkapi_client = linkapi_client

    # client events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"RazBot is ready")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # updating roles for possible uninitiated role
        # get uninitiated role from db
        db_role_obj = db_responder.read_rank_role_from_guild_and_clash(
            member.guild.id, 'uninitiated')
        if db_role_obj:
            discord_role_obj = disnake.utils.get(
                member.guild.roles, id=db_role_obj.discord_role_id)
            if discord_role_obj:
                await member.add_roles(discord_role_obj)

        # sync player data

        # confirm user has been claimed
        db_user_obj = db_responder.read_user(member.id)

        if not db_user_obj:
            db_user_obj = db_responder.claim_user(member.id)

            # user could not be claimed
            if not db_user_obj:
                print_info = f"{member.mention} user couldn't be claimed"

                print(print_info)

        try:
            link_responder.sync_link(
                linkapi_client=self.linkapi_client,
                discord_user_id=db_user_obj.discord_id
            )
        except ConflictError as arg:
            print(arg)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} has left {member.guild.name} id {member.guild.id}')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # if the reactor is a bot
        if user.bot:
            return

        # if the author of the reacted message is not clash discord
        if (reaction.message.author.id !=
                discord_responder.get_client_discord_id()):
            return

        # if there are no embedded messages
        if len(reaction.message.embeds) == 0:
            return

        # if clash discord embedded message is not a help message
        if 'help' not in reaction.message.embeds[0].title:
            return

        ctx = await self.bot.get_context(reaction.message)

        db_guild_obj = db_responder.read_guild(ctx.guild.id)
        db_player_obj = db_responder.read_player_active(user.id)

        if db_player_obj:
            player_obj = await clash_responder.get_player(
                db_player_obj.player_tag, self.coc_client)
        else:
            player_obj = None

        bot_category = discord_responder.help_emoji_to_category(
            reaction.emoji, self.client_data.bot_categories)

        help_dict = discord_responder.help_switch(
            db_guild_obj, db_player_obj, player_obj, user.id, reaction.emoji,
            bot_category, self.client_data.bot_categories, ctx.bot.all_slash_commands)
        field_dict_list = help_dict['field_dict_list']
        emoji_list = help_dict['emoji_list']

        if bot_category:
            embed_title = f"{ctx.bot.user.name} {bot_category.name} help"
        else:
            embed_title = f"{ctx.bot.user.name} help menu"

        embed_list = discord_responder.embed_message(
            icon_url=ctx.bot.user.avatar.url,
            title=embed_title,
            bot_user_name=ctx.bot.user.name,
            field_list=field_dict_list,
            author=user
        )

        for embed in embed_list:
            await reaction.message.edit(embed=embed)

        await reaction.message.clear_reactions()
        if bot_category:
            await reaction.message.add_reaction(self.client_data.back_emoji)
        else:
            for emoji in emoji_list:
                await reaction.message.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        # check if deleted role is a claimed role

        # clan role
        clan_role = db_responder.read_clan_role(role.id)
        # clan role found
        if clan_role:
            deleted_role = db_responder.delete_clan_role(role.id)
            return

        # rank role
        rank_role = db_responder.read_rank_role(role.id)
        # rank role found
        if rank_role:
            deleted_role = db_responder.delete_rank_role(role.id)
            return

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        # check if removed guild is a claimed guild
        db_guild = db_responder.read_guild(guild.id)

        # guild was claimed
        if db_guild:
            deleted_guild = db_responder.delete_guild(guild.id)
            return

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, exception):
        if isinstance(exception, commands.CommandNotFound):
            await inter.send(
                content=f"command '{inter.invoked_with}' could not be found")

        elif isinstance(exception, commands.MissingRequiredArgument):
            if hasattr(inter, "invoked_with"):
                await inter.send(
                    content=(f"command '{inter.invoked_with}' "
                             f"requires more information"))

            else:
                await inter.send(
                    content=f"command requires more information")

        elif hasattr(exception.original, "text"):
            await inter.send(
                content=(f"there was an error that I have not accounted for, "
                         f"please let {self.client_data.author} know.\n\n"
                         f"error text: `{exception.original.text}`"))

        elif hasattr(exception.original, "args"):
            await inter.send(
                content=(f"there was an error that I have not accounted for, "
                         f"please let {self.client_data.author} know.\n\n"
                         f"error text: `{exception.original.args[0]}`"))

        else:
            await inter.send(
                content=(f"there was an error that I have not accounted for, "
                         f"please let {self.client_data.author} know"))
