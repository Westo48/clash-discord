import Clan
from Player import super_troop_list


# PLAYER

def unit_lvl(player_obj, unit_obj, unit_name):
    if not unit_obj:
        # unit not found response
        return (
            f"could not find {unit_name}, "
            f"you either do not have it unlocked or "
            f"it is misspelled."
        )

    if unit_obj.lvl == unit_obj.max_lvl:
        # unit is max lvl
        return (
            f"{player_obj.name} has lvl {unit_obj.lvl} {unit_obj.name}, "
            f"which is max."
        )
    elif unit_obj.lvl == unit_obj.th_max:
        # unit is max for th, but not total max
        return (
            f"{player_obj.name} has lvl {unit_obj.lvl} {unit_obj.name}, "
            f"which is max for TH {player_obj.th_lvl}, "
            f"max {unit_obj.name} is {unit_obj.max_lvl}."
        )
    else:
        # unit is not max for th nor is it total max
        return (
            f"{player_obj.name} has lvl {unit_obj.lvl} {unit_obj.name}, "
            f"max for TH {player_obj.th_lvl} is {unit_obj.th_max}, "
            f"max {unit_obj.name} is {unit_obj.max_lvl}."
        )


# ? discontinue this function
def unit_lvl_all(player_obj):
    response_list = []
    response_list.append(f'{player_obj.name} units:')
    for hero_obj in player_obj.heroes:
        if hero_obj.village == 'home':
            response_list.append(unit_lvl(
                player_obj, hero_obj, hero_obj.name))
            response_list.append('__________')
    for troop_obj in player_obj.troops:
        if troop_obj.village == 'home':
            response_list.append(unit_lvl(
                player_obj, troop_obj, troop_obj.name))
            response_list.append('__________')
    for spell_obj in player_obj.spells:
        if spell_obj.village == 'home':
            response_list.append(unit_lvl(
                player_obj, spell_obj, spell_obj.name))
            response_list.append('__________')
    # removing trailing '__________'
    del response_list[-1]
    return response_list


def active_super_troops(player_obj, active_super_troops):
    if len(active_super_troops) == 0:
        return f"{player_obj.name} does not have any active super troops."
    else:
        super_troop_string = ''
        for super_troop in active_super_troops:
            super_troop_string += f'{super_troop.name} and '

        # cuts the last 5 characters ' and ' from the string
        super_troop_string = super_troop_string[:-5]

        return f"{player_obj.name} has {super_troop_string} currently active."


# DISCORD

def role_add_remove_list(needed_role_list, current_role_list):
    """
        Takes in list of needed and current role id's and
        returns add and remove lists of discord role id's

        Args:
            list
                needed_role_list (int): list of needed discord's role id
            list
                needed_role_list (int): list of current discord's role id

        Returns:
            add_roles_list: list of role id's to add to discord user
            remove_roles_list: list of role id's to remove from discord user
    """

    # add_list
    add_list = []
    for needed_role in needed_role_list:
        if needed_role not in current_role_list:
            # needed and not currently set
            # add to add list
            add_list.append(needed_role)

    # remove_list
    remove_list = []
    for current_role in current_role_list:
        if current_role not in needed_role_list:
            # currently set and not needed
            # add to remove list
            remove_list.append(current_role)

    return add_list, remove_list


