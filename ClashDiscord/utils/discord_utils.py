import utils.coc_utils as coc_utils
from disnake import ApplicationCommandInteraction


async def autocomp_donation(inter: ApplicationCommandInteraction,
                            user_input: str):
    unit_list = []
    unit_list.extend(coc_utils.get_home_troop_order())
    unit_list.extend(coc_utils.get_spell_order())

    autocomp_list = []
    for unit in unit_list:
        if user_input.lower() in unit.lower():
            autocomp_list.append(unit)

    del autocomp_list[25:]
    return [unit for unit in autocomp_list]


async def autocomp_supertroop(inter: ApplicationCommandInteraction,
                              user_input: str):
    unit_list = []
    unit_list.extend(coc_utils.get_super_troop_order())

    autocomp_list = []
    for unit in unit_list:
        if user_input.lower() in unit.lower():
            autocomp_list.append(unit)

    del autocomp_list[25:]
    return [unit for unit in autocomp_list]
