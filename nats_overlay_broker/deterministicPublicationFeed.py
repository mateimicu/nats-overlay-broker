"""Generate a feed of publications."""
import random
import socket
import json
import time

import asyncio
from nats.aio.client import Client as NATS

from nats_overlay_broker import baseNatsAgent
from nats_overlay_broker import person
from nats_overlay_broker import constants
from nats_overlay_broker import exceptional

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

class DeterministicPublicationFeed(baseNatsAgent.BaseNATSAgent):
    """Generate Persons and publish them."""

    async def work(self):
        """Publish random Persons."""
        print("Start injecting Persons ...")

        while True:
            for _ in range(1000):
                for pers in PERSONS:
                    pers._dob = str("{:.25f}".format(time.time()))
                    message = bytes(pers.as_json(), "utf-8")
                    await self._nc.publish(constants.BROKER_PUBLISH_SUBJECT, message)
                    # print("Sending on '{}': {}".format( 
                    #     constants.BROKER_PUBLISH_SUBJECT, message))
            await asyncio.sleep(1)
            print("Sent 1000 messages")
