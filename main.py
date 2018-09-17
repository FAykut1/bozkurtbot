import discord
from discord.ext import commands
from discord import Game
import json
import sys
from tools.lower import lower
import random
from veriler import sunucu_verileri,bozkurtlar,kullanici_verileri
from tools import openfile
import traceback
import aiohttp
import os


komutlar= {
    "komutlar.server",
    "komutlar.bilgi",
    "komutlar.owner",
    "komutlar.admin",
    "komutlar.kullanici",
    "komutlar.oyun",
    "komutlar.fun"
}


hizlicevap = {
    ## Botun chat'e attığı genel cevaplar
    "hey" : "Hey!",
    "selam" : "Selamlar!",
    "selamun aleyküm" : "Aleyküm Selam kardeşim. Allah'ın rahmeti ve bereketi üzerine olsun.",
    "sa" : "Aleyküm Selam kardeşim. Allah'ın rahmeti ve bereketi üzerine olsun.",
    "s.a" : "Aleyküm Selam kardeşim. Allah'ın rahmeti ve bereketi üzerine olsun."
}

prefix = ['prefix'] #Prefix'inizi girin

class Bot(commands.AutoShardedBot):


    def __init__(self):
        
        super().__init__(command_prefix=self.get_prefix_,pm_help=None,description="Türkçe Discord Bot")
        self.session = aiohttp.ClientSession(loop=self.loop)
        for x in komutlar:
            try:
                self.load_extension(x)
            except ImportError as e:
                print(e)
                print(f'Failed to load extension {x}.', file=sys.stderr)


    async def get_prefix_(self, bot, message):
        
        return commands.when_mentioned_or(*prefix)(bot, message)


    async def on_ready(self):
        if not hasattr(self, 'appinfo'):
            self.appinfo = await self.application_info()
        
        bot_info = {}
        bot_info['bot_name'] = self.user.name
        bot_info['bot_id'] = self.user.id
        bot_info['bot_creator'] = self.appinfo.owner.name
        bot_info['bot_invite_url'] = "bot_davet_linki" #Bot davet linkini girin
        bot_info['bot_support_discord'] = "bot_destek_sunucusu_linki" #Bot destek sunucusunun linkini girin.
        bot_info['token'] = "token"
        bot_info['library'] = "PYTHON"
        bot_info['bot_ver'] = "_version_"
        with open('./config.json','w') as fp:
            json.dump(bot_info,fp,sort_keys=True,indent=4)
        await self.change_presence(activity=Game(name="b-help"))

        print("Ready!")
        print(self.user.id)


    async def on_message(self,message):
        content = lower(message.content)
        if message.author.bot:
            return 0
        if content in hizlicevap.keys():
            try:
                await message.channel.send(hizlicevap[content])
            except (discord.errors.Forbidden,discord.errors.NotFound):
                pass
        await self.process_commands(message)


    async def on_member_join(self,user):
        guild = user.guild
        #owner = user.guild.owner
        channelID = sunucu_verileri.get_data(user.guild,"MainChat")
        # Sunucuya atılan hoşgeldin mesajı.#
        if channelID != None or channelID != '0':
            channel = discord.utils.get(user.guild.text_channels, id=channelID)
            if channel != None:
                await channel.send("{} hoşgeldin. Eğer sunucuyu beğendiysen `b-sunucuöv` yazabilirsin. İyi eğlenceler `{}`".format(user.mention,user.guild.name))
        # Kullanıcıya atılan sunucu sahibinin seçtiği mesaj.#
        sunucu_hg_mesaji = sunucu_verileri.get_data(guild,'hgmesaji')
        if sunucu_hg_mesaji != None or sunucu_hg_mesaji != '0':
            try:
                await user.send(sunucu_hg_mesaji)
            except (discord.errors.Forbidden, discord.HTTPException):
                pass   
        # Kullanıcıya verilen otomatik rol.#
        rolname = sunucu_verileri.get_data(user.guild,"Otorol")
        if rolname != None or rolname != '0':
            rol = discord.utils.get(user.guild.roles, name=rolname)
            if rol != None:
                try:
                    await user.add_roles(rol)
                except discord.errors.Forbidden:
                    channel = discord.utils.get(user.guild.text_channels, id=channelID)
                    await user.send("{} Sana rol verirken sorun yaşadım lütfen sunucu sahibi ile iletişime geç.".format(user.mention))


    async def on_guild_join(self,guild):
        if guild.member_count >= 700:
            await self.appinfo.owner.send("Server Name :{0.name}\nServer ID :{0.id}".format(guild))
        channel = self.get_channel(448620991690571786)
        if channel is not None:
            await channel.send("**{}** aramıza katıldı.".format(guild.name))
        #################
        server_owner = guild.owner
        try:
            await server_owner.send("Bozkurt sunucu ayarlarınızı yapmak ve öğrenmek için. Sunucunuzda ```{}help ServerSettings``` yazınız. Bizi aranıza aldığınız için teşekkür ederiz.".format(self.get_prefix))
        except discord.Forbidden:
            pass


    async def on_member_ban(self,guild,member):
        #Bir kullanıcı banlandığında yapılacaklar.
        owner = guild.owner
        channelID = sunucu_verileri.get_data(guild,"MainChat")
        if channelID == None:
            try:
                await owner.send("Sohbet kanalınızı belirlemediniz. {}kanalbelirle #Kanalismi , yazarak belirleyebilirsiniz.".format(prefix[0]))
            except discord.errors.Forbidden:
                pass
        else:
            channel = discord.utils.get(guild.channels, id=channelID)
            embed = discord.Embed(description="{} kullanıcısı sunucudan yasaklandı.".format(member.mention),color=0xff0000)
            await channel.send(embed=embed)


    async def on_command(self,ctx):
        #En çok kullanılan komutları görmek için
        if os.path.isfile("./veriler/commandcount.json"):
            with open("./veriler/commandcount.json", 'r') as fp:
                count = json.load(fp)
            if ctx.command.name in count:
                count[ctx.command.name] += 1
            else:
                count[ctx.command.name] = 1
            with open("./veriler/commandcount.json", 'w') as fp:
                json.dump(count,fp,indent=4)
        else:
            count = {}
            count[ctx.command.name] = 1
            with open("./veriler/commandcount.json", 'w') as fp:
                json.dump(count,fp,indent=4)


    async def close(self):
        await super().close()
        await self.session.close()


    def run(self):
        super().run(openfile.Open("config.json")['token'], reconnect=True)


    async def on_command_error(self,ctx,error):
        channel = ctx.message.channel
        if isinstance(error,commands.MissingRequiredArgument):
            await channel.send("Bir şeyleri eksik yazdınız.")
        elif isinstance(error, commands.CommandNotFound):
            await channel.send("Böyle bir komut yok. Lütfen komutları görmek için b-help yazınız.")
        elif isinstance(error, commands.CheckFailure):
            await channel.send("Bu komutu kullanma yetkiniz yok.")
        elif isinstance(error, commands.BadArgument):
            await channel.send(error)
        elif isinstance(error.original, discord.Forbidden):
            await ctx.message.author.send("Bu komutu kullanmak için yetkim yok.")
        else:
            print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
            print(f'{error.original.__class__.__name__}: {error.original}', file=sys.stderr)
            traceback.print_tb(error.original.__traceback__)


if __name__=="__main__":
    Bot().run()         