import discord
from config.settings import setting
from app.state import state
import logging

LOGGER: logging.Logger = logging.getLogger("Bot_DC")

class AEH(discord.Client):
    async def on_ready(self):
        LOGGER.info(f'Logged in as {self.user} (ID: {self.user.id})')
        await tree.sync()
        state.discord_online = True

    async def on_message(self, message):
        LOGGER.info(f'Message from {message.author}: {message.content}')

    async def on_disconnect(self):
        LOGGER.warning("Disconnected from Discord")
        state.discord_online = False



intents = discord.Intents.default()
intents.message_content = True
client = AEH(intents=intents)
tree = discord.app_commands.CommandTree(client)

@tree.command(name="hello", description="Say hello to the bot")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hello {interaction.user.display_name}!')

def start():
    client.run(setting.DISCORD_TOKEN)

if __name__ == "__main__":
    start()