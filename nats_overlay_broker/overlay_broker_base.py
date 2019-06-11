"""Overlay Broker."""
import asyncio
import redis

from nats_overlay_broker import base_nats_agent
from nats_overlay_broker import exceptional
from nats_overlay_broker import constants

# pylint: disable=dangerous-default-value, abstract-method, broad-except

class BaseBroker(base_nats_agent.BaseNATSAgent):
    """Overlay Broker."""

    def __init__(self, nats_servers=None,
                 redis_host="127.0.0.1", redis_password="Passw0rd"):
        """Initialize the broker agent."""
        super(BaseBroker, self).__init__(nats_servers)
        self._redis_host = redis_host
        self._redis_password = redis_password
        self._redis = None

    @exceptional.america_please_egzblein
    async def prepare(self):
        """Prepare the connection and subscription."""
        await super(BaseBroker, self).prepare()
        for _ in range(constants.RETRY_COUNT):
            try:
                self._redis = redis.StrictRedis(
                    self._redis_host,
                    password=self._redis_password
                )
            except Exception as exc:
                print("Exception: ", exc)
                await asyncio.sleep(constants.ERROT_SLEEP)
