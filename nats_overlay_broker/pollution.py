"""Pollute the `junk` channel."""
import random
import string
import socket

import asyncio

from nats_overlay_broker import base_nats_agent

class Pollution(base_nats_agent.BaseNATSAgent):
    """Pollute the `junk` channel."""

    def __init__(self, *args, **kwargs):
        """Initialize the pollution client."""
        super(Pollution, self).__init__(*args, **kwargs)
        self._host_name = socket.gethostname()
        self._client_random_id = ''.join(random.choice(string.ascii_lowercase) for i in range(4))
        self._client_id = "[{}]-{}".format(self._client_random_id, self._host_name)


    async def work(self):
        """Inject a number in the `junk` channel."""
        print("Start injecting messages ...")
        data = 0
        while True:
            data += 1
            message = bytes(
                "{}: {}".format(self._client_id, data),
                "utf-8"
            )
            await self.publish("junk", message)
            print("Sending on 'junk': {}".format(message))
            await asyncio.sleep(1)
