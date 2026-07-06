from bots.discordbot import start as discord_start
from bots.twitchbot import main as twitch_main
# import app.api.main
# import app.web.flaskapp

import threading
import time

twitch_thread = threading.Thread(target=twitch_main, daemon=True)

if __name__ == "__main__":
    twitch_thread.start()

    discord_start()

    twitch_thread.join()