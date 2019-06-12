"""Generate a random number of subscriptions."""
import time
import json

from nats_overlay_broker import subscription_feed
from nats_overlay_broker import constants
from nats_overlay_broker import exceptional

# pylint: disable=protected-access

SUBCRIPTIONS = [
    [{"op": "==", "val": "Deterministic A", "name": "name"}],
    [{"op": "==", "val": "Deterministic B", "name": "name"}],
    [{"op": "==", "val": "Deterministic C", "name": "name"}],
]

class DeterministicSubscriptionFeed(subscription_feed.SubscriptionFeed):
    """Generate a random number of subscriptions."""

    def __init__(self, *args, **kwargs):
        """Initialize the pollution client."""
        super(DeterministicSubscriptionFeed, self).__init__(*args, **kwargs)
        self._latency = []
        self._all_latency = []
        self._metrics_evaluated["avg-latency"] = 0

    def append_latency(self, delta):
        """Add a new latency data point."""
        self._latency.append(delta)
        if len(self._latency) > constants.BATCH_PROCESS_MESSAGES:
            avg_latency = sum(self._latency) / len(self._latency)
            self._metrics_evaluated["avg-latency-last-batch"] = avg_latency
            self._latency = []

            self._all_latency.append(avg_latency)

            total_avg_latency = sum(self._all_latency) / len(self._all_latency)
            self._metrics_evaluated["avg-latency"] = total_avg_latency

    def __print_metrics(self):
        super(DeterministicSubscriptionFeed, self).__print_metrics()
        print("[Set] all-latency :", self._all_latency)

    @exceptional.america_please_egzblein
    async def dummy_callback(self, msg):
        """Print the data."""
        await super(DeterministicSubscriptionFeed, self).dummy_callback(msg)
        data = json.loads(msg.data.decode())
        delta_dob = time.time() - float(data["dob"])
        self.append_latency(delta_dob)
        if constants.PRINT_STUFF:
            print("Got {}".format(msg.data.decode()))

    @exceptional.america_please_egzblein
    async def work(self):
        """Create a deterministic number of subscriptions."""
        print("Start subscribing ...")
        for subscription in SUBCRIPTIONS:
            subject = await self.get_subject_for_subscription(subscription)
            await self.subscribe_to_subject(subject, self.dummy_callback)
