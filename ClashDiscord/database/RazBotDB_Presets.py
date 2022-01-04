import database.RazBotDB_Query as db_query


# INSERT
def insert(query):
    # execute the query
    db_query.execute_query(query)


# SELECT
def select(query):
    # execute and return query
    data = db_query.fetch_single_query(query)
    return data


def select_list(query):
    # return query
    data = db_query.fetch_all_query(query)
    return data


# UPDATE
def update(query):
    # execute the query
    db_query.execute_query(query)


# DELETE
def delete(query):
    # execute the query
    db_query.execute_query(query)

# CREATE


def create(query):
    # execute the query
    db_query.execute_query(query)


# DROP
def drop(query):
    # execute the query
    db_query.execute_query(query)