def role_switch(player, user_roles, client_clans):
    """
        takes in player role and list of discord user roles,
        returns new and old role
    """

    add_roles = []
    remove_roles = []

    if player is None:

        has_community = False
        # remove all listed roles (clan, member, and uninitiated)
        # give community role
        for role in user_roles:
            # checking for clan roles
            for clan in client_clans:
                if role.name == clan.name:
                    remove_roles.append(role.name)

            # checking for member roles
            if role.name == 'leader':
                remove_roles.append('leader')
            if role.name == 'co-leader':
                remove_roles.append('co-leader')
            if role.name == 'elder':
                remove_roles.append('elder')
            if role.name == 'member':
                remove_roles.append('member')
            if role.name == 'uninitiated':
                remove_roles.append('uninitiated')
            if role.name == 'community':
                has_community = True

        # add community role if community is not False
        if not has_community:
            add_roles.append('community')

        return add_roles, remove_roles

    # checking if the user's clan roles need changing
    old_clan = None
    for role in user_roles:
        for clan in client_clans:
            if role.name == clan.name:
                old_clan = role.name
                break
    new_clan = player.clan_name

    # add the roles to the lists if the clans are not the same
    if old_clan != new_clan:
        # if there is an old clan role then add it to the list
        if old_clan:
            remove_roles.append(old_clan)
        add_roles.append(new_clan)

    # checking if the user's member roles need changing
    new_role = None
    if player.role == 'leader':
        new_role = 'leader'
    elif player.role == 'coLeader':
        new_role = 'co-leader'
    elif player.role == 'admin':
        new_role = 'elder'
    elif player.role == 'member':
        new_role = 'member'
    else:
        new_role = 'uninitiated'

    old_role = None
    for role in user_roles:
        if role.name == 'leader':
            old_role = 'leader'
        if role.name == 'co-leader':
            old_role = 'co-leader'
        if role.name == 'elder':
            old_role = 'elder'
        if role.name == 'member':
            old_role = 'member'
        if role.name == 'uninitiated':
            old_role = 'uninitiated'
        if role.name == 'community':
            remove_roles.append(role.name)

    # add the roles to the lists if the member roles are not the same
    if old_role != new_role:
        # if there is an old clan member role then add it to the list
        if old_role:
            remove_roles.append(old_role)
        add_roles.append(new_role)

    return add_roles, remove_roles


def active_super_troop_role_switch(player, user_roles, active_super_troops):
    """
        takes in list of discord user roles and active super troops,
        returns new and old roles for active super troops
    """

    add_roles = []
    remove_roles = []

    # checking if the user's active super troop roles need changing
    old_super_troop_roles = []
    for role in user_roles:
        for super_troop in super_troop_list:
            if role.name == super_troop:
                old_super_troop_roles.append(role)

    for super_troop in active_super_troops:
        add_roles.append(super_troop.name)

    for old_role in old_super_troop_roles:
        remove_roles.append(old_role.name)

    return add_roles, remove_roles


# todo needs testing
# ? may not need
def client_roles_check(client_roles, user_roles):
    """
        Checks if a user has any of the client_roles and returns True or False
    """
    for value in client_roles:
        if value.is_clash_role:
            for role in user_roles:
                if role.name == value.name:
                    return True
    return False


def role_check(client_role, user_roles):
    """
        Returns True if user has requested role, False if not
    """
    for role in user_roles:
        if role.name == client_role:
            return True
    return False


def nickname_available(nickname, user_list):
    """
        returns a bool
        checks if anyone in the guild has the given display_name
    """
    for user in user_list:
        if nickname == user.display_name:
            return False
    return True


# todo change ctx to channel_list
def channel_changer(ctx, send_id):
    for channel in ctx.guild.channels:
        if channel.id == send_id:
            return channel
    return ctx.channel


def find_user_clan(player_name, client_clans, user_roles, header):
    """
        Returns a client clan if one is found
    """
    for client_clan in client_clans:
        for role in user_roles:

            # if the clan is found
            if client_clan.name == role.name:
                clan = Clan.get(client_clan.tag, header)

                # search the clan members for the given player
                player_tag = clan.find_member(player_name)
                if player_tag:
                    return client_clan
    return None


def player_name_string(display_name):
    if '|' in display_name:
        display_name_chars = ''
        for char in display_name:
            if char == '|':
                break
            else:
                display_name_chars += char
        display_name = display_name_chars
        if display_name[-1] == ' ':
            display_name = display_name[:-1]
    return display_name


def find_channel_member(user_name, channel_members):
    """
        Takes in a user's name and returns the discord member object.
    """
    for member in channel_members:
        if user_name == player_name_string(member.display_name):
            return member
    return ''
