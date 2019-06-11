"""Overlay Broker used to handle subscriptions."""
import uuid

from nats_overlay_broker import overlay_broker_base
from nats_overlay_broker import constants
from nats_overlay_broker import exceptional

class BrokerSubscriptionManager(overlay_broker_base.BaseBroker):
    """Overlay Broker."""

    @staticmethod
    def get_random_subject():
        """Return a random subject name."""
        return constants.FILTER_SUBJECTS.format(uuid.uuid4())

    @exceptional.america_please_egzblein
    async def subject_for_filter(self, msg):
        """Reply with a subject for a given filter."""
        f_subject = self.get_random_subject()
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        self._redis.sadd(data, f_subject)
        await self.inc_metric("subscriptions")
        await self.publish(reply, bytes(f_subject, "utf-8"))


    @exceptional.america_please_egzblein
    async def work(self):
        """All the work for a Broker is done in callbacks."""
        print("[Subscription Manager] Listening for messages ...")

    @exceptional.america_please_egzblein
    async def prepare(self):
        """Prepare the connection and subscription."""
        await super(BrokerSubscriptionManager, self).prepare()
        await self.nats.subscribe(constants.BROKER_SUBJECT_REQUEST, cb=self.subject_for_filter)
