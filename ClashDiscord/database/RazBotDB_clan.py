import database.RazBotDB_Presets as preset

# clan


class Clan(object):
    """
        clan: object for db clan table objects

            Instance Attributes
                guild_id (int): guild id in discord
                clan_tag (str): tag of clan
    """

    def __init__(self, guild_id, clan_tag):
        self.guild_id = guild_id
        self.clan_tag = clan_tag


def insert_clan(guild_id, clan_tag):
    """
        Takes in the discord guild_id, clan_tag
        inserts and returns clan db guild_id, clan_tag
        and if no clan is inserted and found returns None

        Args:
            guild_id (int): guild id received from discord
            clan_tag (int): clan_tag received from user message

        Returns:
            guild_id: discord guild's id
            clan_tag: tag of clan
    """
    # set up the query
    query = (
        f"INSERT into clan (guild_id, clan_tag) "
        f"VALUES ("
        f"(SELECT id FROM guild WHERE guild_id={guild_id}), '{clan_tag}'"
        f");"
    )

    # execute insert query
    preset.insert(query)
    # select and return clan
    data = select_clan(guild_id, clan_tag)
    return data


def select_clan(guild_id, clan_tag):
    """
        Takes in discord guild_id and clan_tag and
        returns discord guild id and clan db clan tag

        Args:
            guild_id (int): discord guild id
            clan_tag (str): clan's tag

        Returns:
            guild id: discord guild id
            clan_tag: clan's tag
    """
    # find the clan based on clan_tag and guild_id
    query = (
        f"SELECT guild.guild_id, clan.clan_tag "
        f"FROM clan "
        f"INNER JOIN guild ON clan.guild_id = guild.id "
        f"WHERE clan.clan_tag = '{clan_tag}' "
        f"AND guild.guild_id = {guild_id};"
    )

    # execute and return query
    data = preset.select(query)
    return data


def select_clan_all_from_guild(guild_id):
    """
        Takes in discord guild_id and
        returns discord guild id and clan db clan tag 
        for all clans in guild

        Args:
            guild_id (int): discord guild id
            clan_tag (str): clan's tag

        Returns:
            guild id: discord guild id
            clan_tag: clan's tag
    """
    # find the clan based on clan_tag and guild_id
    query = (
        f"SELECT guild.guild_id, clan.clan_tag "
        f"FROM clan "
        f"INNER JOIN guild ON clan.guild_id = guild.id "
        f"WHERE guild.guild_id = {guild_id};"
    )

    # execute and return query
    data = preset.select_list(query)
    return data


# ! good query formatting
def select_clan_from_clan_role(discord_role_id, guild_id):
    """
        Takes in discord discord_role_id, guild_id and
        returns clan db clan_tag

        Args:
            guild_id (int): discord's guild id
            discord_role_id (int): discord's role id

        Returns:
            clan_tag: clan's tag
    """
    # find the clan based on clan_tag and guild_id
    query = (
        f"SELECT clan_tag FROM clan "
        f"WHERE id = ("
        f"SELECT clan_id FROM clan_role WHERE discord_role_id = {discord_role_id}"
        f") AND "
        f"guild_id = ("
        f"SELECT id from guild WHERE guild_id={guild_id}"
        f");"
    )

    # execute and return query
    data = preset.select(query)
    return data


def delete_clan(guild_id, clan_tag):
    """
        Takes in the discord guild_id and clan_tag, deletes the db clan and
        returns null to confirm it has been deleted

        Args:
            guild_id (int): id received from discord guild
            clan_tag (str): clan's tag

        Returns:
            null: null confirms it has been deleted
    """
    # set up the query
    query = (
        f"DELETE FROM clan "
        f"WHERE clan_tag = '{clan_tag}' AND "
        f"guild_id = (SELECT id FROM guild WHERE guild_id={guild_id});"
    )

    # execute delete query
    preset.delete(query)
    # confirm deletion from null response
    data = select_clan(guild_id, clan_tag)
    return data


def select_clan_count():
    """
        returns clan count

        Returns:
            clan_count: int of clan count
    """
    # set up the query
    query = (
        f"SELECT COUNT(id) as clan_count FROM clan;"
    )

    # execute and return query
    data = preset.select(query)
    return data


# todo docstring
# todo some sort of confirmation
def create_clan_table():
    # set up the query
    query = (
        "CREATE TABLE clan( "
        "id int not null auto_increment, "
        "guild_id int not null, "
        "clan_tag varchar(28) not null, "
        "primary key(id), "
        "foreign key(guild_id) "
        "references guild (id) "
        "on update no action "
        "on delete cascade "
        ");"
    )

    # execute create query
    preset.create(query)


# todo docstring
# todo some sort of confirmation
def drop_clan_table():
    # set up the query
    query = ("DROP TABLE clan")

    # execute drop query
    preset.drop(query)
