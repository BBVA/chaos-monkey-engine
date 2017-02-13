"""
ChaosMonkey Engine
"""
import os
import errno
from pytz import timezone

from chaosmonkey.api.app import flask_app
from chaosmonkey.engine.cme_manager import manager
from chaosmonkey.engine.scheduler import scheduler
from chaosmonkey.attacks.attack import Attack
from chaosmonkey.dal.cme_sqlalchemy_store import CMESQLAlchemyStore
from chaosmonkey.dal.database import db
from chaosmonkey.modules.module_store import ModulesStore
from chaosmonkey.planners.planner import Planner


def configure_engine(database_uri, attacks_folder, planners_folder, cme_timezone):
    """
    Create a Flask App and all the configuration needed to run the CMEEngine

    * Init and configure the SQLAlchemy store (create db and tables if don't exists)
    * Init ModuleStores (attacks and planners)
    * Configure the timezone and jobstore for the scheduler
    * Configure the CMEManager

    TODO:
        The scheduler start is not made until the first request is made. This is due to
        the way the SQLAlchemy store is created, because it needs the app.context to work
        properly

    :param database_uri:    SQLAlchemy SQLALCHEMY_DATABASE_URI
    :param attacks_folder:  folder to load the attacks modules
    :param planners_folder: folder to load the planners modules
    :param cme_timezone:    timezone to set in the scheduler
    """

    # configure and init FlaskSQLAlchemy
    if database_uri != ":memory:":
        # check for memory database for tests if not, make sure the path exists and create it
        make_sure_path_exists(os.path.dirname(database_uri))

    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % database_uri
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(flask_app)
    with flask_app.app_context():
        db.create_all()
        db.app = flask_app

    # init stores
    sql_store = CMESQLAlchemyStore()
    planners_store = ModulesStore(Planner)
    attacks_store = ModulesStore(Attack)

    # configure the scheduler
    tz = timezone(cme_timezone)
    jobstores = {
        "default": sql_store
    }
    scheduler.configure(jobstores=jobstores, timezone=tz)

    # configure module stores
    attacks_store.load(attacks_folder)
    planners_store.load(planners_folder)

    # configure CMEManager
    manager.configure(scheduler, sql_store, planners_store, attacks_store)


# Start the scheduler in the first request
@flask_app.before_first_request
def start_scheduler():
    if not scheduler.running:
        scheduler.start()


def shutdown_engine():
    """
    Shutdown the scheduler
    """
    if scheduler.running:
        scheduler.shutdown()


def make_sure_path_exists(path):
    """
    Make sure a path exists and create it if don't

    :param path: string path to check
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
