import discord
from discord import app_commands
from discord.ext import tasks
import asyncio
import aiohttp
import os
from dotenv import load_dotenv
from datetime import datetime
import json
import traceback

from monitors.youtube_monitor import YouTubeMonitor
from monitors.twitch_monitor import TwitchMonitor
from monitors.kick_monitor import KickMonitor

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

class ContentBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.youtube_monitor = None
        self.twitch_monitor = None
        self.kick_monitor = None
        self.notification_channel_id = None
        self.last_notifications = {
            'youtube': [],
            'twitch': None,
            'kick': None
        }
    
    async def setup_hook(self):
        await self.tree.sync()
        print("Slash commands synced!")

bot = ContentBot()

@bot.event
async def on_ready():
    print(f'╔═══════════════════════════════════════╗')
    print(f'║  Bot Connected Successfully!          ║')
    print(f'╚═══════════════════════════════════════╝')
    print(f'Bot User: {bot.user.name}#{bot.user.discriminator}')
    print(f'Bot ID: {bot.user.id}')
    print(f'Connected to {len(bot.guilds)} server(s)')
    print(f'─────────────────────────────────────────')
    
    bot.notification_channel_id = int(os.getenv('DISCORD_CHANNEL_ID', 0))
    
    if bot.notification_channel_id:
        channel = bot.get_channel(bot.notification_channel_id)
        if channel:
            if hasattr(channel, 'name'):
                print(f'✅ Notification channel: #{channel.name}')
            else:
                print(f'✅ Notification channel ID: {bot.notification_channel_id}')
        else:
            print(f'⚠️  Warning: Could not find channel with ID {bot.notification_channel_id}')
            print(f'   Make sure the bot is invited to your server!')
    else:
        print('⚠️  Warning: DISCORD_CHANNEL_ID not set')
    
    youtube_channel_id = os.getenv('YOUTUBE_CHANNEL_ID')
    if youtube_channel_id:
        bot.youtube_monitor = YouTubeMonitor(youtube_channel_id)
        print(f'✅ YouTube monitoring enabled')
    else:
        print(f'❌ YouTube monitoring disabled (no channel ID)')
    
    twitch_client_id = os.getenv('TWITCH_CLIENT_ID')
    twitch_client_secret = os.getenv('TWITCH_CLIENT_SECRET')
    twitch_username = os.getenv('TWITCH_USERNAME')
    if twitch_client_id and twitch_client_secret and twitch_username:
        bot.twitch_monitor = TwitchMonitor(twitch_client_id, twitch_client_secret, twitch_username)
        try:
            await bot.twitch_monitor.initialize()
            print(f'✅ Twitch monitoring enabled (@{twitch_username})')
        except Exception as e:
            print(f'❌ Twitch initialization failed: {e}')
            bot.twitch_monitor = None
    else:
        print(f'❌ Twitch monitoring disabled (credentials missing)')
    
    kick_username = os.getenv('KICK_USERNAME')
    if kick_username:
        bot.kick_monitor = KickMonitor(kick_username)
        print(f'✅ Kick monitoring enabled (@{kick_username})')
    else:
        print(f'❌ Kick monitoring disabled (no username)')
    
    print(f'─────────────────────────────────────────')
    if not check_monitors.is_running():
        check_monitors.start()
        print('🔄 Started monitoring loop (checks every 2 minutes)')
    
    print(f'═════════════════════════════════════════')
    print(f'Bot is ready! Use /help to see commands')
    print(f'═════════════════════════════════════════')

