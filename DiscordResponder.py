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


def channel_changer(ctx, send_id):
    for channel in ctx.guild.channels:
        if channel.id == send_id:
            return channel
            break
    return ctx.channel
