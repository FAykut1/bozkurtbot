import discord,requests,safygiphy
from bs4 import BeautifulSoup
from discord.ext import commands
from datetime import datetime
import random

g=safygiphy.Giphy()

class Fun:
    def __init__(self,bot):
        self.bot = bot
        

    @commands.command(aliases=["dog"],pass_context=True)
    async def köpek(self,ctx):
        """Örnek : b-köpek"""
        try:
            r = requests.get("https://random.dog/woof.json")
            r.headers['content-type']
            url = r.text
            a = url.split('"')
            embed=discord.Embed(color=0x00ff00)
            embed.set_image(url=a[3])
            await ctx.send(embed=embed)
        except:
            await ctx.send("Bir şeyler yanlış gitti. Daha sonra tekrar dene.")


    @commands.command(aliases=["cat"],pass_context=True)
    async def kedi(self,ctx):
        """Örnek : b-kedi"""
        try:
            r = requests.get("https://random.cat")
            soup = BeautifulSoup(r.content,'html.parser')
            icerik = soup.find_all('img')
            a = str(icerik[0])
            url = a.split('"')
            embed=discord.Embed(color=0x00ff00)
            embed.set_image(url=url[5])
            await ctx.send(embed=embed)
        except:
            await ctx.send("Bir şeyler yanlış gitti. Daha sonra tekrar dene.")


    @commands.command(pass_context=True)
    async def gif(self,ctx,*,tag:str=None):
        """Örnek : b-gif Funny"""
        try:
            if tag == None:
                tag = "funny"
            gif_tag = tag
            rgif = g.random(tag=str(gif_tag))
            emb = discord.Embed(color=0x00ff00)
            emb.set_image(url=str(rgif.get("data",{}).get('image_original_url')))
            await ctx.send(embed=emb)
        except:
            await ctx.send("Bir şeyler yanlış gitti. Daha sonra tekrar dene.")


    @commands.command(pass_context=True)
    async def marvel(self,ctx):
        """Örnek : b-marvel"""
        try:
            sayi = random.randint(1,32)
            r = requests.get("https://wall.alphacoders.com/tags.php?tid=275&page="+str(sayi))
            soup = BeautifulSoup(r.content,'html.parser')
            icerik = soup.find_all('img')  
            images = []  
            for x in icerik:
                link = x.get('src')
                if "images" in link:
                    images.append(link)
            rasgele_resim = random.randint(1,len(images))
            link = images[rasgele_resim]
            embed=discord.Embed(color=0x00ff00) 
            embed.set_image(url=link)
            await ctx.send(embed=embed)
        except IndexError:
            await ctx.send("Lütfen tekrar deneyiniz.")


    @commands.command(aliases=["mcarchievement"],pass_context=True)
    async def mcbaşarım(self,ctx,*,basarim:str):
        """Örnek : b-mcbaşarım BOZKURT"""
        try:
            aaa = basarim.split(" ")
            string = ""
            for say in range(len(aaa)):
                string += aaa[say]+"%20"
            link = "https://www.minecraftskinstealer.com/achievement/a.php?i=2&h=Basarim%20Acildi%21&t="+string
            embed=discord.Embed(color=0xffffff)
            embed.set_image(url=link)
            await ctx.send(embed=embed)
        except:
            await ctx.send("Bir şeyler yanlış gitti. Daha sonra tekrar dene.")


def setup(bot):
    bot.add_cog(Fun(bot))