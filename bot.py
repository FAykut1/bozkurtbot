import discord,json,os.path,requests,io,random
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import chatfilter,level_system


mesaj_gonderme = 0
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
chat_filter = chatfilter.chat_filters
ads_filter = ["com/","gg/","net/","gg/","org/","http"]
bypass_list = []

@bot.event
async def on_ready():
    await bot.change_presence(game=Game(name="Kızlarla"))
    print("Ready when you are xd")
    print("I am running on " + bot.user.name)
    print(bot.user.id)
    for server in bot.servers:
        servername = server.name
        print(servername)

@bot.event
async def on_message(message):
    global mesaj_gonderme
    mesaj_gonderme += 1
    print(mesaj_gonderme)
    if lower(message.content) == "ping":
        await bot.send_message(message.channel, ":ping_pong:")
    if message.content.startswith('#havalı'):
        await bot.send_message(message.channel, 'Kim Havalı? #isim nickname, göster.')
        def check(msg):
            return msg.content.startswith('#isim')
        message = await bot.wait_for_message(author=message.author, check=check)
        name = message.content[len('#isim'):].strip()
        await bot.send_message(message.channel, '{} gerçekten havalı.'.format(name))
    if lower(message.content) == "selamun aleyküm":
        await bot.send_message(message.channel,"Aleyküm Selam kardeşim. Allah'ın rahmeti ve bereketi üzerine olsun.")
    ##Ads blocked
    for flit in ads_filter:
        if flit in lower(message.content):
            if message.author.server_permissions.administrator:
                print("Reklam yok sayıldı : {0} \nDiscord İsmi : {1}".format(message.author.display_name,message.server.name))
            else:
                try:
                    await bot.delete_message(message)
                    xd = await bot.send_message(message.channel, ":warning:Lütfen reklam yapmayınız. @{}".format(message.author.display_name))
                    await asyncio.sleep(10)
                    await bot.delete_message(xd)
                except discord.errors.NotFound:
                    return
    contents2 = message.content.split(" ")
    for word in contents2:
        if lower(word) in chat_filter:
            if not message.author.id in bypass_list:
                if message.author.server_permissions.administrator:
                    print("Küfür yok sayıldı : {0} \nDiscord İsmi : {1}".format(message.author.display_name,message.server.name))
                else:
                    try:
                        await bot.delete_message(message)
                        xd2 = await bot.send_message(message.channel,":warning:Lütfen bu tür kelimeler kullanmayınız. @{}".format(message.author.display_name))
                        await asyncio.sleep(10)
                        await bot.delete_message(xd2)
                    except discord.errors.NotFound:
                        return
    if mesaj_gonderme == 25:
        asyncio.wait(5)

        await bot.send_message(message.channel, "`{}` resmi botu iyi eğlenceler diler.".format(message.server.name))
        mesaj_gonderme = 0

    ##xp eklemek
    level_system.user_add_xp(message.server.id,message.author.id,2)

    await bot.process_commands(message)

##Ads blocked edited messages
@bot.event
async def on_message_edit(before,after):
    for flit in ads_filter:
        if flit in lower(after.content):
            if after.author.server_permissions.administrator:
                print("Reklam yok sayıldı : {0} \nDiscord İsmi : {1}".format(after.author.display_name, after.server.name))
            else:
                try:
                    await bot.delete_message(after)
                    xd3=await bot.send_message(after.channel, ":warning:Lütfen reklam yapmayınız. @{}".format(after.author.display_name))
                    await asyncio.sleep(10)
                    await bot.delete_message(xd3)
                except discord.errors.NotFound:
                    return
    contents2 = after.content.split(" ")
    for word in contents2:
        if lower(word) in chat_filter:
            if not after.author.id in bypass_list:
                if after.author.server_permissions.administrator:
                    print("Küfür yok sayıldı : {0} \nDiscord İsmi : {1}".format(after.author.display_name,after.server.name))
                else:
                    try:
                        await bot.delete_message(after)
                        xd4 = await bot.send_message(after.channel,":warning:Lütfen bu tür kelimeler kullanmayınız. @{}".format(after.author.display_name))
                        await asyncio.sleep(10)
                        await bot.delete_message(xd4)
                    except discord.errors.NotFound:
                        return

@bot.command(pass_context=True)
async def bilgilerim(ctx,user:discord.Member=None):
    if user is None:
        user = ctx.message.author
        await bot.say('İsim : {0} Katılma Tarihi: {0.joined_at}'.format(user))

