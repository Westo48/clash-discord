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


class ClashDiscord_Emoji(object):
    """
        ClashDiscord_Emoji: object for client emoji's

            Instance Attributes
                discord_id (int): id for emoji in discord
                name (str): emoji name
                discord_name (str): formatted discord_name emoji name
                description (str): description for emoji
    """

    def __init__(self, discord_id, name, discord_name, description):
        self.discord_id = discord_id
        self.name = name
        self.discord_name = discord_name
        self.description = description


class ClashDiscord_Data(object):
    """
        ClashDiscord_Data: object for ClashDiscord client data

            Instance Attributes
                version (str): client version
                prefix (str): prefix for command calls
                embed_color (int): color integer for embed commands
                back_emoji (str): emoji for back button
                bot_categories (list): list of Bot_Category objects
                emojis (list[obj]): list of emoji objects
    """

    version = '2.1.1'
    prefix = '/'
    embed_color = 1752220
    back_emoji = '◀️'
    bot_categories = [
        ClashDiscord_Category(
            'Super User', 'superuser',
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
            'War', 'war', 'War based commands', '⚔️'),
        ClashDiscord_Category(
            'CWL', 'cwl', 'CWL based commands', '🔱')
    ]

    emojis = [

    ]
