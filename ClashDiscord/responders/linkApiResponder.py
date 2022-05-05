from linkAPI.client import LinkApiClient
from linkAPI.errors import *
from linkAPI.playerLinkModel import PlayerLink
from responders import RazBotDB_Responder as db_responder


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


def pull_from_link(
    linkapi_client: LinkApiClient,
    discord_user_id: int
):
    """
        pulls link api data and saves to ClashCommander db

        Args:
            linkapi_client (LinkApiClient): client for linkAPI
            discord_user_id (int): discord user id

        Raises:
            ConflictError: player couldn't be claimed in db
                (either claimed by other player or other error)
    """

    # get link api data
    try:
        player_links = linkapi_client.get_discord_user_link(
            discord_user_id=discord_user_id
        )
    except LoginError:
        print("Error logging into LinkAPI")
        return
    # no player links found, so there is nothing to pull, return
    except NotFoundError:
        print(f"Player tags for discord user id {discord_user_id} "
              f"not found in LinkAPI db")
        return

    claimed_players = db_responder.read_player_list(
        discord_user_id=discord_user_id)

    # add player claim if player has not been claimed by user or anyone else
    for player_link in player_links:

        # prepping player synced value
        player_synced = False

        # check if player has been claimed by user
        for player_claim in claimed_players:

            # player has already been claimed by user
            # move to next player in player links
            # by breaking out of current for loop
            if player_link.player_tag == player_claim.player_tag:
                player_synced = True
                break

        # player data already synced
        # move to next player
        if player_synced:
            continue

        # player data not synced to user
        # search for player claimed by other user
        other_player_claim = db_responder.read_player_from_tag(
            player_tag=player_link.player_tag)

        # player claim found from other user
        # raise conflict error
        if other_player_claim:
            raise ConflictError("Player claimed by different user")

        # other player claim not found
        # claim player
        new_player_claim = db_responder.claim_player(
            discord_user_id=player_link.discord_user_id,
            player_tag=player_link.player_tag
        )

        # player couldn't be claimed
        if not new_player_claim:
            raise ConflictError("Player could not be claimed")

        # player claimed correctly
        # move on to next player
        continue


def push_to_link(
    linkapi_client: LinkApiClient,
    discord_user_id: int
):
    """
        pushes ClashCommander db data to LinkAPI

        Args:
            linkapi_client (LinkApiClient): client for linkAPI
            discord_user_id (int): discord user id

        Raises:
            ConflictError: player couldn't be linked to LinkAPI
                (either claimed by other player or other error)
    """

    claimed_players = db_responder.read_player_list(
        discord_user_id=discord_user_id)

    # no claimed players found, so there is nothing to push, return
    if claimed_players == []:
        return

    # get link api data
    try:
        player_links = linkapi_client.get_discord_user_link(
            discord_user_id=discord_user_id
        )
    except LoginError:
        player_links = []
        print("Error logging into LinkAPI")
    # no player links found, set player_links to empty list []
    except NotFoundError:
        player_links = []

    # add player link if player has not been linked by user or anyone else
    for player_claim in claimed_players:

        # prepping player synced value
        player_synced = False

        # check if player has been linked by user
        for player_link in player_links:

            # player has already been linked by user
            # move to next player in claimed players
            # by breaking out of current for loop
            if player_claim.player_tag == player_link.player_tag:
                player_synced = True
                break

        # player data already synced
        # move to next player
        if player_synced:
            continue

        # player data not synced to user
        # search for player link by other user
        try:
            other_player_link = linkapi_client.get_player_tag_link(
                player_tag=player_claim.player_tag
            )
        except LoginError:
            print("Error logging into LinkAPI")
        # not found, set other player link to None
        except NotFoundError:
            print(f"Player tag {player_claim.player_tag} "
                  f"not found in LinkAPI db")
            other_player_link = None
        except InvalidTagError:
            print(f"Player tag {player_claim.player_tag} not valid")

        # player link found from other user
        # raise conflict error
        if other_player_link:
            raise ConflictError("Player claimed by different user")

        # other player link not found
        # link player
        try:
            linkapi_client.add_link(
                player_tag=player_claim.player_tag,
                discord_user_id=discord_user_id
            )
        except LoginError:
            print("Error logging into LinkAPI")
        except InvalidTagError:
            print(f"Player tag {player_claim.player_tag} not valid")
        except ConflictError:
            print("Player tag {player_claim.player_tag} already in LinkAPI DB")
            raise ConflictError("Tag already in DB")
