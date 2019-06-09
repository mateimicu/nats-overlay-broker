"""Constants used in the project."""

BROKER_PUBLISH_SUBJECT = "broker-publish"
BROKER_SUBJECT_REQUEST = "broker-subject-request"
FILTER_SUBJECTS = "broker.filter-subjects.{}"

BATCH_PROCESS_MESSAGES = 2
SLEEP_TIMEOUT = 10

NATS_TIMEOUT = 5

DEFAULT_NATS_SERVER = ["nats://127.0.0.1:4222"]

RULES = [
    ("name", .5),
    ("dob", .7),
    ("color", 1),
    ("height", .5),
]
EQ_RULE = {'dob': .9}


MAX_SUBSCRIPTIONS = 10000
BATCH = 100