@bot.command(pass_context=True)
async def bilgi(ctx,user:discord.Member):
    embed = discord.Embed(title=user.name,description="Bunları buldum reis.",color=0x00ff00)
    embed.add_field(name="İsim",value=user.name,inline=True)
    embed.add_field(name="ID",value=user.id)
    embed.add_field(name="Durum", value=user.status)
    embed.add_field(name="Rol", value=user.top_role)
    embed.add_field(name="Katılma Tarihi",value=user.joined_at)
    embed.add_field(name="XP",value=level_system.get_xp(ctx.message.server.id,ctx.message.author.id))
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)

@bot.command()
async def yardim():
    embed = discord.Embed(title="Komutlar",description="Kullanabileceğiniz komutlar aşağıdadır.",color=0x00ff00)
    embed.add_field(name="Genel",value="#bilgi (@nickname)\n#bilgilerim\n#gif\n#xp")
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def kicked(ctx,user:discord.Member):
    if ctx.message.author.id == "349602653107388416":
        await bot.kick(user)
        await bot.delete_message(ctx.message)
    else:
        await bot.say("You have not authority.")

##MUTE UNMUTE
@bot.command(pass_context=True)
async def mute(ctx, member: discord.Member):
    if ctx.message.author.server_permissions.administrator:
        role = discord.utils.get(member.server.roles, name='Muted')
        await bot.add_roles(member, role)
        embed = discord.Embed(title="Kullanıcı susturuldu!",description="**{1}** tarafından susturuldu **{0}**!".format(member, ctx.message.author.display_name),color=0xff00f6)
        await bot.say(embed=embed)
    else:
        embed = discord.Embed(title="Yetkin yok.", description="Bu komutu kullanmak için yetkin yok",color=0xff00f6)
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def unmute(ctx, member: discord.Member):
    if ctx.message.author.server_permissions.administrator:
        role = discord.utils.get(member.server.roles, name='Muted')
        await bot.remove_roles(member,role)
        embed = discord.Embed(title="Artık konuşabilir!",description="**{1}** tarafından kaldırıldı. **{0}**!".format(member, ctx.message.author.display_name),color=0xff00f6)
        await bot.say(embed=embed)
    else:
        embed = discord.Embed(title="Yetkin yok.", description="Bu komutu kullanmak için yetkin yok",color=0xff00f6)
        await bot.say(embed=embed)
@bot.command(pass_context=True)
async def xp(ctx):
    xp=level_system.get_xp(ctx.message.server.id,ctx.message.author.id)
    await bot.say("Şuanda `{0}` xp'iniz var. Sayın `{1}`".format(xp,ctx.message.author.display_name))


@bot.command(pass_context = True)
async def gif(ctx):
    dizi = ["http://www.delikeci.com/IcerikResim/2383/700/20141222134934464.gif","http://www.delikeci.com/IcerikResim/2387/700/20141222165443730.gif","http://www.delikeci.com/IcerikResim/2387/700/20141222165849199.gif","http://www.delikeci.com/IcerikResim/2387/700/20141222165707527.gif","http://www.delikeci.com/IcerikResim/2387/700/20141222165620293.gif","http://www.delikeci.com/IcerikResim/2387/700/20141222165549402.gif","http://www.delikeci.com/IcerikResim/2387/700/20141222165923496.gif","http://www.delikeci.com/IcerikResim/2387/700/20141222165517214.gif","https://media.giphy.com/media/xULW8PLGQwyZNaw68U/giphy.gif","https://media.giphy.com/media/Jk4ZT6R0OEUoM/giphy.gif","https://media.giphy.com/media/de5bARu0SsXiU/giphy.gif"]
    sayi = random.randint(0,len(dizi)-1)
    response = requests.get(dizi[sayi],stream=True)
    await bot.send_file(ctx.message.channel,io.BytesIO(response.raw.read()),filename='send.gif',content='{} buyur kardeşim gifin.'.format(ctx.message.author.display_name))

@bot.event
@asyncio.coroutine
def on_member_join(user):
    yield from bot.send_message(user,"**Hey discord sunucumuza hoşgeldin.\n**ßotu kendi sunucunuza eklemek için https://discordapp.com/api/oauth2/authorize?client_id=435549074112905239&permissions=8&scope=bot\n**İyi eğlenceler.\n{0}".format(user.server.owner.mention))
    # role = discord.utils.get(user.server.roles, name='vasifsiz')
    # yield from bot.add_roles(user,role)


bot.run(process.env.bot_token)
