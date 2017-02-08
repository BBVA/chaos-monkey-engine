from flask import url_for
from flask_hal import Document
import test.attacks.attack1 as attack1_module
import test.attacks.attack2 as attack2_module


def test_empty_attack_store_return_hal(app, manager):
    url = url_for("attacks.list_attacks")

    attack_list = []
    manager.attacks_store.set_modules(attack_list)

    with app.test_request_context(url):
        res = app.test_client().get(url)
        assert res.status_code == 200
        assert res.mimetype == "application/hal+json"
        assert res.json == Document(data={"attacks": attack_list}).to_dict()


def test_attack_list_return_hal(app, manager):
    url = url_for("attacks.list_attacks")

    module_list = [attack1_module, attack2_module]
    manager.attacks_store.set_modules(module_list)

    with app.test_request_context(url):

        attack_list = [attack1_module.Attack1(None).to_dict(), attack2_module.Attack2(None).to_dict()]

        res = app.test_client().get(url)
        assert res.status_code == 200
        assert res.mimetype == "application/hal+json"
        assert res.json == Document(data={"attacks": attack_list}).to_dict()
