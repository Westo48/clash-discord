from coc import WarRound
from coc.enums import (
    HERO_ORDER,
    HERO_PETS_ORDER,
    HOME_TROOP_ORDER,
    SPELL_ORDER,
    SIEGE_MACHINE_ORDER,
    SUPER_TROOP_ORDER
)


def get_hero_order():
    """
        returns coc.py HERO_ORDER
    """
    return HERO_ORDER


def get_pet_order():
    """
        returns coc.py HERO_PETS_ORDER
    """
    return HERO_PETS_ORDER


def get_home_troop_order():
    """
        returns coc.py HOME_TROOP_ORDER
    """
    return HOME_TROOP_ORDER


def get_spell_order():
    """
        returns coc.py SPELL_ORDER
    """
    return SPELL_ORDER


def get_siege_order():
    """
        returns coc.py SIEGE_MACHINE_ORDER
    """
    return SIEGE_MACHINE_ORDER


def get_super_troop_order():
    """
        returns coc.py SUPER_TROOP_ORDER
    """
    return SUPER_TROOP_ORDER


def get_war_specified(war_selection, cwl_group):
    """
        gets the necessary coc.WarRound for the given war

        Args:
            war_selection (str): war selection
                ["preparation", "current", "upcoming", None]
            cwl_group (obj): coc.py cwl group object

        Returns:
            enum: WarRound
    """

    # return current war for normal wars
    if cwl_group is None:
        return WarRound.current_war

    # only for cwl
    # war selection has not been specified
    if war_selection is None:
        if cwl_group.state == "preparation":
            return WarRound.current_preparation

        elif cwl_group.state == "inWar":
            return WarRound.current_war

        elif cwl_group.state == "warEnded":
            return WarRound.current_preparation

    # war selection has been specified
    else:
        if war_selection == "previous":
            return WarRound.previous_war

        elif war_selection == "current":
            return WarRound.current_war

        elif war_selection == "upcoming":
            return WarRound.current_preparation

    return WarRound.current_war
