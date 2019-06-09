"""Base Agent to interact with a NATS Cluster."""
import asyncio
import abc

from nats.aio.client import Client as NATS
from nats.aio.errors import ErrTimeout, ErrNoServers
from async_property import async_property


from nats_overlay_broker import constants
from nats_overlay_broker import exceptional

class BaseNATSAgent(abc.ABC):
    """Base Agent."""

    def __init__(self, nats_servers=None):
        """Initialize the agent."""
        self._nats_servers = nats_servers
        if self._nats_servers is None:
            self._nats_servers = constants.DEFAULT_NATS_SERVERS
        self._loop = asyncio.get_event_loop()
        self._nc = None
        self._inc_metric_call = 0
        self._metrics_evaluated = {}

    @exceptional.america_please_egzblein
    async def publish(self, subject, data):
        """Publish some data to a subject."""
        await self.nats.publish(subject, data)

    @exceptional.america_please_egzblein
    async def inc_metric(self, metric, val=1):
        """Increment the metric."""
        self._inc_metric_call += 1
        if metric not in self._metrics_evaluated:
            self._metrics_evaluated[metric] = 0

        self._metrics_evaluated[metric] += val
        if self._inc_metric_call % constants.BATCH_PROCESS_MESSAGES == 0:
            print(" ------ Metrics ------ ")
            for metric_name, value in self._metrics_evaluated.items():
                print("{:15}: {}".format(metric_name, value))
            print("\n"*2)

    @exceptional.america_please_egzblein
    async def prepare(self):
        """Prepare the connection."""
        self._nc = NATS()
        await self._nc.connect(
            servers=self._nats_servers,
            loop=self._loop,
            ping_interval=1,
            max_reconnect_attempts=10,
        )

    @async_property
    async def nats(self):
        """NATS client."""
        for _ in range(constants.RETRY_COUNT):
            try:
                if self._nc.ping():
                    return self._nc
            except (ErrTimeout, ErrNoServers):
                await asyncio.sleep(constants.SLEEP_TIMEOUT)
        raise Exception("Can't connect to NATS server ...")

    @abc.abstractmethod
    async def work(self):
        """What will the agent do."""

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
            self.nats.drain()
            self._loop.close()
