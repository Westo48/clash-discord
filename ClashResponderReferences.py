def date_time_string(days, hours, minutes, seconds):
    time_string = ''
    if days > 0:
        if days == 1:
            days_text = 'day'
        else:
            days_text = 'days'

        time_string += f'{days} {days_text}, '
    if hours > 0:
        if hours == 1:
            hour_text = 'hour'
        else:
            hour_text = 'hours'

        time_string += f'{hours} {hour_text}, '
    if minutes > 0:
        if minutes == 1:
            minute_text = 'minute'
        else:
            minute_text = 'minutes'

        time_string += f'{minutes} {minute_text}, '
    if seconds > 0:
        if seconds == 1:
            second_text = 'second'
        else:
            second_text = 'seconds'

        time_string += f'{seconds} {second_text}, '

    # removing the ', ' from the end of the string
    time_string = time_string[:-2]

    return time_string


def scoreboard_string(war_object):

    if war_object.state == 'inWar':
        if war_object.clan_stars > war_object.opponent_stars:
            if war_object.clan_stars - war_object.opponent_stars == 1:
                star_string = 'star'
            else:
                star_string = 'stars'
            score_string = f'winning by {war_object.clan_stars - war_object.opponent_stars} {star_string}'
        elif war_object.clan_stars < war_object.opponent_stars:
            if war_object.clan_stars - war_object.opponent_stars == 1:
                star_string = 'star'
            else:
                star_string = 'stars'
            score_string = f'losing by {war_object.opponent_stars - war_object.clan_stars} {star_string}'
        else:
            if war_object.clan_destruction_percentage > war_object.opponent_destruction_percentage:
                score_string = f'winning by {war_object.clan_destruction_percentage - war_object.opponent_destruction_percentage} destruction percent'
            elif war_object.clan_destruction_percentage < war_object.opponent_destruction_percentage:
                score_string = f'losing by {war_object.opponent_destruction_percentage - war_object.clan_destruction_percentage} destruction percent'
            else:
                score_string = f'tied'

    elif war_object.state == 'warEnded':
        if war_object.clan_stars > war_object.opponent_stars:
            score_string = f'won by {war_object.clan_stars - war_object.opponent_stars}'
        elif war_object.clan_stars < war_object.opponent_stars:
            score_string = f'lost by {war_object.opponent_stars - war_object.clan_stars}'
        else:
            if war_object.clan_destruction_percentage > war_object.opponent_destruction_percentage:
                score_string = f'won by {war_object.clan_destruction_percentage - war_object.opponent_destruction_percentage}'
            elif war_object.clan_destruction_percentage < war_object.opponent_destruction_percentage:
                score_string = f'lost by {war_object.opponent_destruction_percentage - war_object.clan_destruction_percentage}'
            else:
                score_string = f'tied'

    else:
        score_string = 'You are not in war'

    return score_string


# todo make a get_all_attacks method
def get_all_attacks(war_object):
    all_attacks = []
    for member in war_object.clan_members:
        if len(member.attacks) == 0:
            all_attacks.append(f'{member.name} has not attacked')
        else:
            for attack in member.attacks:
                # find opponent name from tag
                if attack.stars == 1:
                    star_string = 'star'
                else:
                    star_string = 'stars'
                for opponent in war_object.opponent_members:
                    if attack.defender_tag == opponent.tag:
                        all_attacks.append(
                            f'{member.name} (TH {member.th}, position {member.map_position}) attacked {opponent.name} (TH {opponent.th}, position {opponent.map_position}) for {attack.stars} {star_string}.')
            # either lines or mark as a new line
        all_attacks.append('---------------------')
    # possibly remove trailing '--------------------'
    return all_attacks


def get_all_cwl_attacks(cwl_war_object):
    all_attacks = []
    for member in cwl_war_object.clan_members:
        if member.map_position <= 15:
            if len(member.attacks) == 0:
                all_attacks.append(f'{member.name} has not attacked')
            else:
                for attack in member.attacks:
                    # find opponent name from tag
                    if attack.stars == 1:
                        star_string = 'star'
                    else:
                        star_string = 'stars'
                    for opponent in cwl_war_object.opponent_members:
                        if attack.defender_tag == opponent.tag:
                            # will not need these if the append is in the if statement nested in the for loop
                            opponent_name = opponent.name
                            opponent_map_position = opponent.map_position
                            all_attacks.append(
                                f'{member.name} (TH {member.th}, position {member.map_position}) attacked {opponent.name} (TH {opponent.th}, position {opponent.map_position}) for {attack.stars} {star_string}.')
                # either lines or mark as a new line
            all_attacks.append('------------------------')
        # possibly remove trailing '--------------------'
    return all_attacks

