"""Generate a feed of publications."""
import asyncio

from nats_overlay_broker import base_nats_agent
from nats_overlay_broker import person
from nats_overlay_broker import constants

class PublicationFeed(base_nats_agent.BaseNATSAgent):
    """Generate Persons and publish them."""

    async def work(self):
        """Publish random Persons."""
        print("Start injecting Persons ...")

        while True:
            pers = person.Person.get_random_person()
            message = pers.as_json_bytes()

            await self.inc_metric("published-persons")

            await self.publish(constants.BROKER_PUBLISH_SUBJECT, message)
            await asyncio.sleep(constants.SLEEP_TIMEOUT)
