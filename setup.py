"""Nats Overlay Broker packaging setup."""
from setuptools import find_packages
from setuptools import setup

setup(
    name='nats_overlay_broker',
    version='0.0.1',
    keywords='NATS Streaming ',
    license="MIT",
    packages=find_packages(),
    entry_points = {
        'console_scripts': ['nats_overlay_broker=nats_overlay_broker.cli:main'],
      },
)
