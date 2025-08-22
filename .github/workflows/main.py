import discord
from discord.ext import commands
from discord import app_commands
import os
from keep_alive import keep_alive
import random

# ====== Setup ======
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)




GUILD_ID = 1406918069963460728  # replace with your server ID

@bot.event
async def on_ready():
    try:
        guild = discord.Object(id=GUILD_ID)
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
        print(f"✅ Synced {len(synced)} commands to guild {GUILD_ID}")
    except Exception as e:
        print(f"❌ Sync failed: {e}")



# ==============================
# 🎉 Fun Commands
# ==============================
fun_group = app_commands.Group(name="fun", description="Fun commands")

@fun_group.command(name="joke", description="Tell a random joke")
async def joke(interaction: discord.Interaction):
    jokes = [
        "😂 Why don’t skeletons fight? They don’t have the guts.",
        "🤣 Parallel lines have so much in common. It’s a shame they’ll never meet.",
        "😆 Why don’t eggs tell jokes? They might crack up."
    ]
    await interaction.response.send_message(random.choice(jokes))

@fun_group.command(name="coinflip", description="Flip a coin")
async def coinflip(interaction: discord.Interaction):
    await interaction.response.send_message(f"🪙 {random.choice(['Heads', 'Tails'])}")

@fun_group.command(name="roll", description="Roll a dice")
async def roll(interaction: discord.Interaction):
    await interaction.response.send_message(f"🎲 You rolled a {random.randint(1, 6)}")

@fun_group.command(name="rps", description="Play Rock-Paper-Scissors")
async def rps(interaction: discord.Interaction, choice: str):
    bot_choice = random.choice(["rock", "paper", "scissors"])
    await interaction.response.send_message(f"You chose {choice}, I chose {bot_choice}!")

# ==============================
# 🛠️ Tools
# ==============================
tools_group = app_commands.Group(name="tools", description="Useful tools")

@tools_group.command(name="ping", description="Check latency")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"🏓 Pong! {round(bot.latency*1000)}ms")

@tools_group.command(name="avatar", description="Get user avatar")
async def avatar(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    await interaction.response.send_message(member.avatar.url)

@tools_group.command(name="userinfo", description="Get user info")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    embed = discord.Embed(title=f"User Info - {member}", color=discord.Color.blue())
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Joined", value=member.joined_at, inline=True)
    embed.set_thumbnail(url=member.avatar.url)
    await interaction.response.send_message(embed=embed)

# ==============================
# 🎮 Games
# ==============================
games_group = app_commands.Group(name="games", description="Play mini games")

@games_group.command(name="guessnumber", description="Guess a number between 1-10")
async def guessnumber(interaction: discord.Interaction, guess: int):
    number = random.randint(1, 10)
    if guess == number:
        await interaction.response.send_message("🎉 Correct! You guessed the number!")
    else:
        await interaction.response.send_message(f"❌ Wrong! I was thinking of {number}")

# ==============================
# 🔧 Admin
# ==============================
admin_group = app_commands.Group(name="admin", description="Admin commands")

@admin_group.command(name="kick", description="Kick a member")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason"):
    if interaction.user.guild_permissions.kick_members:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"✅ {member} was kicked. Reason: {reason}")
    else:
        await interaction.response.send_message("❌ You don’t have permission.")

@admin_group.command(name="ban", description="Ban a member")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason"):
    if interaction.user.guild_permissions.ban_members:
        await member.ban(reason=reason)
        await interaction.response.send_message(f"✅ {member} was banned. Reason: {reason}")
    else:
        await interaction.response.send_message("❌ You don’t have permission.")

import discord
from discord import app_commands
from discord.ext import commands

# Replace this with YOUR Discord User ID (right-click your profile > Copy ID, must have Dev Mode on)
OWNER_ID = 1234168092553248950  

# --- Change Bot Status Commands (Owner Only) ---

@bot.tree.command(name="set_status", description="Change the bot's status (online, idle, dnd, invisible)")
@app_commands.describe(status="Choose one: online, idle, dnd, invisible")
async def set_status(interaction: discord.Interaction, status: str):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ You are not allowed to use this command.", ephemeral=True)
        return

    status_map = {
        "online": discord.Status.online,
        "idle": discord.Status.idle,
        "dnd": discord.Status.do_not_disturb,
        "invisible": discord.Status.invisible,
    }

    if status.lower() not in status_map:
        await interaction.response.send_message("❌ Invalid status. Choose: online, idle, dnd, invisible")
        return

    await bot.change_presence(status=status_map[status.lower()])
    await interaction.response.send_message(f"✅ Status changed to **{status}**")

@bot.tree.command(name="set_activity", description="Change the bot's activity (playing, listening, watching)")
@app_commands.describe(activity_type="playing, listening, watching", activity="What should I display?")
async def set_activity(interaction: discord.Interaction, activity_type: str, activity: str):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ You are not allowed to use this command.", ephemeral=True)
        return

    activity_map = {
        "playing": discord.Game(name=activity),
        "listening": discord.Activity(type=discord.ActivityType.listening, name=activity),
        "watching": discord.Activity(type=discord.ActivityType.watching, name=activity),
    }

    if activity_type.lower() not in activity_map:
        await interaction.response.send_message("❌ Invalid type. Choose: playing, listening, watching")
        return

    await bot.change_presence(activity=activity_map[activity_type.lower()])
    await interaction.response.send_message(f"✅ Now {activity_type} **{activity}**")

# ==============================
# Add Groups
# ==============================
bot.tree.add_command(fun_group, guild=discord.Object(id=GUILD_ID))
bot.tree.add_command(tools_group, guild=discord.Object(id=GUILD_ID))
bot.tree.add_command(games_group, guild=discord.Object(id=GUILD_ID))
bot.tree.add_command(admin_group, guild=discord.Object(id=GUILD_ID))

# ==============================
# Run Bot
# ==============================
from keep_alive import keep_alive
import os

keep_alive()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("❌ Bot token not found! Did you set it in Replit Secrets?")

bot.run(TOKEN.strip())

