import configparser

import bluebubbles_py


config = configparser.ConfigParser()
config.read("config.ini")
url = config["config"]["url"]
password = config["config"]["password"]

client = bluebubbles_py.Client()


@client.event
async def on_ready():
    print("on ready called")


client.run(url, password)
