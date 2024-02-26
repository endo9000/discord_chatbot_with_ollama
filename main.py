# main.py
from typing import Final
from discord import Intents, Client, Message, DMChannel
from dotenv import load_dotenv
from src.responses import get_response
import os

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
MODEL: Final[str] = os.getenv('MODEL_NAME')

intents: Intents = Intents.default()
intents.message_content = True #NOQA
client: Client = Client(intents=intents)

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("(Message was empty because intents were not enabled probably)")
        return
    if is_private := user_message[0] == '?':
        user_message = user_message[1:]
    try:
        response: str = get_response(MODEL, user_message)
        
        await message.author.send(str(response)) if is_private else await message.channel.send(str(response))
    except Exception as e:
        print(e)
        
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')
    
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    mentioned = client.user.mentioned_in(message)
    is_private = isinstance(message.channel, DMChannel)

    if not mentioned and not is_private:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    
    await message.add_reaction('🤔')
    async with message.channel.typing():
        await send_message(message, user_message)    
    await message.remove_reaction('🤔', member=client.user)

def main() -> None:
    client.run(token=TOKEN)
    
if __name__ == '__main__':
    main()