import disnake
import coc
from asyncio.tasks import sleep
from disnake.ext import commands
from cogs import (
    misc as misc_cog,
    player as player_cog,
    clan as clan_cog,
    war as war_cog,
    cwl as cwl_cog,
    discord as discord_cog,
    client as client_cog,
    admin as admin_cog
)
from data import ClashDiscord_Client_Data
import responders.ClashResponder as clash_responder
import responders.DiscordResponder as discord_responder
import responders.RazBotDB_Responder as db_responder
from utils import discord_utils

client_data = ClashDiscord_Client_Data.ClashDiscord_Data()

coc_client = coc.login(
    email=discord_responder.get_client_email(),
    password=discord_responder.get_client_password()
)

intents = disnake.Intents.all()

bot = commands.Bot(
    command_prefix=client_data.prefix,
    intents=intents,
    test_guilds=discord_responder.get_client_test_guilds())
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f"RazBot is ready")


bot.add_cog(misc_cog.Misc(bot, coc_client, client_data))
bot.add_cog(player_cog.Player(bot, coc_client, client_data))
bot.add_cog(clan_cog.Clan(bot, coc_client, client_data))
bot.add_cog(war_cog.War(bot, coc_client, client_data))
bot.add_cog(cwl_cog.CWL(bot, coc_client, client_data))
bot.add_cog(discord_cog.Discord(bot, coc_client, client_data))
bot.add_cog(client_cog.Client(bot, coc_client, client_data))
bot.add_cog(admin_cog.Admin(bot, coc_client, client_data))

# super user administration
@bot.slash_command()
async def superuser(inter):
    """
        parent for client super user commands
    """

    pass


# superuser guild
@superuser.sub_command_group()
async def guild(inter):
    """
        group for guild commands
    """

    pass


