import requests
from linkAPI.errors import (
    LoginError,
    ConflictError,
    NotFoundError,
    InvalidTagError,
    AuthorizationError
)


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
        request_url = self.base_url + self.login_url
        payload = {
            'username': self.username,
            'password': self.password
        }

        r = requests.post(url=request_url, json=payload)

        if r.status_code == 401:
            raise LoginError("Invalid login credentials")

        self.token = r.json()['token']

    def get_discord_user_link(self, discord_user_id: int):
        if self.token == "":
            try:
                self.login()
            except LoginError:
                raise LoginError("Invalid login credentials")

        url = self.base_url + self.links_url + discord_user_id
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

        return r.json()

    def get_player_tag_link(self, player_tag: str):
        player_tag = player_tag.upper()
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

        return r.json()

    def get_batch_links(self, batch_list: list):

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
        for item in batch_list:
            payload.append(item.upper())

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

        return r.json()

    def add_link(self, player_tag: str, discord_user_id: int):
        player_tag = player_tag.upper()
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
            return {
                'playerTag': player_tag,
                'discordId': discord_user_id
            }

    def delete_link(self, player_tag: str):
        player_tag = player_tag.upper()
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
