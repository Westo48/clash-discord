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
    discord as discord_cog
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


# CLIENT

@bot.slash_command()
async def client(inter):
    """
        parent for client commands
    """

    # defer for every command
    await inter.response.defer()


# client info
@client.sub_command_group()
async def info(inter):
    """
        group for client info commands
    """

    pass


@info.sub_command()
async def overview(inter):
    """
        relevant overview for the client
    """

    field_dict_list = []

    field_dict_list.extend(discord_responder.client_info(
        inter.client, client_data))

    db_guild = db_responder.read_guild(inter.guild.id)

    field_dict_list.extend(discord_responder.client_guild_info(
        inter.guild, db_guild))

    db_players = db_responder.read_player_list(inter.author.id)

    field_dict_list.extend(await discord_responder.client_player_info(
        inter.author, db_players, coc_client))

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{inter.me.display_name} client overview",
        bot_user_name=inter.me.display_name,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# client user
@client.sub_command_group()
async def user(inter):
    """
        group for client user commands
    """

    pass


@user.sub_command()
async def claim(inter):
    """
        claim your discord user
    """

    user = db_responder.claim_user(inter.author.id)

    # user wasn't claimed and now is
    if user:
        embed_description = f"{inter.author.mention} is now claimed"

    # user was already claimed
    else:
        embed_description = f"{inter.author.mention} has already been claimed"

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# client player
@client.sub_command_group()
async def player(inter):
    """
        group for client player commands
    """

    pass


@player.sub_command()
async def claim(
    inter,
    player_tag: str = discord_utils.command_param_dict['required_tag'],
    api_key: str = discord_utils.command_param_dict['api_key']
):
    """
        verify and claim a player,
        a player must be claimed to view and run
        many of ClashDiscord commands

        Parameters
        ----------
        player_tag: player tag to search
        api_key: api key provided from in game
    """

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
    db_user_obj = db_responder.read_user(inter.author.id)
    if not db_user_obj:
        # user has not been claimed
        db_user_obj = db_responder.claim_user(inter.author.id)
        if not db_user_obj:
            # user could not be claimed
            embed_description = f"{inter.author.mention} user couldn't be claimed"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(embed_list, inter)
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

    # authenticate player api key
    player_verified = await clash_responder.verify_token(
        api_key, player_obj.tag, coc_client)
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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # user claimed
    # player is valid
    # player hasn't been claimed
    # player is authenticated
    db_player_obj = db_responder.claim_player(
        inter.author.id, player_obj.tag)

    # succesfully claimed
    if db_player_obj:
        embed_description = (f"{player_obj.name} {player_obj.tag} "
                             f"is now claimed by {inter.author.mention}")
    # failed to claim
    else:
        embed_description = (f"Could not claim {player_obj.name} "
                             f"{player_obj.tag} for {inter.author.mention}")

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@player.sub_command()
async def show(inter):
    """
        shows players claimed by your discord user
    """

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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    message = f"{inter.author.mention} has claimed "
    for db_player_obj in db_player_obj_list:
        player_obj = await clash_responder.get_player(
            db_player_obj.player_tag, coc_client)
        if db_player_obj.active:
            message += f"{player_obj.name} {player_obj.tag} (active), "
        else:
            message += f"{player_obj.name} {player_obj.tag}, "
    # cuts the last two characters from the string ', '
    message = message[:-2]
    await inter.edit_original_message(content=message)


@player.sub_command()
async def update(
    inter,
    player_tag: str = discord_utils.command_param_dict['required_tag']
):
    """
        updates author's active player

        Parameters
        ----------
        player_tag: player tag to set as active
    """

    player_obj = await clash_responder.get_player(player_tag, coc_client)

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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_player_obj = db_responder.read_player(inter.author.id, player_obj.tag)

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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
        return


@player.sub_command()
async def remove(
    inter,
    player_tag: str = discord_utils.command_param_dict['required_tag']
):
    """
        updates author's active player

        Parameters
        ----------
        player_tag: player tag to remove
    """

    player_obj = await clash_responder.get_player(player_tag, coc_client)

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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_player_obj = db_responder.read_player(inter.author.id, player_obj.tag)

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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_active_player_obj = db_responder.read_player_active(inter.author.id)

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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # update was successful
    clash_updated_player_obj = await clash_responder.get_player(
        db_updated_player_obj.player_tag, coc_client)

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

        await discord_responder.send_embed_list(embed_list, inter)
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

    await discord_responder.send_embed_list(embed_list, inter)


