import discord
from discord.ext import commands
from tools import checks
import asyncio
import os
from veriler import sunucu_verileri,kullanici_verileri
from tools import openfile
from tools.lower import lower
from main import komutlar
import random
import json


class Owner:

    def __init__(self,bot):
        self.bot = bot


    @commands.command(pass_context=True,hidden=True)
    @checks.is_owner()
    async def reload(self,ctx,komutismi:str=None):
        if komutismi == None:
            try:
                for x in komutlar:
                    self.bot.unload_extension(x)
                    self.bot.load_extension(x)
                await ctx.send("Başarılı",delete_after=2)
                await ctx.message.delete()
                return
            except (ImportError, SyntaxError, discord.ClientException) as e:
                await ctx.send("Başarısız "+ str(e),delete_after=2)
                await ctx.message.delete()
                return

        try:
            name = "komutlar." + komutismi
            self.bot.unload_extension(name)
            print("unloaded")
            self.bot.load_extension(name)
            print("loaded")
            await ctx.send("Başarılı",delete_after=2)
        except (ImportError, SyntaxError, discord.ClientException) as e:
            await ctx.send("Başarısız "+ str(e),delete_after=2)
        await asyncio.sleep(2)
        await ctx.message.delete()


    @commands.command(pass_context=True,hidden=True)
    @checks.is_owner()
    async def close(self,ctx):
        await ctx.send("Bot Kapatıldı.")
        await self.bot.close()


    @commands.command(pass_context=True,hidden=True)
    @checks.is_owner()
    async def botduyuru(self,ctx,*,duyuru:str):
        # Botun durumunu değiştirerek duyuru mesajı atırır.
        await self.bot.change_presence(activity=discord.Game(name=duyuru))
        await asyncio.sleep(100)
        await self.bot.change_presence(activity=discord.Game(name="{}help | Yazarak Komutları Görebilirsiniz.".format(ctx.prefix))) 

    @commands.command(pass_context=True,hidden=True)
    @checks.is_owner()
    async def addowner(self,ctx, member:discord.Member):
        # Botun kurucusunu ekleyin.
        memberID = member.id
        if os.path.isfile('./veriler/kings.json'):
            with open('./veriler/kings.json','r') as fp:
                king = json.load(fp)
            try:
                king['Owners'].append(memberID)
            except KeyError:
                king['Owners'] = []
                king['Owners'].append(memberID)
            with open('./veriler/kings.json','w') as fp:
                json.dump(king,fp,indent=4)
        else:
            king['Owners'] = []
            king['Owners'].append(memberID)        
            with open('./veriler/kings.json','w') as fp:
                json.dump(king,fp,indent=4)


    async def on_message(self,message):
        if message.author.bot:
            return
        if not message.guild:
            #Bota atılan DM'leri görmenizi sağlar.
            print(message.author.name+" / "+str(message.author.id)+" : "+message.content)


def setup(bot):
    bot.add_cog(Owner(bot))