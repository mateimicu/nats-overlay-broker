"""WSGI Entry Point."""
from nats_overlay_borker import webapp

if __name__ == "__main__":
    webapp.BROKER.run()
