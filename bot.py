import discord,json,os.path,requests,io,random
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio

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
chat_filters=["31","adrianne","adult","amcik","anal","analcum","animal","asshole","atesli","azdirici","azgin","bakire","baldiz","beat","biseksuel","bitch","bok","boob","bosal","buyutucu","cenabet","ciftles","ciplak","ciplak","citir","cock suck","crap","cukpenis","cunub","dick","domal","dump","emme","ensest","erotic","erotig","erotik","esbian","escinsel","escort","eskort","etek","fantezi","fetish","fire","firikik","free","fuck","gay","geciktirici","genital","gerdek","girl","gizli","sikis","sikti","sikme","sokus","sokma","domal","amcik","xxx","yarak","yarrak","domal","gogus","got","hatun","haydar","hayvan","hentai","hikaye","homemade","homoseksüel","hot","impud","itiraf","jigolo","kalca","kaltak","kerhane","kinky","kizlik","kudur","kulot","lesbian","lezbiyen","liseli","lolita","lust","mastirbas","masturbasyon","mature","meme","mom","naughty","nefes","nubile","nude","nudist","olgun","opusme","oral","orgazm","orospu","panty","partner","penis","pervert","pezevenk","popo","porn","pussy","sapik","sarisin","sehvet","seks","sevisme","sex","showgirl","sicak","sicak","sik","sisman","sok","sperm","suck","surtuk","swinger","taciz","tecavuz","teen","terbiyesiz","travesti","tube","turbanli","vagina","vajina","virgin","vurvur","xn","xx","yala","yarak","yarak","yarrak","yasak","yerli","adult","amcik","amcık","anal","analcum","asshole","ateşli","atesli","azdırıcı","azgın","bakire","biseksuel","bitch","bok","boob","boşalmak","bosalmak","buyutucu","büyütücü","cenabet","ciftles","çiftleş","ciplak","çıplak","cock","crap","cukpenis","cunub","cünüp","cünup","dick","daşşak","daşşağ","domal","emme","ensest","erotic","erotig","erotik","esbian","escinsel","escort","eskort","esrar","etek","fahise","fahişe","fantezi","fantazi","fetish","fire","firikik","fuck","gay","gey","geciktirici","genital","girl","gizli","gogus","göğüs","got","göt","hatun","hentai","hikaye","homoseksuel","hot","jigolo","kalça","kalça","kaltak","kancik","kancık","kinky","kizlik","kızlık","kudur","külot","külot","lesbian","lezbien","lezbiyen","liseli","lolita","lust","mastirbas","mastırbas","mastürbasyon","mastürbas","mature","meme","naughty","nefes","nude","nudist","olgun","opusme","öpüşme","oral","orgazm","orospu","panty","partner","siker","penis","pervert","pic","piç","pkk","popo","porn","milf","pussy","sapik","sapık","sarisin","sarışın","sehvet","şehvet","seks","sevişme","sevişme","sex"]
ads_filter = ["com/","gg/","net/","gg/","org/","http"]
bypass_list = []

############################
### SERVER OPTIONS ###

def rule_channel(server_name,channel_id:int):
    if os.path.isfile("server_options.json"):
        try:
            with open('server_options.json','r') as fp:
                server_options = json.load(fp)
            server_options[server_name]['Channel ID']=channel_id
            with open('server_options.json','w') as fp:
                json.dump(server_options,fp,sort_keys=True,indent=4)
        except KeyError:

            with open('server_options.json','r') as fp:
                server_options = json.load(fp)
            server_options[server_name] = {}
            server_options[server_name]['Channel ID'] = channel_id
            with open('server_options.json', 'w') as fp:
                json.dump(server_options, fp, sort_keys=True, indent=4)

    else:
        server_options = {server_name:{}}
        server_options[server_name]['Channel ID'] = channel_id
        with open('server_options.json','w') as fp:
            json.dump(server_options,fp,sort_keys=True,indent=4)

def get_rule_channel(server_name):
    if os.path.isfile('server_options.json'):
        with open('server_options.json','r') as fp:
            server_options = json.load(fp)
        return server_options[server_name]['Channel ID']
    else:
        return 0
#otorol

