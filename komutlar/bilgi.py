import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import json
import random
from tools import openfile
import time


class Bilgi:
    
    def __init__(self,bot):
        bilgi = openfile.Open('config.json')
        if bilgi is None:
            self.bot = bot
            return
        self.bot = bot
        self.destek_sunucu = bilgi['bot_support_discord']
        self.bot_link = bilgi['bot_invite_url']
        self.bot_version = bilgi['bot_ver']
        self.library = bilgi['library']
        self.bot_owner = bilgi['bot_creator'] 


    @commands.command(aliases=["btc"],pass_context=True)
    async def bitcoin(self,ctx):
        """Örnek : b-bitcoin"""
        r = requests.get("http://www.bitcoinfiyati.com/")
        soup = BeautifulSoup(r.content,'html.parser')
        icerik = soup.find_all('span',attrs={'class':'Bid'})
        embed = discord.Embed(title="Güncel Bitcoin Değeri",description="{}".format(icerik[0].text),color=0xFF0000)
        await ctx.send(embed=embed)


    @commands.command(aliases=["producer"],pass_context=True)
    async def yapımcı(self,ctx):
        """Örnek : b-yapımcı"""
        embed = discord.Embed(title="Yapımcı Bilgileri")
        embed.add_field(name="İsim",value=self.bot_owner)
        embed.add_field(name="Bot Davet Linki",value=self.bot_link,inline=False)
        embed.add_field(name="Destek Sunucu",value=self.destek_sunucu,inline=False)
        await ctx.send(embed=embed)
        
        
    @commands.command(aliases=["botinfo"],pass_context=True)
    async def botbilgi(self,ctx):
        """Örnek : b-botbilgi"""
        user = 0
        sv = 0
        for guild in self.bot.guilds:
            sv+=1
            user += guild.member_count
        embed = discord.Embed(color=0xffffff)
        embed.set_author(name=self.bot.user.name,icon_url=self.bot.user.avatar_url)
        embed.add_field(name='Sürüm',value=self.bot_version,inline=True)
        embed.add_field(name='ID',value=self.bot.user.id,inline=True)
        embed.add_field(name='Yapımcı',value=self.bot.appinfo.owner.name,inline=True)
        embed.add_field(name='Kütüphane',value=self.library,inline=True)
        embed.add_field(name='Sunucular',value=sv,inline=True)
        embed.add_field(name='Kullanıcılar',value=user,inline=True)
        embed.add_field(name='Patreon',value='https://goo.gl/MQzWtx',inline=True)
        embed.add_field(name='Davet',value=self.bot_link,inline=True)
        embed.add_field(name='Destek',value=self.destek_sunucu,inline=True)
        await ctx.send(embed=embed)


    @commands.command(pass_context=True)
    async def ligsıralaması(self,ctx):
        """Örnek : b-ligsıralaması"""
        embed = discord.Embed(title="Süper Lig Sıralamsı")
        sıralama = 0
        r = requests.get("https://www.sporx.com/spor-toto-super-lig-puan-durumu")
        soup = BeautifulSoup(r.content,'html.parser')
        icerik = soup.find_all('td',attrs={'class':'td-team'},limit=18)
        lig = []
        for x in icerik:
            takim = x.text
            lig.append(takim)
        for name in lig:
            sıralama+=1
            embed.add_field(name=str(sıralama)+".",value=name,inline=False)
        await ctx.send(embed=embed)


    @commands.command(pass_context=True)
    async def atatürk(self,ctx):
        """Örnek : b-atatürk"""
        r = requests.get("http://biriz.biz/ata/")
        soup = BeautifulSoup(r.content,'html.parser')
        icerik = soup.find_all('img')
        sayi = random.randint(1,len(icerik))
        link = icerik[sayi].get('src')
        true_link = "http://biriz.biz/ata/"
        image_link = true_link + link
        r = requests.get("https://tr.wikiquote.org/wiki/Mustafa_Kemal_Atat%C3%BCrk")
        soup = BeautifulSoup(r.content,'html.parser')
        icerik = soup.find_all('li',limit=123)
        sayi = random.randint(0,123)
        embed=discord.Embed(title=icerik[sayi].text,color=0x00ff00)
        embed.set_image(url=image_link)
        await ctx.send(embed=embed)


    @commands.command(pass_context=True)
    async def call(self,ctx):
        """Örnek : b-call"""
        embed=discord.Embed(description="[Buraya tıklayarak botu sunucunuza çağırabilirsiniz.]({})".format(self.bot_link),color=0x000000)
        embed.set_author(name=self.bot.user.name,url=self.bot_link,icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)


    @commands.command(pass_context=True)
    async def ping(self,ctx):
        """Örnek : b-ping"""
        try:
            pingtime = time.time()
            pingms = await ctx.send("*Pinging...*")
            ping = (time.time() - pingtime) * 1000
            await pingms.edit(content="**Pong!** :ping_pong:  The ping time is `%dms`" % ping)

        except:
            pass


    @commands.command(aliases=["donate"])
    async def bağış(self, ctx):
        """Bozkurtu desteklemek için bağış yollayabilirsiniz."""
        await ctx.send("https://www.patreon.com/bozkurtbot , Bağışlarınız için şimdiden teşekkürler.")


def setup(bot):
    bot.add_cog(Bilgi(bot))