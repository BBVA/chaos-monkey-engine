from unittest.mock import patch
import sys
import pytest
from chaosmonkey.modules.module_store import ModulesStore
from chaosmonkey.attacks.attack import Attack
import chaosmonkey.attacks.attack as module_attack


class AttackMock(Attack):
    @staticmethod
    def to_dict():
        pass

    def run(self):
        pass


def test_load_raise_exception_for_invalid_path():
    modules = ModulesStore(Attack)
    with pytest.raises(ValueError):
        modules.load("")


@patch.object(ModulesStore, "_get_module_names")
def test_load_path_with_no_modules(get_module_names_mock):
    get_module_names_mock.return_value = ["InvalidModule"]
    modules = ModulesStore(Attack)
    with pytest.raises(ValueError):
        modules.load("/tmp")


@patch.object(ModulesStore, "_get_module_names")
@patch.object(ModulesStore, "_validate_path")
def test_load_path_with_valid_modules(validate_path_mock, get_module_names_mock):
    module_list = ["sys", "os"]
    get_module_names_mock.return_value = module_list
    validate_path_mock.return_value = True
    modules_store = ModulesStore(Attack)
    modules_store.load("/tmp")
    assert len(modules_store.modules) == len(module_list)


def test_get_module_names():
    with patch("chaosmonkey.modules.module_store.listdir") as listdir_mock, \
         patch("chaosmonkey.modules.module_store.isfile") as isfile_mock:

        listdir_mock.return_value = ["test.py", "tost.py"]
        isfile_mock.return_value = True

        modules_store = ModulesStore(Attack)
        module_names = modules_store._get_module_names("")
        assert len(module_names) == 2
        assert module_names == ["test", "tost"]


def test_ref_to_obj():
    modules_store = ModulesStore(Attack)
    modules_store.add(module_attack)
    obj = modules_store._ref_to_obj("chaosmonkey.attacks.attack:Attack")
    assert obj is Attack


@patch.object(ModulesStore, "get_modules")
def test_list(modules_mock):
    sys.path.insert(0, "attacks")
    module = __import__("terminate_ec2_instance")
    modules_store = ModulesStore(Attack)
    modules_mock.return_value = [module]

    assert len(modules_store.list()) == 1


def test_add():
    sys.path.insert(0, "attacks")
    module = __import__("terminate_ec2_instance")
    modules_store = ModulesStore(Attack)
    modules_store.add(module)
    assert len(modules_store.list()) == 1


def test_remove():
    sys.path.insert(0, "attacks")
    module = __import__("terminate_ec2_instance")
    modules_store = ModulesStore(Attack)
    modules_store.add(module)
    modules_store.remove("terminate_ec2_instance")
    assert len(modules_store.list()) == 0
