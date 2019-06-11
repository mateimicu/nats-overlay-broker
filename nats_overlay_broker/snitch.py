"""Simple listener for all the messages."""
from nats_overlay_broker import base_nats_agent

class Snitch(base_nats_agent.BaseNATSAgent):
    """Snitch all the messages that are passed."""


    async def message_handler(self, msg):
        """Process a snitched message."""
        subject = msg.subject
        await self.inc_metric("sniched-messages")
        # await self.inc_metric("sniched-for-{}".format(subject))

    async def work(self):
        """All the work is done in callbacks."""
        print("Listening for messages ...")

    async def prepare(self):
        """Prepare the connection and subscription."""
        await super(Snitch, self).prepare()
        await self.nats.subscribe(">", cb=self.message_handler)
