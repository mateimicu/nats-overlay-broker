"""Simple listener for all the messages."""
import asyncio
from nats.aio.client import Client as NATS

from nats_overlay_broker import baseNatsAgent


class Snitch(baseNatsAgent.BaseNATSAgent):
    """Snitch all the messages that are passed."""


    async def message_handler(self, msg):
        """Process a snitched message."""
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print("Received a message on '{subject} - {reply}': {data}".format(
              subject=subject, reply=reply, data=data))


    async def work(self):
        print("Listening for messages ...")

    async def prepare(self):
        """Prepare the connection and subscription."""
        await super(Snitch, self).prepare()

        # "*" matches any token, at any level of the subject.
        await self._nc.subscribe(">", cb=self.message_handler)
