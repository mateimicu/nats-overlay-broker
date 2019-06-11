"""Base Agent to interact with a NATS Cluster."""
import asyncio
import abc


from nats.aio.client import Client as NATS
from nats.aio import errors

from nats_overlay_broker import constants
from nats_overlay_broker import exceptional

# pylint: disable=broad-except
ITEMS_TO_EXCLUDE = [
    "process-dummy-broker",
]

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
        self._subjects_subscribed_to = set()

    @exceptional.america_please_egzblein
    async def publish(self, subject, data):
        """Publish some data to a subject."""
        await self.inc_metric("published-data")
        await self.nats.publish(subject, data)

    @exceptional.america_please_egzblein
    async def inc_metric(self, metric, val=1):
        """Increment the metric."""
        # exclude verbose metrics
        for exc in ITEMS_TO_EXCLUDE:
            if exc in metric:
                return 
        self._inc_metric_call += 1
        if metric not in self._metrics_evaluated:
            self._metrics_evaluated[metric] = 0

        self._metrics_evaluated[metric] += val

    def _prune_metrics(self):
        """Prune metrics."""
        new_metrics = {}
        for metric_name, value in self._metrics_evaluated.items():
            if not isinstance(value, int) or value > constants.MIN_VALUE_METRIC:
                new_metrics[metric_name] = value
        self._metrics_evaluated = new_metrics

    def __print_metrics_header(self):
        """Print the header of the metrics section."""
        print(" ------ Metrics ------ ")

    def __print_metrics_footer(self):
        """Print the header of the metrics section."""
        print("\n"*2)

    def __print_metrics(self):
        """"Print Metrics body."""
        for metric_name, value in self._metrics_evaluated.items():
            print("{:15}: {}".format(metric_name, value))

    async def metrics(self):
        """Print Metrics."""
        while True:
            # self._prune_metrics()
            self.__print_metrics_header()
            self.__print_metrics()
            self.__print_metrics_footer()
            await asyncio.sleep(constants.METRICS_SLEEP)

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

    @property
    def nats(self):
        """NATS client."""
        return self._nc

    async def subscribe_to_subject(self, subject, cb):
        """Subscribe to a subject."""
        sid = await self.nats.subscribe(subject, cb=cb)
        self._subjects_subscribed_to.add(sid)
        await self.inc_metric("create-subscription")

    @abc.abstractmethod
    async def work(self):
        """What will the agent do."""

    async def shutdown(self, signal):
        print("Received exit signal {}...".format(signal.name))
        tasks = [t for t in asyncio.all_tasks() if t is not
                 asyncio.current_task()]
        try:
            print("Subscribe from all nats subjects.")
            for sid in self._subjects_subscribed_to:
                
                await self.nats.unsubscribe(sid)

            print("Drain nats connections.")
            await self.nats.drain()
        except errors.ErrConnectionClosed:
            print("Nats connection terminated already ...")

        print("Cancel all async tasks.")
        [task.cancel() for task in tasks]

        # self.metrics will never stop, maybe from asyncio.sleep
        # print("Canceling outstanding tasks")
        # await asyncio.gather(*tasks)
        self._loop.stop()
        print("Shutdown complete.")

    def start(self):
        """Start the client."""
        print("Start agent ...")
        for sig in constants.TERM_SIGNALS:
            self._loop.add_signal_handler(
                sig, lambda sig=sig: asyncio.create_task(self.shutdown(sig)))

        try:
            asyncio.ensure_future(self.prepare())
            asyncio.ensure_future(self.metrics())
            asyncio.ensure_future(self.work())
            self._loop.run_forever()
        finally:
            print("Closing Loop")
            self._loop.close()

