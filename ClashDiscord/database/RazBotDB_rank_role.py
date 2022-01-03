import database.RazBotDB_Presets as preset


# rank role
class RankRole(object):
    """
        RankRole: object for db rank role table objects

            Instance Attributes
                discord_guild_id (int): guild id in discord
                discord_role_id (int): role id in discord
                model_name (str): db rank role model name
                clash_name (str): role name from clash API
    """

    def __init__(self, discord_guild_id, discord_role_id, model_name, clash_name):
        self.discord_guild_id = discord_guild_id
        self.discord_role_id = discord_role_id
        self.model_name = model_name
        self.clash_name = clash_name

# INSERT
# todo docstring


def insert_rank_role(discord_role_id, discord_guild_id, model_name):
    # set up the query
    query = (
        f"INSERT into "
        f"rank_role (discord_role_id, guild_id, model_id) "
        f"VALUES "
        f"("
        f"{discord_role_id}, "
        f"(SELECT id FROM guild WHERE guild_id={discord_guild_id}), "
        f"(SELECT id FROM rank_role_model WHERE name = '{model_name}')"
        f");"
    )

    # execute insert query
    preset.insert(query)
    # select and return inserted rank_role_id
    data = select_rank_role(discord_role_id)
    return data


# SELECT
def select_rank_role(discord_role_id):
    """
        Takes in discord_role_id and
        returns rank_role db discord_role_id, model_name and clash_name

        Args:
            discord_role_id (int): role id in discord

        Returns:
            discord_guild_id: guild id in discord
            discord_role_id: role id in discord
            model_name: db rank role model name
            clash_name: role name from clash API
    """
    # find the rank_role_model based on discord role id
    query = (
        f"SELECT guild.guild_id as discord_guild_id, "
        f"rank_role.discord_role_id as discord_role_id, "
        f"rank_role_model.name as rank_model_name, "
        f"rank_role_model.clash_name as clash_name "
        f"FROM rank_role "
        f"INNER JOIN rank_role_model ON rank_role.model_id = rank_role_model.id "
        f"INNER JOIN guild ON rank_role.guild_id = guild.id "
        f"WHERE rank_role.discord_role_id = {discord_role_id};"
    )

    # execute and return query
    data = preset.select(query)
    return data


def select_guild_rank_role(discord_guild_id):
    """
        Takes discord_guild_id and returns
        list rank_role db discord_role_id, model_name and clash_name

        Args:
            list
                discord_guild_id (int): guild id in discord

        Returns:
            list
                discord_guild_id: guild id in discord
                discord_role_id: role id in discord
                model_name: db rank role model name
                clash_name: role name from clash API
    """

    # find the rank_role_model based on discord guild id
    query = (
        f"SELECT guild.guild_id as discord_guild_id, "
        f"rank_role.discord_role_id as discord_role_id, "
        f"rank_role_model.name as rank_model_name, "
        f"rank_role_model.clash_name as clash_name "
        f"FROM rank_role "
        f"INNER JOIN rank_role_model ON rank_role.model_id = rank_role_model.id "
        f"INNER JOIN guild ON rank_role.guild_id = guild.id "
        f"WHERE guild.guild_id = {discord_guild_id};"
    )

    # execute and return query
    data = preset.select_list(query)
    return data


def select_rank_role_from_list(discord_role_id_list):
    """
        Takes in list of discord_role_id and returns
        list rank_role db discord_role_id, model_name and clash_name

        Args:
            list
                discord_role_id (int): role id in discord

        Returns:
            list
                discord_guild_id: guild id in discord
                discord_role_id: role id in discord
                model_name: db rank role model name
                clash_name: role name from clash API
    """

    if len(discord_role_id_list) == 0:
        return []

    where_string = ""
    for role_id in discord_role_id_list:
        where_string += f"rank_role.discord_role_id = {role_id} OR "

    # cuts the last four characters from the string ' OR '
    where_string = where_string[:-4]

    # find the rank_role_model based on discord role id
    query = (
        f"SELECT guild.guild_id as discord_guild_id, "
        f"rank_role.discord_role_id as discord_role_id, "
        f"rank_role_model.name as rank_model_name, "
        f"rank_role_model.clash_name as clash_name "
        f"FROM rank_role "
        f"INNER JOIN rank_role_model ON rank_role.model_id = rank_role_model.id "
        f"INNER JOIN guild ON rank_role.guild_id = guild.id "
        f"WHERE {where_string};"
    )

    # execute and return query
    data = preset.select_list(query)
    return data


