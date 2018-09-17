from discord.ext import commands
import discord
import requests
from bs4 import BeautifulSoup
import os
from veriler import sunucu_verileri
from riotwatcher import RiotWatcher


class Oyun:


    def __init__(self,bot):
        self.bot = bot
        self.watcher = RiotWatcher('RIOT API')

    @commands.group(pass_context=True,description="League Of Legends için özel komutlar.")
    async def lol(self,ctx):
        """Örnek : b-lol"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Lol ile ilgili komutları görmek için {}help lol".format(ctx.prefix))


    @lol.command(pass_context=True,description="Şampiyonların counter'larını gösterir.")
    async def counter(self,ctx,*,champname:str):
        """Örnek : b-lol counter Vayne"""
        r = requests.get('http://www.lolcounter.com/champions/'+champname)
        soup = BeautifulSoup(r.content,'html.parser')
        icerik = soup.find(class_='weak-block')
        icerik_items = icerik.find_all('div',attrs={'class':"name"})
        weak = []
        for x in icerik_items:
            weak.append(x.text)
        strong = []
        icerik2 = soup.find(class_='strong-block')
        icerik2_items = icerik2.find_all('div',attrs={'class':'name'})
        for x in icerik2_items:
            strong.append(x.text)
        weakAndstrong = [weak,strong]
        weak = weakAndstrong[0]
        weak_string = ""
        for weak_str in weak:
            weak_string += weak_str +', '
        strong = weakAndstrong[1]
        strong_string = ""
        for strong_str in strong:
            strong_string += strong_str + ', '
        embed = discord.Embed(color=0xad1dfe)
        embed.add_field(name=champname.upper()+" Karşısında Güçlü Olanlar",value=weak_string)
        embed.add_field(name=champname.upper()+" Karşısında Zayıf Olanlar",value=strong_string)
        await ctx.send(embed=embed)


    @lol.command(aliases=["info"],pass_context=True,description="Kullanıcı adını yazdığınız kişinin Lol bilgilerini gösterir.")
    async def bilgi(self,ctx, bolge:str,*, sihirdar_adi:str):
        """Örnek : b-lol bilgi <tr> <SihirdarAdı>"""
        def bolgeler(bolge):
            bolgeler = {
                'tr':'tr1',
                'br':'br1',
                'eune':'eun1',
                'euw':'euw1',
                'jp':'jp1',
                'kr':'kr',
                'lan':'la1',
                'las':'la2',
                'na':'na1',
                'oce':'oc1',
                'ru':'ru1',
                'pbe':'pbe1'
                }
            try:
                return bolgeler[bolge]
            except KeyError:
                return False
        region = bolgeler(bolge)
        if region == False:
            await ctx.send("O isimde bir bölge yok lütfen bölgenizi yazınız. Örnek: b-lol bilgi tr <SihirdarAdı>")
            return
        try:
            me = self.watcher.summoner.by_name(region, sihirdar_adi)
            summonerID = me['id']
            league = self.watcher.league.positions_by_summoner(region, summonerID)
        except requests.HTTPError as err:
            if err.response.status_code == 404:
                await ctx.send(await ctx.send("`{}` sihirdar bulunamadı.".format(sihirdar_adi)))
                return
            elif err.response.status_code == 429:
                await ctx.send("Lütfen daha sonra tekrar deneyiniz.")
                return
            elif err.response.status_code == 404:
                await ctx.send("Veri bulunamadı.")
                return
            elif err.response.status_code == 422:
                await ctx.send("Oyuncu bulundu. Ancak henüz oyun oynamamış.")
                return
            elif err.response.status_code == 422:
                await ctx.send("Oyuncu bulundu. Ancak henüz oyun oynamamış.")    
                return  
        for x in league:
            if x['queueType'] == 'RANKED_SOLO_5x5':
                soloq = league.index(x)
                soloq = league[soloq]
                name = me['name']
                level = me['summonerLevel']
                wins =soloq['wins']
                losses = soloq['losses']
                sums = wins+losses
                rateo = (wins/sums)*100

                embed = discord.Embed(title=name,description="Sihirdarı hakkında bulduklarım.", color=0x00ff00)
                embed.add_field(name='Level',value=level)
                embed.add_field(name='Lig', value=soloq['tier']+' '+soloq['rank'])
                embed.add_field(name='Lig İsmi', value=soloq['leagueName'])
                embed.add_field(name='Lig Puanı', value=soloq['leaguePoints'])
                embed.add_field(name='Toplam Oyun', value=sums)
                embed.add_field(name='Kazanma', value=soloq['wins'])
                embed.add_field(name='Kaybetme', value=soloq['losses'])
                embed.add_field(name='Kazanma Oranı', value="%{0}".format(int(rateo)))

                await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Oyun(bot))