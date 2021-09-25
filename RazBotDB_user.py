import RazBotDB_Presets as preset
import RazBotDB_user as user
import RazBotDB_player as player
import RazBotDB_guild as guild
import RazBotDB_clan as clan
import RazBotDB_clan_role as clan_role
import RazBotDB_rank_role_model as rank_role_model
import RazBotDB_rank_role as rank_role


class User(object):
    """
        User: object for db user table objects

            Instance Attributes
                discord_id (int): user id in discord
                admin (bool): TF of admin status
                super_user (bool): TF of super_user status
    """

    def __init__(self, discord_id, admin, super_user):
        self.discord_id = discord_id
        self.admin = admin
        self.super_user = super_user


def insert_raz_super_user(discord_user_id):
    # set up query
    query = (
        f"INSERT into user (discord_id, admin, super_user) "
        f"VALUES ({discord_user_id}, TRUE, TRUE);"
    )

    # execute insert query
    preset.insert(query)
    # select and return user
    data = select_user_raz()
    return data


def insert_user(discord_id):
    """
        Takes in discord_id, creates user in user db,
        and returns user db ID and discord_id

        Args:
            discord_id (int): id received from discord

        Returns:
            ID: user's ID in db
            discord_id: user's discord id in db
    """
    # set up query
    query = (
        f"INSERT into user (discord_id) VALUES ({discord_id});"
    )

    # execute insert query
    preset.insert(query)
    # select and return user
    data = select_user(discord_id)
    return data


def insert_user_admin(discord_id):
    """
        Takes in discord_id, creates admin user in user db,
        and returns user db ID and discord_id

        Args:
            discord_id (int): id received from discord

        Returns:
            ID: user's ID in db
            discord_id: user's discord id in db
    """
    # set up query
    query = (
        f"INSERT into user (discord_id, admin) VALUES ({discord_id}, TRUE)"
    )

    # execute insert query
    preset.insert(query)
    # select and return user
    data = select_user(discord_id)
    return data


def select_user_raz():
    # set up the query
    query = (
        "SELECT id, discord_id FROM user WHERE discord_id=250312821647081472"
    )

    # execute and return query
    data = preset.select(query)
    return data


def select_user(discord_id):
    """
        Takes in the discord_id and returns discord_id, admin, and super_user

        Args:
            discord_id (int): id received from discord

        Returns:
            discord_id: user's discord id in db
            admin: 1 or 0 (T or F) if user is admin
            super_user: 1 or 0 (T or F) if user is super user
    """
    # set up the query
    query = (
        f"SELECT discord_id, admin, super_user FROM user WHERE discord_id={discord_id}"
    )

    # execute and return query
    data = preset.select(query)
    return data


def select_user_list(discord_id_list):
    """
        Takes in list of discord_id and returns
        discord_id, admin, and super_user of all users

        Args:
            discord_id_list (list(int)): list of discord_id

        Returns:
            discord_id: user's discord id in db
            admin: 1 or 0 (T or F) if user is admin
            super_user: 1 or 0 (T or F) if user is super user
    """
    # set up the query
    query = (
        f"SELECT discord_id, admin, super_user FROM user "
        f"WHERE "
    )

    for discord_id in discord_id_list:
        query += f"discord_id = {discord_id} OR "

    # cuts the last four characters from the string ' OR '
    query = query[:-4]
    query += ';'

    # execute and return query
    data = preset.select_list(query)
    return data


def select_user_all():
    """
        user db discord_id, admin, and super_user of all users

        Returns:
            discord_id: user's discord id in db
            admin: 1 or 0 (T or F) if user is admin
            super_user: 1 or 0 (T or F) if user is super user
    """
    # set up the query
    query = (
        f"SELECT discord_id, admin, super_user FROM user"
    )

    # execute and return query
    data = preset.select_list(query)
    return data


def update_user_admin_toggle(discord_id):
    """
        takes in the discord_id and toggles the db admin status,
        returns None if not found

        Args:
            discord_id (int): id received from discord

        Returns:
            discord_id: user's discord id in db
            admin: 1 or 0 (T or F) if user is admin
            super_user: 1 or 0 (T or F) if user is super user
    """
    # get user admin data
    data = select_user(discord_id)
    if data:
        # separate tuple
        discord_id, admin, super_user = data

        # set up the query toggling the admin status
        query = (
            f"UPDATE user "
            f"SET admin = {not bool(admin)} "
            f"WHERE discord_id = {discord_id};"
        )

        # execute update query
        preset.update(query)
        # select and return user
        data = select_user(discord_id)
        return data

    else:
        return None


def delete_user(discord_id):
    """
        Takes in the discord_id and deletes associated user,
        returns None to prove user was deleted.

        Args:
            discord_id (int): id received from discord

        Returns:
            ID: user's ID in db
            discord_id: user's discord id in db
    """
    # set up the query
    query = (
        f"DELETE FROM user WHERE discord_id={discord_id}"
    )

    # execute delete query
    preset.delete(query)
    # search user to show it was deleted
    data = select_user(discord_id)
    return data


# todo some sort of confirmation
def create_user_table():
    # set up the query
    query = (
        "CREATE TABLE user ( "
        "id int not null auto_increment, "
        "discord_id bigint unique not null, "
        "admin boolean not null default false, "
        "super_user boolean not null default false, "
        "primary key (id)"
        ");"
    )

    # execute create query
    preset.create(query)


def drop_user_table():
    # set up the query
    query = ("DROP TABLE user")

    # execute drop query
    preset.drop(query)
