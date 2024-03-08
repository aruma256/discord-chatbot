from openai import OpenAI
openai_client = OpenAI()

MODEL = "gpt-4-turbo-preview"
MESSAGES = []

def chat(user_message: str) -> str:
    if not MESSAGES:
        MESSAGES.append({"role": "system", "content": "**重要: 回答は端的に**（長文を求められた場合を除く）"})
    MESSAGES.append({"role": "user", "content": user_message})
    response = openai_client.chat.completions.create(
        model=MODEL,
        messages=MESSAGES,
        # temperature=0,
    )
    response_message = response.choices[0].message
    MESSAGES.append(response_message)
    return response_message.content


# ######################################################

import os
import discord

DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


# @client.event
# async def on_ready():
#     print(f'Logged in as {client.user}')


def on_mention(user_content: str) -> str:
    match user_content:
        case "reset":
            MESSAGES.clear()
            return "resetしました"
        case _:
            return chat(user_content)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if client.user in message.mentions:
        user_content = message.content.replace(f'<@{client.user.id}>', '').strip()
        reply_content = on_mention(user_content)
        await message.channel.send(f'{message.author.mention} {reply_content}')


client.run(DISCORD_TOKEN)
