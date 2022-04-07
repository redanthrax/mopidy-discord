'''
this is probably like the worst way to go about this but I Don't care I'm not good at this I just wanted to have cool rich presence on Dick Cord
'''
import logging, threading, asyncio, datetime

from mopidy.audio import PlaybackState

import pypresence, requests
import musicbrainzngs as mb

logger = logging.getLogger(__name__)
__version__ = pkg_resources.get_distribution("Mopidy-Discord").version

class DiscordThread(threading.Thread):
    def __init__(self, config, core, pid):
        super().__init__()
        self.core = core
        self.config = config
        self.name = "DiscordThread"
        self.pid = pid

        self.discord = None

        self.updateEvent = threading.Event()
        self.shutdownEvent = threading.Event()
        
        self.event_loop = None
    
    def run(self):
        logger.info("Starting Discord RPC")

        self.event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.event_loop)

        self.discord = pypresence.Presence(self.config["discord"]["client_id"])
        self.discord.connect()

        logger.info("Entering Discord event loop")
        while True:
            if self.shutdownEvent.is_set():
                break
            if not self.updateEvent.is_set():
                continue

            logger.info("Updating presence")

            playback = self.core.playback
            library = self.core.library
            track = playback.get_current_track().get()
            # TODO: make a thing that displays the presence for a few seconds
            #       before clearing and make it possible to change it in the
            #       config
            if not (track and (playback.get_state().get() == PlaybackState.PLAYING)):
                self.discord.clear(self.pid)
                self.updateEvent.clear()
                continue

            # TODO: what the fuck is this god I don't know how to write code
            tuples = library.get_images([track.uri]).get()[track.uri]
            cover_uri = tuples[0].uri
            if cover_uri[:4] != "http":
                cover_uri = get_cover(track)
                if cover_uri == "":
                    cover_uri = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Arch_Linux_logo.svg/1280px-Arch_Linux_logo.svg.png" # TODO: replace with built in fallback from the app

            # TODO: make this look nicer
            length = int(track.length * 0.001) # milliseconds -> seconds
            position = int(playback.get_time_position().get() * 0.001) # milliseconds -> seconds
            current_time = int(datetime.datetime.now().timestamp()) # seconds

            start_time = current_time - position
            end_time = start_time + length

            # TODO: use the config as format for details and state etc.
            self.discord.update(
                    details = f"{track.name} - {list(track.artists)[0].name}",
                    state = f"{track.album.name}",
                    large_image = cover_uri,
                    small_image = "large_fallback", # TODO: make this configurable and maybe make it show the backend source??
                    large_text = "Mopidy",
                    small_text = "spaghetti cat", # TODO: line 76
                    instance = True,
                    start = start_time,
                    end = end_time,
                    pid = self.pid
                )

            self.updateEvent.clear()

        logger.info("Closing Discord RPC")
        self.discord.close()

# TODO: try to upload local cover file to remote server instead of bothering
#       musicbrainz
def get_cover(track):
    # this could probably easily fail LOL
    img_url = ""
    mb.set_useragent(app="mopidy-discord", version=__version__, contact="fantoro@outlook.com")

    recordings = mb.search_release_groups(track.album.name, artistname=list(track.artists)[0].name)
    recording = recordings["release-group-list"][0]
    release = recording["release-list"][0]
    imgs = mb.get_release_group_image_list(recording["id"])

    img_url = imgs["images"][0]["thumbnails"]["large"]

    return img_url
