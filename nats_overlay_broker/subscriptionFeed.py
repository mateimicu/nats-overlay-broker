"""Generate a random number of subscriptions."""
import random
import socket
import json

import asyncio
from nats.aio.client import Client as NATS

from nats_overlay_broker import baseNatsAgent
from nats_overlay_broker import person
from nats_overlay_broker import constants


class SubscriptionFeed(baseNatsAgent.BaseNATSAgent):
    """Generate a random number of subscriptions."""

    @staticmethod
    def serialize_subscription(subscription):
        return bytes(json.dumps(subscription), "utf-8")

    async def dummy_callback(self, msg):
        """Print the data."""
        subject = msg.subject
        data = msg.data.decode()
        await self.inc_metric("process-dummy")
        await self.inc_metric("process-dummy-{}".format(subject))

    async def get_subject_for_subscription(self, subscription):
        s_subscription = self.serialize_subscription(subscription)
        response = await self._nc.request(constants.BROKER_SUBJECT_REQUEST, s_subscription, 1)
        subject = response.data.decode()

        return subject

    async def subscribe_to_subject(self, subject):
        await self._nc.subscribe(subject, cb=self.dummy_callback)
        await self.inc_metric("create-subscription")

    async def work(self):
        """Generate a random Number of subscriptions."""
        print("Start subscribing ...")

        for _ in range(int(constants.MAX_SUBSCRIPTIONS/constants.BATCH)):
            subscriptions = person.gen_subscriptions(
                constants.BATCH, constants.RULES, constants.EQ_RULE)

            for subscription in subscriptions:
                data = self.serialize_subscription(subscription)
                subject = await self.get_subject_for_subscription(subscription)
                await self.subscribe_to_subject(subject)