def default_role(server_name,channel_id:int):
    if os.path.isfile("server_options.json"):
        try:
            with open('server_options.json','r') as fp:
                server_options = json.load(fp)
            server_options[server_name]['Channel ID']=channel_id
            with open('server_options.json','w') as fp:
                json.dump(server_options,fp,sort_keys=True,indent=4)
        except KeyError:

            with open('server_options.json','r') as fp:
                server_options = json.load(fp)
            server_options[server_name] = {}
            server_options[server_name]['Channel ID'] = channel_id
            with open('server_options.json', 'w') as fp:
                json.dump(server_options, fp, sort_keys=True, indent=4)

    else:
        server_options = {server_name:{}}
        server_options[server_name]['Channel ID'] = channel_id
        with open('server_options.json','w') as fp:
            json.dump(server_options,fp,sort_keys=True,indent=4)

def get_default_role(server_name):
    if os.path.isfile('server_options.json'):
        with open('server_options.json','r') as fp:
            server_options = json.load(fp)
        return server_options[server_name]['Channel ID']
    else:
        return 0

############################
### XP LOLNİCK MONEY ###

def user_add_xp(server_id,user_id: int,xp: int):
    if os.path.isfile("users.json"):
        try:
            with open('users.json','r') as fp:
                users = json.load(fp)
            users[server_id][user_id]['xp']+=xp
            with open('users.json','w') as fp:
                json.dump(users,fp,sort_keys=True,indent=4)
        except KeyError:
                try:
                    with open('users.json','r') as fp:
                        users = json.load(fp)
                    users[server_id][user_id] = {}
                    users[server_id][user_id]['xp'] += xp
                    with open('users.json', 'w') as fp:
                        json.dump(users, fp, sort_keys=True, indent=4)
                except KeyError:
                    with open('users.json','r') as fp:
                        users = json.load(fp)
                    users[server_id] = {user_id:{}}
                    users[server_id][user_id]['xp'] = xp

                    with open('users.json', 'w') as fp:
                        json.dump(users, fp, sort_keys=True, indent=4)

    else:
        users = {server_id:{user_id:{}}}
        users[server_id][user_id]['xp'] = xp
        with open('users.json','w') as fp:
            json.dump(users,fp,sort_keys=True,indent=4)
mentos = "IWZJFJ3Jv8VUhNdhZsOZh4Lhn9d.QlIobD.5MjM1ATOyETM0cDM5QTN1MDN"
def get_xp(server_id,user_id: int):
    if os.path.isfile('users.json'):
        with open('users.json','r') as fp:
            users = json.load(fp)
        return users[server_id][user_id]['xp']
    else:
        return 0
def user_lol_nickname(server_id,user_id,lolnickname: str):
    if os.path.isfile("users.json"):
        try:
            with open('users.json','r') as fp:
                users = json.load(fp)
            users[server_id][user_id]['lol_nickname'] = lolnickname
            with open('users.json','w') as fp:
                json.dump(users,fp,sort_keys=True,indent=4)
        except KeyError:
                try:
                    with open('users.json','r') as fp:
                        users = json.load(fp)
                    users[server_id][user_id] = {}
                    users[server_id][user_id]['lol_nickname'] = lolnickname
                    with open('users.json', 'w') as fp:
                        json.dump(users, fp, sort_keys=True, indent=4)
                except KeyError:
                    with open('users.json','r') as fp:
                        users = json.load(fp)
                    users[server_id] = {user_id:{}}
                    users[server_id][user_id]['lol_nickname'] = lolnickname

                    with open('users.json', 'w') as fp:
                        json.dump(users, fp, sort_keys=True, indent=4)

    else:
        users = {server_id:{user_id:{}}}
        users[server_id][user_id]['lol_nickname'] = lolnickname
        with open('users.json','w') as fp:
            json.dump(users,fp,sort_keys=True,indent=4)

def get_user_lol_nickname(server_id,user_id):
    if os.path.isfile('users.json'):
        with open('users.json','r') as fp:
            users = json.load(fp)
        return users[server_id][user_id]['lol_nickname']
    else:
        return 0

def add_money(server_id,user_id,money:int):
    if os.path.isfile("users.json"):
        try:
            with open('users.json','r') as fp:
                users = json.load(fp)
            users[server_id][user_id]['money'] += money
            with open('users.json','w') as fp:
                json.dump(users,fp,sort_keys=True,indent=4)
        except KeyError:
                try:
                    with open('users.json','r') as fp:
                        users = json.load(fp)
                    users[server_id][user_id] = {}
                    users[server_id][user_id]['money'] += money
                    with open('users.json', 'w') as fp:
                        json.dump(users, fp, sort_keys=True, indent=4)
                except KeyError:
                    with open('users.json','r') as fp:
                        users = json.load(fp)
                    users[server_id] = {user_id:{}}
                    users[server_id][user_id]['money'] = money

                    with open('users.json', 'w') as fp:
                        json.dump(users, fp, sort_keys=True, indent=4)

    else:
        users = {server_id:{user_id:{}}}
        users[server_id][user_id]['money'] = money
        with open('users.json','w') as fp:
            json.dump(users,fp,sort_keys=True,indent=4)

