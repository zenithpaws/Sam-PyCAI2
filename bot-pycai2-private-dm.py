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
        return token_doc.to_dict().get("token")
    else:
        return None

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

    print("[PyCAI2] Bot Message: ", r)
    return r

async def get_available_character_ids():
    """Retrieve available character IDs from Firestore."""
    available_ids = []

    try:
        collection_ref = db.collection('character_ids')
        docs = await collection_ref.get()  # Asynchronous operation
        for doc in docs:
            data = doc.to_dict()
            # Check if the "used" field is False
            if not data.get("used", False):
                available_ids.append(data.get("id"))
    except Exception as e:
        print(f"Error fetching available character IDs: {e}")

    return available_ids

async def is_character_id_used(char_id):
    """Check if a character ID is already used."""
    try:
        doc_ref = db.collection("character_ids").where("id", "==", char_id)
        docs = await doc_ref.get()
        for doc in docs:
            data = doc.to_dict()
            return data.get("used", False)
    except Exception as e:
        print(f"Error checking if character ID is used: {e}")
        return True

async def set_character_id_used(char_id, value):
    """Update the 'used' field of a character ID."""
    try:
        doc_ref = db.collection("character_ids").where("id", "==", char_id)
        docs = await doc_ref.get()
        for doc in docs:
            doc.reference.update({"used": value})
    except Exception as e:
        print(f"Error setting character ID used: {e}")

async def start_new_chat(channel_id):
    """Start a new chat using an available character ID and the Discord channel ID."""
    try:
        # Get a list of available character IDs
        available_ids = await get_available_character_ids()

        # Check if there are any available character IDs
        if available_ids:
            for char_id in available_ids:
                # Check if the character ID is already used
                if not await is_character_id_used(char_id):
                    # Mark the selected character ID as used
                    await set_character_id_used(char_id, True)

                    # Start a new chat using the selected character ID and the DM channel ID
                    await start_new_chat(char_id, channel_id)
                    return  # Exit the loop after starting a chat
            print("No available character IDs.")
        else:
            print("No available character IDs.")
    except Exception as e:
        print(f"Error starting new chat: {e}")


# Function to fetch c.ai API key from Firestore
def get_cai_owner_id():
    doc_ref = db.collection("secrets").document("c.ai_ownerid")
    doc = doc_ref.get()
    return doc.to_dict()["id"]

# Function to fetch c.ai API key from Firestore
async def get_cai_char_id():
    """Retrieve an available character ID from Firestore."""
    try:
        collection_ref = db.collection("character_ids")
        docs = await collection_ref.get()  # Asynchronous operation

        # Iterate through the documents to find an available character ID
        for doc in docs:
            data = doc.to_dict()
            if not data.get("used", False):
                return data.get("id")

        # If no available character ID is found
        print("No available character IDs.")
        return None

    except Exception as e:
        print(f"Error fetching character ID: {e}")
        return None

# Function to fetch c.ai API key from Firestore
def get_cai_chat_id():
    doc_ref = db.collection("secrets").document("c.ai_chatid")
    doc = doc_ref.get()
    return doc.to_dict()["id"]

# Initialize PyCAI2 variables
owner_id = get_cai_owner_id()
char = get_cai_char_id()
chat_id = get_cai_chat_id()
client = PyAsyncCAI2(owner_id)
public_channel_id = 1238511476302545017

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
    await bot.change_presence(status=nextcord.Status.dnd)

# Event: When bot receives a message
@bot.event
async def on_message(message):
    if message.author == bot.user or not isinstance(message.channel, nextcord.DMChannel):
        return

    print(get_cai_char_id)
    username = message.author.name
    response = await pycai(f"{username}: {message.content}")

    await message.channel.send(response)

    # Check if the user is sending a message for the first time
    if response.startswith("Hello! I'm your assistant"):
        try:
            # Start a new chat using an available character ID and the DM channel ID
            await start_new_chat(message.channel.id)
        except Exception as e:
            print(f"Error starting new chat: {e}")


# Command to reset chat
@bot.slash_command(description="Command to test the permissioncheck function")
async def permissiontest(ctx):
    if await permission_check(ctx):
        await ctx.send("test success")

# Run the bot
if __name__ == "__main__":
    run_bot()