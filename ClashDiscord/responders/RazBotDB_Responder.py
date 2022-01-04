import database.RazBotDB_user as user
import database.RazBotDB_player as player
import database.RazBotDB_guild as guild
import database.RazBotDB_clan as clan
import database.RazBotDB_clan_role as clan_role
import database.RazBotDB_rank_role_model as rank_role_model
import database.RazBotDB_rank_role as rank_role
import database.RazBotDB_db as db


# todo reevaluate arg ordering
# todo change discord_id and related variable names
# todo have the objects and none returned by the player, guild, clan, etc files

# todo see if you can instanciate a user directly or if you have to break it up first
# user
def claim_user(discord_user_id):
    """
        claims user and returns user object instance,
            if user has been previously claimed return None

        Args:
            discord_user_id (int): discord id for user

        Returns:
            obj: user object (discord_id, admin, super_user)
    """
    user_data = user.select_user(discord_user_id)
    # check if user_data is None
    # if user data is not None that means user has been claimed
    if user_data:
        # if user_data has values then return None
        return None
    else:
        user_data = user.insert_user(discord_user_id)
        user_discord_id, user_admin, user_super_user = user_data
        user_obj = user.User(user_discord_id, bool(
            user_admin), bool(user_super_user))
        return user_obj


def read_user(discord_user_id):
    """
        finds user in db, if user is not found returns None

        Args:
            discord_user_id (int): discord id for user

        Returns:
            obj: user object (discord_id, admin, super_user)
    """
    user_data = user.select_user(discord_user_id)
    # if user data is found return user
    if user_data:
        user_discord_id, user_admin, user_super_user = user_data
        return user.User(user_discord_id, bool(
            user_admin), bool(user_super_user))
    else:
        return None


def read_user_from_tag(player_tag):
    """
        finds user with given player tag in db,
        if user is not found returns None

        Args:
            player_tag (str): requested player tag

        Returns:
            obj: user object (discord_id, admin, super_user)
    """
    user_data = user.select_user_from_tag(player_tag)
    # if user data is found return user
    if user_data:
        user_discord_id, user_admin, user_super_user = user_data
        return user.User(user_discord_id, bool(
            user_admin), bool(user_super_user))
    else:
        return None


def delete_user(discord_user_id):
    """
        deletes user and returns None if the user 
        could not be found after deletion,
        if user_obj is returned then user couldn't be deleted

        Args:
            discord_user_id (int): discord id for user

        Returns:
            obj: user object (discord_id, admin, super_user)
    """
    user_found = user.delete_user(discord_user_id)
    if user_found:
        # user was found after deletion
        user_discord_id, user_admin, user_super_user = user_found
        user_obj = user.User(user_discord_id, bool(
            user_admin), bool(user_super_user))
        return user_obj
    else:
        # user was not found after deletion
        return None


# player

def claim_player(discord_user_id, player_tag):
    """
        claims player and returns player object instance, 
        if player has been previously claimed return None

        Args:
            discord_user_id (int): discord id for user

        Returns:
            obj: player object (player_tag, active)
    """

    # check if user has another player
    active_player_data = player.select_player_active(discord_user_id)

    if active_player_data:
        # if a user has a active player
        player_data = player.insert_player_alt(discord_user_id, player_tag)
    else:
        # if a player does not have a active player
        player_data = player.insert_player_active(discord_user_id, player_tag)

    if player_data:
        player_tag, active = player_data
        return player.Player(player_tag, bool(active))
    else:
        return None


def read_player_list(discord_user_id):
    """
        returns all players associated with discord id
        and returns empty list if no players are found

        Args:
            discord_user_id (int): discord id for user

        Returns:
            list: list of player object (player_tag, active)
    """
    player_list = list(player.select_player_all(discord_user_id))
    player_obj_list = []
    for item in player_list:
        player_tag, player_active = item
        player_obj_list.append(player.Player(player_tag, bool(player_active)))
    return player_obj_list


