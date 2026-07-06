from bots.discordbot import start as discord_start
from bots.twitchbot import main as twitch_main
# import app.api.main
# import app.web.flaskapp

import threading

if __name__ == "__main__":
    twitch_thread = threading.Thread(target=twitch_main, daemon=True)

    twitch_thread.start()

    discord_start()

    twitch_thread.join()