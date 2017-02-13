import logging
import signal
import click
from gevent.wsgi import WSGIServer
from chaosmonkey.engine.app import configure_engine, shutdown_engine
from chaosmonkey.api.app import flask_app


@click.command(name='chaos-monkey-engine')
@click.option("--port", "-p", default=5000, help="Port used to expose the CM API. Default 5000")
@click.option("--timezone", "-t", default="Europe/Madrid", help="Timezone to configure the scheduler. "
                                                                "Default 'Europe/Madrid'")
@click.option("--database-uri", "-d", required=True, help="SQLAlchemy database uri")
@click.option("--attacks-folder", "-a", required=True, help="Path to the folder where the attacks are stored")
@click.option("--planners-folder", "-p", required=True, help="Path to the folder where the planners are stored")
def cm(port, timezone, database_uri, attacks_folder, planners_folder):
    """
    Chaos Monkey Engine command line utility

    """
    log = logging.getLogger(__name__)
    configure_engine(database_uri, attacks_folder, planners_folder, timezone)

    log.info("Engine configured")
    log.debug("database: %s", database_uri)
    log.debug("attacks folder: %s", attacks_folder)
    log.debug("planners folder: %s", planners_folder)
    log.debug("timezone: %s", timezone)

    try:
        # Catch SIGTERM and convert it to a SystemExit
        signal.signal(signal.SIGTERM, sigterm_handler)
        log.info("Serving API at port %s", port)
        run_api_server(flask_app, port)
    except (KeyboardInterrupt, SystemExit):
        shutdown_engine()


def run_api_server(app, port=5000):
    """
    Runs a gevent server on a given port. Default port is 5000.

    :param app: WSGI-compliant app to be run
    :param port: port for the gevent server
    :type port: int
    :return: None
    """
    log = logging.getLogger('api')

    http_server = WSGIServer(('', port), app, log=log)
    http_server.serve_forever()


def sigterm_handler():
    raise SystemExit(1)
