import logging, os

import pykka
from mopidy import core
from mopidy.audio import PlaybackState

import mopidy_discord.discordthread as discordthread

logger = logging.getLogger(__name__)

class DiscordFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super(DiscordFrontend, self).__init__()
        self.config = config
        self.core = core
        self.discord = None
        self.lock = False

    def on_start(self):
        logger.info("Starting Discord RPC")
        self.discord = discordthread.DiscordThread(self.config, self.core, os.getpid())
        self.discord.start()
        self.discord.updateEvent.set()

    def on_stop(self):
        logger.info("Stopping Discord RPC")
        self.discord.shutdownEvent.set()

    def on_event(self, event, **kwargs):
        self.discord.updateEvent.set()
