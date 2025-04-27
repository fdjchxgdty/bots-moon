import discord
from discord.ext import commands
import json
import requests
from typing import Optional

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# بيانات السور
with open('surahs.json', 'r', encoding='utf-8') as f:
    surahs = json.load(f)

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} is ready!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="القرآن الكريم"))

@bot.command(name='آية')
async def get_ayah(ctx, surah_num: int, ayah_num: int):
    """الحصول على آية محددة"""
    try:
        surah = next(s for s in surahs if s['number'] == surah_num)
        url = f"http://api.alquran.cloud/v1/ayah/{surah_num}:{ayah_num}/ar.alafasy"
        response = requests.get(url)
        data = response.json()
        
        if data['code'] == 200:
            ayah = data['data']
            embed = discord.Embed(
                title=f"سورة {surah['name']} - الآية {ayah_num}",
                description=ayah['text'],
                color=discord.Color.green()
            )
            embed.set_footer(text="التفسير متوفر باستخدام !تفسير [رقم السورة] [رقم الآية]")
            await ctx.send(embed=embed)
        else:
            await ctx.send("حدث خطأ أثناء جلب الآية. يرجى المحاولة لاحقاً.")
    except:
        await ctx.send("لم يتم العثور على السورة أو الآية المطلوبة. يرجى التأكد من الأرقام.")

@bot.command(name='سورة')
async def get_surah(ctx, surah_num: int):
    """الحصول على معلومات عن سورة"""
    try:
        surah = next(s for s in surahs if s['number'] == surah_num)
        embed = discord.Embed(
            title=f"سورة {surah['name']}",
            description=f"عدد الآيات: {surah['numberOfAyahs']}\nالنوع: {surah['revelationType']}",
            color=discord.Color.blue()
        )
        embed.add_field(name="التفسير المختصر", value=surah['summary'], inline=False)
        await ctx.send(embed=embed)
    except:
        await ctx.send("لم يتم العثور على السورة المطلوبة. يرجى التأكد من الرقم.")

@bot.command(name='تفسير')
async def get_tafsir(ctx, surah_num: int, ayah_num: int):
    """الحصول على تفسير آية"""
    try:
        url = f"http://api.alquran.cloud/v1/ayah/{surah_num}:{ayah_num}/ar.muyassar"
        response = requests.get(url)
        data = response.json()
        
        if data['code'] == 200:
            ayah = data['data']
            embed = discord.Embed(
                title=f"تفسير سورة {surah['name']} - الآية {ayah_num}",
                description=ayah['text'],
                color=discord.Color.gold()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("حدث خطأ أثناء جلب التفسير. يرجى المحاولة لاحقاً.")
    except:
        await ctx.send("لم يتم العثور على التفسير المطلوب.")

@bot.command(name='بحث')
async def search_quran(ctx, *, query: str):
    """البحث في القرآن الكريم"""
    try:
        url = f"http://api.alquran.cloud/v1/search/{query}/ar/all"
        response = requests.get(url)
        data = response.json()
        
        if data['code'] == 200 and data['data']['count'] > 0:
            results = data['data']['matches'][:5]  # إظهار أول 5 نتائج فقط
            embed = discord.Embed(
                title=f"نتائج البحث عن: {query}",
                color=discord.Color.purple()
            )
            
            for result in results:
                surah_name = next(s['name'] for s in surahs if s['number'] == result['surah']['number'])
                embed.add_field(
                    name=f"سورة {surah_name} - الآية {result['numberInSurah']}",
                    value=result['text'],
                    inline=False
                )
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("لم يتم العثور على نتائج للبحث المطلوب.")
    except:
        await ctx.send("حدث خطأ أثناء البحث. يرجى المحاولة لاحقاً.")

bot.run('MTM2NDMzNDkzMTE3MzcwMzczMA.GVJ14F.ErE3w7lwHGxVaqcW3GFx4tUA5Fo_aHjsMFsWLU')
