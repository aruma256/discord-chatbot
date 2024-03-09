from openai import OpenAI
openai_client = OpenAI()

MODEL = "gpt-4-turbo-preview"

def chat(message_history: list[dict]) -> str:
    message_history.insert(0, {"role": "system", "content": "**重要: 回答は端的に**（長文を求められた場合を除く）"})
    response = openai_client.chat.completions.create(
        model=MODEL,
        messages=message_history,
        # temperature=0,
    )
    response_message = response.choices[0].message
    return response_message.content


# ######################################################

import os
import discord

DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_message(original_message):
    if original_message.author == client.user:
        return
    #
    message = original_message
    message_history = []
    is_last_message_reply_to_bot = False
    while True:
        content = message.content
        is_last_message_reply_to_bot = client.user in message.mentions
        content = content.replace(f'<@{client.user.id}>', '').strip()
        if message.author == client.user:
            message_history.append({"role": "assistant", "content": content})
        else:
            message_history.append({"role": "user", "content": content})
        if message.reference is None:
            break
        message = await message.channel.fetch_message(message.reference.message_id)
    if not is_last_message_reply_to_bot:
        return
    if len(message_history) >= 10:
        await original_message.reply("（会話長すぎるので打ち切ります...）", mention_author=True)
        return
    message_history.reverse()
    response = chat(message_history)
    await original_message.reply(response, mention_author=True)


client.run(DISCORD_TOKEN)
