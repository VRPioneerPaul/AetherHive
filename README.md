# AetherHive ![WIP](https://img.shields.io/badge/status-WIP-yellow)

AetherHive is a personal project of mine in which I am building a Twitch and Discord bot using TwitchIO and Discord.py. Also a Web UI connecting them both.

## 1. Current capabilities

The Twitch bot currently can read chat and listen to a handful of commands.

**Command syntax:** `<required>` `[optional]` `{choice}`

The commands include:
- `!hi`
- `!say <message>`
- `!add <num1> <num2>`
- `!multiply <num1> <num2>` (alias: times, mul)
- `!choice <option1> <option2> [option...]` (alias: choose, pick)
- `!give <name> <amount> [message]` (alias: thank, thanks)
- `!socials {discord|youtube|twitch}` - subcommand aliases: `dc`, `yt`, `tw`

The Discord bot has the least functionality currently with its only command being:
- `!hello`

## 2. Tech Stack

I am using a variety of things that includes:
- TwitchIO
- discord.py
- FastAPI
- Flask
- Asqlite
- HTML/CSS/JS

## 3. Installation/Setup

1. Clone the repo
2. Install the requirements in the `requirements.txt`
3. Set up a Discord bot and Twitch application
4. Set up the `.env` file in this way:
    - DISCORD_TOKEN (Discord bot token)
    - CLIENT_ID     (Twitch application Id)
    - CLIENT_SECRET (Twitch application secret)
    - BOT_ID        (Id of the Twitch bot account)
    - OWNER_ID      (Id of the account of the application)
    - You can use the following link for getting the IDs just from the name of the accounts: https://paru.app/blog/Twitch-get-user-and-streamer-id
5. Run the file `main.py` in the root directory
6. On first run you'll need the permissions to your Twitch account (for viewing chat and events) so just log-in with this link: [OAuth Link](http://localhost:4343/oauth?scopes=user:read:chat%20user:write:chat%20user:bot%20channel:bot%20channel:read:redemptions%20channel:manage:redemptions%20channel:read:subscriptions%20bits:read%20moderator:read:chatters%20moderator:read:followers%20channel:read:moderators%20channel:read:vips%20channel:read:goals%20channel:read:hype_train%20channel:read:polls%20channel:read:predictions&force_verify=true) after giving the Twitch application this redirect link: http://localhost:4343/oauth/callback

## 4. Roadmap

- [x] basic Twitch bot
- [x] basic Discord bot
- [ ] combined Web UI (status and live log)
- [x] one file starts all
- [ ] advanced bot capabilities
- [ ] advanced Web UI (ability to add commands and things from it)

maybe more in the future...

## 5. License

No license yet.

## 6. Contribution

No contribution for now.

## Why I am doing this

This is a project of mine I am going to be using to learn Python in a way I could maybe ship real apps at the end.
I am doing this next to drawing for my rebranding on social media. I was going by VRPioneerPaul but now I am going by Aether (day-to-day) and AetherPioneer (formally).
