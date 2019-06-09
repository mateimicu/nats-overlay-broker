#!/usr/bin/env python
import requests
import sys
import json
from packaging import version

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage {} <image_name>".format(sys.argv[0]))
        return
    url = "https://registry.hub.docker.com/v1/repositories/{}/tags".format(sys.argv[1])
    response = requests.get(url)
    response.raise_for_status()

    tags = json.loads(response.text)

    versions = []
    for item in tags:
        try:
            versions.append(version.parse(item["name"]))
        except version.InvalidVersion:
            pass

    versions.sort(reverse=True)
    if len(versions):
        latest_version = versions.pop(0)
    else:
        latest_version = version.Version("0.0.0")
    next_version = version.Version(
        "{}.{}.{}".format(
            latest_version.release[0],
            latest_version.release[1],
            latest_version.release[2]+1,
        )
    )
    print(next_version)

if __name__ == "__main__":
    main()