@guild.sub_command()
async def show(inter):
    """
        *super user*
        "*super user* shows all guilds ClashDiscord is in
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    field_dict_list = []

    for guild in inter.client.guilds:
        field_dict_list.append({
            'name': f"{guild.name}",
            'value': f"{guild.id}"
        })

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"**ClashDiscord Guilds**",
        description=f"Guild Count: {len(inter.client.guilds)}",
        bot_user_name=inter.me.display_name,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )
    await discord_responder.send_embed_list(embed_list, inter)


@guild.sub_command()
async def remove(inter, guild_id: str):
    """
        *super user*
        delete a claimed guild from id

        Parameters
        ----------
        guild_id: id for guild to remove claim
    """

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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
        return

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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    deleted_guild_obj = db_responder.delete_guild(guild_id)

    # guild was deleted properly
    if deleted_guild_obj is None:
        embed_description = f"guild with id {guild_id} was deleted"

    # guild could not be deleted
    else:
        embed_description = f"guild with id {guild_id} could not be deleted"

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@guild.sub_command()
async def leave(inter, guild_id: str):
    """
        *super user*
        force ClashDiscord to leave a claimed guild from id

        Parameters
        ----------
        guild_id: id for guild for ClashDiscord to leave
    """

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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    await guild.leave()
    deleted_guild = disnake.utils.get(inter.bot.guilds, id=guild.id)

    # guild was deleted properly
    if deleted_guild is None:
        embed_description = (f"{inter.me.display_name} left "
                             f"guild {guild.name} id {guild.id}")

    # guild could not be deleted
    else:
        embed_description = (f"{inter.me.display_name} could not leave "
                             f"guild {guild.name} id {guild.id}")

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# superuser user
@superuser.sub_command_group()
async def user(inter):
    """
        group for user commands
    """

    # defer for every superuser user command
    await inter.response.defer(ephemeral=True)


@user.sub_command()
async def adminshow(inter):
    """
        *super user*
        return a list of all admin users
    """

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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
        return

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

        await discord_responder.send_embed_list(embed_list, inter)
        return

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

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{inter.me.display_name} admin users",
        bot_user_name=inter.me.display_name,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@user.sub_command()
async def admintoggle(
    inter,
    user: disnake.User = discord_utils.command_param_dict['user']
):
    """
        *super user*
        toggle a user's admin bool

        Parameters
        ----------
        user: user toggle admin
    """

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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # user was updated and is now an admin
    if updated_user_obj.admin:
        embed_description = f"{user.mention} is now an admin"

    # user was updated and is now not an admin
    else:
        embed_description = f"{user.mention} is no longer an admin"

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@user.sub_command()
async def remove(
    inter,
    user: disnake.User = discord_utils.command_param_dict['user'],
):
    """
        *super user*
        claim a clan's discord role

        Parameters
        ----------
        user: user to remove claim
    """

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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    deleted_user_obj = db_responder.delete_user(user.id)

    # user was deleted properly
    if deleted_user_obj is None:
        embed_description = f"{user.mention} was deleted"

    # user could not be deleted
    else:
        embed_description = f"{user.mention} could not be deleted"

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# superuser player
@superuser.sub_command_group()
async def player(inter):
    """
        group for player commands
    """

    # defer for every superuser player command
    await inter.response.defer(ephemeral=True)


@player.sub_command()
async def claim(
    inter,
    player_tag: str,
    user: disnake.User = discord_utils.command_param_dict['user']
):
    """
        *super user*
        claim a player for the mentioned user

        Parameters
        ----------
        player_tag: player tag link user to
        user: user to link player to
    """

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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # confirm valid player_tag
    player_obj = await clash_responder.get_player(
        player_tag, coc_client)

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

        await discord_responder.send_embed_list(embed_list, inter)
        return

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

        await discord_responder.send_embed_list(embed_list, inter)
        return

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

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@player.sub_command()
async def remove(
    inter,
    player_tag: str,
    user: disnake.User = discord_utils.command_param_dict['user']
):
    """
        *super user*
        remove a player for the mentioned user

        Parameters
        ----------
        player_tag: player tag to remove
        user: user to remove player from
    """

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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # confirm valid player_tag
    player_obj = await clash_responder.get_player(
        player_tag, coc_client)

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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # update was successful
    clash_updated_player_obj = await clash_responder.get_player(
        db_updated_player_obj.player_tag, coc_client)

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

    await discord_responder.send_embed_list(embed_list, inter)


# client events
@bot.event
async def on_member_join(ctx):
    # get uninitiated role from db
    db_role_obj = db_responder.read_rank_role_from_guild_and_clash(
        ctx.guild.id, 'uninitiated')
    if db_role_obj:
        discord_role_obj = disnake.utils.get(
            ctx.guild.roles, id=db_role_obj.discord_role_id)
        if discord_role_obj:
            await ctx.add_roles(discord_role_obj)


@bot.event
async def on_member_remove(member):
    print(f'{member} has left {member.guild.name} id {member.guild.id}')


@bot.event
async def on_reaction_add(reaction, user):
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

    ctx = await bot.get_context(reaction.message)

    db_guild_obj = db_responder.read_guild(ctx.guild.id)
    db_player_obj = db_responder.read_player_active(user.id)

    if db_player_obj:
        player_obj = await clash_responder.get_player(
            db_player_obj.player_tag, coc_client)
    else:
        player_obj = None

    bot_category = discord_responder.help_emoji_to_category(
        reaction.emoji, client_data.bot_categories)

    help_dict = discord_responder.help_switch(
        db_guild_obj, db_player_obj, player_obj, user.id, reaction.emoji,
        bot_category, client_data.bot_categories, ctx.bot.all_slash_commands)
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
        author_display_name=user.display_name,
        author_avatar_url=user.avatar.url
    )

    for embed in embed_list:
        await reaction.message.edit(embed=embed)

    await reaction.message.clear_reactions()
    if bot_category:
        await reaction.message.add_reaction(client_data.back_emoji)
    else:
        for emoji in emoji_list:
            await reaction.message.add_reaction(emoji)


@bot.event
async def on_guild_role_delete(role):
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

"""
@bot.event
async def on_guild_remove(guild):
    # check if removed guild is a claimed guild
    db_guild = db_responder.read_guild(guild.id)

    # guild was claimed
    if db_guild:
        deleted_guild = db_responder.delete_guild(guild.id)
        return
"""


@bot.event
async def on_slash_command_error(inter, exception):
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
                     f"please let {client_data.author} know.\n\n"
                     f"error text: `{exception.original.text}`"))

    elif hasattr(exception.original, "args"):
        await inter.send(
            content=(f"there was an error that I have not accounted for, "
                     f"please let {client_data.author} know.\n\n"
                     f"error text: `{exception.original.args[0]}`"))

    else:
        await inter.send(
            content=(f"there was an error that I have not accounted for, "
                     f"please let {client_data.author} know"))


if __name__ == "__main__":
    bot.run(discord_responder.get_client_token())
