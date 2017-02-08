from flask import json
from behave import when, then, given


def request_with_payload(context, method, endpoint, payload):
    """make N attacks available on the attack store"""
    with context.app.test_request_context():
        full_endpoint = "/api/1" + endpoint
        res = context.client.open(
            full_endpoint,
            method=method,
            content_type='application/json',
            data=payload
        )
        context.last_response = res


def request_with_querystring(context, method, endpoint, querystring):
    """make N attacks available on the attack store"""

    with context.app.test_request_context():
        full_endpoint = "/api/1" + endpoint
        res = context.client.open(
            full_endpoint,
            method=method,
            content_type='application/json',
            query_string=json.loads(querystring)
        )
        context.last_response = res


@when(u'the user makes a "{method}" request to "{endpoint}" endpoint with {payload}')
def step_impl(context, method, endpoint, payload):
    """make N attacks available on the attack store"""

    if payload == "payload":
        payload = context.table[0]["payload"]
        request_with_payload(context, method, endpoint, payload)
    elif payload == "querystring":
        querystring = context.table[0]["querystring"]
        request_with_querystring(context, method, endpoint, querystring)
    else:
        with context.app.test_request_context():
            full_endpoint = "/api/1" + endpoint
            res = context.client.open(
                full_endpoint,
                method=method,
                content_type='application/json',
                data=payload
            )
            context.last_response = res


@when(u'the user makes a "{method}" request to "{endpoint}" endpoint')
def step_impl(context, method, endpoint):
    """make N attacks available on the attack store"""

    if "{plan_id}" in endpoint:
        endpoint = endpoint.replace("{plan_id}", context.last_plan.id)

    with context.app.test_request_context():
        full_endpoint = "/api/1" + endpoint
        res = context.client.open(
            full_endpoint,
            method=method,
            content_type='application/json'
        )
        context.last_response = res


@then(u'the api response code is {response_code}')
def step_impl(context, response_code):
    assert context.last_response.status_code == int(response_code)


@then(u'the api response payload is {response}')
def step_impl(context, response):
    json_response = json.loads(context.last_response.get_data())
    response = json.loads(response)
    print(json_response)
    print(response)
    assert json_response == response