def read_player(discord_user_id, player_tag):
    """
        returns player where discord user id and player tag
        and returns None if no player is found

        Args:
            discord_user_id (int): discord id for user
            player_tag (str): user's player tag

        Returns:
            obj: player object (player_tag, active)
    """
    player_data = player.select_player_from_user_tag(
        discord_user_id, player_tag)
    if player_data:
        player_tag, active = player_data
        return player.Player(player_tag, bool(active))
    else:
        return None


def read_player_from_tag(player_tag):
    """
        returns player where player tag
        and returns None if no player is found

        Args:
            player_tag (str): user's player tag

        Returns:
            obj: player object (player_tag, active)
    """
    player_data = player.select_player_from_tag(player_tag)
    if player_data:
        player_tag, active = player_data
        return player.Player(player_tag, bool(active))
    else:
        return None


def read_player_active(discord_user_id):
    """
        returns user's active player
        and returns None if no player is found

        Args:
            discord_user_id (int): discord id for user

        Returns:
            obj: player object (player_tag, active)
    """
    player_data = player.select_player_active(
        discord_user_id)
    if player_data:
        player_tag, active = player_data
        return player.Player(player_tag, bool(active))
    else:
        return None


def update_player_active(discord_user_id, player_tag):
    """
        updates user's active player 
        and returns None if no player is found

        Args:
            discord_user_id (int): discord id for user
            player_tag (str): user's player tag

        Returns:
            obj: player object (player_tag, active)
    """
    player_data = player.update_player_active(discord_user_id, player_tag)
    if player_data:
        player_tag, active = player_data
        return player.Player(player_tag, bool(active))
    else:
        return None


# todo if active player is deleted and another player remains change the active player
def delete_player(discord_user_id, player_tag):
    """
        deletes the requested user's player 
        and returns None if the player could not be found after deletion
        if player_obj is returned then player couldn't be deleted

        Args:
            discord_user_id (int): discord id for user
            player_tag (str): user's player tag

        Returns:
            obj: player object (player_tag, active)
    """
    # delete the player
    player_found = player.delete_player(discord_user_id, player_tag)
    player_data = player.select_player_from_user_tag(
        discord_user_id, player_tag)
    if player_data:
        player_tag, active = player_data
        return player.Player(player_tag, bool(active))
    else:
        return None


# guild
def claim_guild(discord_user_id, discord_guild_id):
    """
        claims guild and returns guild object instance,
        if guild has been previously claimed return None

        Args:
            discord_user_id (int): discord id for user
            discord_guild_id (int): discord id for guild

        Returns:
            obj: guild object (guild_id, admin_user_id,
                bot_channel, active, dev)
    """
    guild_data = guild.select_guild(discord_guild_id)
    # check if guild_data is None
    # if guild data is not None that means guild has been claimed
    if guild_data:
        # if guild_data has values then return None
        return None

    guild_data = guild.insert_guild(discord_guild_id, discord_user_id)

    if guild_data:
        # if guild data is found return guild
        guild_id, admin_user_id, bot_channel, active, dev = guild_data
        guild_obj = guild.Guild(
            guild_id, admin_user_id, bot_channel, bool(active), bool(dev))
        return guild_obj

    else:
        return None


def read_guild(discord_guild_id):
    """
        finds guild in db, if guild is not found returns None

        Args:
            discord_guild_id (int): discord id for guild

        Returns:
            obj: guild object (guild_id, admin_user_id,
                bot_channel, active, dev)
    """
    guild_data = guild.select_guild(discord_guild_id)

    if guild_data:
        # if guild data is found return guild
        guild_id, admin_user_id, bot_channel, active, dev = guild_data
        guild_obj = guild.Guild(
            guild_id, admin_user_id, bot_channel, bool(active), bool(dev))
        return guild_obj

    else:
        return None


def delete_guild(discord_guild_id):
    """
        deletes the requested guild 
        and returns None if the guild could not be found after deletion
        if guild_obj is returned then guild couldn't be deleted

        Args:
            discord_guild_id (int): discord id for guild

        Returns:
            obj: guild object (guild_id, admin_user_id,
                bot_channel, active, dev)
    """
    # delete the guild
    guild_data = guild.delete_guild(discord_guild_id)
    if guild_data:
        guild_id, admin_user_id, bot_channel, active, dev = guild_data
        guild_obj = guild.Guild(
            guild_id, admin_user_id, bot_channel, bool(active), bool(dev))
        return guild_obj
    else:
        return None


