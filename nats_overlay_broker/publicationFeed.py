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
            message = bytes(pers.as_json(), "utf-8")
            await self._nc.publish(constants.BROKER_PUBLISH_SUBJECT, message)
            print("Sending on '{}': {}".format( 
                constants.BROKER_PUBLISH_SUBJECT, message))
            await asyncio.sleep(1)
