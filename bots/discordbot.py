import discord
import os
from dotenv import load_dotenv

load_dotenv()

class AEH(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await tree.sync()

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')



intents = discord.Intents.default()
intents.message_content = True
client = AEH(intents=intents)
tree = discord.app_commands.CommandTree(client)

@tree.command(name="hello", description="Say hello to the bot")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hello {interaction.user.display_name}!')

client.run(os.getenv('DISCORD_TOKEN'))