# clan
def claim_clan(discord_guild_id, clan_tag):
    """
        claims clan and returns clan object instance,
        if clan has been previously claimed return None

        Args:
            discord_guild_id (int): discord id for guild
            clan_tag (str): tag for clan

        Returns:
            obj: clan object (guild_id, clan_tag)
    """
    clan_data = clan.select_clan(discord_guild_id, clan_tag)
    # check if clan_data is None
    # if clan data is not None that means clan has been claimed
    # only when clan has been claimed by guild trying to claim
    if clan_data:
        # if clan_data has values then return None
        return None

    clan_data = clan.insert_clan(discord_guild_id, clan_tag)

    if clan_data:
        # if clan data is found return clan
        guild_id, clan_tag = clan_data
        clan_obj = clan.Clan(guild_id, clan_tag)
        return clan_obj
    else:
        return None


def read_clan(discord_guild_id, clan_tag):
    """
        finds clan in db, if clan is not found returns None

        Args:
            discord_guild_id (int): discord id for guild
            clan_tag (str): tag for clan

        Returns:
            obj: clan object (guild_id, clan_tag)
    """
    clan_data = clan.select_clan(discord_guild_id, clan_tag)

    if clan_data:
        # if clan data is found return clan
        guild_id, clan_tag = clan_data
        clan_obj = clan.Clan(guild_id, clan_tag)
        return clan_obj

    else:
        return None


def read_clan_list_from_guild(discord_guild_id):
    """
        finds clans in db, if clan is not found returns empty list

        Args:
            discord_guild_id (int): discord id for guild

        Returns:
            obj list: list of clan object (guild_id, clan_tag)
    """

    clan_data_list = list(clan.select_clan_all_from_guild(discord_guild_id))
    clan_obj_list = []
    for item in clan_data_list:
        guild_id, clan_tag = item
        clan_obj_list.append(clan.Clan(guild_id, clan_tag))
    return clan_obj_list


def delete_clan(discord_guild_id, clan_tag):
    """
        deletes the requested guild's clan 
        and returns None if the clan could not be found after deletion
        if clan_obj is returned then clan couldn't be deleted

        Args:
            discord_guild_id (int): discord id for guild
            clan_tag (str): clan's tag

        Returns:
            obj: clan object (guild_id, clan_tag)
    """
    # delete the clan
    clan_data = clan.delete_clan(discord_guild_id, clan_tag)
    if clan_data:
        guild_id, clan_tag = clan_data
        return clan.Clan(guild_id, clan_tag)
    else:
        return None


# clan role
def claim_clan_role(discord_role_id, discord_guild_id, clan_tag):
    """
        claims clan_role and returns clan_role object instance,
        if clan_role has been previously claimed return None

        Args:
            discord_role_id (int): discord id for role
            discord_guild_id (int): discord id for guild
            clan_tag (str): tag for clan

        Returns:
            obj: clan role object 
                (discord_guild_id, discord_role_id, clan_tag)
    """
    clan_role_data = clan_role.select_clan_role(discord_role_id)
    # check if clan_role_data is None
    # if clan role data is not None that means clan role has been claimed
    # only when clan role has been claimed by guild trying to claim role
    if clan_role_data:
        # if clan_role_data has values then return None
        return None

    clan_role_data = clan_role.insert_clan_role(
        discord_role_id, discord_guild_id, clan_tag)

    if clan_role_data:
        # if clan role data is found return clan role object
        discord_guild_id, discord_role_id, clan_tag = clan_role_data
        return clan_role.ClanRole(discord_guild_id, discord_role_id, clan_tag)

    else:
        return None


def read_clan_role(discord_role_id):
    """
        finds clan_role in db, if clan_role is not found returns None

        Args:
            discord_role_id (int): discord id for role

        Returns:
            obj: clan role object 
                (discord_guild_id, discord_role_id, clan_tag)
    """
    clan_role_data = clan_role.select_clan_role(discord_role_id)

    if clan_role_data:
        # if clan role data is found return clan
        discord_guild_id, discord_role_id, clan_tag = clan_role_data
        return clan_role.ClanRole(discord_guild_id, discord_role_id, clan_tag)

    else:
        return None


