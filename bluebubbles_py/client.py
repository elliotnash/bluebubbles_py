import asyncio
import inspect
import signal
from typing import Coroutine


class Client:
    def __init__(self):
        self.tasks = []
        self.loop = asyncio.get_event_loop()

    # event registrar
    def event(self, event: Coroutine):
        setattr(self, event.__name__, event)

    def __dispatch(self, event: str, *args, **kwargs):
        coro = getattr(self, event, None)
        if inspect.iscoroutinefunction(coro):
            asyncio.create_task(coro(*args, **kwargs), name=f"bluebubbles_py: {event}")

    async def start(self, url: str, password: str):
        self.__dispatch("on_connect")

    def run(self, url: str, password: str):
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
