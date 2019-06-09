"""Base Agent to interact with a NATS Cluster."""
import asyncio
from nats.aio.client import Client as NATS
import abc


class BaseNATSAgent(abc.ABC):
    """Base Agent."""

    def __init__(self, nats_servers=["nats://127.0.0.1:4222"]):
        """Initialize the agent."""
        self._nats_servers = nats_servers
        self._loop = asyncio.get_event_loop()
        self._nc = None

    async def prepare(self):
        """Prepare the connection."""
        self._nc = NATS()
        for _ in range(10):
            try:
                await self._nc.connect(
                    servers=self._nats_servers,
                    loop=self._loop,
                    ping_interval=20,
                    max_reconnect_attempts=10,
                )
                break
            except Exception as exc:
                print("Exception in trying to connect: ", exc)
                await asyncio.sleep(1)

    @abc.abstractmethod 
    async def work(self):
        pass


    def start(self):
        """Start the client."""
        print("Start agent ...")

        try:
            asyncio.ensure_future(self.prepare())
            asyncio.ensure_future(self.work())
            self._loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            print("Closing Loop")
            self._nc.drain()
            self._loop.close()
