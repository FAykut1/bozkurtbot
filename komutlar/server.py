import discord
from discord.ext import commands
from tools import checks
from veriler import sunucu_verileri,kullanici_verileri
from tools.lower import lower
import json
import os
import asyncio

swear_filter = ['engellemek_istediğiniz_küfürler']
ads_filter = ["com/","gg/","net/","org/","http","https"] # Değiştirmeyin.


class ServerSettings:
    def __init__(self,bot):
        self.bot = bot


    @commands.command(aliases=["serverinfo"],pass_context=True)
    async def sunucubilgi(self,ctx):
        """Örnek : b-sunucubilgi"""
        guild = ctx.message.author.guild
        if sunucu_verileri.get_data(guild,"Adblock") == 1:
            reklam = 'Açık'
        else:
            reklam = 'Kapalı'
        if sunucu_verileri.get_data(guild,"BadWordBlock") == 1:
            kufur = 'Açık'
        else:
            kufur = 'Kapalı'
        MainChat = sunucu_verileri.get_data(guild,"MainChat")
        if MainChat == None or MainChat == '0':
            MainChat = 'Belirtilmedi'
        else:
            MainChat = self.bot.get_channel(MainChat)
        ovgu = sunucu_verileri.get_data(guild,'praise')
        if ovgu == None:
            ovgu = 0
        createDate = "{0.day}/{0.month}/{0.year}".format(guild.created_at)
        embed = discord.Embed(title="{} sunucu bilgileri.\n".format(guild.name),description='Sunucumuza ait bilgileri aşağıda bulabilirsiniz.',color=0xFF00FF)
        embed.add_field(name="Kurucu :",value=guild.owner.mention)
        embed.add_field(name="Övgü Sayısı :",value=ovgu)
        embed.add_field(name="Üye Sayısı :",value=guild.member_count)
        embed.add_field(name="Rol Sayısı :",value=len(guild.roles))
        embed.add_field(name="Yazı Kanalı Sayısı :",value=len(guild.text_channels))
        embed.add_field(name="Ses Kanalı Sayısı :",value=len(guild.voice_channels))
        embed.add_field(name="Kategori Kanalı Sayısı :",value=len(guild.categories))
        embed.add_field(name="Genel Chat Kanalı :", value = MainChat.name)
        embed.add_field(name="Reklam Engelleme :",value=reklam)
        embed.add_field(name="Küfür Engelleme :",value=kufur)
        embed.add_field(name="Kuruluş Tarihi :",value=createDate)
        await ctx.send(embed=embed)


    @commands.command(pass_context=True)
    @checks.is_admin()
    async def kanalbelirle(self,ctx,kanal:discord.TextChannel):
        """Örnek : b-kanalbelirle #genel"""
        channelID = kanal.id
        guild = kanal.guild
        channel = ctx.message.channel
        sunucu_verileri.add_data(guild,"MainChat",channelID)
        await channel.send("Ana sohbet kanalınızı belirlediniz. "+kanal.mention)


    @commands.command(pass_context=True)
    @checks.is_admin()
    async def kanalkaldır(self,ctx):
        """Örnek : b-kanalkaldır"""
        guild = ctx.message.guild
        channel = ctx.message.channel
        sunucu_verileri.add_data(guild,"MainChat",'0')
        await channel.send("Ana sohbet kanalınızı kaldırdınız.")


    @commands.command(aliases=["adblock"],pass_context=True)
    @checks.is_admin()
    async def reklamengelle(self,ctx,value:str=None):
        """Örnek : b-reklamengelle aktif/pasif"""
        guild = ctx.message.author.guild
        if lower(value) == "aktif" or value == "1" or lower(value) == "aç":
            sunucu_verileri.add_data(guild,"Adblock",1)
            embed = discord.Embed(title="Reklam engelleme",description="Açık",color=0x0000FF)
            await ctx.send(embed=embed)
        elif lower(value) == "pasif" or value == "0" or lower(value) == "kapat":
            sunucu_verileri.add_data(guild,"Adblock",0)
            embed = discord.Embed(title="Reklam engelleme",description="Kapalı",color=0x0000FF)
            await ctx.send(embed=embed)
        elif value == None:
            data = sunucu_verileri.get_data(guild,"Adblock")
            if data == None or data == 0:
                sunucu_verileri.add_data(guild,"Adblock",1)
                embed = discord.Embed(title="Reklam engelleme",description="Açık",color=0x0000FF)
                await ctx.send(embed=embed)
            else:
                sunucu_verileri.add_data(guild,"Adblock",0)
                embed = discord.Embed(title="Reklam engelleme",description="Kapalı",color=0x0000FF)
                await ctx.send(embed=embed)             
        else:
            embed = discord.Embed(title="Reklam engelleme",description="Açmak için : aktif\n Kapatmak için : pasif",color=0x0000FF)
            await ctx.send(embed=embed)


    @commands.command(pass_context=True)
    @checks.is_admin()
    async def küfürengelle(self,ctx,value:str=None):
        """Örnek : b-küfürengelle aktif/pasif"""
        guild = ctx.message.author.guild
        if lower(value) == "aktif" or value == "1" or lower(value) == "aç":
            sunucu_verileri.add_data(guild,"BadWordBlock",1)
            embed = discord.Embed(title="Kötü kelime engelleme",description="Açık",color=0x0000FF)
            await ctx.send(embed=embed)
        elif lower(value) == "pasif" or value == "0" or lower(value) == "kapat":
            sunucu_verileri.add_data(guild,"BadWordBlock",0)
            embed = discord.Embed(title="Kötü kelime engelleme",description="Kapalı",color=0x0000FF)
            await ctx.send(embed=embed)
        elif value == None:
            data = sunucu_verileri.get_data(guild,"BadWordBlock")
            if data == None or data == 0:
                sunucu_verileri.add_data(guild,"BadWordBlock",1)
                embed = discord.Embed(title="Kötü kelime engelleme",description="Açık",color=0x0000FF)
                await ctx.send(embed=embed)
            else:
                sunucu_verileri.add_data(guild,"BadWordBlock",0)
                embed = discord.Embed(title="Kötü kelime engelleme",description="Kapalı",color=0x0000FF)
                await ctx.send(embed=embed)                        
        else:
            embed = discord.Embed(title="Kötü kelime engelleme",description="Açmak için : aktif\n Kapatmak için : pasif",color=0x0000FF)
            await ctx.send(embed=embed)


    @commands.command(pass_context=True)
    @checks.is_admin()
    async def otorol(self,ctx,rol:discord.Role=None):
        """b-otorol @rol, kapatmak için rol etiketlemeyin."""
        guild = ctx.message.author.guild
        if rol == None:
            sunucu_verileri.add_data(guild,"Otorol", '0')
            await ctx.send("Otorol kapatıldı.")
        elif rol == discord.Role:
            sunucu_verileri.add_data(guild,"Otorol", rol.name)
            await ctx.send("Tebrikler artık sunucunuza gelen kişiler otomatik olarak {0.mention} rolüne atanacak.".format(rol))


    @commands.command()
    @checks.is_admin()
    async def özelhgmesajı(self, ctx, *,mesaj:str=None):
        """b-özelhgmesajı Sunucumuza hoşgeldiniz iyi eğlenceler | Boş bırakırsanız mesaj atmaz."""
        guild = ctx.message.author.guild
        if mesaj == None:
            sunucu_verileri.add_data(guild,"hgmesaji", '0')
        try:
            sunucu_verileri.add_data(guild,"hgmesaji", mesaj)
            await ctx.send("Hoşgeldin mesajını ayarlanmıştır.")
        except:
            await ctx.send("Bir sorun oluştu Lütfen tekrar deneyiniz.")


    async def on_message(self,message):
        if message.author.bot:
            return
        if not message.guild:
            return
        guild = message.channel.guild
        # KÖTÜ KELİME ENGELLEME
        badWordValue = sunucu_verileri.get_data(guild,"BadWordBlock")
        if badWordValue == 1: 
            for word in swear_filter:
                if word in lower(message.content):
                    if not message.author.guild_permissions.administrator:
                        try:
                            await message.delete()
                            if self.bot.user.mentioned_in(message):
                                msg = await message.channel.send(":warning:AAAA BU YAPTIĞIN ÇOK AYIP. <@{}>".format(message.author.id),delete_after=3)
                                await msg.delete()
                            else:
                                msg = await message.channel.send(":warning:Lütfen küfür etmeyiniz. <@{}>".format(message.author.id),delete_after=3)
                                await msg.delete()
                        except discord.errors.NotFound:
                            pass
        # REKLAM ENGELLEME
        adblock = sunucu_verileri.get_data(guild,"Adblock")
        if adblock == 1: 
            for flit in ads_filter:
                if flit in lower(message.content):
                    if message.author.guild_permissions.administrator:
                        pass
                    else:
                        try:
                            await message.delete()
                            msg = await message.channel.send( ":warning: Lütfen reklam yapmayınız. :warning: {}".format(message.author.mention),delete_after=3)

                        except discord.errors.NotFound:
                            pass


def setup(bot):
    bot.add_cog(ServerSettings(bot))