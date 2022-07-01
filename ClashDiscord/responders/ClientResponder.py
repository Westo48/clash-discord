import data.RazBot_Data as RazBot_Data
from responders.ClashResponder import get_player

from responders.AuthResponder import player_verification

from disnake.utils import get


def get_client_discord_id():
    """
        returns RazBot_Data client discord id
    """

    return RazBot_Data.RazBot_Data().discord_id


def get_client_token():
    """
        returns RazBot_Data client token
    """

    return RazBot_Data.RazBot_Data().token


def get_client_test_guilds():
    """
        returns RazBot_Data client test guilds
    """

    test_guilds = RazBot_Data.RazBot_Data().test_guilds

    if len(test_guilds) > 0:
        return test_guilds

    else:
        return None


def get_client_email():
    """
        returns RazBot_Data client coc email
    """

    return RazBot_Data.RazBot_Data().coc_dev_email


def get_client_password():
    """
        returns RazBot_Data client coc password
    """

    return RazBot_Data.RazBot_Data().coc_dev_password


def get_linkapi_username():
    """
        returns RazBot_Data client link api username
    """

    return RazBot_Data.RazBot_Data().link_api_username


def get_linkapi_password():
    """
        returns RazBot_Data client link api password
    """

    return RazBot_Data.RazBot_Data().link_api_password


def client_info(client, client_data):
    field_dict_list = []

    field_dict_list.append({
        'name': "**Client Info**",
        'value': "_ _",
        'inline': False
    })

    field_dict_list.append({
        'name': "author",
        'value': client_data.author
    })

    field_dict_list.append({
        'name': "description",
        'value': client_data.description
    })

    field_dict_list.append({
        'name': "server count",
        'value': f"{len(client.guilds)}"
    })

    field_dict_list.append({
        'name': "version",
        'value': client_data.version
    })

    return field_dict_list


def client_guild_info(guild, db_guild):
    field_dict_list = []

    field_dict_list.append({
        'name': "**Client Server Info**",
        'value': "_ _",
        'inline': False
    })

    field_dict_list.append({
        'name': f"{guild.name} owner",
        'value': f"{guild.owner.mention}"
    })

    field_dict_list.append({
        'name': f"{guild.name} member count",
        'value': f"{len(guild.members)}"
    })

    if db_guild is None:
        field_dict_list.append({
            'name': f"{guild.name} not claimed",
            'value': f"please claim the server using `admin server claim`"
        })
        return field_dict_list

    db_guild_admin = get(guild.members, id=db_guild.admin_user_id)

    if db_guild_admin is None:
        guild_admin_value = f"id: {db_guild.admin_user_id}"
    else:
        guild_admin_value = f"{db_guild_admin.mention}"

    field_dict_list.append({
        'name': "ClashCommander server admin",
        'value': guild_admin_value
    })

    return field_dict_list


async def client_player_info(author, db_players, coc_client):
    field_dict_list = []

    field_dict_list.append({
        'name': "**Client Player Info**",
        'value': "_ _",
        'inline': False
    })

    # linked players count
    field_dict_list.append({
        'name': f"{author.display_name} players",
        'value': f"{len(db_players)}"
    })

    for db_player in db_players:
        player_verification_payload = await player_verification(
            db_player, author, coc_client)

        if not player_verification_payload['verified']:
            field_dict_list.extend(
                player_verification_payload['field_dict_list'])
            continue

        player = player_verification_payload['player_obj']

        field_dict_list.append({
            'name': player.name,
            'value': player.tag
        })

    return field_dict_list


async def client_player_list(db_player_list, user, coc_client):

    message = f"{user.mention} has claimed:\n\n"

    for db_player in db_player_list:
        player = await get_player(
            db_player.player_tag, coc_client)

        # player not found in clash
        if player is None:
            message += f"**{db_player.player_tag} not found in clash please remove**\n"
            continue

        if db_player.active:
            message += f"{player.name} {player.tag} (active)\n"
        else:
            message += f"{player.name} {player.tag}\n"

    # cuts the last one character from the string '\n'
    message = message[:-1]

    return message
