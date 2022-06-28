import disnake
from disnake.ext.commands import Bot

from data import ClashDiscord_Client_Data as ClientData
from views.help_view import HelpMainView
from buttons.help_main import HelpMainBtn
from responders import (
    DiscordResponder as discord_responder,
    HelpResponder as help_responder,
    RazBotDB_Responder as db_responder
)


class HelpSuperUserBtn(disnake.ui.Button):
    def __init__(
            self, bot: Bot, client_data: ClientData.ClashDiscord_Data):
        super().__init__(
            label="Super User", style=disnake.ButtonStyle.primary)
        self.bot = bot
        self.client_data = client_data

    async def callback(
            self,
            inter: disnake.MessageInteraction):

        await inter.response.defer()

        field_dict_list = []
        db_user = db_responder.read_user(inter.author.id)

        # user not claimed
        if db_user is None:
            field_dict_list.append({
                'name': "user is not super user",
                'value': "must be super user to view super user commands"
            })

        # if user is not super user
        elif not db_user.super_user:
            field_dict_list.append({
                'name': "user is not super user",
                'value': "must be super user to view super user commands"
            })

        # db user is super user
        else:
            # get the proper message
            for category in self.client_data.bot_categories:
                # category name matches button label
                if category.name == self.label:
                    field_dict_list.extend(help_responder.help_super_user(
                        inter=inter, all_commands=self.bot.all_slash_commands,
                        bot_category=category))

                    break

            if len(field_dict_list) == 0:
                field_dict_list.append({
                    'name': f"{self.label} category not found",
                    'value': f"please let {self.client_data.author} know"
                })

        view = HelpMainView(
            buttons=[HelpMainBtn(bot=self.bot, client_data=self.client_data)])

        embed_list = discord_responder.embed_message(
            icon_url=self.bot.user.avatar.url,
            title=f"{inter.me.display_name} {self.label} help menu",
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author=inter.author
        )

        # edit the original message with the updated embeds
        await inter.edit_original_message(embeds=embed_list, view=view)


class HelpAdminBtn(disnake.ui.Button):
    def __init__(
            self, bot: Bot, client_data: ClientData.ClashDiscord_Data):
        super().__init__(
            label="Admin", style=disnake.ButtonStyle.primary)
        self.bot = bot
        self.client_data = client_data

    async def callback(
        self,
        inter: disnake.ApplicationCommandInteraction
    ):
        await inter.response.defer()

        field_dict_list = []
        db_user = db_responder.read_user(inter.author.id)
        db_guild = db_responder.read_guild(inter.guild.id)

        # user not claimed
        if db_user is None:
            field_dict_list.append({
                'name': "user is not admin user",
                'value': "must be admin user to view admin user commands"
            })

        # guild not claimed
        elif db_guild is None:
            field_dict_list.append({
                'name': "guild not claimed",
                'value': "please claim guild using `admin guild claim`"
            })

        # user is not guild admin and is not an admin
        elif (db_guild.admin_user_id != db_user.discord_id
                and not db_user.admin):
            field_dict_list.append({
                'name': "user is not admin user",
                'value': "must be admin user to view admin user commands"
            })

        else:
            # get the proper message
            for category in self.client_data.bot_categories:
                # category name matches button label
                if category.name == self.label:
                    field_dict_list.extend(help_responder.help_admin(
                        inter=inter, all_commands=self.bot.all_slash_commands,
                        bot_category=category))

                    break

            if len(field_dict_list) == 0:
                field_dict_list.append({
                    'name': f"{self.label} category not found",
                    'value': f"please let {self.client_data.author} know"
                })

        view = HelpMainView(
            buttons=[HelpMainBtn(bot=self.bot, client_data=self.client_data)])

        embed_list = discord_responder.embed_message(
            icon_url=self.bot.user.avatar.url,
            title=f"{inter.me.display_name} {self.label} help menu",
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author=inter.author
        )

        # edit the original message with the updated embeds
        await inter.edit_original_message(embeds=embed_list, view=view)


