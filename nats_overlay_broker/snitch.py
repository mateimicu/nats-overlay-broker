"""Simple listener for all the messages."""
import asyncio
from nats_overlay_broker import base_nats_agent

class Snitch(base_nats_agent.BaseNATSAgent):
    """Snitch all the messages that are passed."""

    def __init__(self, *args, **kwargs):
        super(Snitch, self).__init__(*args, **kwargs)
        self._last_recorder = 0

    async def message_handler(self, _):
        """Process a snitched message."""
        # subject = msg.subject
        # await self.inc_metric("sniched-for-{}".format(subject))
        await self.inc_metric("sniched-messages")

    async def _monitor_throughput(self):
        """Monitor the amount of messages passing for second."""
        await asyncio.sleep(1)
        recorder_now = self._metrics_evaluated.get("sniched-messages", 0)
        self._metrics_evaluated["throughpu"] =  recorder_now - self._last_recorder
        self._last_recorder = recorder_now

    async def work(self):
        """All the work is done in callbacks."""
        print("Listening for messages ...")
        await asyncio.ensure_future(self._monitor_throughput())

    async def prepare(self):
        """Prepare the connection and subscription."""
        await super(Snitch, self).prepare()
        await self.nats.subscribe(">", cb=self.message_handler)
