import database.RazBotDB_Presets as preset


# guild
class Guild(object):
    """
        Guild: object for db guild table objects

            Instance Attributes
                guild_id (int): guild id in discord
                admin_user_id (int): discord id of guild's admin user
                bot_chanel (int): bot channel id in discord (nullable)
                active (bool): TF of active status
                dev (bool): TF of dev status
    """

    def __init__(self, guild_id, admin_user_id, bot_channel, active, dev):
        self.guild_id = guild_id
        self.admin_user_id = admin_user_id
        self.bot_channel = bot_channel
        self.active = active
        self.dev = dev


# CREATE
def insert_guild(guild_id, admin_user_id):
    """
        Takes in the discord guild_id, discord admin_user_id
        inserts guild db guild_id, admin_user_id, bot_channel, active, dev
        and if no guild is found returns None

        Args:
            guild_id (int): guild id received from discord
            admin_user_id (int): admin_user_id received from discord

        Returns:
            guild_id: discord guild's id
            admin_user_id: db id of admin user
            bot_channel: nullable channel for bot responses
            active: bool of active channel
            dev: bool of dev guild
    """
    # set up the query
    query = (
        f"INSERT into guild (guild_id, admin_user_id) "
        f"VALUES ({guild_id}, ("
        f"SELECT ID FROM user WHERE discord_id={admin_user_id}));"
    )

    # execute insert query
    preset.insert(query)
    # select and return guild
    data = select_guild(guild_id)
    return data


# todo add docstring
def insert_guild_dev(guild_id, admin_user_id):
    # set up the query
    query = (
        f"INSERT into guild (guild_id, admin_user_id, dev) "
        f"VALUES ({guild_id}, {admin_user_id}, TRUE);"
    )

    # execute insert query
    preset.insert(query)
    # select and return guild
    data = select_guild(guild_id)
    return data


def select_guild(guild_id):
    """
        Takes in the discord guild_id and
        returns guild db guild_id, admin_user_id, bot_channel, active, dev
        and if no guild is found returns None

        Args:
            discord_id (int): id received from discord

        Returns:
            guild_id: discord guild's id
            admin_user_id: discord id of admin user
            bot_channel: nullable channel for bot responses
            active: bool of active channel
            dev: bool of dev guild
    """
    # find the guild based on guild_id
    query = (
        f"SELECT guild.guild_id, user.discord_id as admin_user_id, "
        f"guild.bot_channel, active, dev "
        f"FROM guild "
        f"INNER JOIN user ON guild.admin_user_id = user.id "
        f"WHERE guild.guild_id = {guild_id};"
    )

    # execute and return query
    data = preset.select(query)
    return data


def delete_guild(guild_id):
    """
        Takes in the discord guild_id, deletes the db guild and
        returns null to confirm it has been deleted

        Args:
            guild_id (int): id received from discord guild

        Returns:
            null: null confirms it has been deleted
    """
    # set up the query
    query = (
        f"DELETE FROM guild "
        f"WHERE guild_id = {guild_id};"
    )

    # execute delete query
    preset.delete(query)
    # confirm deletion from null response
    data = select_guild(guild_id)
    return data


def select_guild_count():
    """
        returns guild count

        Returns:
            guild_count: int of guild count
    """
    # set up the query
    query = (
        f"SELECT COUNT(id) as guild_count FROM guild;"
    )

    # execute and return query
    data = preset.select(query)
    return data


# todo docstring
# todo some sort of confirmation
def create_guild_table():
    # set up the query
    query = (
        "CREATE TABLE guild( "
        "id int not null auto_increment, "
        "guild_id bigint unique not null, "
        "bot_channel int unique, "
        "admin_user_id int not null, "
        "active boolean not null default true, "
        "dev boolean not null default false, "
        "primary key(id), "
        "foreign key(admin_user_id) "
        "references user (id) "
        "on update no action "
        "on delete cascade"
        ");"
    )

    # execute create query
    preset.create(query)


# todo docstring
# todo some sort of confirmation
def drop_guild_table():
    # set up the query
    query = ("DROP TABLE guild")

    # execute drop query
    preset.drop(query)