class HelpClientBtn(disnake.ui.Button):
    def __init__(
            self, bot: Bot, client_data: ClientData.ClashDiscord_Data):
        super().__init__(
            label="Client", style=disnake.ButtonStyle.primary)
        self.bot = bot
        self.client_data = client_data

    async def callback(
        self,
        inter: disnake.MessageInteraction
    ):
        await inter.response.defer()

        field_dict_list = []

        # get the proper message
        for category in self.client_data.bot_categories:
            # category name matches button label
            if category.name == self.label:
                field_dict_list.extend(help_responder.help_client(
                    inter=inter, all_commands=self.bot.all_slash_commands,
                    bot_category=category))

                break

        if len(field_dict_list) == 0:
            field_dict_list.append({
                'name': f"{self.label} category not found",
                'value': f"please let {self.client_data.author} know"
            })

        view = HelpMainView(
            buttons=[HelpMainBtn(bot=self.bot, client_data=self.client_data)])

        embed_list = discord_responder.embed_message(
            icon_url=self.bot.user.avatar.url,
            title=f"{inter.me.display_name} {self.label} help menu",
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author=inter.author
        )

        # edit the original message with the updated embeds
        await inter.edit_original_message(embeds=embed_list, view=view)


class HelpDiscordBtn(disnake.ui.Button):
    def __init__(
            self, bot: Bot, client_data: ClientData.ClashDiscord_Data):
        super().__init__(
            label="Discord", style=disnake.ButtonStyle.primary)
        self.bot = bot
        self.client_data = client_data

    async def callback(
        self,
        inter: disnake.MessageInteraction
    ):
        await inter.response.defer()

        field_dict_list = []

        # get the proper message
        for category in self.client_data.bot_categories:
            # category name matches button label
            if category.name == self.label:
                field_dict_list.extend(help_responder.help_category_list(
                    inter=inter, all_commands=self.bot.all_slash_commands,
                    bot_category=category))

                break

        if len(field_dict_list) == 0:
            field_dict_list.append({
                'name': f"{self.label} category not found",
                'value': f"please let {self.client_data.author} know"
            })

        view = HelpMainView(
            buttons=[HelpMainBtn(bot=self.bot, client_data=self.client_data)])

        embed_list = discord_responder.embed_message(
            icon_url=self.bot.user.avatar.url,
            title=f"{inter.me.display_name} {self.label} help menu",
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author=inter.author
        )

        # edit the original message with the updated embeds
        await inter.edit_original_message(embeds=embed_list, view=view)


class HelpAnnounceBtn(disnake.ui.Button):
    def __init__(
            self, bot: Bot, client_data: ClientData.ClashDiscord_Data):
        super().__init__(
            label="Announce", style=disnake.ButtonStyle.primary)
        self.bot = bot
        self.client_data = client_data

    async def callback(
        self,
        inter: disnake.MessageInteraction
    ):
        await inter.response.defer()

        field_dict_list = []

        # get the proper message
        for category in self.client_data.bot_categories:
            # category name matches button label
            if category.name == self.label:
                field_dict_list.extend(help_responder.help_category_list(
                    inter=inter, all_commands=self.bot.all_slash_commands,
                    bot_category=category))

                break

        if len(field_dict_list) == 0:
            field_dict_list.append({
                'name': f"{self.label} category not found",
                'value': f"please let {self.client_data.author} know"
            })

        view = HelpMainView(
            buttons=[HelpMainBtn(bot=self.bot, client_data=self.client_data)])

        embed_list = discord_responder.embed_message(
            icon_url=self.bot.user.avatar.url,
            title=f"{inter.me.display_name} {self.label} help menu",
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author=inter.author
        )

        # edit the original message with the updated embeds
        await inter.edit_original_message(embeds=embed_list, view=view)


class HelpPlayerBtn(disnake.ui.Button):
    def __init__(
            self, bot: Bot, client_data: ClientData.ClashDiscord_Data):
        super().__init__(
            label="Player", style=disnake.ButtonStyle.primary)
        self.bot = bot
        self.client_data = client_data

    async def callback(
        self,
        inter: disnake.MessageInteraction
    ):
        await inter.response.defer()

        field_dict_list = []

        # get the proper message
        for category in self.client_data.bot_categories:
            # category name matches button label
            if category.name == self.label:
                field_dict_list.extend(help_responder.help_category_list(
                    inter=inter, all_commands=self.bot.all_slash_commands,
                    bot_category=category))

                break

        if len(field_dict_list) == 0:
            field_dict_list.append({
                'name': f"{self.label} category not found",
                'value': f"please let {self.client_data.author} know"
            })

        view = HelpMainView(
            buttons=[HelpMainBtn(bot=self.bot, client_data=self.client_data)])

        embed_list = discord_responder.embed_message(
            icon_url=self.bot.user.avatar.url,
            title=f"{inter.me.display_name} {self.label} help menu",
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author=inter.author
        )

        # edit the original message with the updated embeds
        await inter.edit_original_message(embeds=embed_list, view=view)


