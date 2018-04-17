import discord
from discord import Game
from discord.ext.commands import Bot
import asyncio

buyukAlfabe = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
kucukAlfabe = "abcçdefgğhıijklmnoöprsştuüvyz"
def lower(text:str):
    newText=str()
    for i in text:
        if i in buyukAlfabe:
            index = buyukAlfabe.index(i)
            newText +=kucukAlfabe[index]
        else:
            newText +=i

    return newText

bot = Bot(command_prefix='#')
##Kötü kelimeler buraya
chat_filter = ["şerefsizler","orospu çocukları","ibne","piç","göt","yarrak","orospu"]
ads_filter = ["com/","gg/","net/","gg/","org/","http"]
bypass_list = []

@bot.event
async def on_ready():
    await bot.change_presence(game=Game(name="Kızlarla"))
    print("Ready when you are xd")
    print("I am running on " + bot.user.name)
    print(bot.user.id)
@bot.event
async def on_message(message):
    if lower(message.content) == "ping":
        await bot.send_message(message.channel, ":ping_pong:")
    if message.content.startswith('#havalı'):
        await bot.send_message(message.channel, 'Kim Havalı? #isim nickname, göster.')

        def check(msg):
            return msg.content.startswith('#isim')

        message = await bot.wait_for_message(author=message.author, check=check)
        name = message.content[len('#isim'):].strip()
        await bot.send_message(message.channel, '{} gerçekten havalı.'.format(name))
    for flit in ads_filter:
        if flit in lower(message.content):
            try:
                await bot.delete_message(message)
                await bot.send_message(message.channel, ":warning:Lütfen reklam yapmayınız kullanmayınız.")
            except discord.errors.NotFound:
                return
    contents2 = message.content.split(" ")
    for word in contents2:
        if lower(word) in chat_filter:
            if not message.author.id in bypass_list:
                try:
                    await bot.delete_message(message)
                    await bot.send_message(message.channel,":warning:Lütfen bu tür kelimeler kullanmayınız.")
                except discord.errors.NotFound:
                    return
    await bot.process_commands(message)


@bot.command(pass_context=True)
async def bilgilerim(ctx,user:discord.Member=None):
    if user is None:
        user = ctx.message.author
        await bot.say('İsim : {0} Katılma Tarihi: {0.joined_at}'.format(user))

@bot.command(pass_context=True)
async def bilgi(ctx,user:discord.Member):
    embed = discord.Embed(title=user.name,description="Bunları buldum reis.")
    embed.add_field(name="İsim",value=user.name,inline=True)
    embed.add_field(name="ID",value=user.id,inline=True)
    embed.add_field(name="Durum", value=user.status, inline=True)
    embed.add_field(name="Rol", value=user.top_role)
    embed.add_field(name="Katılma Tarihi",value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)


bot.run("NDM1NTQ5MDc0MTEyOTA1MjM5.DbakRQ.OsJ2CZYXBWuoYDTGmoNLiGOQ2NU")



