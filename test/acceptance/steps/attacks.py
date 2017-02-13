from test.attacks import attack1, attack2, required_schema
from behave import given


@given(u'there are {n_attacks} attacks available')
def step_there_are_n_attacks_available(context, n_attacks):
    """make N attacks available on the attack store"""

    # as there are only 2 attacks for tests
    if int(n_attacks) > 2:
        raise ValueError("Can't be more than 2 attacks")

    module_list = [attack1, attack2]
    for i in range(0, int(n_attacks)):
        context.manager.attacks_store.add(module_list[i])


@given(u'the {module_name} module is available in attacks')
def step_there_are_n_attacks_available(context, module_name):
    """make N attacks available on the attack store"""

    module = None
    if module_name == "attack1":
        module = attack1
    elif module_name == "attack2":
        module = attack2
    elif module_name == "required_schema":
        module = required_schema

    context.manager.attacks_store.add(module)