def read_clan_role_list(discord_role_id_list):
    """
        finds clan_role in db, 
        if no clan_role is not found returns empty list

        Args:
            list
                discord_role_id (int): discord id for role

        Returns:
            list
                obj: clan role object 
                    (discord_guild_id, discord_role_id, clan_tag)
    """
    clan_role_data = clan_role.select_clan_role_from_list(discord_role_id_list)

    clan_role_list = []
    for role in clan_role_data:
        # add each role object to clan_role_list
        discord_guild_id, discord_role_id, clan_tag = role
        clan_role_list.append(clan_role.ClanRole(
            discord_guild_id, discord_role_id, clan_tag))

    return clan_role_list


def read_guild_clan_role(discord_guild_id):
    """
        finds clan_role in db from guild id, 
        if no clan_role is not found returns empty list

        Args:
            discord_guild_id (int): discord id for guild

        Returns:
            list
                obj: clan role object
                    (discord_guild_id, discord_role_id, clan_tag)
    """
    clan_role_data = clan_role.select_clan_role_from_guild(discord_guild_id)

    clan_role_list = []
    for role in clan_role_data:
        # add each role object to clan_role_list
        discord_guild_id, discord_role_id, clan_tag = role
        clan_role_list.append(clan_role.ClanRole(
            discord_guild_id, discord_role_id, clan_tag))

    return clan_role_list


def read_clan_role_from_tag(discord_guild_id, clan_tag):
    """
        finds clan_role in db, if clan_role is not found returns None

        Args:
            discord_guild_id (int): discord id for guild
            clan_tag (str): tag for clan

        Returns:
            obj: clan role object 
                (discord_guild_id, discord_role_id, clan_tag)
    """
    clan_role_data = clan_role.select_clan_role_from_tag(
        discord_guild_id, clan_tag)

    if clan_role_data:
        # if clan role data is found return clan
        discord_guild_id, discord_role_id, clan_tag = clan_role_data
        return clan_role.ClanRole(discord_guild_id, discord_role_id, clan_tag)

    else:
        return None


def delete_clan_role(discord_role_id):
    """
        deletes the requested clan_role 
        and returns None if the clan_role could not be found after deletion
        if clan_role_obj is returned then clan_role couldn't be deleted

        Args:
            discord_role_id (int): discord id for role

        Returns:
            obj: clan role object 
                (discord_guild_id, discord_role_id, clan_tag)
    """
    # delete the clan role
    clan_role_data = clan_role.delete_clan_role(discord_role_id)
    if clan_role_data:
        discord_guild_id, discord_role_id, clan_tag = clan_role_data
        return clan_role.ClanRole(discord_guild_id, discord_role_id, clan_tag)
    else:
        return None


# rank role model
def read_rank_role_model(rank_model_name):
    """
        finds rank_role_model in db, if rank_role_model is not found 
        returns None

        Args:
            discord_role_id (int): discord id for role

        Returns:
            obj: rank role model object (model_name, clash_name)
    """
    rank_role_model_data = (
        rank_role_model.select_rank_role_model_name(rank_model_name))

    if rank_role_model_data:
        # if rank role model data is found return rank role model
        model_name, clash_name = rank_role_model_data
        rank_role_model_obj = rank_role_model.RankRoleModel(
            model_name, clash_name)
        return rank_role_model_obj

    else:
        return None


