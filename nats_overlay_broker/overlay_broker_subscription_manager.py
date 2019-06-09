"""Overlay Broker."""
import uuid
import json

import redis
import asyncio
from nats.aio.client import Client as NATS


from nats_overlay_broker import overlay_broker_base
from nats_overlay_broker import constants
from nats_overlay_broker import person
from nats_overlay_broker import exceptional

class BrokerSubscriptionManager(overlay_broker_base.BaseBroker):
    """Overlay Broker."""

    @staticmethod
    def get_random_subject():
        return constants.FILTER_SUBJECTS.format(uuid.uuid4())

    @exceptional.america_please_egzblein
    async def subject_for_filter(self, msg):
        f_subject = self.get_random_subject()
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        self._redis.sadd(data, f_subject)
        await self.inc_metric("subscriptions")
        print("Received a message on '{subject} - {reply}': {data} -> {f_subject}".format(
              subject=subject, reply=reply, data=data, f_subject=f_subject))
        await self.publish(reply, bytes(f_subject, "utf-8"))


    @exceptional.america_please_egzblein
    async def work(self):
        print("[Subscription Manager] Listening for messages ...")

    @exceptional.america_please_egzblein
    async def prepare(self):
        """Prepare the connection and subscription."""
        await super(BrokerSubscriptionManager, self).prepare()
        await self._nc.subscribe(constants.BROKER_SUBJECT_REQUEST, cb=self.subject_for_filter)