class HelpClanBtn(disnake.ui.Button):
    def __init__(
            self, bot: Bot, client_data: ClientData.ClashDiscord_Data):
        super().__init__(
            label="Clan", style=disnake.ButtonStyle.primary)
        self.bot = bot
        self.client_data = client_data

    async def callback(
        self,
        inter: disnake.MessageInteraction
    ):
        await inter.response.defer()

        field_dict_list = []

        # get the proper message
        for category in self.client_data.bot_categories:
            # category name matches button label
            if category.name == self.label:
                field_dict_list.extend(help_responder.help_category_list(
                    inter=inter, all_commands=self.bot.all_slash_commands,
                    bot_category=category))

                break

        if len(field_dict_list) == 0:
            field_dict_list.append({
                'name': f"{self.label} category not found",
                'value': f"please let {self.client_data.author} know"
            })

        view = HelpMainView(
            buttons=[HelpMainBtn(bot=self.bot, client_data=self.client_data)])

        embed_list = discord_responder.embed_message(
            icon_url=self.bot.user.avatar.url,
            title=f"{inter.me.display_name} {self.label} help menu",
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author=inter.author
        )

        # edit the original message with the updated embeds
        await inter.edit_original_message(embeds=embed_list, view=view)


class HelpWarBtn(disnake.ui.Button):
    def __init__(
            self, bot: Bot, client_data: ClientData.ClashDiscord_Data):
        super().__init__(
            label="War", style=disnake.ButtonStyle.primary)
        self.bot = bot
        self.client_data = client_data

    async def callback(
        self,
        inter: disnake.MessageInteraction
    ):
        await inter.response.defer()

        field_dict_list = []

        # get the proper message
        for category in self.client_data.bot_categories:
            # category name matches button label
            if category.name == self.label:
                field_dict_list.extend(help_responder.help_category_list(
                    inter=inter, all_commands=self.bot.all_slash_commands,
                    bot_category=category))

                break

        if len(field_dict_list) == 0:
            field_dict_list.append({
                'name': f"{self.label} category not found",
                'value': f"please let {self.client_data.author} know"
            })

        view = HelpMainView(
            buttons=[HelpMainBtn(bot=self.bot, client_data=self.client_data)])

        embed_list = discord_responder.embed_message(
            icon_url=self.bot.user.avatar.url,
            title=f"{inter.me.display_name} {self.label} help menu",
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author=inter.author
        )

        # edit the original message with the updated embeds
        await inter.edit_original_message(embeds=embed_list, view=view)


class HelpCWLBtn(disnake.ui.Button):
    def __init__(
            self, bot: Bot, client_data: ClientData.ClashDiscord_Data):
        super().__init__(
            label="CWL", style=disnake.ButtonStyle.primary)
        self.bot = bot
        self.client_data = client_data

    async def callback(
        self,
        inter: disnake.MessageInteraction
    ):
        await inter.response.defer()

        field_dict_list = []

        # get the proper message
        for category in self.client_data.bot_categories:
            # category name matches button label
            if category.name == self.label:
                field_dict_list.extend(help_responder.help_category_list(
                    inter=inter, all_commands=self.bot.all_slash_commands,
                    bot_category=category))

                break

        if len(field_dict_list) == 0:
            field_dict_list.append({
                'name': f"{self.label} category not found",
                'value': f"please let {self.client_data.author} know"
            })

        view = HelpMainView(
            buttons=[HelpMainBtn(bot=self.bot, client_data=self.client_data)])

        embed_list = discord_responder.embed_message(
            icon_url=self.bot.user.avatar.url,
            title=f"{inter.me.display_name} {self.label} help menu",
            bot_user_name=inter.me.display_name,
            field_list=field_dict_list,
            author=inter.author
        )

        # edit the original message with the updated embeds
        await inter.edit_original_message(embeds=embed_list, view=view)
