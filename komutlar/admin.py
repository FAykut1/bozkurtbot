import discord
from discord.ext import commands
from tools import checks
import random


class Admin:

    def __init__(self,bot):
        self.bot = bot
        self.blockChannels = {}


    @commands.command(aliases=["yasakla"],pass_context=True)
    @checks.is_admin()
    async def ban(self, ctx, member:discord.Member):
        """Örnek : b-ban @Bozkurt"""
        await ctx.guild.ban(member,delete_message_days=7)


    @commands.command(aliases=["at"],pass_context=True)
    @checks.is_admin()
    async def kick(self, ctx, member:discord.Member, *,sebep:str=None):
        """Örnek : b-kick @Bozkurt"""
        await member.kick(reason=sebep)
        embed = discord.Embed(title="Kullanıcı atıldı",description="{}".format(member.mention),color=0x00ff00)
        embed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
        embed = discord.Embed()


    @commands.command(aliases=["clear"],pass_context=True)
    @checks.is_admin()
    async def sil(self,ctx, number:int):
        """Örnek : b-sil 99"""
        if number >= 100:
            await ctx.send("Lütfen aynı anda en fazla 99 mesaj siliniz.")
            return
        channel = ctx.message.channel
        await ctx.message.delete()
        messages = await channel.history(limit=number).flatten()
        try:
            await channel.delete_messages(messages)
        except discord.HTTPException:
            await ctx.send("Silmek istediğiniz mesajlar 14 günü geçtiği için silinemiyor.",delete_after=2)
            return
        await ctx.send(":ballot_box_with_check: {} tane mesaj silindi :ballot_box_with_check:".format(len(messages)),delete_after=2)


    @commands.command(aliases=["mute"],pass_context=True)
    @checks.is_admin()
    async def sustur(self,ctx,user:discord.Member):
        """Örnek : b-sustur @Bozkurt"""
        flag = 0
        for role in ctx.message.guild.roles:
            if role.name == 'Muted':
                await user.add_roles(role)
                embed = discord.Embed(title="Kullanıcı susturuldu!",description="{}".format(user.mention),color=0x00ff00)
                embed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
                await ctx.send(embed=embed)
                flag = 1
        if flag == 0:
            overwrite = discord.PermissionOverwrite(send_messages=False)
            role = await ctx.message.guild.create_role(name='Muted')
            for channel in ctx.message.guild.text_channels:
                await channel.set_permissions(role, overwrite=overwrite)
            embed = discord.Embed(title="Kullanıcı susturuldu!",description="{}".format(user.mention),color=0x00ff00)
            embed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)
            await user.add_roles(role)
    
    
    @commands.command(aliases=["unmute"],pass_context=True)
    @checks.is_admin()
    async def susturma(self,ctx,user:discord.Member):
        """Örnek : b-susturma @Bozkurt"""
        role = discord.utils.get(ctx.message.guild.roles,name='Muted')
        await user.remove_roles(role)
        embed = discord.Embed(title="Kullanıcı artık konuşabilir!",description="{}".format(user.mention),color=0x00ff00)
        await ctx.send(embed=embed)


    @commands.command(aliases=["announce"],pass_context=True)
    @checks.is_admin()
    async def duyuru(self,ctx,kanal:discord.TextChannel,*,mesaj:str):
        """Örnek : b-duyuru #duyurukanalı @everyone YAPILACAKDUYURU"""
        embed = discord.Embed(title="DUYURU!",color=0xffffff)
        embed.add_field(name=ctx.message.author.name,value=mesaj+"@everyone")
        await kanal.send(embed=embed)


    @commands.command(aliases=["raffle"],pass_context=True)
    @checks.is_admin()
    async def çekiliş(self,ctx,*,mesaj:str):
        """Örnek : b-çekiliş (Çekiliş Mesajı)"""
        users = []
        try:
            for user in ctx.message.guild.members:
                if user.status != discord.Status.offline:
                    users.append(user)
        except IndexError:
            pass
        sayi = random.randint(1,len(users))
        embed = discord.Embed(title="{} Çekilişinin Kazananı".format(mesaj),description="<@{0.id}>".format(users[sayi]),color=0x010470)
        kazanan = users[sayi]
        embed.set_thumbnail(url=kazanan.avatar_url)
        await ctx.send(embed=embed)


    @commands.group(pass_context=True)
    @checks.is_admin()
    async def rol(self, ctx):
        """Örnek : b-help rol yazarak komutları görebilirsiniz."""
        if ctx.invoked_subcommand is None:
            await ctx.send("Rol'le ilgili komutları görmek için {}help rol".format(ctx.prefix))


    @rol.command(name="sil",pass_context=True)
    async def _delete_Role(self, ctx, roles:discord.Role):
        """Örnek : b-rol sil @rol"""
        role = roles
        try:
            await ctx.send("{} isimli rol silindi!".format(role))
            await role.role_delete()
        except discord.Forbidden:
            await ctx.send("Bu komutu kullanmak için bana yetki vermelisin.")

    
    @rol.command(name="ekle",pass_context=True,description="Kullanıcıya rol ekleyebilirsiniz.")
    async def _add_role(self,ctx,member:discord.Member,roles:discord.Role):
        """Örnek : b-rol ekle @Kullanıcı @EklenecekRol"""
        try:
            await member.add_roles(roles)
            await ctx.send("`{}` Rolünü {} kullanıcısına eklediniz.".format(roles.name,member.mention))
        except discord.Forbidden:
            await ctx.send("Bu komutu kullanmak için bana yetki vermelisin.")


    @rol.command(name="çıkar",pass_context=True,description="Kullanıcının rolünü çıkarabilirsiniz.")
    async def role_remove(self,ctx,member:discord.Member,roles:discord.Role):
        """Örnek : b-rol çıkar @Kullanıcı @ÇıkarılacakRol"""
        try:
            await member.remove_roles(roles)
            await ctx.send("`{}` Rolünü {} kullanıcısından çıkardınız.".format(roles.name,member.mention))
        except discord.Forbidden:
            await ctx.send("Bu komutu kullanmak için bana yetki vermelisin.")
            



def setup(bot):
    bot.add_cog(Admin(bot))