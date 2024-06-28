import nextcord
import firebase_admin
from nextcord.ext import commands
from PyCAI2 import PyAsyncCAI2
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# PyCAI2 configuration
owner_id = '8afbe083178984f92c6b8eaee69c052afc64418b' # sam's owner id
char = "5d2GJlzpVwb9dCPmV5Ze3Tgl0M2YetbyQArCS89KDuQ"
chat_id = "d3583395-c4f2-4f9e-9e18-fea560e755ca"
client = PyAsyncCAI2(owner_id)

# Discord bot configuration
bot = commands.Bot(command_prefix="f!", intents=nextcord.Intents.all())

# Function to get the bot token from Firestore
def get_bot_token():
    # Assuming the personal access token is stored in a document named 'bot_token'
    token_ref = db.collection("secrets").document("bot_token")
    token_doc = token_ref.get()
    if token_doc.exists:
        return token_doc.to_dict().get("token")
    else:
        return None

token = get_bot_token()

# Ticket system configuration
ticket_message = 1238946770025971854
ticket_category = 1238946598533333104 # ticket-category 
ticket_channel = 1238946703877476452 # ticket-channel
reactemoji = "🌸"

# PyCAI enabled flag
pycai_enabled = True

# Allowed channel ID
allowed_channel_id = 1238946262514925588 # allowed-channel
authorized_user_id = 487638433179762688 # zenithpaws

# Add event for PyCAI2
@bot.event
async def on_message(message):
    global pycai_enabled

    if message.channel.id == allowed_channel_id:
        if message.author == bot.user:
            return

        # Check if the message contains commands to disable or enable the bot
        if 'f!disable' in message.content or 'f!enable' in message.content:
            await bot.process_commands(message)
        # Check if the message contains the command to create a new chat
        elif 'f!rtv' in message.content:
            await bot.process_commands(message)
        # Check if the message contains the command to close the channel
        elif 'f!close' in message.content:
            await bot.process_commands(message)
        # Process normal messages if the bot is enabled
        elif pycai_enabled:
            await process_message(message)
        # Ignore messages if the bot is disabled
        else:
            return

# Function to handle messages
async def process_message(message):
    username = message.author.name
    response = await pycai(f"{username}: {message.content}")

    if any(bad_word in response for bad_word in ["@everyone", "@here", "<@&1182758208922714133>"]):
        await message.channel.send("I'm sorry, I'm not allowed to mention everyone, here")
        return
    
    await message.channel.send(response)

# Function to interact with PyCAI2
async def pycai(message):
    print("[PyCAI2] STARTING TO PROCESS MESSAGE")
    print("MESSAGE:", message)
    
    async with client.connect(owner_id) as chat2:
        r = await chat2.send_message(char, message, chat_id)

    if any(bad_word in r for bad_word in ["@everyone", "@here", "<@&1182758208922714133>"]):
        return "I'm sorry, I'm not allowed to mention everyone, here"

    print("[PyCAI2] Bot Message: ", r)
    return r

# Add event for ticket system
@bot.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    message = await bot.get_channel(ticket_channel).fetch_message(ticket_message)
    if reactemoji not in [reaction.emoji for reaction in message.reactions]:
        await message.add_reaction(reactemoji)

@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    user = guild.get_member(payload.user_id)

    if payload.message_id == ticket_message and str(payload.emoji) == reactemoji and not user.bot:
        message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        if reactemoji not in [reaction.emoji for reaction in message.reactions]:
            await message.add_reaction
        else:
            await message.remove_reaction(payload.emoji, user)
        category = bot.get_channel(ticket_category)
        channel_name = f"{user.name}"

        for channel in category.text_channels:
            if channel.name.lower() == channel_name.lower():
                print(f"Conversation Already Open - {user.name}#{user.discriminator} ({user.id})")
                return
        overwrites = {
            guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            user: nextcord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True)
        }

        channel = await category.create_text_channel(name=channel_name, overwrites=overwrites)
        embed = nextcord.Embed(
            title="Conversation Created !",
            description="Do f!activate to talk with the femboy assistant, f!close to delete the channel",
            color=0x2b2d31
        )
        embed.set_author(name=user.name+"#"+user.discriminator, icon_url=str(user.avatar.url))
        message = await channel.send(user.mention,embed=embed)
        print(f"Conversation created - {user.name}#{user.discriminator} ({user.id})")

@bot.command()
async def close(ctx):
    if ctx.channel.category_id == ticket_category:  # Ensure command is used in the appropriate category
        channel_name = ctx.channel.name
        user_name = ctx.author.name
        if channel_name.lower() == user_name.lower():
            await ctx.channel.delete()  # Delete the channel
        else:
            await ctx.send("You can only close your own ticket channel.")
    else:
        await ctx.send("This command can only be used in the ticket category.")

# Command to disable PyCAI
@bot.command()
async def disable(ctx):
    global pycai_enabled
    if ctx.author.id == authorized_user_id:
        if not pycai_enabled:
            await ctx.send("PyCAI is already disabled.")
        else:
            pycai_enabled = False
            await ctx.send("PyCAI has been disabled.")
    else:
        return

# Command to enable PyCAI
@bot.command()
async def enable(ctx):
    global pycai_enabled
    if ctx.author.id == authorized_user_id:
        pycai_enabled = True
        await ctx.send("PyCAI has been enabled.")
    else:
        return

# Run the bot
bot.run(token)
