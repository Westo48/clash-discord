class ClashDiscord_Category(object):
    """
        ClashDiscord_Category: object for client command categories

            Instance Attributes
                name (str): category name
                brief (str): formatted brief category name
                description (str): category description
                emoji (str): emoji for category
    """

    def __init__(self, name, brief, description, emoji):
        self.name = name
        self.brief = brief
        self.description = description
        self.emoji = emoji


class ClashDiscord_Data(object):
    """
        ClashDiscord_Data: object for ClashDiscord client data

            Instance Attributes
                version (str): client version
                embed_color (int): color integer for embed commands
                back_emoji (str): emoji for back button
                bot_categories (list): list of Bot_Category objects
    """

    version = '1.2.0'
    embed_color = 1752220
    back_emoji = '◀️'
    bot_categories = [
        ClashDiscord_Category(
            'Client Super User', 'clientsuperuser',
            'ClashDiscord client based commands for super user', '🧠'),
        ClashDiscord_Category(
            'Client', 'client', 'ClashDiscord client based commands', '🤖'),
        ClashDiscord_Category(
            'Discord', 'discord', 'Discord based commands', '💻'),
        ClashDiscord_Category(
            'Player', 'player', 'Player based commands', '😎'),
        ClashDiscord_Category(
            'Clan', 'clan', 'Clan based commands', '🏠'),
        ClashDiscord_Category(
            'War', 'war', 'War based commands', '🗡️'),
        ClashDiscord_Category(
            'CWL Group', 'cwlgroup', 'CWL Group based commands', '🔱'),
        ClashDiscord_Category(
            'CWL War', 'cwlwar', 'CWL War based commands', '⚔️')
    ]
