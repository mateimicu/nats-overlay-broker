"""Generate a random number of subscriptions."""
import random
import socket
import json
import time

import asyncio
from nats.aio.client import Client as NATS

from nats_overlay_broker import subscriptionFeed 
from nats_overlay_broker import person
from nats_overlay_broker import constants
from nats_overlay_broker import exceptional


SUBCRIPTIONS = [
    [{"op": "==", "val": "Deterministic A", "name": "name"}],
    [{"op": "==", "val": "Deterministic B", "name": "name"}],
    [{"op": "==", "val": "Deterministic C", "name": "name"}],
]
class DeterministicSubscriptionFeed(subscriptionFeed.SubscriptionFeed):
    """Generate a random number of subscriptions."""

    def __init__(self, nats_servers=["nats://127.0.0.1:4222"]):
        """Initialize the pollution client."""
        super(DeterministicSubscriptionFeed, self).__init__(nats_servers)
        self._latency = []

    def append_latency(self, delta):
        self._latency.append(delta)

        if len(self._latency) > constants.BATCH_PROCESS_MESSAGES:
            avg_latency = sum(self._latency) / len(self._latency)
            self._metrics_evaluated["avg-latency"] = avg_latency
            self._latency = []

    @exceptional.america_please_egzblein
    async def dummy_callback(self, msg):
        """Print the data."""
        await super(DeterministicSubscriptionFeed, self).dummy_callback(msg)        
        self.append_latency(delta_dob)

    @exceptional.america_please_egzblein
    async def work(self):
        """Create a deterministic number of subscriptions."""
        print("Start subscribing ...")

        for subscription in SUBCRIPTIONS:
            data = self.serialize_subscription(subscription)
            subject = await self.get_subject_for_subscription(subscription)
            await self.subscribe_to_subject(subject)
