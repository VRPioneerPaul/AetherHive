from dataclasses import dataclass

@dataclass
class BotState:
    discord_online: bool = False
    twitch_online: bool = False

    @property
    def overall_online(self) -> bool:
        return self.discord_online and self.twitch_online

state = BotState()