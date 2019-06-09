"""Generate a random number of subscriptions."""
import random
import socket
import json

import asyncio
from nats.aio.client import Client as NATS

from nats_overlay_broker import baseNatsAgent
from nats_overlay_broker import person
from nats_overlay_broker import constants

RULES = [
    ("name", .5),
    ("dob", .7),
    ("color", 1),
    ("height", .5),
]
EQ_RULE = {'dob': .9}

class SubscriptionFeed(baseNatsAgent.BaseNATSAgent):
    """Generate a random number of subscriptions."""

    async def work(self):
        """Generate a random Number of subscriptions."""
        print("Start injecting Persons ...")

        subscriptions = person.gen_subscriptions(10000, RULES, EQ_RULE)
        print(len(subscriptions))
        # while True:
            # pers = person.Person.get_random_person()
            # message = bytes(pers.as_json(), "utf-8")
            # await self._nc.publish(constants.BROKER_PUBLISH_TOPIC, message)
            # print("Sending on '{}': {}".format( 
            #     constants.BROKER_PUBLISH_TOPIC, message))
