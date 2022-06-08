import database.RazBotDB_Presets as preset


class Player(object):
    """
        Player: object for db player table objects

            Instance Attributes
                player_tag (str): player's clash tag
                active (bool): TF of if player is user's active
                super_user (bool): TF of super_user status
    """

    def __init__(self, player_tag, active):
        self.player_tag = player_tag
        self.active = active


# todo work on working with multiple tables at the same time
# player


# todo working with sub-queries
def select_player_raz():
    # find player based on user_id
    discord_id = 250312821647081472
    query = (
        f"SELECT player_tag, active FROM player "
        f"WHERE user_id = "
        f"(SELECT id FROM user WHERE discord_id={discord_id}) "
        f"AND active=true"
    )

    # execute and return query
    data = preset.select(query)
    return data


def select_player_from_user_tag(discord_id, player_tag):
    """
        Takes in the player_tag, discord_id
        returns player db player_tag and active or None if not found

        Args:
            player_tag (str): string of player's tag

        Returns:
            player_tag: player's tag
            active: bool of active or not
    """
    # find the player based on user_id
    query = (
        f"SELECT player_tag, active FROM player "
        f"WHERE user_id = "
        f"(SELECT ID FROM user WHERE discord_id={discord_id}) "
        f"AND player_tag = '{player_tag}'"
    )

    # execute and return query
    data = preset.select(query)
    return data


def select_player_from_tag(player_tag):
    """
        Takes in the player_tag and
        returns player db player_tag and active or None if not found

        Args:
            player_tag (str): string of player's tag

        Returns:
            player_tag: player's tag
            active: bool of active or not
    """
    # find the player based on user_id
    query = (
        f"SELECT player_tag, active FROM player "
        f"WHERE player_tag = '{player_tag}'"
    )

    # execute and return query
    data = preset.select(query)
    return data


def select_player_active(discord_id):
    """
        Takes in the discord_id and
        returns player db player_tag and active

        Args:
            discord_id (int): id received from discord

        Returns:
            player_tag: user's active player tag
            active: bool of active or not
    """
    # find the player based on user_id
    query = (
        f"SELECT player_tag, active FROM player "
        f"WHERE user_id = "
        f"(SELECT ID FROM user WHERE discord_id={discord_id}) "
        f"AND active=true"
    )

    # execute and return query
    data = preset.select(query)
    return data


def select_player_alt(discord_id):
    """
        Takes in the discord_id and
        returns player db player_tag and active

        Args:
            discord_id (int): id received from discord

        Returns:
            player_tag: user's active player tag
            active: bool of active or not
    """
    # find the player based on user_id
    query = (
        f"SELECT player_tag, active FROM player "
        f"WHERE user_id = "
        f"(SELECT id FROM user WHERE discord_id={discord_id}) "
        f"AND active = false"
    )

    # execute and return query
    data = preset.select(query)
    return data


def select_player_all(discord_id):
    """
        Takes in the discord_id and
        returns player db player_tag and active

        Args:
            discord_id (int): id received from discord

        Returns:
            player_tag: user's active player tag
            active: bool of active or not
    """
    # find the player based on user_id
    query = (
        f"SELECT player_tag, active FROM player "
        f"WHERE user_id = "
        f"(SELECT id FROM user WHERE discord_id={discord_id}) "
    )

    # execute and return query
    data = preset.select_list(query)
    return data


def insert_raz_player(discord_user_id, player_tag):
    # set up the query
    query = (
        f"INSERT into player (user_id, player_tag) "
        f"VALUES ((SELECT ID FROM user WHERE discord_id={discord_user_id}), "
        f"'{player_tag}');"
    )

    # execute insert query
    preset.insert(query)
    # select and return player
    data = select_player_raz()
    return data


