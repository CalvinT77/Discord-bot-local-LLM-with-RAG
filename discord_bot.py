import discord
from dotenv import load_dotenv
from discord.ext import commands
import os
import llm # Imports your file above
import asyncio # Required for the executor

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

@bot.event
async def on_message(message):
    # Prevent bot from replying to itself
    if message.author == bot.user:
        return
    
    # print(f'Message from {message.author}: {message.content}') # Optional logging
    await bot.process_commands(message)

@bot.command()
async def speak(ctx, *, arg):
    # message explaining bot is thinking
    status_msg = await ctx.send(f"*Thinking about: {arg[:20]}...*")

   # loop the llm in a seperate thread
    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(None, llm.llm_speak, str(ctx.author.name), arg)
    await loop.run_in_executor(None, llm.remember, str(ctx.author.name), arg)

    # make sure the response is under 2000 and if not split response up into chunks
    if len(response) <= 2000:
        await status_msg.edit(content=response)
    else:
        chunk_size = 1900 
        chunks = [response[i:i + chunk_size] for i in range(0, len(response), chunk_size)]

        # Edit the "Thinking..." message with the first chunk
        await status_msg.edit(content=chunks[0])

        # Send the rest as new messages
        for chunk in chunks[1:]:
            await ctx.send(chunk)

DISCORD_SECRET = os.getenv("DISCORD_SECRET")
bot.run(DISCORD_SECRET)