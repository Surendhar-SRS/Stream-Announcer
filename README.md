# Discord Content Notification Bot 🤖

A powerful Python Discord bot that automatically notifies your Discord server when you go live or post new content on YouTube, Twitch, and Kick. Features modern slash commands and beautiful rich embeds!

## ✨ Features

- 🎥 **YouTube**: Get notified with rich embeds when new videos are uploaded
- 🔴 **Twitch**: Get instant alerts when you go live with stream details and viewer counts
- 🟢 **Kick**: Get notified when you start streaming on Kick
- 💬 **Modern Slash Commands**: Easy-to-use Discord slash commands
- 📢 Beautiful rich embed notifications with thumbnails, colors, and clickable links
- ⚡ Real-time monitoring (automatically checks every 2 minutes)
- 🎯 Fully customizable per platform
- 🔔 @everyone mentions for maximum visibility
- 📊 Detailed status tracking and manual content checking

## 🚀 Quick Start

### 1. Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to "Bot" section and click "Add Bot"
4. Enable these Privileged Gateway Intents:
   - **Message Content Intent** ✅
5. Copy the bot token (you'll need this later)
6. Go to OAuth2 > URL Generator:
   - Select scopes: `bot`, `applications.commands`
   - Select bot permissions: 
     - `Send Messages`
     - `Embed Links`
     - `Read Messages/View Channels`
     - `Mention Everyone`
7. Use the generated URL to invite the bot to your server

### 2. Get Your Discord Channel ID

1. Enable Developer Mode in Discord (Settings > Advanced > Developer Mode)
2. Right-click the channel where you want notifications
3. Click "Copy ID"

### 3. Platform-Specific Setup

#### YouTube (Optional)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **YouTube Data API v3**
4. Create credentials (API Key)
5. Get your YouTube Channel ID from your channel URL or channel settings

**Free quota:** 10,000 units/day (plenty for this bot!)

#### Twitch (Optional)
1. Go to [Twitch Developer Console](https://dev.twitch.tv/console)
2. Enable 2FA on your Twitch account first
3. Register a new application
4. Get your Client ID and generate a Client Secret
5. Note your Twitch username

#### Kick (Optional)
- Just need your Kick username (no API key required!) 🎉

### 4. Configure Environment Variables

Add these secrets in the Replit Secrets tab:

**Required:**
```
DISCORD_TOKEN - Your Discord bot token
DISCORD_CHANNEL_ID - The channel ID for notifications
```

**Optional (configure only the platforms you want to monitor):**
```
YOUTUBE_API_KEY - Your YouTube API key
YOUTUBE_CHANNEL_ID - Your YouTube channel ID
TWITCH_CLIENT_ID - Your Twitch application client ID
TWITCH_CLIENT_SECRET - Your Twitch application secret
TWITCH_USERNAME - Your Twitch username
KICK_USERNAME - Your Kick username
```

## 💬 Slash Commands

The bot uses modern Discord slash commands. Just type `/` in any channel to see available commands!

| Command | Description | Permissions |
|---------|-------------|-------------|
| `/status` | View monitoring status for all configured platforms | Everyone |
| `/test` | Send a test notification to verify the bot is working | Admin only |
| `/check` | Manually check for new content on all platforms right now | Admin only |
| `/help` | Show detailed help and bot information | Everyone |

### Command Examples

**Check Bot Status:**
```
/status
```
Shows which platforms are being monitored, usernames/channel IDs, and check interval.

**Test Notifications:**
```
/test
```
Sends a test embed to verify the bot is working correctly (admin only).

**Manual Content Check:**
```
/check
```
Immediately checks all platforms for new content without waiting for the automatic interval (admin only).

**Get Help:**
```
/help
```
Shows all available commands and setup information.

## 📋 How It Works

The bot automatically checks your configured platforms **every 2 minutes**:

- **YouTube**: Fetches recent videos using YouTube Data API and notifies about new uploads
- **Twitch**: Checks if you're live using Twitch API and sends notification when stream starts
- **Kick**: Monitors your channel using Kick's public API and notifies when you go live

### Notification Features

Rich embed notifications include:
- 🎨 Platform-specific color coding (Red for YouTube, Purple for Twitch, Green for Kick)
- 🖼️ High-quality thumbnails and stream previews
- 📊 Live viewer counts for streams
- 🔗 Direct clickable links to content
- ⏰ Timestamps for all notifications
- 📢 @everyone mentions to alert all server members

## 🎨 Example Notifications

### YouTube Video Notification
```
@everyone New video uploaded! 🎬

┌─ New YouTube Video! 🎥
│ Video Title Here
│ 
│ 📅 Published: 2 hours ago
│ 🔗 Watch Now: [Click Here]
│ 
└─ [Full-size thumbnail preview]
```

### Twitch Stream Notification
```
@everyone Stream is LIVE! 🎮

┌─ 🔴 LIVE on Twitch!
│ Stream Title Here
│ 
│ 🎮 Game: Minecraft
│ 👥 Viewers: 1,234
│ 🔗 Watch Now: [Join Stream]
│ 
└─ [Live stream preview]
```

### Kick Stream Notification
```
@everyone Stream is LIVE on Kick! 🚀

┌─ 🟢 LIVE on Kick!
│ Stream Title Here
│ 
│ 📂 Category: Just Chatting
│ 👥 Viewers: 567
│ 🔗 Watch Now: [Join Stream]
│ 
└─ [Live stream preview]
```

## 🔧 Running the Bot

The bot starts automatically on Replit. You can also run it manually with:

```bash
python main.py
```

### Successful Startup Output
```
╔═══════════════════════════════════════╗
║  Bot Connected Successfully!          ║
╚═══════════════════════════════════════╝
Bot User: YourBot#1234
Bot ID: 1234567890
Connected to 1 server(s)
─────────────────────────────────────────
✅ Notification channel: #announcements
✅ YouTube monitoring enabled
✅ Twitch monitoring enabled (@yourusername)
✅ Kick monitoring enabled (@yourusername)
─────────────────────────────────────────
🔄 Started monitoring loop (checks every 2 minutes)
═════════════════════════════════════════
Bot is ready! Use /help to see commands
═════════════════════════════════════════
```

## 🛠️ Configuration Tips

### Minimum Setup (Just Discord)
You only need these 2 secrets to start:
- `DISCORD_TOKEN`
- `DISCORD_CHANNEL_ID`

The bot will run but won't monitor any platforms until you add platform credentials.

### Single Platform Setup
For example, to only monitor Twitch:
- `DISCORD_TOKEN` ✅
- `DISCORD_CHANNEL_ID` ✅
- `TWITCH_CLIENT_ID` ✅
- `TWITCH_CLIENT_SECRET` ✅
- `TWITCH_USERNAME` ✅

### Full Setup (All Platforms)
Add all 8 environment secrets to monitor YouTube, Twitch, and Kick simultaneously.

## ⚙️ Advanced Features

- **Smart Duplicate Detection**: The bot remembers which content it has already notified about
- **Stream State Tracking**: Tracks when streams start and end to avoid duplicate notifications
- **Error Handling**: Graceful error handling with detailed logging
- **Automatic Recovery**: Bot automatically recovers from API errors and continues monitoring
- **Beautiful Console Output**: Color-coded console logs with emojis for easy debugging

## 📝 Notes

- The bot needs to be invited to your Discord server with proper permissions
- YouTube monitoring requires a Google Cloud API key (free tier available with 10,000 units/day)
- Twitch monitoring requires a Twitch developer application
- Kick monitoring works without any API keys
- Check interval is set to 2 minutes to respect API rate limits and avoid excessive requests
- The bot uses Discord's modern slash commands for a better user experience

## 🐛 Troubleshooting

**Bot doesn't send notifications:**
- Make sure the bot is invited to your server
- Verify `DISCORD_CHANNEL_ID` is correct
- Check that the bot has permissions to send messages in the notification channel
- Use `/status` to verify which platforms are configured

**YouTube not working:**
- Verify your `YOUTUBE_API_KEY` is valid
- Check that YouTube Data API v3 is enabled in Google Cloud Console
- Ensure your channel ID is correct

**Twitch not working:**
- Verify your Client ID and Secret are correct
- Make sure your Twitch username is spelled correctly
- Check that 2FA is enabled on your Twitch account

**Slash commands not appearing:**
- Wait a few minutes after inviting the bot (Discord caches commands)
- Try kicking and re-inviting the bot with the correct scopes
- Make sure you invited the bot with `applications.commands` scope

## 📄 License

Stream-Announcer License

Copyright (c) 2025 Surendhar SRS

Permission is hereby granted to any person obtaining a copy of this project and its associated source code (the “Bot”) to use, copy, and modify the Bot for personal or educational purposes only, subject to the following conditions:

Non-Commercial Use Only:
This Bot and its source code may not be sold, offered for sale, or used for any commercial purpose.
You are not permitted to accept payment, donations, or other compensation in exchange for access to, or hosting of, this Bot or its modified versions.

Modification and Redistribution:

You may modify the source code for personal use only (for example, customizing it for your own Discord server).

You may not redistribute, publish, or host modified versions of the Bot publicly.

If you wish to suggest improvements or features, please submit a pull request to the official GitHub repository.

Attribution:
Proper credit must be given to the original author by including this license and a link to the original GitHub repository in any distributed copy or derivative work.

No Warranty:
This project is provided “as is”, without warranty of any kind, express or implied, including but not limited to merchantability or fitness for a particular purpose.
The author shall not be liable for any claim, damages, or other liability arising from the use of this project.

## 🤝 Support

If you need help:
1. Use `/help` command in Discord for bot-specific help
2. Check the console logs for error messages
3. Verify all environment variables are set correctly
4. Make sure all API credentials are valid and active

---

Made with ❤️ for content creators who want to keep their community engaged!
