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
