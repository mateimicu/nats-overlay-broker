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

# RULES = [
# ]
# EQ_RULE = {}

MAX_SUBSCRIPTIONS = 100
BATCH = 1

class SubscriptionFeed(baseNatsAgent.BaseNATSAgent):
    """Generate a random number of subscriptions."""

    @staticmethod
    def serialize_subscription(subscription):
        return bytes(json.dumps(subscription), "utf-8")

    async def dummy_callback(self, msg):
        """Print the data."""
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()

        print("[Dummy] Received a message on '{subject} - {reply}': {data}".format(
              subject=subject, reply=reply, data=data))

    async def get_subject_for_subscription(self, subscription):
        s_subscription = self.serialize_subscription(subscription)
        response = await self._nc.request(constants.BROKER_SUBJECT_REQUEST, s_subscription, 1)
        subject = response.data.decode()
        print("Got for subscription -> subject: {} -> {}".format(
            s_subscription, subject))
        return subject


    async def work(self):
        """Generate a random Number of subscriptions."""
        print("Start subscribing ...")

        for _ in range(int(MAX_SUBSCRIPTIONS/BATCH)):
            subscriptions = person.gen_subscriptions(BATCH, RULES, EQ_RULE)
            for subscription in subscriptions:
                data = self.serialize_subscription(subscription)
                subject = await self.get_subject_for_subscription(subscription)
                print("Subscribe to: {}".format(subject))
                await self._nc.subscribe(subject, cb=self.dummy_callback)
