from flask import json
from behave import then


@then(u'the response is HAL')
def the_response_is_HAL(context):
    json_response = json.loads(context.last_response.get_data())
    assert "_links" in json_response
    assert "self" in json_response.get("_links")
