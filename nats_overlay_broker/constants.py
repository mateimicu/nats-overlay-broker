"""Constants used in the project."""
import signal

BROKER_PUBLISH_SUBJECT = "broker-publish"
BROKER_SUBJECT_REQUEST = "broker-subject-request"
FILTER_SUBJECTS = "broker.filter-subjects.{}"

DEFAULT_NATS_SERVERS = ["nats://127.0.0.1:4222"]

NATS_TIMEOUT = 5

RULES = [
    ("name", .5),
    ("dob", .7),
    ("color", 1),
    ("height", .5),
]
EQ_RULE = {'dob': .9}


BATCH_PROCESS_MESSAGES = 500
DETERMINISTIC_SLEEP_TIMEOUT = 0
SLEEP_TIMEOUT = 0
METRICS_SLEEP = 5
RETRY_COUNT = 10
ERROT_SLEEP = 3

MIN_VALUE_METRIC = 10

MAX_SUBSCRIPTIONS = 10000
BATCH = 100

TERM_SIGNALS = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
