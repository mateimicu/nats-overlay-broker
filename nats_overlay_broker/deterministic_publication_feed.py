"""Generate a feed of publications."""
import time
import asyncio

from nats_overlay_broker import base_nats_agent
from nats_overlay_broker import person
from nats_overlay_broker import constants
from nats_overlay_broker import exceptional

# pylint: disable=protected-access

PERSONS = [
    person.Person(
        name="Deterministic A",
        dob="2021-10-16 21:08:09",
        heartrate=24,
        color="red",
        height=2.4
    ),
    person.Person(
        name="Deterministic B",
        dob="2021-10-16 21:08:09",
        heartrate=24,
        color="red",
        height=2.4
    ),
    person.Person(
        name="Deterministic C",
        dob="2021-10-16 21:08:09",
        heartrate=24,
        color="red",
        height=2.4
    ),
    person.Person(
        name="Deterministic D",
        dob="2021-10-16 21:08:09",
        heartrate=24,
        color="red",
        height=2.4
    ),
]

class DeterministicPublicationFeed(base_nats_agent.BaseNATSAgent):
    """Generate Persons and publish them in a deterministic way."""

    @exceptional.america_please_egzblein
    async def work(self):
        """Publish random Persons."""
        print("Start injecting Persons ...")

        while True:
            for _ in range(constants.BATCH_PROCESS_MESSAGES):
                for pers in PERSONS:
                    pers._dob = str("{:.25f}".format(time.time()))
                    message = bytes(pers.as_json(), "utf-8")
                    await self.publish(constants.BROKER_PUBLISH_SUBJECT, message)
            await asyncio.sleep(constants.DETERMINISTIC_SLEEP_TIMEOUT)
