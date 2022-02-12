import utils.coc_utils as coc_utils
from disnake import ApplicationCommandInteraction
from disnake.ext import commands


async def autocomp_unit(
    inter: ApplicationCommandInteraction,
    user_input: str
):
    unit_list = []
    unit_list.extend(coc_utils.get_home_troop_order())
    unit_list.extend(coc_utils.get_spell_order())

    autocomp_list = []
    for unit in unit_list:
        if user_input.lower() in unit.lower():
            autocomp_list.append(unit)

    del autocomp_list[25:]
    return [unit for unit in autocomp_list]


async def autocomp_supertroop(
    inter: ApplicationCommandInteraction,
    user_input: str
):
    unit_list = []
    unit_list.extend(coc_utils.get_super_troop_order())

    autocomp_list = []
    for unit in unit_list:
        if user_input.lower() in unit.lower():
            autocomp_list.append(unit)

    del autocomp_list[25:]
    return [unit for unit in autocomp_list]


command_param_dict = {
    'user': commands.Param(
        description="*optional* user to search for active player",
        default=None),
    'clan_role': commands.Param(
        description="*optional* clan role to use linked clan",
        default=None),
    'tag': commands.Param(
        description="*optional* tag to search",
        default=None),
    'unit_name': commands.Param(
        description="name of the unit you would like information on",
        default=None),
    'unit_type': commands.Param(
        description="*optional* type of unit to return information for",
        default="all",
        choices=[
            "all", "hero", "pet", "troop", "spell", "siege"
        ]
    )
}
