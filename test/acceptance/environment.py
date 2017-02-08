from chaosmonkey.engine.cme_manager import manager as cme_manager
from chaosmonkey.engine.app import configure_engine
from chaosmonkey.dal.executor_model import Executor
from chaosmonkey.dal.plan_model import Plan
from chaosmonkey.api.app import flask_app


def before_all(context):
    root = context.config.userdata.get("root", "./")

    """Set up flask app and blueprints"""
    database_uri = ":memory:"
    attacks_folder = root + "attacks"
    planners_folder = root + "planners"
    cme_timezone = "Europe/Madrid"

    configure_engine(database_uri, attacks_folder, planners_folder, cme_timezone)
    if not cme_manager.scheduler.running:
        cme_manager.scheduler.start()
    else:
        cme_manager.scheduler.resume()

    # Empty the module stores
    cme_manager.attacks_store.set_modules([])
    cme_manager.planners_store.set_modules([])

    context.app = flask_app
    context.client = flask_app.test_client()
    context.manager = cme_manager


def after_scenario(context, scenario):
    Plan.query.delete()
    Executor.query.delete()
    context.manager.planners_store.set_modules([])
    context.manager.attacks_store.set_modules([])
    context.manager.scheduler.remove_all_jobs()
