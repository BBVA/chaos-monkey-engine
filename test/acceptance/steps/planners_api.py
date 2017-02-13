from flask import url_for, json
from behave import when, then


@when('the user makes a request to the get planners endpoint')
def the_user_makes_a_request_to_get_planners(context):
    with context.app.test_request_context():
        url = url_for("planners.list_planners")
        res = context.client.get(url)
        context.last_response = res


@then(u'the api responds with {n_planners} planners')
def the_api_responsds_with_n_attacks(context, n_planners):
    json_response = json.loads(context.last_response.get_data())
    assert "planners" in json_response
    assert int(n_planners) == len(json_response.get("planners"))
