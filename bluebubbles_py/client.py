import asyncio
import inspect
import signal
from typing import Coroutine


class Client:
    """A client connection to BlueBubbles, used to interface with the BlueBubbles API"""

    def __init__(self):
        self.loop = asyncio.get_event_loop()

    # event registrar
    def event(self, event: Coroutine) -> Coroutine:
        """
        Registers a listener for a BlueBubbles event.
        Events must be coroutines.

        Parameters:
            event (Coroutine): The event to register
        """
        setattr(self, event.__name__, event)
        return event

    def __dispatch(self, event: str, *args, **kwargs):
        coro = getattr(self, event, None)
        if inspect.iscoroutinefunction(coro):
            asyncio.create_task(coro(*args, **kwargs), name=f"bluebubbles_py: {event}")

    async def start(self, url: str, password: str):
        """
        Coroutine which starts the event loop from an already existing asyncio context.
        Similar to :meth:`.run`, but from an async context.

        Parameters:
            url (str): The BlueBubbles server URL to connect to.
            password (str): The BlueBubbles password.
        """
        self.__dispatch("on_connect")

    def run(self, url: str, password: str):
        """
        Blocking method which starts the event loop and connects to the BlueBubbles server.

        Parameters:
            url (str): The BlueBubbles server URL to connect to.
            password (str): The BlueBubbles password.
        """
        print(f"Print called with url {url} and password {password}")
        try:
            self.loop.add_signal_handler(signal.SIGINT, self.loop.stop)
            self.loop.add_signal_handler(signal.SIGTERM, self.loop.stop)
        except (NotImplementedError, RuntimeError):
            pass

        asyncio.ensure_future(self.start(url, password), loop=self.loop)
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            print("stopping bluebubbles_py")