# client guild
@client.sub_command_group()
async def guild(inter):
    """
        group for client guild commands
    """

    pass


@guild.sub_command()
async def claim(inter):
    """
        claim a discord guild and set yourself
        as the guild admin for ClashDiscord
    """

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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    field_dict_list = [{
        "name": f"{inter.guild.name} is now claimed",
        "value": f"admin user {inter.author.mention}"
    }]

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        bot_user_name=inter.me.display_name,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# client clan
@client.sub_command_group()
async def clan(inter):
    """
        group for client clan commands
    """

    pass


@clan.sub_command()
async def claim(
    inter,
    clan_tag: str = discord_utils.command_param_dict['required_tag']
):
    """
        *admin*
        claim the requested clan

        Parameters
        ----------
        clan_tag: clan tag to claim
    """

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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    clan_obj = await clash_responder.get_clan(clan_tag, coc_client)

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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    claimed_clan_obj = db_responder.read_clan(inter.guild.id, clan_obj.tag)

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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    embed_description = f"{clan_obj.name} has been claimed"

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@clan.sub_command()
async def show(inter):
    """
        *admin*
        clans claimed by a discord guild

        Parameters
        ----------
        clan_tag: clan tag to claim
    """

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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_clan_obj_list = db_responder.read_clan_list_from_guild(inter.guild.id)

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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    embed_title = f"{inter.guild.name} claimed clans"

    field_dict_list = []
    for db_clan in db_clan_obj_list:
        clan = await clash_responder.get_clan(
            db_clan.clan_tag, coc_client)

        field_dict_list.append({
            "name": clan.name,
            "value": clan.tag
        })

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=embed_title,
        bot_user_name=inter.me.display_name,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@clan.sub_command()
async def remove(
    inter,
    clan_tag: str = discord_utils.command_param_dict['required_tag']
):
    """
        *admin*
        deletes the requested clan claim

        Parameters
        ----------
        clan_tag: clan tag to delete from client
    """

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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    clan_obj = await clash_responder.get_clan(clan_tag, coc_client)

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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    db_clan_deletion = db_responder.delete_clan(inter.guild.id, clan_obj.tag)
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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    embed_description = (f"{clan_obj.name} has been deleted "
                         f"from {inter.guild.name}")

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# client roles
@client.sub_command_group()
async def role(inter):
    """
        group for client role commands
    """

    pass


@role.sub_command()
async def show(inter):
    """
        *admin*
        shows all roles claimed by a discord guild
    """

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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    field_dict_list = []

    db_clan_role_list = db_responder.read_guild_clan_role(inter.guild.id)

    db_rank_role_list = db_responder.read_guild_rank_role(inter.guild.id)

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
                db_role.clan_tag, coc_client)

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

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=f"{inter.guild.name} claimed roles",
        bot_user_name=inter.me.display_name,
        field_list=field_dict_list,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@role.sub_command()
async def remove(
    inter,
    role: str = discord_utils.command_param_dict['role']
):
    """
        *admin*
        remove the claimed discord role,
        the role will not be deleted from discord

        Parameters
        ----------
        role: role object to remove claim
    """

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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

            await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

            await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    embed_description = f"{role.mention} is not claimed"

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# client clan role
@client.sub_command_group()
async def clanrole(inter):
    """
        group for client clan role commands
    """

    pass


@clanrole.sub_command()
async def claim(
    inter,
    role: str = discord_utils.command_param_dict['role'],
    clan_tag: str = discord_utils.command_param_dict['required_tag']
):
    """
        *admin*
        claim a clan's discord role

        Parameters
        ----------
        role: role object to claim and link to claimed clan
        clan_tag: clan tag to link to role
    """

    clan_obj = await clash_responder.get_clan(clan_tag, coc_client)

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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
        return

    embed_description = f"{role.mention} has been claimed for clan {clan_obj.tag}"

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# client rank role
@client.sub_command_group()
async def rankrole(inter):
    """
        group for client rank role commands
    """

    pass


@rankrole.sub_command()
async def claim(
    inter,
    role: str = discord_utils.command_param_dict['role'],
    rank_name: str = discord_utils.command_param_dict['rank_name']
):
    """
        *admin*
        claim a rank's discord role

        Parameters
        ----------
        role: role object to claim and link to client rank
        rank_name: requested rank to link to role
    """

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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

        await discord_responder.send_embed_list(embed_list, inter)
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

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


# admin
@bot.slash_command()
async def admin(inter):
    """
        parent for client admin commands
    """

    # defer for every command
    await inter.response.defer()


