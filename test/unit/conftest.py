import pytest
from chaosmonkey.engine.app import configure_engine, shutdown_engine
from chaosmonkey.engine.cme_manager import manager as cme_manager
from chaosmonkey.api.app import flask_app


def pytest_addoption(parser):
    """Options to configure attacks and planners root"""
    parser.addoption("--root", action="store", default="./",
                     help="src root folder")


@pytest.fixture(scope="session")
def root_src(request):
    return request.config.getoption("--root")


@pytest.yield_fixture(scope="session")
def app(root_src):
    """Crete app for test with context."""
    database_uri = ":memory:"
    attacks_folder = root_src + "attacks"
    planners_folder = root_src + "planners"
    cme_timezone = "Europe/Madrid"

    configure_engine(database_uri, attacks_folder, planners_folder, cme_timezone)
    cme_manager.scheduler.start()
    yield flask_app
    tear_down()


def tear_down():
    shutdown_engine()


@pytest.fixture
def manager():
    return cme_manager


@pytest.fixture
def plan(manager):
    plan = manager.add_plan("plan name")
    yield plan
    manager.delete_plan(plan.id)
