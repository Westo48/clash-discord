import requests
from linkAPI.errors import (
    LoginError,
    ConflictError,
    NotFoundError,
    InvalidTagError,
    AuthorizationError
)
from linkAPI.playerLinkModel import PlayerLink


class LinkApiClient(object):
    """

    """

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    token = ""

    base_url = "https://cocdiscord.link"
    login_url = f"/login"
    links_url = f"/links/"
    batch_url = f"/batch"

    def login(self):
        """
            LinkAPI Client login

            errors:
                Login Error
        """
        request_url = self.base_url + self.login_url
        payload = {
            'username': self.username,
            'password': self.password
        }

        r = requests.post(url=request_url, json=payload)

        if r.status_code == 401:
            raise LoginError("Invalid login credentials")

        self.token = r.json()['token']

    def instanciate_player_link(self, player_tag: str, discord_user_id: str):
        return PlayerLink(
            player_tag=player_tag,
            discord_user_id=int(discord_user_id)
        )

    def instanciate_player_link_list(self, player_links: list):
        return_list = []
        for link in player_links:
            return_list.append(
                self.instanciate_player_link(
                    player_tag=link['playerTag'],
                    discord_user_id=link['discordId']
                )
            )

        return return_list

    def get_discord_user_link(self, discord_user_id: int):
        """
            gets linked players using discord ID

            Args:
                discord_user_id (int): user ID from discord

            Raises:
                LoginError: failed login
                NotFoundError: data not found

            Returns:
                list: list of PlayerLink objects
                    player_tag, discord_user_id
        """
        if self.token == "":
            try:
                self.login()
            except LoginError:
                raise LoginError("Invalid login credentials")

        url = self.base_url + self.links_url + str(discord_user_id)
        header = {
            'Authorization': f"Bearer {self.token}"
        }

        r = requests.get(url=url, headers=header)

        # invalid token
        if r.status_code == 401:
            try:
                self.login()
                r = requests.get(url=url, headers=header)
            except LoginError:
                raise LoginError("Invalid login credentials")

        # no user is found with requested id
        if r.status_code == 404:
            raise NotFoundError("No user found with requested id")

        # no user is found with requested id
        if r.json() == []:
            raise NotFoundError("No user found with requested id")

        player_links = self.instanciate_player_link_list(player_links=r.json())

        return player_links

    def get_player_tag_link(self, player_tag: str):
        """
            gets linked player using player tag

            Args:
                player_tag (str): clash of clans player tag

            Raises:
                LoginError: failed login
                NotFoundError: data not found
                InvalidTagError: invalid player tag

            Returns:
                PlayerLink: Player Link Object
                    player_tag, discord_user_id
        """

        # change string to upper
        player_tag = player_tag.upper()
        # remove '#' from player tag
        player_tag = player_tag.replace('#', '')

        if self.token == "":
            try:
                self.login()
            except LoginError:
                raise LoginError("Invalid login credentials")

        url = self.base_url + self.links_url + player_tag
        header = {
            'Authorization': f"Bearer {self.token}"
        }

        r = requests.get(url=url, headers=header)

        # invalid token
        if r.status_code == 401:
            try:
                self.login()
                r = requests.get(url=url, headers=header)
            except LoginError:
                raise LoginError("Invalid login credentials")

        # no player is found with requested tag
        if r.status_code == 404:
            raise NotFoundError("No player found with requested tag")

        # tag is invalid
        if r.status_code == 400:
            raise InvalidTagError("Invalid player tag")

        # no player is found with requested tag
        if r.json() == []:
            raise NotFoundError("No player found with requested tag")

        response_link = r.json()

        player_link = self.instanciate_player_link(
            player_tag=response_link[0]['playerTag'],
            discord_user_id=response_link[0]['discordId']
        )

        return player_link

    def get_batch_links(self, batch_list: list):
        """
            gets linked player using list of discord ids and player tags

            Args:
                batch_list (list): list of strings for 
                    discord ids and player tags

            Raises:
                LoginError: failed login
                NotFoundError: data not found

            Returns:
                list: list of PlayerLink objects
                    player_tag, discord_user_id
        """

        if self.token == "":
            try:
                self.login()
            except LoginError:
                raise LoginError("Invalid login credentials")

        url = self.base_url + self.batch_url
        header = {
            'Authorization': f"Bearer {self.token}"
        }
        payload = []
        # adding items in batch list and formatting player tags
        for item in batch_list:
            payload_item = item.upper()
            payload_item = payload_item.replace('#', '')
            payload.append(payload_item)

        r = requests.post(url=url, headers=header, json=payload)

        # invalid token
        if r.status_code == 401:
            try:
                self.login()
                r = requests.get(url=url, headers=header)
            except LoginError:
                raise LoginError("Invalid login credentials")

        # no discord user or player tag found
        if r.status_code == 404:
            raise NotFoundError("data is not found with supplied information")

        # no user is found with requested id
        if r.json() == []:
            raise NotFoundError("data is not found with supplied information")

        player_links = self.instanciate_player_link_list(player_links=r.json())

        return player_links

    def add_link(self, player_tag: str, discord_user_id: int):
        """
            adds a player link

            Args:
                player_tag (str): clash of clans player tag
                discord_user_id (int): user ID from discord

            Raises:
                LoginError: failed login
                InvalidTagError: invalid player tag
                ConflictError: link data already in db

            Returns:
                PlayerLink: Player Link Object
                    player_tag, discord_user_id
        """

        # change string to upper
        player_tag = player_tag.upper()
        # remove '#' from player tag
        player_tag = player_tag.replace('#', '')

        if self.token == "":
            try:
                self.login()
            except LoginError:
                raise LoginError("Invalid login credentials")

        url = self.base_url + self.links_url
        header = {
            'Authorization': f"Bearer {self.token}"
        }
        payload = {
            'playerTag': f"{player_tag}",
            'discordId': f"{discord_user_id}"
        }

        r = requests.post(url=url, headers=header, json=payload)

        # invalid token
        if r.status_code == 401:
            try:
                self.login()
                r = requests.get(url=url, headers=header)
            except LoginError:
                raise LoginError("Invalid login credentials")

        # tag is invalid
        if r.status_code == 400:
            raise InvalidTagError("Invalid player tag")

        # tag is already in DB
        if r.status_code == 409:
            raise ConflictError("Tag already in DB")

        if r.status_code == 200:
            player_link = self.instanciate_player_link(
                player_tag=player_tag,
                discord_user_id=discord_user_id)
            return player_link

    def delete_link(self, player_tag: str):
        """
            deletes a player link

            Args:
                player_tag (str): _description_

            Raises:
                LoginError: failed login
                NotFoundError: data not found
        """

        # change string to upper
        player_tag = player_tag.upper()
        # remove '#' from player tag
        player_tag = player_tag.replace('#', '')

        if self.token == "":
            try:
                self.login()
            except LoginError:
                raise LoginError("Invalid login credentials")

        url = self.base_url + self.links_url + player_tag
        header = {
            'Authorization': f"Bearer {self.token}"
        }

        r = requests.delete(url=url, headers=header)

        # invalid token
        if r.status_code == 401:
            try:
                self.login()
                r = requests.get(url=url, headers=header)
            except LoginError:
                raise LoginError("Invalid login credentials")

        # tag is invalid
        if r.status_code == 404:
            raise NotFoundError("Tag not found in DB")
