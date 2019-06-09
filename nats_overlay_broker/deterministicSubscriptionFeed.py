"""Generate a random number of subscriptions."""
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


SUBCRIPTIONS = [
    [{"op": "==", "val": "Deterministic A", "name": "name"}],
    [{"op": "==", "val": "Deterministic B", "name": "name"}],
    [{"op": "==", "val": "Deterministic C", "name": "name"}],
]
class DeterministicSubscriptionFeed(baseNatsAgent.BaseNATSAgent):
    """Generate a random number of subscriptions."""

    def __init__(self, nats_servers=["nats://127.0.0.1:4222"]):
        """Initialize the pollution client."""
        super(DeterministicSubscriptionFeed, self).__init__(nats_servers)
        self._subscriptions_count = 0
        self._latency = []

    def append_latency(self, delta):
        self._latency.append(delta)

        if len(self._latency) > 1000:
            print("AVG LATENCY: ", sum(self._latency) / len(self._latency))
            self._latency = []

    @staticmethod
    def serialize_subscription(subscription):
        return bytes(json.dumps(subscription), "utf-8")

    @exceptional.america_please_egzblein
    async def dummy_callback(self, msg):
        """Print the data."""
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        dob_sent = float(json.loads(data)["dob"])
        dob_recv = time.time()
        delta_dob = dob_recv - dob_sent
        
        self.append_latency(delta_dob)
        # print("[Dummy] Received a message on '{subject} - {reply}': {data}".format(
        #       subject=subject, reply=reply, data=data))

    @exceptional.america_please_egzblein
    async def get_subject_for_subscription(self, subscription):
        s_subscription = self.serialize_subscription(subscription)
        response = await self._nc.request(constants.BROKER_SUBJECT_REQUEST, s_subscription, 5)
        subject = response.data.decode()
        print("Got for subscription -> subject: {} -> {}".format(
            s_subscription, subject))
        return subject


    @exceptional.america_please_egzblein
    async def subscribe_to_subject(self, subject):
        self._subscriptions_count += 1
        if self._subscriptions_count % 1000 == 0:
            print("DATA :", self._subscriptions_count)
        await self._nc.subscribe(subject, cb=self.dummy_callback)

    @exceptional.america_please_egzblein
    async def work(self):
        """Generate a random Number of subscriptions."""
        print("Start subscribing ...")

        for _ in range(3):
            for subscription in SUBCRIPTIONS:
                data = self.serialize_subscription(subscription)
                subject = await self.get_subject_for_subscription(subscription)
                # print("[{}] Subscribe to: {}".format(self._subscriptions_count, subject))
                await self.subscribe_to_subject(subject)
