"""Base Agent to interact with a NATS Cluster."""
import asyncio
from nats.aio.client import Client as NATS
import abc

from nats_overlay_broker import constants
from nats_overlay_broker import exceptional

class BaseNATSAgent(abc.ABC):
    """Base Agent."""

    def __init__(self, nats_servers=["nats://127.0.0.1:4222"]):
        """Initialize the agent."""
        self._nats_servers = nats_servers
        self._loop = asyncio.get_event_loop()
        self._nc = None
        self._inc_metric_call = 0
        self._metrics_evaluated = {}

    @exceptional.america_please_egzblein

    async def publish(seld, subject, data):
        """Publish some data to a subject."""
        await self._nc.publish(subject, data)

    @exceptional.america_please_egzblein
    async def inc_metric(self, metric, val=1):
        self._inc_metric_call += 1
        if metric not in self._metrics_evaluated:
            self._metrics_evaluated[metric] = 0

        self._metrics_evaluated[metric] += val
        if self._inc_metric_call % constants.BATCH_PROCESS_MESSAGES:
            print(" ------ Metrics ------ ")
            for metric, value in self._metrics_evaluated.items():
                print("{:15}: {}".format(metric, value))
            print("\n"*2)

    @exceptional.america_please_egzblein
    async def prepare(self):
        """Prepare the connection."""
        self._nc = NATS()
        for _ in range(10):
            try:
                await self._nc.connect(
                    servers=self._nats_servers,
                    loop=self._loop,
                    ping_interval=1,
                    max_reconnect_attempts=10,
                )
                break
            except Exception as exc:
                print("Exception in trying to connect: ", exc)
                await asyncio.sleep(1)

    @abc.abstractmethod 
    async def work(self):
        """What will the agent do."""
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
