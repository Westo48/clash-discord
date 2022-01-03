import database.RazBotDB_Presets as preset


# rank role model
class RankRoleModel(object):
    """
        RankRoleModel: object for db rank role model table objects

            Instance Attributes
                name (str): role name
                clash_name (str): role name from clash API
    """

    def __init__(self, name, clash_name):
        self.name = name
        self.clash_name = clash_name


# INSERT
# todo docstring


def insert_rank_role_model_setup():
    # set up the query
    query = (
        f"INSERT into "
        f"rank_role_model (name, clash_name) "
        f"VALUES "
        f"('leader', 'leader'), "
        f"('co-leader', 'coLeader'), "
        f"('elder', 'admin'), "
        f"('member', 'member'),"
        f"('uninitiated', 'uninitiated');"
    )

    # execute insert query
    preset.insert(query)
    # select and return all rank_role_model
    data = select_rank_role_model_all()
    return data


# SELECT
def select_rank_role_model(id):
    """
        Takes in rank_role_model db id and
        returns rank_role_model db name and clash_name

        Args:
            id (int): rank_role_model db id

        Returns:
            name: role name
            clash_name: clash api role name
    """
    # find the rank_role_model based on id
    query = (
        f"SELECT name, clash_name FROM rank_role_model "
        f"WHERE id = {id};"
    )

    # execute and return query
    data = preset.select(query)
    return data


def select_rank_role_model_name(name):
    """
        Takes in rank_role_model db name and
        returns rank_role_model db name and clash_name

        Args:
            name (str): rank_role_model db name

        Returns:
            name: role name
            clash_name: clash api role name
    """
    # find the rank_role_model based on name
    query = (
        f"SELECT name, clash_name FROM rank_role_model "
        f"WHERE name = '{name}';"
    )

    # execute and return query
    data = preset.select(query)
    return data


def select_rank_role_model_all():
    """
        Returns rank_role_model db name and clash_name of all in table

        Returns:
            name: role name
            clash_name: clash api role name
    """
    # select all rank_role_models in table
    query = (
        f"SELECT name, clash_name FROM rank_role_model;"
    )

    # execute and return query
    data = preset.select_list(query)
    return data


# CREATE
def create_rank_role_model_table():
    # set up the query
    query = (
        f"CREATE TABLE rank_role_model("
        f"id int not null auto_increment, "
        f"name varchar(28) not null, "
        f"clash_name varchar(28) not null, "
        f"primary key(id)"
        f");"
    )

    # execute create query
    preset.create(query)


# DROP
# todo docstring
# todo some sort of confirmation
def drop_rank_role_model_table():
    # set up the query
    query = ("DROP TABLE rank_role_model")

    # execute drop query
    preset.drop(query)
