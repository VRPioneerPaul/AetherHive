import asyncio
import logging
import random
from typing import TYPE_CHECKING
import asqlite
from config.settings import setting
import twitchio
from twitchio import eventsub
from twitchio.ext import commands

if TYPE_CHECKING:
    import sqlite3


LOGGER: logging.Logger = logging.getLogger("Bot")


CLIENT_ID = setting.CLIENT_ID
CLIENT_SECRET = setting.CLIENT_SECRET
BOT_ID = setting.BOT_ID
OWNER_ID = setting.OWNER_ID 


class Bot(commands.AutoBot):
    def __init__(self, *, token_database: asqlite.Pool, subs: list[eventsub.SubscriptionPayload]) -> None:
        self.token_database = token_database

        super().__init__(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            bot_id=BOT_ID,
            owner_id=OWNER_ID,
            prefix="!",
        )

    async def setup_hook(self) -> None:
        await self.add_component(CommandLists(self))

    async def event_oauth_authorized(self, payload: twitchio.authentication.UserTokenPayload) -> None:
        await self.add_token(payload.access_token, payload.refresh_token)

        if not payload.user_id:
            return

        if payload.user_id == self.bot_id:
            return

        subs: list[eventsub.SubscriptionPayload] = [
            eventsub.ChatMessageSubscription(broadcaster_user_id=payload.user_id, user_id=self.bot_id),
        ]

        resp: twitchio.MultiSubscribePayload = await self.multi_subscribe(subs)
        if resp.errors:
            LOGGER.warning("Failed to subscribe to: %r, for user: %s", resp.errors, payload.user_id)

    async def add_token(self, token: str, refresh: str) -> twitchio.authentication.ValidateTokenPayload:
        resp: twitchio.authentication.ValidateTokenPayload = await super().add_token(token, refresh)

        query = """
        INSERT INTO tokens (user_id, token, refresh)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET
            token = excluded.token,
            refresh = excluded.refresh;
        """

        async with self.token_database.acquire() as connection:
            await connection.execute(query, (resp.user_id, token, refresh))

        LOGGER.info("Added token to the database for user: %s", resp.user_id)
        return resp

    async def event_ready(self) -> None:
        LOGGER.info("Successfully logged in as: %s", self.bot_id)

#        await setup_eventsub(self)


class CommandLists(commands.Component):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.Component.listener()
    async def event_message(self, payload: twitchio.ChatMessage) -> None:
        print(f"[{payload.broadcaster.name}] - {payload.chatter.name}: {payload.text}")

    @commands.command()
    async def hi(self, ctx: commands.Context) -> None:
        await ctx.reply(f"Hi {ctx.chatter}!")

    @commands.command()
    async def say(self, ctx: commands.Context, *, message: str) -> None:
        await ctx.send(message)

    @commands.command()
    async def add(self, ctx: commands.Context, left: int, right: int) -> None:
        await ctx.reply(f"{left} + {right} = {left + right}")

    @commands.command(aliases=["times", "mul"])
    async def multiply(self, ctx: commands.Context, left: int, right: int) -> None:
        await ctx.reply(f"{left} * {right} = {left * right}")

    @commands.command(aliases=["choose", "pick"])
    async def choice(self, ctx: commands.Context, *choices: str) -> None:
        await ctx.reply(f"You provided {len(choices)} choices, I choose: {random.choice(choices)}")

    @commands.command(aliases=["thanks", "thank"])
    async def give(self, ctx: commands.Context, user: twitchio.User, amount: int, *, message: str | None = None) -> None:
        msg = f"with message: {message}" if message else ""
        await ctx.send(f"{ctx.chatter.mention} gave {amount} thanks to {user.mention} {msg}")

    @commands.group(invoke_fallback=True)
    async def socials(self, ctx: commands.Context) -> None:
        await ctx.send("Available socials: !socials discord, !socials youtube, !socials twitch")

    @socials.command(name="discord", aliases=["dc"])
    async def socials_discord(self, ctx: commands.Context) -> None:
        await ctx.send("discord.gg/invite/qXXPVv2xss (Aether Hub the Community Server)")

    @socials.command(name="youtube", aliases=["yt"])
    async def socials_youtube(self, ctx: commands.Context) -> None:
        await ctx.send("youtube.com/@aetherpioneer")

    @socials.command(name="twitch", aliases=["tw"])
    async def socials_twitch(self, ctx: commands.Context) -> None:
        await ctx.send("twitch.tv/aetherpioneer (You're already here!) twitch.tv/aetherhelper (The Bot Account)")

async def setup_eventsub(self):
    broadcaster_id = str(self.owner_id)

    await self.subscribe_websocket(
        payload=eventsub.ChannelSubscribeSubscription(
            broadcaster_user_id=broadcaster_id
        )
    )

    await self.subscribe_websocket(
        payload=eventsub.ChannelCheerSubscription(
            broadcaster_user_id=broadcaster_id
        )
    )

    await self.subscribe_websocket(
        payload=eventsub.ChannelRaidSubscription(
            to_broadcaster_user_id=broadcaster_id
        )
    )

    await self.subscribe_websocket(
        payload=eventsub.ChannelPointsRedeemAddSubscription(
            broadcaster_user_id=broadcaster_id
        )
    )

async def setup_database(db: asqlite.Pool) -> tuple[list[tuple[str, str]], list[eventsub.SubscriptionPayload]]:
    query = """CREATE TABLE IF NOT EXISTS tokens(user_id TEXT PRIMARY KEY, token TEXT NOT NULL, refresh TEXT NOT NULL)"""
    async with db.acquire() as connection:
        await connection.execute(query)

        rows: list[sqlite3.Row] = await connection.fetchall("""SELECT * from tokens""")

        tokens: list[tuple[str, str]] = []
        subs: list[eventsub.SubscriptionPayload] = []

        for row in rows:
            tokens.append((row["token"], row["refresh"]))

            if row["user_id"] == BOT_ID:
                continue

            subs.extend([eventsub.ChatMessageSubscription(broadcaster_user_id=row["user_id"], user_id=BOT_ID),
            ])

    return tokens, subs

def main() -> None:
    twitchio.utils.setup_logging(level=logging.INFO)

    async def runner() -> None:
        async with asqlite.create_pool("tokens.db") as tdb:
            tokens, subs = await setup_database(tdb)

            async with Bot(token_database=tdb, subs=subs) as bot:
                for pair in tokens:
                    await bot.add_token(*pair)

                await bot.start(load_tokens=False)

    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        LOGGER.warning("Shutting down due to KeyboardInterrupt")


if __name__ == "__main__":
    main()