# admin player
@admin.sub_command_group()
async def player(inter):
    """
        group for player commands
    """

    pass


@player.sub_command()
async def claim(
    inter,
    player_tag: str,
    user: disnake.User = discord_utils.command_param_dict['user']
):
    """
        *admin*
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

    # author is not admin
    if not db_author_obj.admin:
        embed_description = f"{inter.author.mention} is not admin"

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
            embed_description = f"{user.mention} user couldn't be claimed"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(embed_list, inter)
            return

    # admin is not a super user and author is not the user
    if (not db_author_obj.super_user
            and db_author_obj.discord_id != db_user_obj.discord_id):
        # admin users are not allowed to update admins or super users
        if db_user_obj.admin or db_user_obj.super_user:
            embed_description = (f"admins are not allowed to update "
                                 f"admins or super users")

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

    # succesfully claimed
    if db_player_obj:
        embed_description = (f"{player_obj.name} {player_obj.tag} "
                             f"is now claimed by {user.mention}")
    # failed to claim
    else:
        embed_description = (f"Could not claim {player_obj.name} "
                             f"{player_obj.tag} for {user.mention}")

    embed_list = discord_responder.embed_message(
        icon_url=inter.bot.user.avatar.url,
        description=embed_description,
        bot_user_name=inter.me.display_name,
        author_display_name=inter.author.display_name,
        author_avatar_url=inter.author.avatar.url
    )

    await discord_responder.send_embed_list(embed_list, inter)


@player.sub_command()
async def show(
    inter,
    user: disnake.User = discord_utils.command_param_dict['user']
):
    """
        *admin*
        shows players claimed by the mentioned user

        Parameters
        ----------
        user: user to show player tags
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

    # author is not admin
    if not db_author_obj.admin:
        embed_description = f"{inter.author.mention} is not admin"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # confirm db user exists
    db_user_obj = db_responder.read_user(user.id)
    if db_user_obj is None:
        embed_description = f"{user.mention} has not been claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # admin is not a super user and author is not the user
    if (not db_author_obj.super_user
            and db_author_obj.discord_id != db_user_obj.discord_id):
        # admin users are not allowed to update admins or super users
        if db_user_obj.admin or db_user_obj.super_user:
            embed_description = (f"admins are not allowed to update "
                                 f"admins or super users")

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author_display_name=inter.author.display_name,
                author_avatar_url=inter.author.avatar.url
            )

            await discord_responder.send_embed_list(embed_list, inter)
            return

    db_player_obj_list = db_responder.read_player_list(user.id)

    # user has no claimed players
    if len(db_player_obj_list) == 0:
        embed_description = (f"{user.mention} does not have any "
                             f"claimed players")

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    message = f"{user.mention} has claimed "
    for db_player_obj in db_player_obj_list:
        player_obj = await clash_responder.get_player(
            db_player_obj.player_tag, coc_client)
        if db_player_obj.active:
            message += f"{player_obj.name} {player_obj.tag} (active), "
        else:
            message += f"{player_obj.name} {player_obj.tag}, "
    # cuts the last two characters from the string ', '
    message = message[:-2]
    await inter.edit_original_message(content=message)


@player.sub_command()
async def remove(
    inter,
    player_tag: str,
    user: disnake.User = discord_utils.command_param_dict['user']
):
    """
        *admin*
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

    # author is not admin
    if not db_author_obj.admin:
        embed_description = f"{inter.author.mention} is not admin"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # confirm db user exists
    db_user_obj = db_responder.read_user(user.id)
    if db_user_obj is None:
        embed_description = f"{user.mention} has not been claimed"

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            description=embed_description,
            bot_user_name=inter.me.display_name,
            author_display_name=inter.author.display_name,
            author_avatar_url=inter.author.avatar.url
        )

        await discord_responder.send_embed_list(embed_list, inter)
        return

    # admin is not a super user and author is not the user
    if (not db_author_obj.super_user
            and db_author_obj.discord_id != db_user_obj.discord_id):
        # admin users are not allowed to update admins or super users
        if db_user_obj.admin or db_user_obj.super_user:
            embed_description = (f"admins are not allowed to update "
                                 f"admins or super users")

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


@bot.event
async def on_guild_remove(guild):
    # check if removed guild is a claimed guild
    db_guild = db_responder.read_guild(guild.id)

    # guild was claimed
    if db_guild:
        deleted_guild = db_responder.delete_guild(guild.id)
        return


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