# rank role
def claim_rank_role(discord_role_id, discord_guild_id, rank_model_name):
    """
        claims rank_role and returns rank_role object instance,
        if rank_role has been previously claimed return None

        Args:
            discord_role_id (int): discord id for role
            discord_guild_id (int): discord id for guild
            rank_model_name (str): name of rank role model name

        Returns:
            obj: rank role object 
                (discord_guild_id, discord_role_id, model_name, clash_name)
    """
    rank_role_data = rank_role.select_rank_role(discord_role_id)
    # check if rank_role_data is None
    # if rank role data is not None that means rank role has been claimed
    # only when rank role has been claimed by guild trying to claim role
    if rank_role_data:
        # if rank_role_data has values then return None
        return None

    rank_role_data = rank_role.insert_rank_role(
        discord_role_id, discord_guild_id, rank_model_name)

    if rank_role_data:
        # if rank role data is found return rank role object
        discord_guild_id, discord_role_id, model_name, clash_name = rank_role_data
        return rank_role.RankRole(
            discord_guild_id, discord_role_id, model_name, clash_name)
    else:
        return None


def read_rank_role(discord_role_id):
    """
        finds rank_role in db, if rank_role is not found returns None

        Args:
            discord_role_id (int): discord id for role

        Returns:
            obj: rank role object 
                (discord_guild_id, discord_role_id, model_name, clash_name)
    """
    rank_role_data = rank_role.select_rank_role(discord_role_id)

    if rank_role_data:
        # if rank role data is found return rank role
        (discord_guild_role, discord_role_id,
         model_name, clash_name) = rank_role_data
        rank_role_obj = rank_role.RankRole(
            discord_guild_role, discord_role_id, model_name, clash_name)
        return rank_role_obj

    else:
        return None


def read_guild_rank_role(discord_guild_id):
    """
        finds rank_role in db, 
        if no rank_role is not found returns empty list

        Args:
            discord_guild_id (int): discord id for guild

        Returns:
            list
                obj: rank role object 
                    (discord_guild_id, discord_role_id, 
                    model_name, clash_name)
    """
    rank_role_data = rank_role.select_guild_rank_role(discord_guild_id)

    rank_role_list = []
    for role in rank_role_data:
        # add each role object to rank_role_list
        (discord_guild_role, discord_role_id,
         model_name, clash_name) = role
        rank_role_list.append(rank_role.RankRole(
            discord_guild_role, discord_role_id, model_name, clash_name))

    return rank_role_list


def read_rank_role_list(discord_role_id):
    """
        finds rank_role in db, 
        if no rank_role is not found returns empty list

        Args:
            discord_role_id (int): discord id for role

        Returns:
            list
                obj: rank role object 
                    (discord_guild_id, discord_role_id, 
                    model_name, clash_name)
    """
    rank_role_data = rank_role.select_rank_role_from_list(discord_role_id)

    rank_role_list = []
    for role in rank_role_data:
        # add each role object to rank_role_list
        (discord_guild_role, discord_role_id,
         model_name, clash_name) = role
        rank_role_list.append(rank_role.RankRole(
            discord_guild_role, discord_role_id, model_name, clash_name))

    return rank_role_list


def read_rank_role_from_guild_and_clash(discord_guild_id, clash_name):
    """
        finds rank_role in db, if rank_role is not found returns None

        Args:
            discord_role_id (int): discord id for role
            clash_name (str): db rank role clash name

        Returns:
            obj: rank role object 
                (discord_guild_id, discord_role_id, model_name, clash_name)
    """
    rank_role_data = rank_role.select_rank_role_name_from_guild_and_clash(
        discord_guild_id, clash_name)

    if rank_role_data:
        # if rank role data is found return rank role
        discord_guild_role, discord_role_id, model_name, clash_name = rank_role_data
        rank_role_obj = rank_role.RankRole(
            discord_guild_role, discord_role_id, model_name, clash_name)
        return rank_role_obj

    else:
        return None


def delete_rank_role(discord_role_id):
    """
        deletes the requested rank_role 
        and returns None if the rank_role could not be found after deletion
        if rank_role_obj is returned then rank_role couldn't be deleted

        Args:
            discord_role_id (int): discord id for role

        Returns:
            obj: rank role object 
                (discord_guild_id, discord_role_id, model_name, clash_name)
    """
    # delete the rank role
    rank_role_data = rank_role.delete_rank_role(discord_role_id)
    if rank_role_data:
        discord_guild_role, discord_role_id, model_name, clash_name = rank_role_data
        return rank_role.RankRole(discord_guild_role, discord_role_id, model_name, clash_name)
    else:
        return None
