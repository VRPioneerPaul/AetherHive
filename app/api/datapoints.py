from dataclasses import dataclass

@dataclass
class TwitchData:
    twitch_online: bool = False
    twitch_game: str = ''
    twitch_title: str = ''
    twitch_viewers: int = 0
    latest_follow: str = ''
    latest_sub: str = ''
    latest_cheer: str = ''
    latest_raid: str = ''
    latest_message: str = ''

@dataclass
class DiscordData:
    guild_members: int = 0
    latest_message: str = ''

dcdata = DiscordData()
twdata = TwitchData()