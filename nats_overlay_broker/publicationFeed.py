"""Generate a feed of publications."""
import random
import socket
import json

import asyncio
from nats.aio.client import Client as NATS

from nats_overlay_broker import baseNatsAgent
from nats_overlay_broker import person
from nats_overlay_broker import constants

class PublicationFeed(baseNatsAgent.BaseNATSAgent):
    """Generate Persons and publish them."""

    async def work(self):
        """Publish random Persons."""
        print("Start injecting Persons ...")

        while True:
            pers = person.Person.get_random_person()
            message = pers.as_json_bytes()

            await self.inc_metric("published-persons")

            await self.publish(constants.BROKER_PUBLISH_SUBJECT, message)
            await asyncio.sleep(constants.SLEEP_TIMEOUT)
