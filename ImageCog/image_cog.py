"""
参考 -> https://gist.github.com/Gorialis/3cbf25ea665b2cebd2f9450e9ab141b9
"""

import discord
from discord.ext import commands
import aiohttp

from PIL import Image, ImageDraw,ImageFont #pip install -U Pillow
from io import BytesIO

import re
import discord
from discord.ext import commands

class MemberConverter(commands.IDConverter):
    async def convert(self, ctx, argument):
        match = self._get_id_match(argument) or re.match(r'<@!?([0-9]+)>$', argument)
        guild = ctx.guild
        if match is None:
            result = guild.get_member_named(argument)
        else:
            user_id = int(match.group(1))
            result = guild.get_member(user_id)
        if result is None:
            result = discord.utils.find(lambda m: argument in m.name, guild.members)
        if result is None:
            result = discord.utils.find(lambda m: m.nick and argument in m.nick, guild.members)
        if result is None:
            result = discord.utils.find(lambda m: argument.lower() in m.name.lower(), guild.members)
        if result is None:
            result = discord.utils.find(lambda m: m.nick and argument.lower() in m.nick.lower(), guild.members)
        return result or ctx.author

class Ranking(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)

    async def get_avatar(self, member: discord.Member) -> bytes:
        avatar_bytes = await member.avatar_url_as(format="png",size=128).read()
        return avatar_bytes

    def get_amount(self,amount):
        if len(str(amount)) >= 6:
           return f"{round(amount / 1000000,1)} M"
        elif len(str(amount)) >= 4:
           return f"{round(amount / 1000,1)} K"
        else:return str(amount)

    async def process_ranks(self,avatar_bytes: bytes, colour: dict, member:discord.Member):
        def funt(size=20,index=0, encoding='', layout_engine=None):
            return ImageFont.truetype(r"Cogs/ImageCog/sea.ttf",size,index=index,encoding=encoding,layout_engine=layout_engine)
        async def get_page(number: int=0):
            params = {'page':number}
            async with self.session.get(f"https://mee6.xyz/api/plugins/levels/leaderboard/{member.guild.id}",params=params) as r:
                if r.status == 200:
                    return await r.json()
        im = Image.open(BytesIO(avatar_bytes))
        background = Image.new("RGB",(650, 200),(0,0,1))
        chara = Image.open("Cogs/ImageCog/splash.png")
        mask = Image.open("Cogs/ImageCog/gradation.png").resize(chara.size).convert("L")
        background.paste(chara.convert("RGB"),(background.size[0]-chara.size[0],0),mask=mask)
        back_draw = ImageDraw.Draw(background)
        back_draw.line(((0,0),(background.size[0],0)),fill=colour,width=10)
        back_draw.line(((0,background.size[1]),background.size),fill=colour,width=10)
        back_draw.line(((0,0),(0,background.size[1])),fill=colour,width=10)
        back_draw.line(((background.size[0],0),background.size),fill=colour,width=10)
        for i in range(3):
            back_draw.line(((background.size[0]/4-i*30-20,0),(0, background.size[0]/4-i*30-20)),fill=colour,width=10)
        rgb_avatar = im.convert("RGB")
        mask = Image.new("L", im.size,0)
        mask_draw = ImageDraw.Draw(mask)
        avatar_y = int(background.size[1] / 2 - im.size[1] / 2)
        mask_draw.ellipse(((0,0),im.size), fill=255)
        background.paste(rgb_avatar, (15,avatar_y),mask=mask)
        fnt = funt() 
        back_draw.text((int(im.size[0]/4+15),5),"MEE6",font=fnt)
        fnt = funt(30)
        back_draw.text((int(background.size[0] / 4),30),member.name,font=fnt)
        if member.bot:
            string = "The user is a bot"
            back_draw.text((int(background.size[0] / 4), 90), string, font=fnt, fill=(225, 225, 0))
            background.save("rank.png")
            return
        if not await get_page(1):
            string = "API has dead!!"
            back_draw.text((int(background.size[0] / 4), 90), string, font=fnt, fill=(225, 225, 0))
            background.save("rank.png")
            return f"https://mee6.xyz/api/plugins/levels/leaderboard/{member.guild.id}"
        member_ = {}
        def get_member(page,players):
            index = players.index(member.id)
            member_['rank'] = index + 100 * number + 1
            for k,v in page['players'][index].items():
                member_[k] = v
        for number in range(int(len([c for c in member.guild.members if not c.bot]) / 100 + 1)+1):
            page = await get_page(number)
            if page is None:break
            if len(page['players']) == 0:break
            players = [int(c['id']) for c in page['players']]
            if member.id in players:
                get_member(page,players)
                break
        if member_:
            rank_string = f"Rank#{member_['rank']} Lv {member_['level']}"
            back_draw.text((int(background.size[0] / 4),70),rank_string,font=fnt,fill=(225,225,0))
            line = Image.new("RGB", (450,25),(128,128,128))
            _exp1,_exp2,_exp3 = member_['detailed_xp']
            exp1 = self.get_amount(_exp1)
            exp2 = self.get_amount(_exp2)
            fnt = funt(25)
            exp_string = f"{exp1} / {exp2}"
            back_draw.text((int((background.size[0]-len(exp_string)*(fnt.size/2))-75),130-fnt.size),exp_string,font=fnt,fill=(225,225,0))
            exp_line = Image.new("RGB", (round((450 /_exp2)*_exp1),25),colour)
            line.paste(exp_line.convert("RGB"),(0,0))
            background.paste(line.convert("RGB"),(int(background.size[0] / 4),135))
        background.save("rank.png")

    @commands.command(name="mee6")
    @commands.cooldown(type=commands.BucketType.user,per=30,rate=1)
    async def mee6_rank(self, ctx, *, member: MemberConverter = None):
        member = member or ctx.author
        async with ctx.typing():
            member_color = member.colour.to_rgb()
            avatar_bytes = await self.get_avatar(member)
            result = await self.process_ranks(avatar_bytes, member_color,member)
            file = discord.File("rank.png")
            await ctx.send(result,file=file)


def setup(bot: commands.Bot):
    bot.add_cog(Ranking(bot))
