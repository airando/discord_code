"""
参考 -> https://gist.github.com/Gorialis/3cbf25ea665b2cebd2f9450e9ab141b9
"""

import discord
from discord.ext import commands
import aiohttp
from PIL import Image, ImageDraw,ImageFont #pip install -U Pillow
from io import BytesIO

class ImageCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.member_ = None
        self.session = aiohttp.ClientSession(loop=bot.loop)

    async def get_avatar(self, member: discord.Member) -> bytes:
        avatar_url = str(member.avatar_url_as(format="png",size=128))
        async with self.session.get(avatar_url) as response:
            avatar_bytes = await response.read()

        return avatar_bytes

    async def process_ranks(self,avatar_bytes: bytes, colour: dict, member:discord.Member) -> BytesIO:
        def funt(size=20,index=0, encoding='', layout_engine=None):
            return ImageFont.truetype(r"Cogs/japarifont.ttf",size,index=index,encoding=encoding,layout_engine=layout_engine)
        async def get_page(number: int=0):
            params = {'page':number}
            async with self.session.get(f"https://mee6.xyz/api/plugins/levels/leaderboard/{member.guild.id}",params=params) as r:
                if r.status == 200:
                    return await r.json()
        im = Image.open(BytesIO(avatar_bytes))
        background = Image.new("RGB",(650, 200),colour)
        back_draw = ImageDraw.Draw(background)
        backs = Image.new("RGB",(630, 180),0)
        _back_draw = backs.convert("RGB")
        background.paste(_back_draw,(10,10))
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
        member_ = None
        for number in range(int(len(member.guild.members) / 100 + 1)+1):
            page = await get_page(number)
            if len(page['players']) == 0:break
            players = [int(c['id']) for c in page['players']]
            if member.id in players:
                index = players.index(member.id)
                member_ = {}
                member_['rank'] = index + 100 * number + 1
                for k,v in page['players'][index].items():
                    member_[k] = v
                break
        if member_:
            back_draw.text((int(background.size[0] / 4),70),f"Rank#{member_['rank']}",font=fnt,fill=(225,225,0))
            
        background.save("rank.png")

    @commands.command(name="rank")
    async def mee6_rank(self, ctx, *, member: discord.Member = None):

        member = member or ctx.author
        async with ctx.typing():
            member_color = member.colour.to_rgb()
            avatar_bytes = await self.get_avatar(member)

            await self.process_ranks(avatar_bytes, member_color,member)
            file = discord.File("rank.png")
            await ctx.send(file=file)


def setup(bot: commands.Bot):
    bot.add_cog(ImageCog(bot))
