import configparser
from pathlib import Path

import bluebubbles_py


def main():
    config = configparser.ConfigParser()
    config.read(Path(__file__).parent.joinpath(Path("config.ini")))
    url = config["config"]["url"]
    password = config["config"]["password"]

    client = bluebubbles_py.Client()

    @client.event
    async def on_connect():
        print("client has been connect, ready to send + receive messages")

    @client.event
    async def on_ready():
        print("client's cache is ready")

    client.run(url, password)


if __name__ == "__main__":
    main()
