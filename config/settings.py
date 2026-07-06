from dotenv import load_dotenv
import os
from dataclasses import dataclass

load_dotenv()

@dataclass(frozen=True)
class Setting:
    CLIENT_ID: str
    CLIENT_SECRET: str
    BOT_ID: str
    OWNER_ID: str
    DISCORD_TOKEN: str

setting = Setting(
    CLIENT_ID=os.getenv('CLIENT_ID', ''),
    CLIENT_SECRET=os.getenv('CLIENT_SECRET', ''),
    BOT_ID=os.getenv('BOT_ID', ''),
    OWNER_ID=os.getenv('OWNER_ID', ''),
    DISCORD_TOKEN=os.getenv('DISCORD_TOKEN', '')
)