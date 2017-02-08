from flask import json
from behave import when, then, given


@then('the api responds with {n_plans} plans')
def step_impl(context, n_plans):
    json_response = json.loads(context.last_response.get_data())
    assert "plans" in json_response
    assert int(n_plans) == len(json_response.get("plans"))

