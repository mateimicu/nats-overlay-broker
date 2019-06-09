"""Overlay Broker."""

import redis
import asyncio

from nats.aio.client import Client as NATS

from nats_overlay_broker import baseNatsAgent
from nats_overlay_broker import constants
from nats_overlay_broker import person
from nats_overlay_broker import exceptional

class BaseBroker(baseNatsAgent.BaseNATSAgent):
    """Overlay Broker."""

    def __init__(self, nats_servers=["nats://127.0.0.1:4222"], 
                redis_host="127.0.0.1", redis_password="Passw0rd"):
        """Initialize the broker agent."""
        super(BaseBroker, self).__init__(nats_servers)
        self._redis_host = redis_host
        self._redis_password = redis_password

    async def prepare(self):
        """Prepare the connection and subscription."""
        await super(BaseBroker, self).prepare()
        self._redis = redis.StrictRedis(self._redis_host, password=self._redis_password)

