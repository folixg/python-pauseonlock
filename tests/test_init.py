from pauseonlock import PauseOnLock
from dbus_next.aio import MessageBus
import asyncio


class TestPauseOnLock:
    loop = asyncio.get_event_loop()

    def test_init(self):
        pol = PauseOnLock()
        assert isinstance(pol.bus, MessageBus)
        assert pol.running_players == []

    def test_connect_bus(self):
        pol = PauseOnLock()
        assert not pol.bus.connected
        self.loop.run_until_complete(pol.connect_to_bus())
        assert pol.bus.connected
