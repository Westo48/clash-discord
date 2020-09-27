import Clan


# todo reset this for new clan use
def role_switch(player_role, user_roles):
    """
        takes in player role and list of discord user roles,
        returns new and old role
    """
    if player_role == 'leader':
        new_role = 'Leader'
    elif player_role == 'coLeader':
        new_role = 'Co-Leader'
    elif player_role == 'admin':
        new_role = 'Elder'
    elif player_role == 'member':
        new_role = 'Member'
    else:
        new_role = 'Uninitiated'

    old_role = ''
    for role in user_roles:
        if role.name == 'Leader':
            old_role = 'Leader'
            break
        if role.name == 'Co-Leader':
            old_role = 'Co-Leader'
            break
        if role.name == 'Elder':
            old_role = 'Elder'
            break
        if role.name == 'Member':
            old_role = 'Member'
            break
        if role.name == 'Uninitiated':
            old_role = 'Uninitiated'
            break

    return new_role, old_role


def role_check(check_role, user_roles):
    for role in user_roles:
        if role.name == check_role:
            return True
    return False


def nickname_available(nickname, user_list):
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
    for client_clan in client_clans:
        for role in user_roles:
            if client_clan.name == role.name:
                clan = Clan.get(client_clan.tag, header)
                player_tag = clan.find_member(player_name)
                if player_tag != '':
                    return client_clan
    return ''


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
    "takes in a user's name and returns the discord member object"
    for member in channel_members:
        if user_name == player_name_string(member.display_name):
            return member
    return ''
