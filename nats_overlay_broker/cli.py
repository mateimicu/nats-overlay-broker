#!/usr/bin/env python
"""Basic CLI implementation."""
import argparse
from nats_overlay_broker import webapp
from nats_overlay_broker import snitch
from nats_overlay_broker import pollution
from nats_overlay_broker import publicationFeed
from nats_overlay_broker import subscriptionFeed

MODES = {
    "broker": 
        lambda args: webapp.BROKER.run(host='0.0.0.0', port='7777'),

    "publisher": 
        lambda args: publicationFeed.PublicationFeed(args.nats_server).start(),

    "subscriber": 
        lambda args: subscriptionFeed.SubscriptionFeed(args.nats_server).start(),

    "snitch": 
        lambda args: snitch.Snitch(args.nats_server).start(),

    "pollution": 
    lambda args: pollution.Pollution(args.nats_server).start()
}

def get_parser():
    """Create a new Argument Parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="host to bind the server",
                        choices=MODES.keys())
    parser.add_argument("--nats-server", help="port to bind the server",
                        default=["nats://127.0.0.1:4222"],  nargs='+')
    return parser

def main():
    """Main entry point for the CLI."""
    parser = get_parser()
    args = parser.parse_args()
    MODES[args.mode](args)

if __name__ == "__main__":
    main()
