"""Overlay Broker used to multiplex messages."""
import json

from nats_overlay_broker import overlay_broker_base
from nats_overlay_broker import constants
from nats_overlay_broker import person
from nats_overlay_broker import exceptional

class BrokerMultiplexer(overlay_broker_base.BaseBroker):
    """Overlay Broker that will multiplex messages."""

    def get_filters(self):
        """Get all the filters from redis."""
        for possible_filter in self._redis.keys("*"):
            if self._redis.type(possible_filter) == b"set":
                yield possible_filter

    @exceptional.america_please_egzblein
    async def multiplex(self, msg):
        """Multiplex a message on all subscriptions that match."""
        subject = msg.subject
        pers = person.Person(**json.loads(msg.data.decode()))

        await self.inc_metric("message-recv")
        for _filter in self.get_filters():
            if not pers.applies_to(json.loads(_filter)):
                await self.inc_metric("message-droped")
                continue

            subjects = self._redis.sscan(_filter)[1]
            await self.inc_metric("message-forwarded")
            await self.inc_metric("message-multiplex", len(subjects))
            for subject in subjects:
                await self.publish(subject.decode(), msg.data)

    async def work(self):
        """All the work is done in callbacks."""
        print("Listening for messages to multiplex ...")

    async def prepare(self):
        """Prepare the connection and subscription."""
        await super(BrokerMultiplexer, self).prepare()
        await self.nats.subscribe(constants.BROKER_PUBLISH_SUBJECT, cb=self.multiplex)
