#!/usr/bin/env python3
import argparse
import asyncio
from enum import Enum
import logging

from dbus_next.aio import MessageBus


class Services(Enum):
    PLAYER = 0
    SCREENSAVER = 1


class PauseOnLock:
    def __init__(self, debug=False):
        self.bus = MessageBus()
        self.running_players = []
        self.logger = logging.getLogger(__name__)
        self._configure_logging(debug)
        if debug:
            self.logger.info("Running with debug output enabled")

    DBUS_INTRO = """
        <node>
            <interface name="org.freedesktop.DBus">
                <method name="ListNames">
                    <arg direction="out" type="as"/>
                </method>
            </interface>
        </node>
    """
    PLAYER_INTRO = """
        <node>
            <interface name="org.mpris.MediaPlayer2.Player">
                <method name="Play"/>
                <method name="Pause"/>
                <property type="s" name="PlaybackStatus" access="read"/>
            </interface>
        </node>
    """

    def _configure_logging(self, debug=False):
        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.WARNING)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    async def connect_to_bus(self):
        await self.bus.connect()

    async def get_service_list(self, service_type: Services) -> list:
        obj = self.bus.get_proxy_object(
            "org.freedesktop.DBus", "/org/freedesktop/DBus", self.DBUS_INTRO
        )
        dbus = obj.get_interface("org.freedesktop.DBus")
        services = await dbus.call_list_names()
        if service_type == Services.PLAYER:
            return [x for x in services if "org.mpris.MediaPlayer2" in x]
        if service_type == Services.SCREENSAVER:
            return [
                x for x in services if ".ScreenSaver" in x and ".freedesktop." not in x
            ]
        else:
            raise ValueError

    async def update_running_players(self):
        self.running_players = []
        player_list = await self.get_service_list(Services.PLAYER)
        self.logger.debug(f"Players visible on dbus: {player_list}")
        for p in player_list:
            obj = self.bus.get_proxy_object(
                p, "/org/mpris/MediaPlayer2", self.PLAYER_INTRO
            )
            player_iface = obj.get_interface("org.mpris.MediaPlayer2.Player")
            if "Playing" == await player_iface.get_playback_status():
                self.running_players.append(player_iface)
                self.logger.debug(f"Added {p} to list of running players")

    async def play_pause_players(self, lock_status: bool):
        if lock_status:
            await self.update_running_players()
            for player in self.running_players:
                await player.call_pause()
                self.logger.debug(f"Paused {player.bus_name}")

        else:
            for player in self.running_players:
                await player.call_play()
                self.logger.debug(f"Resumed {player.bus_name}")

    def on_lock_change(self, value):
        self.logger.debug(f'Screensaver status changed to "{value}"')
        asyncio.create_task(self.play_pause_players(value))

    async def run(self):
        await self.connect_to_bus()
        screensavers = await self.get_service_list(Services.SCREENSAVER)
        for s in screensavers:
            introspection = (
                f'<node><interface name="{s}"><signal name="ActiveChanged">'
                '<arg type="b" name="new_value"></arg></signal></interface></node>'
            )
            obj = self.bus.get_proxy_object(s, f"/{s.replace('.', '/')}", introspection)
            iface = obj.get_interface(s)
            iface.on_active_changed(self.on_lock_change)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Pause media players when locking your screen "
            "and resume playback when unlocking"
        )
    )
    parser.add_argument("--debug", action="store_true", help="Print debug output")
    args = parser.parse_args()
    # run the main function in an endless loop
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(PauseOnLock(args.debug).run())
    loop.run_forever()


if __name__ == "__main__":
    main()
