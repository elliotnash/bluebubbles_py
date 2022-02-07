import config

import bluebubbles_py


def main():
    client = bluebubbles_py.Client()

    @client.event
    async def on_connect():
        print("client has been connect, ready to send + receive messages")

    @client.event
    async def on_ready():
        print("client's cache is ready")

    client.run(config.url, config.password)


if __name__ == "__main__":
    main()
