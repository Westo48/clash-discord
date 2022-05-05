class PlayerLink(object):
    """

        PlayerLink: object for LinkAPI player links

            Instance Attributes
                player_tag (str): clash of clans player tag
                discord_user_id (int): discord user id
    """

    def __init__(self, player_tag, discord_user_id):
        self.player_tag = player_tag
        self.discord_user_id = discord_user_id
