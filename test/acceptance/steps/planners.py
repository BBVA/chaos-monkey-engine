from test.planners import planner1, planner2, two_executors, required_schema
from behave import given


@given(u"there are {n_planners} planners available")
def step_there_are_n_planners_available(context, n_planners):
    """make N planners available on the planners store"""

    # as there are only 2 attacks for tests
    if int(n_planners) > 2:
        raise ValueError("Can't be more than 2 planners")

    module_list = [planner1, planner2]
    for i in range(0, int(n_planners)):
        context.manager.planners_store.add(module_list[i])


@given(u'the {module_name} module is available in planners')
def step_there_are_n_attacks_available(context, module_name):
    """add a planner module to the store"""

    module = None
    if module_name == "planner1":
        module = planner1
    elif module_name == "planner2":
        module = planner2
    elif module_name == "two_executors":
        module = two_executors
    elif module_name == "required_schema":
        module = required_schema

    context.manager.planners_store.add(module)
