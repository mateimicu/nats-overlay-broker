#!/usr/bin/env python
"""Basic CLI implementation."""
import argparse
import logging
import sys


from nats_overlay_broker import snitch
from nats_overlay_broker import pollution
from nats_overlay_broker import publicationFeed
from nats_overlay_broker import subscriptionFeed
from nats_overlay_broker import deterministicPublicationFeed
from nats_overlay_broker import deterministicSubscriptionFeed
from nats_overlay_broker import overlay_broker_multiplexer
from nats_overlay_broker import overlay_broker_subscription_manager


MODES = {
    "broker-m": 
        lambda args: overlay_broker_multiplexer.BrokerMultiplexer(nats_servers=args.nats_server,redis_host=args.redis_host,redis_password=args.redis_password).start(),
    "broker-sm": 
        lambda args: overlay_broker_subscription_manager.BrokerSubscriptionManager(nats_servers=args.nats_server,redis_host=args.redis_host,redis_password=args.redis_password).start(),

    "publisher": 
        lambda args: publicationFeed.PublicationFeed(args.nats_server).start(),

    "determinist-subscriber": 
        lambda args: deterministicSubscriptionFeed.DeterministicSubscriptionFeed(args.nats_server).start(),

    "determinist-publisher": 
        lambda args: deterministicPublicationFeed.DeterministicPublicationFeed(args.nats_server).start(),

    "subscriber": 
        lambda args: subscriptionFeed.SubscriptionFeed(args.nats_server).start(),

    "snitch": 
        lambda args: snitch.Snitch(args.nats_server).start(),

    "pollution": 
    lambda args: pollution.Pollution(args.nats_server).start()
}

def prepare_logger():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

def get_parser():
    """Create a new Argument Parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="host to bind the server",
                        choices=MODES.keys())
    parser.add_argument("--nats-server", help="port to bind the server",
                        default=["nats://127.0.0.1:4222"],  nargs='+')
    parser.add_argument("--redis-host", help="redis host",
                        default="127.0.0.1")
    parser.add_argument("--redis-password", help="redis password",
                        default="Passw0rd")
    return parser

def main():
    """Main entry point for the CLI."""
    print("Agent ...", flush=True)
    prepare_logger()

    parser = get_parser()
    args = parser.parse_args()
    print(args, flush=True)

    MODES[args.mode](args)

if __name__ == "__main__":
    main()
