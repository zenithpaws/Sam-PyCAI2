import nextcord
import firebase_admin
from nextcord.ext import commands
from PyCAI2 import PyAsyncCAI2
from firebase_admin import credentials, firestore

# Create a bot instance
prefix = "/"
intents = nextcord.Intents.all()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix=prefix, intents=intents)

# Initialize Firebase
cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Function to get the bot token from Firestore
def get_bot_token():
    # Assuming the personal access token is stored in a document named 'bot_token'
    token_ref = db.collection("secrets").document("bot_token")
    token_doc = token_ref.get()
    if token_doc.exists:
        return token_doc.to_dict().get("test_bot_token")
    else:
        return None

# Function to fetch c.ai API key from Firestore
def get_cai_owner_id():
    doc_ref = db.collection("secrets").document("c.ai_ownerid")
    doc = doc_ref.get()
    return doc.to_dict()["ryzenid"]

# Function to fetch c.ai Character ID from Firestore
def get_cai_char_id(id):
    doc_ref = db.collection("character_ids").document(f"id{id}")
    doc = doc_ref.get()
    return doc.to_dict()["char_id"]

# Function to fetch c.ai Chat ID from Firestore
def get_cai_chat_id(id):
    doc_ref = db.collection("character_ids").document(f"id{id}")
    doc = doc_ref.get()
    return doc.to_dict()["chat_id"]

# Function to fetch c.ai Creator ID from Firestore
def get_cai_creator_id(id):
    doc_ref = db.collection("character_ids").document(f"id{id}")
    doc = doc_ref.get()
    return doc.to_dict()["creator_id"]

# Function to check what roles are allowed to run commands
async def get_allowed_roles():
    """Retrieve allowed roles from Firestore."""
    allowed_roles = {}

    try:
        doc_ref = db.collection('role_names').document('allowed_commands')
        doc = doc_ref.get()  # Remove 'await' from here
        if doc.exists:
            data = doc.to_dict()
            allowed_roles = {role_name: allow for role_name, allow in data.items()}  # Get the dictionary of allowed roles
    except Exception as e:
        print(f"Error fetching allowed roles: {e}")

    return allowed_roles

# Function to check the user for permissions to run the command
async def permission_check(ctx):
    """Check permissions for executing commands."""
    allowed_roles = await get_allowed_roles()  # Await the asynchronous operation

    # Get the names of the roles the user has
    user_role_names = [role.name for role in ctx.user.roles]

    # Check if any of the user's roles are allowed
    for role_name in user_role_names:
        if role_name in allowed_roles and allowed_roles[role_name]:
            return True

    # If none of the user's roles match the allowed roles or if the roles are not allowed
    await ctx.send("You do not have permission to use this command.")
    return False

async def get_channel_id(command_name, channel_name):
    """Get the channel ID from Firestore."""
    channel_ref = db.collection("channel_ids").document(command_name)
    try:
        snapshot = channel_ref.get()
        if snapshot.exists:
            return snapshot.to_dict().get(channel_name)
        else:
            return None
    except Exception as e:
        print(f"Error getting channel ID: {e}")
        return None

async def set_channel_id(command_name, channel_name, channel_id):
    """Set the channel ID in Firestore."""
    channel_ref = db.collection("channel_ids").document(command_name)
    try:
        channel_ref.set({channel_name: channel_id})
    except Exception as e:
        print(f"Error setting channel ID: {e}")

# Function to interact with PyCAI2
async def pycai(message):

    print("[PyCAI2] STARTING TO PROCESS MESSAGE")
    print("MESSAGE:", message)
    
    async with client.connect(owner_id) as chat2:
        r = await chat2.send_message(char, message, chat_id)

    if any(bad_word in r for bad_word in ["@"]):
        return "I'm sorry, I'm not allowed to mention roles"

    print("[PyCAI2] Bot Message: ", r)
    return r

# Initialize PyCAI2 variables
current_id = 0
owner_id = get_cai_owner_id()
char = get_cai_char_id(current_id)
chat_id = get_cai_chat_id(current_id)
client = PyAsyncCAI2(owner_id)
public_channel_id = 1238946262514925588

# Function to start the bot
def run_bot():
    # Get the personal access token from Firestore
    token = get_bot_token()
    if token:
        # Initialize the bot with the token
        bot.run(token)
    else:
        print("Failed to retrieve Firebase personal access token.")

# Event: When the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} is now online')
    await bot.change_presence(status=nextcord.Status.online)

# Event: When bot gets message
@bot.event
async def on_message(message):
    if message.author == bot.user or message.channel.id != public_channel_id:
        return

    username = message.author.name
    response = await pycai(f"{username}: {message.content}")

    if message.channel.id == public_channel_id:
        if any(bad_word in response for bad_word in ["@"]):
            await message.channel.send("I'm sorry, I'm not allowed to mention roles")
            return

        await message.channel.send(response)
        return

# Command to reset chat
@bot.slash_command(description="Command to reset chat")
async def rc(ctx):
    if await permission_check(ctx):
        async with client.connect(owner_id) as chat2:
            await chat2.new_chat({get_cai_char_id(current_id)}, {get_cai_chat_id(current_id)}, {get_cai_creator_id(current_id)}, False)

# Command to test the permissioncheck function
@bot.slash_command(description="Command to test the permissioncheck function")
async def permissiontest(ctx):
    if await permission_check(ctx):
        await ctx.send("test success")

# Command to kill bot script
@bot.slash_command(description="Command to kill bot script")
async def kill(ctx):
    if await permission_check(ctx):
        quit()

# Run the bot
if __name__ == "__main__":
    run_bot()