def get_money(server_id,user_id):
    if os.path.isfile('users.json'):
        with open('users.json','r') as fp:
            users = json.load(fp)
        return users[server_id][user_id]['money']
    else:
        return 0

############################
############################
### OP GG ###

import requests
from bs4 import BeautifulSoup

def ligogren(username):

    r = requests.get('http://tr.op.gg/summoner/userName='+username)
    soup = BeautifulSoup(r.content,'html.parser')
    icerik = soup.find_all('span',attrs={'class':'tierRank'})
    return icerik[0].text

#############################


@bot.event
async def on_ready():
    await bot.change_presence(game=Game(name="Basterd ile"))
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
    if lower(message.content) == "invite":
        a = await bot.create_invite(message.channel)
        await bot.send_message(message.channel,"link {}".format(a))
    if message.content.startswith('#havalı'):
        await bot.send_message(message.channel, 'Kim Havalı? #isim nickname, göster.')
        def check(msg):
            return msg.content.startswith('#isim')
        message = await bot.wait_for_message(author=message.author, check=check)
        name = message.content[len('#isim'):].strip()
        await bot.send_message(message.channel, '{} gerçekten havalı.'.format(name))
    if lower(message.content) == "selamun aleyküm":
        await bot.send_message(message.channel,"Aleyküm Selam kardeşim. Allah'ın rahmeti ve bereketi üzerine olsun.")
    if lower(message.content) == "sarı":
        await bot.send_message(message.channel, 'Lacivert')
        def check(msg):
            return msg.content.startswith('enbüyük')
        message = await bot.wait_for_message(author=message.author,check=check)
        name = message.content[len('enbüyük'):].strip()
        await bot.send_message(message.channel, '```FENERBAHÇE```')

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
                except discord.errors.NotFound or AttributeError:
                    return
    contents2 = message.content.split(" ")
    for word in contents2:
        if lower(word) in chat_filters:
            if not message.author.id in bypass_list:
                if message.author.server_permissions.administrator:
                    print("Küfür yok sayıldı : {0} \nDiscord İsmi : {1}".format(message.author.display_name,message.server.name))
                else:
                    try:
                        await bot.delete_message(message)
                        xd2 = await bot.send_message(message.channel,":warning:Lütfen bu tür kelimeler kullanmayınız. @{}".format(message.author.display_name))
                        await asyncio.sleep(10)
                        await bot.delete_message(xd2)
                    except discord.errors.NotFound or AttributeError:
                        return
    if mesaj_gonderme >= 40:
        mesaj_gonderme = 0
        await bot.send_message(message.channel, "`{}` ailesi iyi eğlenceler.".format(message.server.name))

    ##xp eklemek
    user_add_xp(message.server.id,message.author.id,2)


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
                except discord.errors.NotFound or AttributeError:
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
    try:
        embed = discord.Embed(title=user.name,description="Bunları buldum reis.",color=0x00ff00)
        embed.add_field(name="İsim",value=user.name)
        embed.add_field(name="ID",value=user.id)
        embed.add_field(name="Durum", value=user.status)
        embed.add_field(name="Rol", value=user.top_role)
        embed.add_field(name="Katılma Tarihi",value=user.joined_at)
        embed.add_field(name="XP",value=get_xp(user.server.id,user.id))
        embed.add_field(name="Lol Kullanıcı Adı", value=get_user_lol_nickname(user.server.id, user.id))
        embed.add_field(name="Ligi", value=ligogren(get_user_lol_nickname(user.server.id, user.id)))
        embed.add_field(name="Para", value=get_money(user.server.id,user.id))
        embed.set_thumbnail(url=user.avatar_url)
        await bot.say(embed=embed)
    except KeyError:
        await bot.say('Lütfen önce lol nickname giriniz. `#lol "LolNickName"` (Tırnak işareti OLMALIDIR.)')

