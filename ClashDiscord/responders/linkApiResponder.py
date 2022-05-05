from linkAPI.client import LinkApiClient
from linkAPI.errors import *
from linkAPI.playerLinkModel import PlayerLink


def add_secure_link(linkapi_client: LinkApiClient,
                    player_tag: str, discord_user_id: int):
    """
        adding player link from a secured method (api key or super user)

        Args:
            linkapi_client (LinkApiClient): client for linkAPI
            player_tag (str): clash of clans player tag
            discord_user_id (int): user ID from discord

        Raises:
            ConflictError: database conflict
    """
    player_link = None

    # get LinkAPI player link
    try:
        player_link = linkapi_client.get_player_tag_link(
            player_tag=player_tag)
    except LoginError:
        print("Error logging into LinkAPI")
    except NotFoundError:
        pass
    except InvalidTagError:
        print(f"Player tag {player_tag} not valid")

    # player link found
    if player_link:
        # player link user doesn't match db user
        # player supplied api key
        # link needs to be deleted so it can be added
        if player_link.discord_user_id != discord_user_id:
            try:
                linkapi_client.delete_link(
                    player_tag=player_tag)
                player_link = None
            except LoginError:
                print("Error logging into LinkAPI")
            except NotFoundError:
                print(f"Player tag {player_tag} not found in LinkAPI db")

    # player link not found or deleted
    if not player_link:
        # add link in LinkAPI
        try:
            player_link = linkapi_client.add_link(
                player_tag=player_tag,
                discord_user_id=discord_user_id)
        except LoginError:
            print("Error logging into LinkAPI")
        except InvalidTagError:
            print(f"Player tag {player_tag} not valid")
        except ConflictError:
            print("Player tag {player_tag} already in LinkAPI DB")
            raise ConflictError("Tag already in DB")


def add_link(linkapi_client: LinkApiClient,
             player_tag: str, discord_user_id: int):
    """
        adding player link

        Args:
            linkapi_client (LinkApiClient): client for linkAPI
            player_tag (str): clash of clans player tag
            discord_user_id (int): user ID from discord

        Raises:
            ConflictError: database conflict
    """
    player_link = None

    # get LinkAPI player link
    try:
        player_link = linkapi_client.get_player_tag_link(
            player_tag=player_tag)
    except LoginError:
        print("Error logging into LinkAPI")
    except NotFoundError:
        pass
    except InvalidTagError:
        print(f"Player tag {player_tag} not valid")

    # player link found
    if player_link:
        # player link user doesn't match db user
        # player supplied api key
        # link needs to be deleted so it can be added
        if player_link.discord_user_id != discord_user_id:
            raise ConflictError("Tag already in DB")

    # player link not found or deleted
    if not player_link:
        # add link in LinkAPI
        try:
            player_link = linkapi_client.add_link(
                player_tag=player_tag,
                discord_user_id=discord_user_id)
        except LoginError:
            print("Error logging into LinkAPI")
        except InvalidTagError:
            print(f"Player tag {player_tag} not valid")
        except ConflictError:
            print("Player tag {player_tag} already in LinkAPI DB")
            raise ConflictError("Tag already in DB")


def remove_link(linkapi_client: LinkApiClient,
                player_tag: str):
    """
        removing player link

        Args:
            linkapi_client (LinkApiClient): client for linkAPI
            player_tag (str): clash of clans player tag

        Raises:
            ConflictError: database conflict
    """
    try:
        linkapi_client.delete_link(
            player_tag=player_tag)
    except LoginError:
        print("Error logging into LinkAPI")
    except NotFoundError:
        print(f"Player tag {player_tag} not found in LinkAPI db")
