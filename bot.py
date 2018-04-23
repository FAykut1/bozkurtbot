import discord
from discord.ext import commands
from discord.ext.commands import Bot


client = discord.Client()
bot_prefix = "$."
bot = commands.Bot(command_prefix=bot_prefix)

@bot.event
async def on_ready():
    print("Bot Online!")
    print("Name {}".format(bot.user.name))
    print("ID {}".format(bot.user.id))

@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say("Pong")


bot.run("NDM1NTQ5MDc0MTEyOTA1MjM5.Db9hJg.hFq_XXOVl3soad_YT28k0h5vMHI")