@tasks.loop(minutes=2)
async def check_monitors():
    if not bot.notification_channel_id:
        return
    
    channel = bot.get_channel(bot.notification_channel_id)
    if not channel or not hasattr(channel, 'send'):
        return
    
    if bot.youtube_monitor:
        try:
            new_videos = await bot.youtube_monitor.check_new_videos(bot.last_notifications['youtube'])
            for video in new_videos:
                embed = discord.Embed(
                    title="New YouTube Video! 🎥",
                    description=f"**{video['title']}**",
                    color=0xFF0000,
                    url=video['url'],
                    timestamp=datetime.now()
                )
                embed.set_author(name="YouTube Upload", icon_url="https://www.youtube.com/s/desktop/d743f786/img/favicon_144x144.png")
                embed.set_image(url=video['thumbnail'])
                embed.add_field(name="📅 Published", value=video['published'], inline=True)
                embed.add_field(name="🔗 Watch Now", value=f"[Click Here]({video['url']})", inline=True)
                embed.set_footer(text="YouTube Notification System", icon_url=bot.user.display_avatar.url)
                
                await channel.send(content="@everyone New video uploaded! 🎬", embed=embed)
                bot.last_notifications['youtube'].append(video['video_id'])
                print(f"📺 Notified: New YouTube video - {video['title']}")
        except Exception as e:
            print(f"❌ Error checking YouTube: {e}")
            traceback.print_exc()
    
    if bot.twitch_monitor:
        try:
            stream_info = await bot.twitch_monitor.check_live()
            if stream_info and not bot.last_notifications['twitch']:
                embed = discord.Embed(
                    title="🔴 LIVE on Twitch!",
                    description=f"**{stream_info['title']}**",
                    color=0x9146FF,
                    url=stream_info['url'],
                    timestamp=datetime.now()
                )
                embed.set_author(name="Twitch Live", icon_url="https://static.twitchcdn.net/assets/favicon-32-e29e246c157142c94346.png")
                embed.set_image(url=stream_info['thumbnail'])
                embed.add_field(name="🎮 Game", value=stream_info['game'], inline=True)
                embed.add_field(name="👥 Viewers", value=f"{stream_info['viewers']:,}", inline=True)
                embed.add_field(name="🔗 Watch Now", value=f"[Join Stream]({stream_info['url']})", inline=False)
                embed.set_footer(text="Twitch Notification System", icon_url=bot.user.display_avatar.url)
                
                await channel.send(content="@everyone Stream is LIVE! 🎮", embed=embed)
                bot.last_notifications['twitch'] = stream_info['stream_id']
                print(f"🎮 Notified: Twitch live - {stream_info['title']}")
            elif not stream_info and bot.last_notifications['twitch']:
                bot.last_notifications['twitch'] = None
                print("📴 Twitch stream ended")
        except Exception as e:
            print(f"❌ Error checking Twitch: {e}")
            traceback.print_exc()
    
    if bot.kick_monitor:
        try:
            stream_info = await bot.kick_monitor.check_live()
            if stream_info and not bot.last_notifications['kick']:
                embed = discord.Embed(
                    title="🟢 LIVE on Kick!",
                    description=f"**{stream_info['title']}**",
                    color=0x53FC18,
                    url=stream_info['url'],
                    timestamp=datetime.now()
                )
                embed.set_author(name="Kick Live", icon_url="https://kick.com/favicon.ico")
                if stream_info['thumbnail']:
                    embed.set_image(url=stream_info['thumbnail'])
                embed.add_field(name="📂 Category", value=stream_info['category'], inline=True)
                embed.add_field(name="👥 Viewers", value=f"{stream_info['viewers']:,}", inline=True)
                embed.add_field(name="🔗 Watch Now", value=f"[Join Stream]({stream_info['url']})", inline=False)
                embed.set_footer(text="Kick Notification System", icon_url=bot.user.display_avatar.url)
                
                await channel.send(content="@everyone Stream is LIVE on Kick! 🚀", embed=embed)
                bot.last_notifications['kick'] = True
                print(f"🚀 Notified: Kick live - {stream_info['title']}")
            elif not stream_info and bot.last_notifications['kick']:
                bot.last_notifications['kick'] = None
                print("📴 Kick stream ended")
        except Exception as e:
            print(f"❌ Error checking Kick: {e}")
            traceback.print_exc()

@bot.tree.command(name="status", description="Check bot monitoring status and configuration")
async def status(interaction: discord.Interaction):
    """Check the bot status and monitoring configuration"""
    
    embed = discord.Embed(
        title="📊 Bot Monitoring Status",
        description="Current platform monitoring configuration",
        color=0x5865F2,
        timestamp=datetime.now()
    )
    
    youtube_status = "✅ **Active**" if bot.youtube_monitor else "❌ **Disabled**"
    twitch_status = "✅ **Active**" if bot.twitch_monitor else "❌ **Disabled**"
    kick_status = "✅ **Active**" if bot.kick_monitor else "❌ **Disabled**"
    
    youtube_detail = f'Channel ID: `{os.getenv("YOUTUBE_CHANNEL_ID", "")[:20]}...`' if bot.youtube_monitor else 'Not configured'
    twitch_detail = f'Username: `@{os.getenv("TWITCH_USERNAME", "")}`' if bot.twitch_monitor else 'Not configured'
    kick_detail = f'Username: `@{os.getenv("KICK_USERNAME", "")}`' if bot.kick_monitor else 'Not configured'
    
    embed.add_field(
        name="🎥 YouTube",
        value=f"{youtube_status}\n{youtube_detail}",
        inline=False
    )
    
    embed.add_field(
        name="🎮 Twitch",
        value=f"{twitch_status}\n{twitch_detail}",
        inline=False
    )
    
    embed.add_field(
        name="🚀 Kick",
        value=f"{kick_status}\n{kick_detail}",
        inline=False
    )
    
    embed.add_field(
        name="⏱️ Check Interval",
        value="Every **2 minutes**",
        inline=False
    )
    
    embed.add_field(
        name="📢 Notification Channel",
        value=f"<#{bot.notification_channel_id}>" if bot.notification_channel_id else "Not set",
        inline=False
    )
    
    active_platforms = sum([bool(bot.youtube_monitor), bool(bot.twitch_monitor), bool(bot.kick_monitor)])
    embed.set_footer(text=f"Monitoring {active_platforms}/3 platforms • Bot uptime tracking enabled", icon_url=bot.user.display_avatar.url)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="test", description="Send a test notification to verify the bot is working")
