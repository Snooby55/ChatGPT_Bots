import openai
import discord
from discord.ext import commands

openai.api_key = "api_key"
TOKEN = 'token'

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.command()
async def ask(ctx, *, question):
    await ctx.send("Wait, I'm forming an answer.")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Question: {question}\nAnswer:",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    answer = response['choices'][0]['text'].strip()
    if len(answer) <= 2000:
        await ctx.send(answer)
    else:
        chunks = [answer[i:i+2000] for i in range(0, len(answer), 2000)]
        for chunk in chunks:
            await ctx.send(chunk)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)

client.run(TOKEN)
