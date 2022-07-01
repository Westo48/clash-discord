from disnake import (
    ApplicationCommandInteraction as Interaction
)
from disnake.ui.view import View
from views.help_view import (
    HelpMainView as main_view,
)
from buttons.help_categories import (
    HelpSuperUserBtn as superuser_btn,
    HelpAdminBtn as admin_btn,
    HelpClientBtn as client_btn,
    HelpDiscordBtn as discord_btn,
    HelpAnnounceBtn as announce_btn,
    HelpPlayerBtn as player_btn,
    HelpClanBtn as clan_btn,
    HelpWarBtn as war_btn,
    HelpCWLBtn as cwl_btn
)
from data import ClashDiscord_Client_Data as Client_Data
from responders import (
    RazBotDB_Responder as db_responder
)


def help_main(
        bot,
        inter: Interaction,
        client_data: Client_Data.ClashDiscord_Data):

    help_dict = {
        'field_dict_list': [],
        'view': View
    }
    button_list = []

    # get the db user
    db_user = db_responder.read_user(inter.author.id)

    # return client user help if user not found
    if db_user is None:
        for category in client_data.bot_categories:
            if category.brief == "client":
                help_dict['field_dict_list'].append({
                    'name': f"{category.emoji} {category.name}",
                    'value': category.description
                })

                button_list.append(
                    client_btn(bot=bot, client_data=client_data))

                help_dict['view'] = main_view(
                    buttons=button_list)

                return help_dict

    # get the db guild
    db_guild = db_responder.read_guild(inter.guild.id)

    for category in client_data.bot_categories:

        # super user check
        if category.brief == "superuser":
            if db_user.super_user:
                help_dict['field_dict_list'].append({
                    'name': f"{category.emoji} {category.name}",
                    'value': category.description
                })

                button_list.append(
                    superuser_btn(bot=bot, client_data=client_data))

            continue

        # admin check
        elif category.brief == "admin":
            # user is admin or user is guild admin
            if db_user.admin or (db_guild.admin_user_id == inter.author.id):
                help_dict['field_dict_list'].append({
                    'name': f"{category.emoji} {category.name}",
                    'value': category.description
                })

                button_list.append(
                    admin_btn(bot=bot, client_data=client_data))

            continue

        elif category.brief == "client":
            help_dict['field_dict_list'].append({
                'name': f"{category.emoji} {category.name}",
                'value': category.description
            })

            button_list.append(
                client_btn(bot=bot, client_data=client_data))

            continue

        elif category.brief == "discord":
            help_dict['field_dict_list'].append({
                'name': f"{category.emoji} {category.name}",
                'value': category.description
            })

            button_list.append(
                discord_btn(bot=bot, client_data=client_data))

            continue

        elif category.brief == "announce":
            help_dict['field_dict_list'].append({
                'name': f"{category.emoji} {category.name}",
                'value': category.description
            })

            button_list.append(
                announce_btn(bot=bot, client_data=client_data))

            continue

        elif category.brief == "player":
            help_dict['field_dict_list'].append({
                'name': f"{category.emoji} {category.name}",
                'value': category.description
            })

            button_list.append(
                player_btn(bot=bot, client_data=client_data))

            continue

        elif category.brief == "clan":
            help_dict['field_dict_list'].append({
                'name': f"{category.emoji} {category.name}",
                'value': category.description
            })

            button_list.append(
                clan_btn(bot=bot, client_data=client_data))

            continue

        elif category.brief == "war":
            help_dict['field_dict_list'].append({
                'name': f"{category.emoji} {category.name}",
                'value': category.description
            })

            button_list.append(
                war_btn(bot=bot, client_data=client_data))

            continue

        elif category.brief == "cwl":
            help_dict['field_dict_list'].append({
                'name': f"{category.emoji} {category.name}",
                'value': category.description
            })

            button_list.append(
                cwl_btn(bot=bot, client_data=client_data))

            continue

    help_dict['view'] = main_view(
        buttons=button_list)

    return help_dict