# todo update docstring
def insert_player_active(discord_id, player_tag):
    """
        Takes in the player_tag and discord_id then
        returns player db player_tag and active

        Args:
            discord_id (int): id received from discord

        Returns:
            player_tag: user's active player tag
            active: bool of active or not
    """
    # set up the query
    query = (
        f"INSERT into player (user_id, player_tag) "
        f"VALUES ((SELECT ID FROM user WHERE discord_id={discord_id}), "
        f"'{player_tag}');"
    )

    # execute update query
    preset.update(query)
    # select and return player
    data = select_player_active(discord_id)
    return data


# todo update docstring
def insert_player_alt(discord_id, player_tag):
    """
        Takes in the player_tag and discord_id then
        returns player db player_tag and active

        Args:
            discord_id (int): id received from discord

        Returns:
            player_tag: user's active player tag
            active: bool of active or not
    """
    # set up the query
    query = (
        f"INSERT into player (user_id, player_tag, active) "
        f"VALUES ((SELECT ID FROM user WHERE discord_id={discord_id}), "
        f"'{player_tag}', FALSE);"
    )

    # execute update query
    preset.update(query)
    # select and return player
    data = select_player_alt(discord_id)
    return data


def update_player_active(discord_id, player_tag):
    """
        Takes in discord_id and player_tag, 
        updates current active to false and sets requested player_tag to active

        Args:
            discord_id (int): id received from discord
            player_tag (str): string of player's tag

        Returns:
            player_tag: user's active player tag
            active: bool of active or not
    """
    # set up the query
    # change the user's active player to false
    query = (
        f"UPDATE player "
        f"SET active=false "
        f"WHERE user_id = "
        f"(SELECT id FROM user WHERE discord_id={discord_id}) "
        f"AND active=true;"
    )

    # execute update query
    preset.update(query)

    # change requested user's player to active
    query = (
        f"UPDATE player "
        f"SET active=true "
        f"WHERE user_id = "
        f"(SELECT id FROM user WHERE discord_id={discord_id}) "
        f"AND player_tag='{player_tag}';"
    )

    # execute update query
    preset.update(query)
    # select and return player
    data = select_player_active(discord_id)
    return data


# todo confirm deletion from null response
def delete_player(discord_id, player_tag):
    """
        Takes in discord_id and player_tag, 
        and deletes the requested user's player

        Args:
            discord_id (int): id received from discord
            player_tag (str): string of player's tag

        Returns:
            bool if player could be found after deletion query execution
    """
    # set up the query
    # delete the requested
    query = (
        f"DELETE FROM player "
        f"WHERE user_id = "
        f"(SELECT id FROM user WHERE discord_id={discord_id}) "
        f"AND player_tag = '{player_tag}';"
    )

    # execute delete query
    preset.delete(query)

    # select and return player
    data = select_player_from_user_tag(discord_id, player_tag)
    if data:
        return True
    else:
        return False


def delete_player_from_tag(player_tag):
    """
        Takes in player_tag, 
        and deletes the requested user's player

        Args:
            player_tag (str): string of player's tag

        Returns:
            bool if player could be found after deletion query execution
    """
    # set up the query
    # delete the requested
    query = (
        f"DELETE FROM player "
        f"WHERE player_tag = '{player_tag}';"
    )

    # execute delete query
    preset.delete(query)

    # select and return player
    data = select_player_from_tag(player_tag)
    if data:
        return True
    else:
        return False


def select_player_count():
    """
        returns player count

        Returns:
            player_count: int of player count
    """
    # set up the query
    query = (
        f"SELECT COUNT(id) as player_count FROM player;"
    )

    # execute and return query
    data = preset.select(query)
    return data


# todo some sort of confirmation
def create_player_table():
    # set up the query
    query = (
        "CREATE TABLE player (  "
        "id int not null auto_increment, "
        "user_id int not null, "
        "player_tag varchar(28) unique not null, "
        "active boolean not null default true, "
        "primary key (id), "
        "foreign key (user_id) "
        "references user (id) "
        "on update no action "
        "on delete cascade"
        ");"
    )

    # execute create query
    preset.create(query)


# todo some sort of confirmation
def drop_player_table():
    # set up the query
    query = ("DROP TABLE player")

    # execute drop query
    preset.drop(query)
