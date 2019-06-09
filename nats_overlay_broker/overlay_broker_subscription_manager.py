"""Overlay Broker."""
import uuid
import json

import redis
import asyncio
from nats.aio.client import Client as NATS


from nats_overlay_broker import baseNatsAgent
from nats_overlay_broker import constants
from nats_overlay_broker import person
from nats_overlay_broker import exceptional

class BrokerSubscriptionManager(baseNatsAgent.BaseNATSAgent):
    """Overlay Broker."""

    def __init__(self, nats_servers=["nats://127.0.0.1:4222"], 
                redis_host="127.0.0.1", redis_password="Passw0rd"):
        """Initialize the broker agent."""
        super(BrokerSubscriptionManager, self).__init__(nats_servers)
        print("init")
        self._redis_host = redis_host
        self._redis_password = redis_password

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
        print("Received a message on '{subject} - {reply}': {data} -> {f_subject}".format(
              subject=subject, reply=reply, data=data, f_subject=f_subject))
        await self._nc.publish(reply, bytes(f_subject, "utf-8"))

    @exceptional.america_please_egzblein
    async def work(self):
        print("[Subscription Manager] Listening for messages ...")

    @exceptional.america_please_egzblein
    async def prepare(self):
        """Prepare the connection and subscription."""
        await super(BrokerSubscriptionManager, self).prepare()

        self._redis = redis.StrictRedis(self._redis_host, password=self._redis_password)

        # "*" matches any token, at any level of the subject.
        await self._nc.subscribe(constants.BROKER_SUBJECT_REQUEST, cb=self.subject_for_filter)