@app_commands.checks.has_permissions(administrator=True)
async def test(interaction: discord.Interaction):
    """Test the notification system"""
    
    embed = discord.Embed(
        title="🔔 Test Notification",
        description="This is a test notification from your content monitoring bot!",
        color=0xFFD700,
        timestamp=datetime.now()
    )
    
    embed.add_field(name="✅ Bot Status", value="Online and operational", inline=True)
    embed.add_field(name="📡 Connection", value="Stable", inline=True)
    embed.add_field(name="🔧 Commands", value="All systems go!", inline=True)
    embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
    
    await interaction.response.send_message(embed=embed)
    print(f"🧪 Test notification sent by {interaction.user.name}")

@bot.tree.command(name="check", description="Manually check for new content on all platforms right now")
@app_commands.checks.has_permissions(administrator=True)
async def check(interaction: discord.Interaction):
    """Manually trigger a check for new content"""
    
    await interaction.response.defer(thinking=True)
    
    results = []
    
    if bot.youtube_monitor:
        try:
            new_videos = await bot.youtube_monitor.check_new_videos(bot.last_notifications['youtube'])
            results.append(f"🎥 YouTube: {len(new_videos)} new video(s)")
        except Exception as e:
            results.append(f"🎥 YouTube: Error - {str(e)[:50]}")
    else:
        results.append("🎥 YouTube: Not configured")
    
    if bot.twitch_monitor:
        try:
            stream_info = await bot.twitch_monitor.check_live()
            if stream_info:
                results.append(f"🎮 Twitch: LIVE now!")
            else:
                results.append(f"🎮 Twitch: Not live")
        except Exception as e:
            results.append(f"🎮 Twitch: Error - {str(e)[:50]}")
    else:
        results.append("🎮 Twitch: Not configured")
    
    if bot.kick_monitor:
        try:
            stream_info = await bot.kick_monitor.check_live()
            if stream_info:
                results.append(f"🚀 Kick: LIVE now!")
            else:
                results.append(f"🚀 Kick: Not live")
        except Exception as e:
            results.append(f"🚀 Kick: Error - {str(e)[:50]}")
    else:
        results.append("🚀 Kick: Not configured")
    
    embed = discord.Embed(
        title="🔍 Manual Check Results",
        description="\n".join(results),
        color=0x00FF00,
        timestamp=datetime.now()
    )
    embed.set_footer(text=f"Checked by {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
    
    await interaction.followup.send(embed=embed)
    print(f"🔍 Manual check triggered by {interaction.user.name}")

@bot.tree.command(name="help", description="Show all available commands and bot information")
async def help_command(interaction: discord.Interaction):
    """Show help information"""
    
    embed = discord.Embed(
        title="🤖 Content Monitor Bot - Help",
        description="I monitor YouTube, Twitch, and Kick for new content and notify you when you go live or upload videos!",
        color=0x5865F2,
        timestamp=datetime.now()
    )
    
    embed.add_field(
        name="📋 Available Commands",
        value=(
            "`/status` - View monitoring status for all platforms\n"
            "`/test` - Send a test notification (Admin only)\n"
            "`/check` - Manually check for new content (Admin only)\n"
            "`/help` - Show this help message"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🔔 How It Works",
        value=(
            "The bot automatically checks every **2 minutes** for:\n"
            "• New YouTube videos & Live \n"
            "• Twitch live streams\n"
            "• Kick live streams\n\n"
            "When new content is detected, everyone gets notified!"
        ),
        inline=False
    )
    
    embed.add_field(
        name="⚙️ Setup",
        value=(
            "Configure platforms via environment secrets:\n"
            "`DISCORD_TOKEN`, `DISCORD_CHANNEL_ID` (required)\n"
            "`YOUTUBE_API_KEY`, `YOUTUBE_CHANNEL_ID` (optional)\n"
            "`TWITCH_CLIENT_ID`, `TWITCH_CLIENT_SECRET`, `TWITCH_USERNAME` (optional)\n"
            "`KICK_USERNAME` (optional)"
        ),
        inline=False
    )
    
    embed.set_footer(text="Made with ❤️ for content creators", icon_url=bot.user.display_avatar.url)
    
    await interaction.response.send_message(embed=embed)

@test.error
async def test_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("❌ You need administrator permissions to use this command!", ephemeral=True)

@check.error
async def check_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("❌ You need administrator permissions to use this command!", ephemeral=True)

def main():
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ Error: DISCORD_TOKEN not found in environment variables")
        print("Please set up your Discord bot token in the Secrets tab")
        return
    
    try:
        bot.run(token)
    except discord.LoginFailure:
        print("❌ Error: Invalid Discord token")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
