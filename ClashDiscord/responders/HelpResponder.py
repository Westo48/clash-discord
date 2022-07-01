from disnake.ext.commands import Bot
from disnake import (
    ApplicationCommandInteraction as Interaction
)
from data import ClashDiscord_Client_Data as Client_Data
from responders import (
    RazBotDB_Responder as db_responder
)


def help_super_user(
        inter: Interaction,
        all_commands: list,
        bot_category: Client_Data.ClashDiscord_Category):

    field_dict_list = []

    db_user = db_responder.read_user(inter.author.id)

    # if user is not super user
    if not db_user.super_user:
        field_dict_list.append({
            'name': "user is not super user",
            'value': "must be super user to view super user commands"
        })
        return field_dict_list

    for parent in all_commands.values():
        # command is not in the correct category
        if not bot_category.brief == parent.name:
            continue

        field_dict_list = help_command_dict_list(parent)
    return field_dict_list


def help_admin(
        inter: Interaction,
        all_commands: list,
        bot_category: Client_Data.ClashDiscord_Category):

    field_dict_list = []

    db_guild = db_responder.read_guild(inter.guild.id)

    # guild not claimed
    if db_guild is None:
        field_dict_list.append({
            'name': "server not claimed",
            'value': "please claim server using `admin server claim`"
        })
        return field_dict_list

    db_user = db_responder.read_user(inter.author.id)

    # user is not guild admin and is not an admin
    if (db_guild.admin_user_id != db_user.discord_id
            and not db_user.admin):
        field_dict_list.append({
            'name': "user is not admin user",
            'value': "must be admin user to view admin user commands"
        })
        return field_dict_list

    for parent in all_commands.values():
        # command is not in the correct category
        if not bot_category.brief == parent.name:
            continue

        field_dict_list = help_command_dict_list(parent)

        if len(field_dict_list) == 0:
            field_dict_list.append({
                'name': "server not claimed",
                'value': "please claim server using `admin server claim`"
            })
            return field_dict_list

    return field_dict_list


def help_client(
        inter: Interaction,
        all_commands: list,
        bot_category: Client_Data.ClashDiscord_Category):

    field_dict_list = []

    db_guild = db_responder.read_guild(inter.guild.id)

    # guild not claimed
    if db_guild is None:
        field_dict_list.append({
            'name': "server not claimed",
            'value': "please claim server using `admin server claim`"
        })
        return field_dict_list

    for parent in all_commands.values():
        # command is not in the correct category
        if not bot_category.brief == parent.name:
            continue

        field_dict_list = help_command_dict_list(parent)

        if len(field_dict_list) == 0:
            field_dict_list.append({
                'name': "server not claimed",
                'value': "please claim server using `admin server claim`"
            })
            return field_dict_list

    return field_dict_list


def help_category_list(
        inter: Interaction,
        all_commands: list,
        bot_category: Client_Data.ClashDiscord_Category):

    field_dict_list = []

    for parent in all_commands.values():
        # command is not in the correct category
        if not bot_category.brief == parent.name:
            continue

        field_dict_list = help_command_dict_list(parent)

    return field_dict_list


def help_command_dict_list(parent):
    field_dict_list = []

    # repeating for each child
    for group in parent.children.values():
        if hasattr(group, 'children'):
            for child in group.children.values():
                option_string = ""
                for param in child.option.options:
                    if param.name == "option":
                        for choice in param.choices:
                            option_string += f"{choice.name}, "

                value_string = child.docstring["description"]

                # command options found
                if option_string != "":
                    value_string = (f"command options: `{option_string[:-2]}`\n"
                                    + value_string)

                field_dict_list.append({
                    'name': child.qualified_name,
                    'value': value_string
                })

        else:
            option_string = ""
            for param in group.option.options:
                if param.name == "option":
                    for choice in param.choices:
                        option_string += f"{choice.name}, "

            value_string = group.docstring["description"]

            # command options found
            if option_string != "":
                value_string = (f"command options: `{option_string[:-2]}`\n"
                                + value_string)

            field_dict_list.append({
                'name': group.qualified_name,
                'value': value_string
            })
    return field_dict_list
