import discord
from discord.ext import commands
import random
from datetime import datetime
from veriler import kullanici_verileri,sunucu_verileri
import asyncio


class Kullanici:
    def __init__(self,bot):
        self.bot = bot
        

    @commands.command(pass_context=True)
    async def pf(self,ctx,user:discord.Member):
        """Örnek : b-pf @Bozkurt"""
        embed=discord.Embed(title="{} kişisinin profil fotoğrafı".format(user.name))
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)


    @commands.command(aliases=["userinfo"],pass_context=True)
    async def bilgi(self,ctx,user:discord.Member):
        """Örnek : b-bilgi @Bozkurt"""
        status = user.status
        guild = ctx.message.guild
        if status == discord.Status.online:
            status='Çevrimiçi'
        elif status == discord.Status.idle:
            status='Boşta'
        elif status == discord.Status.dnd:
            status='Rahatsız Etmeyin'
        ovgu = kullanici_verileri.get_user_data(user,guild,"praise")
        if ovgu == None:
            ovgu=0
        joinedAt = str(user.joined_at.day)+"/"+str(user.joined_at.month)+"/"+str(user.joined_at.year)
        createdAt = str(user.created_at.day) + "/" + str(user.created_at.month) + "/" + str(user.created_at.year)
        embed = discord.Embed(title=user.name,description="Bunları buldum reis.",color=0x00ff00)
        embed.add_field(name="İsim",value=user.name)
        embed.add_field(name="ID", value=user.id)
        embed.add_field(name="Durum", value=status)
        embed.add_field(name="Rol", value=user.top_role)
        embed.add_field(name="Övgü", value=ovgu)
        embed.add_field(name="Sunucuya Katılma Tarihi",value=joinedAt)
        embed.add_field(name="Discord'a Katılma Tarihi",value=createdAt)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)


    @commands.command(aliases=["number"],pass_context=True)
    async def sayı(self,ctx,number1:int,number2:int):
        """Örnek : b-sayı 1 100"""
        sayi = random.randint(number1,number2)
        await ctx.send("Tuttuğum sayı {}".format(sayi))


    @commands.command(aliases=["tell","say"],pass_context=True)
    async def söyle(self,ctx,*,say:str):
        await ctx.send(say)



    @commands.command(aliases=["praise"],pass_context=True)
    async def öv(self,ctx,user:discord.Member):
        """Örnek : b-öv @Bozkurt"""
        author = ctx.message.author
        guild = ctx.message.guild
        praiseusers = kullanici_verileri.get_user_data(user,guild,"praiseUsers")
        userPraise = kullanici_verileri.get_user_data(user,guild,"praise")
        if praiseusers != None:  
            if str(author.id) in praiseusers:
                await ctx.send("Bu kişiyi zaten övmüşsünüz.")
            else:
                if userPraise == None:
                    kullanici_verileri.add_user_data(user,guild,"praise",1)
                else:
                    kullanici_verileri.add_user_data(user,guild,"praise",userPraise+1)
                kullanici_verileri.add_list_user_data(user,guild,"praiseUsers",str(author.id))
                await ctx.send("<@{}> için 1 övgü de <@{}> attı.".format(user.id,ctx.message.author.id))    
        else:
            if userPraise == None:
                kullanici_verileri.add_user_data(user,guild,"praise",1)
            else:
                kullanici_verileri.add_user_data(user,guild,"praise",userPraise+1)
            kullanici_verileri.add_list_user_data(user,guild,"praiseUsers",str(author.id))
            await ctx.send("<@{}> için 1 övgü de <@{}> attı.".format(user.id,ctx.message.author.id))    


    @commands.command()
    async def sunucuöv(self,ctx):
        """Örnek : b-sunucuöv"""
        author = ctx.message.author
        guild = ctx.message.guild
        praiseusers = sunucu_verileri.get_data(guild, "praiseUsers")
        userPraise = sunucu_verileri.get_data(guild, "praise")
        if praiseusers != None:  
            if author.id in praiseusers:
                await ctx.send("Bu sunucuyu zaten övmüşsünüz.")
            else:
                if userPraise == None:
                    sunucu_verileri.add_data(guild,"praise",1)
                else:
                    sunucu_verileri.add_data(guild,"praise",userPraise+1)
                sunucu_verileri.add_list_data(guild,"praiseUsers",author.id)
                await ctx.send("{0.name} sunucusu için 1 övgü de {1.mention} attı.".format(guild,author))    
        else:
            if userPraise == None:
                sunucu_verileri.add_data(guild,"praise",1)
            else:
                sunucu_verileri.add_data(guild,"praise",userPraise+1)
            sunucu_verileri.add_list_data(guild,"praiseUsers",author.id)
            await ctx.send("{0.name} sunucusu için 1 övgü de {1.mention} attı.".format(guild,author))


    @commands.command(aliases=["mypraise"],pass_context=True)
    async def övgülerim(self,ctx):
        """Örnek : b-övgülerim"""
        author = ctx.message.author
        guild = ctx.message.guild
        ovgu = kullanici_verileri.get_user_data(author,guild,"praise")
        if ovgu == None:
            ovgu = 0
        embed=discord.Embed(title="{}".format(author.name),description="Övgü Puanı: "+str(ovgu),color=0x00ff00)
        await ctx.send(embed=embed)
        

    @commands.command(pass_context=True)
    async def afk(self,ctx,*,reason:str):
        """Örnek : b-afk Oturuyor"""
        user = ctx.message.author
        guild = ctx.message.guild
        kullanici_verileri.add_user_data(user,guild,"afkDesc",reason)
        await ctx.send("Şuanda `{}` sebebiyle afksınız. {}".format(reason,user.mention))


    @commands.command(aliases=["deafk"],pass_context=True)
    async def afkdeğilim(self,ctx):
        """Örnek : b-afkdeğilim"""
        guild = ctx.message.guild
        user = ctx.message.author
        kullanici_verileri.add_user_data(user,guild,"afkDesc",'0')
        await ctx.send("{} artık afk değilsin.".format(user.mention))


    async def on_message(self,message):
        user = message.author
        if user.bot:
            return 
        if not message.guild:
            return 
        if message.content.startswith("prefix"): # prefix'inizi girin.
            return 
        # Kullanıcının guild kaydını kontrol eder yoksa ekler!
        try:
            kullanici_verileri.add_user_server_data(user,message.guild)
        except AttributeError:
            pass
        # Afk etiketlendiğinde atılacak mesaj.
        if "@" in message.content:
            for randomUser in message.guild.members:
                if randomUser.mentioned_in(message):
                    afkMesaji = kullanici_verileri.get_user_data(randomUser,message.guild,"afkDesc")
                    if afkMesaji != None and afkMesaji != '0':
                        emb = discord.Embed(title="Şuanda kendisi afk size şu mesajı bıraktı",description='`'+randomUser.name+'`'+" : "+'`'+str(afkMesaji)+'`',colour=0x002492)
                        try:
                            await message.channel.send(embed=emb)
                        except discord.errors.Forbidden:
                            pass


def setup(bot):
    bot.add_cog(Kullanici(bot))