def select_rank_role_all_from_guild(discord_guild_id):
    """
        Takes in discord_guild_id and
        returns rank_role db list discord_role_id, model_name and clash_name

        Args:
            discord_guild_id (int): role id in discord

        Returns:
            discord_guild_id: guild id in discord
            discord_role_id: role id in discord
            model_name: db rank role model name
            clash_name: role name from clash API
    """
    # find the rank_role_model based on discord guild id
    query = (
        f"SELECT guild.guild_id as discord_guild_id, "
        f"rank_role.discord_role_id as discord_role_id, "
        f"rank_role_model.name as rank_model_name, "
        f"rank_role_model.clash_name as clash_name "
        f"FROM rank_role "
        f"INNER JOIN rank_role_model ON rank_role.model_id = rank_role_model.id "
        f"INNER JOIN guild ON rank_role.guild_id = guild.id "
        f"WHERE guild.guild_id = {discord_guild_id};"
    )

    # execute and return query
    data = preset.select_list(query)
    return data


def select_rank_role_name_from_guild_and_clash(discord_guild_id, clash_name):
    """
        Takes in discord_guild_id, clash_name
        returns rank_role db discord_role_id, model_name and clash_name

        Args:
            discord_guild_id (int): role id in discord
            clash_name (str): db rank role clash name

        Returns:
            discord_guild_id: guild id in discord
            discord_role_id: role id in discord
            model_name: db rank role model name
            clash_name: role name from clash API
    """
    # find the rank_role based on discord guild id and clash name
    query = (
        f"SELECT guild.guild_id as discord_guild_id, "
        f"rank_role.discord_role_id as discord_role_id, "
        f"rank_role_model.name as rank_model_name, "
        f"rank_role_model.clash_name as clash_name "
        f"FROM rank_role "
        f"INNER JOIN rank_role_model ON rank_role.model_id = rank_role_model.id "
        f"INNER JOIN guild ON rank_role.guild_id = guild.id "
        f"WHERE guild.guild_id = {discord_guild_id} "
        f"AND rank_role_model.clash_name = '{clash_name}';"
    )

    # execute and return query
    data = preset.select(query)
    return data


# DELETE
def delete_rank_role(discord_role_id):
    """
        Takes in discord_role_id, deletes the db rank_role and
        returns null to confirm it has been deleted

        Args:
            discord_role_id (int): discord's role id

        Returns:
            null: null confirms it has been deleted
    """
    # delete the rank_role based on discord_role_id
    query = (
        f"DELETE FROM rank_role "
        f"WHERE discord_role_id = {discord_role_id};"
    )

    # execute delete query
    preset.delete(query)
    # confirm deletion from null response
    data = select_rank_role(discord_role_id)
    return data


# CREATE
def create_rank_role_table():
    # set up the query
    query = (
        f"CREATE TABLE rank_role("
        f"id int not null auto_increment, "
        f"discord_role_id bigint unique not null, "
        f"guild_id int not null, "
        f"model_id int not null, "
        f"primary key(id), "
        f"foreign key(guild_id) "
        f"references guild (id) "
        f"on update no action "
        f"on delete cascade, "
        f"foreign key(model_id) "
        f"references rank_role_model (id) "
        f"on update no action "
        f"on delete cascade"
        f");"
    )

    # execute create query
    preset.create(query)


# DROP
# todo docstring
# todo some sort of confirmation
def drop_rank_role_table():
    # set up the query
    query = ("DROP TABLE rank_role")

    # execute drop query
    preset.drop(query)
