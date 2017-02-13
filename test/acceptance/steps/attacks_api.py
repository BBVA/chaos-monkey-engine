from flask import url_for, json
from behave import when, then


@when('the user makes a request to the get attacks')
def the_user_makes_a_request_to_get_attacks(context):
    with context.app.test_request_context():
        url = url_for("attacks.list_attacks")
        res = context.client.get(url)
        context.last_response = res


@then(u'the api responds with {n_attacks} attacks')
def the_api_responsds_with_n_attacks(context, n_attacks):
    json_response = json.loads(context.last_response.get_data())
    assert "attacks" in json_response
    assert int(n_attacks) == len(json_response.get("attacks"))
