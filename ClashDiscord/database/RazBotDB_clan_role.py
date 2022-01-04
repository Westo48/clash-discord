import database.RazBotDB_Presets as preset


# clan role
class ClanRole(object):
    """
        ClanRole: object for db clan role table objects

            Instance Attributes
                discord_guild_id (int): guild id in discord
                discord_role_id (int): role id in discord
                clan_tag (str): tag of clan
    """

    def __init__(self, discord_guild_id, discord_role_id, clan_tag):
        self.discord_guild_id = discord_guild_id
        self.discord_role_id = discord_role_id
        self.clan_tag = clan_tag


# INSERT
def insert_clan_role(discord_role_id, guild_id, clan_tag):
    """
        Takes in the discord discord_role_id, guild_id, clan_tag
        inserts and returns clan_role db discord_role_id, guild_id, clan_tag
        and if no clan_role is inserted and found returns None

        Args:
            discord_role_id (int): discord role id received from discord
            guild_id (int): guild id received from discord
            clan_tag (int): clan_tag received from user message

        Returns:
            discord_guild_id: discord's guild id
            discord_role_id: discord's role id
            clan_tag: clan's tag
    """
    # set up the query
    query = (
        f"INSERT into clan_role (discord_role_id, clan_id) "
        f"VALUES ({discord_role_id}, "
        f"(SELECT id FROM clan WHERE clan_tag = '{clan_tag}' AND "
        f"guild_id = (SELECT id from guild WHERE guild_id={guild_id})"
        f"));"
    )

    # execute insert query
    preset.insert(query)
    # select and return clan_role
    data = select_clan_role(discord_role_id)
    return data


# SELECT
def select_clan_role(discord_role_id):
    """
        Takes in discord_role_id and
        returns clan_role db discord_role_id and clan db id

        Args:
            discord_role_id (int): discord's role id

        Returns:
            discord_guild_id: discord's guild id
            discord_role_id: discord's role id
            clan_tag: clan's tag
    """
    # find the clan_role based on discord_role_id
    query = (
        f"SELECT guild.guild_id as discord_guild_id, "
        f"clan_role.discord_role_id as discord_role_id, "
        f"clan.clan_tag as clan_tag "
        f"FROM clan_role "
        f"INNER JOIN clan ON clan_role.clan_id = clan.id "
        f"INNER JOIN guild ON clan.guild_id = guild.id "
        f"WHERE clan_role.discord_role_id = {discord_role_id};"
    )

    # execute and return query
    data = preset.select(query)
    return data


def select_clan_role_from_list(discord_role_id_list):
    """
        Takes in list of discord_role_id and
        returns clan_role db discord_role_id and clan db id

        Args:
            list
                discord_role_id (int): discord's role id

        Returns:
            list
                discord_guild_id: discord's guild id
                discord_role_id: discord's role id
                clan_tag: clan's tag
    """

    if len(discord_role_id_list) == 0:
        return []

    where_string = ""
    for role_id in discord_role_id_list:
        where_string += f"clan_role.discord_role_id = {role_id} OR "

    # cuts the last four characters from the string ' OR '
    where_string = where_string[:-4]

    # find the clan_role based on discord_role_id
    query = (
        f"SELECT guild.guild_id as discord_guild_id, "
        f"clan_role.discord_role_id as discord_role_id, "
        f"clan.clan_tag as clan_tag "
        f"FROM clan_role "
        f"INNER JOIN clan ON clan_role.clan_id = clan.id "
        f"INNER JOIN guild ON clan.guild_id = guild.id "
        f"WHERE {where_string};"
    )

    # execute and return query
    data = preset.select_list(query)
    return data


def select_clan_role_from_guild(discord_guild_id):
    """
        Takes in discord_guild_id and
        returns clan_role db discord_role_id and clan db id

        Args:
            list
                discord_guild_id (int): discord's guild id

        Returns:
            list
                discord_guild_id: discord's guild id
                discord_role_id: discord's role id
                clan_tag: clan's tag
    """

    # find the clan_role based on discord_guild_id
    query = (
        f"SELECT guild.guild_id as discord_guild_id, "
        f"clan_role.discord_role_id as discord_role_id, "
        f"clan.clan_tag as clan_tag "
        f"FROM clan_role "
        f"INNER JOIN clan ON clan_role.clan_id = clan.id "
        f"INNER JOIN guild ON clan.guild_id = guild.id "
        f"WHERE guild.guild_id = {discord_guild_id};"
    )

    # execute and return query
    data = preset.select_list(query)
    return data


def select_clan_role_from_tag(discord_guild_id, clan_tag):
    """
        finds clan role obj matching guild id and clan tag

        Args:
            discord_guild_id (int): discord id for guild
            clan_tag (str): tag for clan

        Returns:
            discord_guild_id: discord's guild id
            discord_role_id: discord's role id
            clan_tag: clan's tag
    """
    # find the clan_role based on discord_role_id
    query = (
        f"SELECT guild.guild_id as discord_guild_id, "
        f"clan_role.discord_role_id as discord_role_id, "
        f"clan.clan_tag as clan_tag "
        f"FROM clan_role "
        f"INNER JOIN clan ON clan_role.clan_id = clan.id "
        f"INNER JOIN guild ON clan.guild_id = guild.id "
        f"WHERE guild.guild_id = {discord_guild_id} "
        f"AND clan.clan_tag = '{clan_tag}';"
    )

    # execute and return query
    data = preset.select(query)
    return data


# DELETE
def delete_clan_role(discord_role_id):
    """
        Takes in discord_role_id, deletes the db clan_role and
        returns null to confirm it has been deleted

        Args:
            discord_role_id (int): discord's role id

        Returns:
            null: null confirms it has been deleted
    """
    # delete the clan_role based on discord_role_id
    query = (
        f"DELETE FROM clan_role "
        f"WHERE discord_role_id = {discord_role_id};"
    )

    # execute delete query
    preset.delete(query)
    # confirm deletion from null response
    data = select_clan_role(discord_role_id)
    return data


# CREATE
# todo docstring
# todo some sort of confirmation
def create_clan_role_table():
    # set up the query
    query = (
        f"CREATE TABLE clan_role( "
        f"id int not null auto_increment, "
        f"discord_role_id bigint unique not null, "
        f"clan_id int not null, "
        f"primary key(id), "
        f"foreign key(clan_id) "
        f"references clan (id) "
        f"on update no action "
        f"on delete cascade"
        f");"
    )

    # execute create query
    preset.create(query)


# DROP
# todo docstring
# todo some sort of confirmation
def drop_clan_role_table():
    # set up the query
    query = ("DROP TABLE clan_role")

    # execute drop query
    preset.drop(query)