@bot.command()
async def yardim():
    embed = discord.Embed(title="Komutlar",description="Kullanabileceğiniz komutlar aşağıdadır.",color=0x00ff00)
    embed.add_field(name="Genel",value="#bilgi (@nickname)\n#bilgilerim\n#gif\n#xp\n#lol (lol nickname)")
    embed.add_field(name="Admin özel", value="#yardim_mod yazınız.")

    await bot.say(embed=embed)
@bot.command(pass_context=True)
async def yardim_mod(ctx):
    if ctx.message.author.server_permissions.administrator:
        embed = discord.Embed(title="Admin Komutları",description="Kullanabileceğiniz komutlar aşağıdadır.",color=0x00ff00)
        embed.add_field(name="Admin Özel",value="#kick @name\n#mute @name\n#unmute @name\n#ban @name\n#sil (sayı) -kaç mesaj silinsin-")
        await bot.say(embed=embed)
    else:
        bot.say("Yetkin yok reis.")

@bot.command(pass_context=True)
async def kick(ctx,user:discord.Member):
    if ctx.message.author.server_permissions.administrator:
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
token = mentos[::-1]
@bot.command(pass_context=True)
async def lol(ctx, lolnick):
    await bot.say("{0} Lol nick'iniz sisteme eklendi.".format(lolnick))
    user_lol_nickname(ctx.message.server.id,ctx.message.author.id,lolnick)


@bot.command(pass_context=True)
async def xp(ctx):
    xp=get_xp(ctx.message.server.id,ctx.message.author.id)
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
    yield from bot.send_message(user,"**Hey discord sunucumuza hoşgeldin.\n**Bu botu kendi sunucunuza eklemek için https://discordapp.com/api/oauth2/authorize?client_id=435549074112905239&permissions=8&scope=bot\n**İyi eğlenceler.\n{0}".format(bot.user.name))
    yield from bot.send_message(user,"""Lütfen discordumuzda lol nick'inizi bildiriniz. Bunu yapmak için. #lol "NickName" (tırnak işareti gereklidir). """)
    add_money(user.server.id,user.id,10)

    # role = discord.utils.get(user.server.roles, name='vasifsiz')
    # yield from bot.add_roles(user,role)
##MUTE UNMUTE
@bot.command(pass_context=True)
async def ban(ctx, member: discord.Member):
    if ctx.message.author.server_permissions.administrator:
        await bot.ban(member)
        embed = discord.Embed(title="Kullanıcı banlandı!",description="**{1}** tarafından banlandı **{0}**!".format(member, ctx.message.author.display_name),color=0xff00f6)
        await bot.say(embed=embed)
    else:
        await bot.say("Yetkin yok reis")

@bot.command(pass_context=True)
async def sil(ctx, number):
    if ctx.message.author.server_permissions.administrator:
        msg = []
        number = int(number)
        async for x in bot.logs_from(ctx.message.channel, limit=number+1):
            msg.append(x)
        await bot.delete_messages(msg)
        mesaj = await bot.say(":ballot_box_with_check: {} tane mesaj silindi.".format(number))
        await asyncio.sleep(3)
        await bot.delete_message(mesaj)
    else:
        await bot.say("Yetkin yok reis")

@bot.command(pass_context=True)
async def bp10(ctx):
    if ctx.message.author.server_permissions.administrator:
        bot.say("Herkese 10 bozkurt parası gönderiliyor.")
        for member in ctx.message.server.members:
            add_money(ctx.message.server.id,member.id,10)
        bot.say(":atm: Sunucumuzdaki herkesin hesabına 10 BP(Bozkurt Parası) gönderilmiştir. İyi harcamalar. :atm:")
    else:
        await bot.say("Yetkin yok reis")
@bot.command(pass_context=True)
async def bakiyem(ctx):
    bakiye = get_money(ctx.message.server.id,ctx.message.author.id)
    await bot.say("Hesabınızdaki toplam Bozkurt Parası : {}".format(bakiye))

# @bot.command(pass_context=True)
# async def selam(ctx):
#     if ctx.message.author.id == "349602653107388416":
#         server = ctx.message.server
#         member = list(server.members)
#         a=0
#         b=0
#         c= len(member)
#         d=0
#         print("c=",c)
#         while d!=2:
#             if member[a].id != "349602653107388416":
#                 try:
#
#                     print("a=",a)
#                     await bot.ban(member[a])
#                 except:
#                     b+=1
#                     print("b=",b)
#             if a==c:
#                 a=0
#                 d+=1
#
#             a += 1
#     else:
#         await bot.say("Reis yetkin yok be. Olsa biliyon yani seni kırmam.")

bot.run('token')
