from argparse import ArgumentParser
from flask import Flask, render_template
from gqlalchemy import Memgraph
import logging
import os
import time
from functools import wraps
import graph_data

memgraph = Memgraph()

log = logging.getLogger(__name__)
app = Flask(
    __name__,
)
args = None


def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        log.info(f"Time for {func.__name__} is {duration}")
        return result

    return wrapper


def init_log():
    logging.basicConfig(level=logging.DEBUG)
    log.info("Logging enabled")
    logging.getLogger("werkzeug").setLevel(logging.WARNING)


def parse_args():
    """Parse command line arguments."""

    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="0.0.0.0", help="Host address.")
    parser.add_argument("--port", default=5000, type=int, help="App port.")
    parser.add_argument(
        "--debug",
        default=True,
        action="store_true",
        help="Run web server in debug mode.",
    )
    parser.add_argument(
        "--populate",
        dest="populate",
        action="store_true",
        help="Run app with data loading.",
    )
    parser.set_defaults(populate=False)
    log.info(__doc__)
    return parser.parse_args()


@log_time
def load_data():
    """Load data into the database."""

    if not args.populate:
        log.info("Data is loaded in Memgraph.")
        return
    log.info("Loading data into Memgraph.")
    try:
        memgraph.drop_database()
        graph_data.load()
    except Exception as e:
        log.info(e)
        log.info("Data loading error.")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


def connect_to_memgraph():
    connection_established = False
    while not connection_established:
        try:
            if memgraph._get_cached_connection().is_active():
                connection_established = True
        except:
            log.info("Memgraph probably isn't running.")
            time.sleep(4)


def main():
    global args
    args = parse_args()
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        init_log()
        connect_to_memgraph()
        load_data()
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
