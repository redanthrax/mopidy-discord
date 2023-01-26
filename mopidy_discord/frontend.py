import logging, os, datetime, asyncio, json

import pykka
from mopidy import core
from mopidy.audio import PlaybackState
from pypresence import Presence

import mopidy_discord.discordthread as discordthread

logger = logging.getLogger(__name__)

class DiscordFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super().__init__()
        self.core = core
        self.config = config
        self.discord = None
        self.connected = False
        self.event_loop = None
        self.set_exception_handler = self.presence_handler
    
    def presence_handler(self, exception, future):
        logger.error(exception)

    def update_presence(self, tl_track, time_position=0):
        logger.info("Updating presence")
        playback = self.core.playback
        library = self.core.library
        track = playback.get_current_track().get()
        try:
            tuples = library.get_images([track.uri]).get()[track.uri]
            cover_uri = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Archlinux-vert-dark.svg/533px-Archlinux-vert-dark.svg.png" # TODO: replace with built in fallback from the app
            if len(tuples) > 0:
                cover_uri = tuples[0].uri
                if cover_uri[:4] != "http":
                    try:
                        cover_uri = get_cover(track)
                    except:
                        logger.info("Could not get cover")

            # TODO: make this look nicer
            length = int(track.length * 0.001) # milliseconds -> seconds
            position = int(playback.get_time_position().get() * 0.001) # milliseconds -> seconds


            current_time = int(datetime.datetime.now().timestamp()) # seconds
            start_time = current_time - position
            end_time = start_time + length
            details = (f"{track.name} - {list(track.artists)[0].name}")[:128]
            state = (f"{track.album.name}")[:128]

            # TODO: use the config as format for details and state etc.
            self.discord.update(
                    details = details,
                    state = state,
                    large_image = cover_uri,
                    small_image = "large_fallback", # TODO: make this configurable and maybe make it show the backend source??
                    large_text = "Mopidy",
                    small_text = "cover",
                    instance = True,
                    start = start_time,
                    end = end_time,
                    pid = os.getpid()
                )
        except pypresence.PyPresenceException:
            logger.error("Presence updated failed...")

    def on_start(self):
        logger.info("Starting Discord Presence")
        try:
            self.event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.event_loop)
            self.discord = Presence(
                    self.config["discord"]["client_id"],
                    pipe=0,
                    loop=self.event_loop,
                    handler=DiscordFrontend.presence_handler)
            self.discord.connect()
            logger.info("Discord connected")
            self.connected = True
        except Exception as e:
            logger.error("Failed to connect", e)
    
    def playback_state_changed(self, old_state, new_state):
        if new_state == "stopped":
            self.discord.clear()

    def track_playback_started(self, tl_track):
        self.update_presence(tl_track)
        
    def track_playback_ended(self, tl_track, time_position):
        self.discord.clear()

    def track_playback_paused(self, tl_track, time_position):
        self.discord.clear()

    def track_playback_resumed(self, tl_track, time_position):
        self.update_presence(tl_track, time_position)
