import database.RazBotDB_Presets as preset
import database.RazBotDB_user as user
import database.RazBotDB_player as player
import database.RazBotDB_guild as guild
import database.RazBotDB_clan as clan
import database.RazBotDB_clan_role as clan_role
import database.RazBotDB_rank_role_model as rank_role_model
import database.RazBotDB_rank_role as rank_role


# DB RESET

# todo make this 1 or 3 queries
def db_reset():
    # drop tables
    rank_role.drop_rank_role_table()
    rank_role_model.drop_rank_role_model_table()
    clan_role.drop_clan_role_table()
    clan.drop_clan_table()
    player.drop_player_table()
    guild.drop_guild_table()
    user.drop_user_table()

    # create tables
    user.create_user_table()
    player.create_player_table()
    guild.create_guild_table()
    clan.create_clan_table()
    clan_role.create_clan_role_table()
    rank_role_model.create_rank_role_model_table()
    rank_role.create_rank_role_table()

    # set Raz values
    user.insert_raz_super_user(250312821647081472)
    player.insert_raz_player(250312821647081472, '#RGQ8RGU9')
    guild.insert_guild_dev(798603935022710844, 1)
    rank_role_model.insert_rank_role_model_setup()


# RazBotDB
def select_table(table_name):
    """
        Takes in the table_name and selects the associated table.

        Args:
            table_name (str): name of the requested table

        Returns:
            TABLE: data pertaining to the table
    """
    # set up the query
    query = (
        f"SELECT * FROM information_schema.tables "
        f"WHERE table_name = '{table_name}'"
    )

    # execute and return query
    data = preset.select(query)
    return data


def select_table_all():
    """
        Returns all tables in SCHEMA RAZBOT.

        Returns:
            TABLE: data pertaining to the table
    """
    # set up the query
    query = (
        f"SELECT * FROM information_schema.tables "
        f"WHERE table_schema = 'RAZBOT'"
    )

    # execute and return query
    data = preset.select_list(query)
    return data
