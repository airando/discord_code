import discord
from discord.ext import commands
import aiohttp
from PIL import Image, ImageDraw,ImageFont
from functools import partial

from io import BytesIO

# 型ヒント用
from typing import Union

class ImageCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        # あとでループを取得できるようにBotへの参照を保持します。
        self.bot = bot

        # アバターの画像データを入手できるようにClientSessionをつくる
        self.session = aiohttp.ClientSession(loop=bot.loop)

    # アバターの画像データをダウンロードする関数
    async def get_avatar(self, user: Union[discord.User, discord.Member]) -> bytes:

        # アバターのPNG形式のURLを取得する
        # アバターの画像は通常1024x1024ですが、保証はされていないので注意しましょう。
        avatar_url = str(user.avatar_url_as(format="png",size=128))

        # リクエストする
        async with self.session.get(avatar_url) as response:
            # レスポンスの内容を読み込む
            avatar_bytes = await response.read()

        return avatar_bytes

    # 画像処理の主要部分
    @staticmethod
    async def processing(avatar_bytes: bytes, colour: dict, member:discord.Member) -> BytesIO:
        def funt(size=20,index=0, encoding='', layout_engine=None):
            return ImageFont.truetype(r"Cogs/japarifont.ttf",size,index=index,encoding=encoding,layout_engine=layout_engine)
        async def get_page(number: int=0):
            params = {'page':number}
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://mee6.xyz/api/plugins/levels/leaderboard/{member.guild.id}") as r:
                    if r.status == 200:
                        return await r.json()
        # BytesIOで画像データをバイトストリームにしてPILでロードする
        # ただのbytesを渡せばなりません
        with Image.open(BytesIO(avatar_bytes)) as im:
          
            # アバターと同じサイズで新しい画像をつくる。
            # colourは画像のデフォルト塗りつぶし色。この場合は、指定したユーザーのメンバーリストに表示する色です。
            with Image.new("RGB",(650, 200),colour) as background:
                back_draw = ImageDraw.Draw(background)
                with Image.new("RGB",(630, 180),0) as backs:
                    _back_draw = backs.convert("RGB")
                    background.paste(_back_draw,(10,10))
                # アバター画像にアルファチャンネルが付いていないことを確かめます。
                rgb_avatar = im.convert("RGB")

                # マスクで使用できる新しい画像をつくる。
                # 0は #000000 や (0, 0, 0) と同じく、塗りつぶし色を黒にします。
                # モードは前と違って、RGB じゃなくて L (グレースケール)です。
                with Image.new("L", im.size,0) as mask:

                    # ImageDraw.Drawは画像に「描く」ためのPILから提供されるクラスです。
                    # こうやって丸・四角・線などを画像に描けます
                    mask_draw = ImageDraw.Draw(mask)
                    avatar_y = int(background.size[1] / 2 - im.size[1] / 2)
                    # Draw.ellipseで(0, 0)から画像の下右に (つまり、画像のサイズに合わせる) 楕円を描きます
                    mask_draw.ellipse(((0,0),im.size), fill=255)

                    # マスクを使用しながらアバターを背景に貼り付ける
                    background.paste(rgb_avatar, (15,avatar_y),mask=mask)
                fnt = funt() 
                back_draw.text((int(im.size[0]/4+15),5),"MEE6",font=fnt)
                fnt = funt(30)
                back_draw.text((int(background.size[0] / 4),30),member.name,font=fnt)
                member_ = None
                for number in int(len(member.guild.members) / 100):
                    page = await get_page(number)
                    if len(page['players']) == 0:break
                    players = [int(c['id']) for c in page['players']]
                    if member.id in players:
                        index = players.index(member.id)
                        member_ = {'rank':index + 1}
                        for k,v in page['players'][index].items():
                            member_[k] = v
                if member_ is not None:
                    back_draw.text((int(background.size[0] / 4),60),member_['rank'],font=fnt,fill=(225,225,0))
                # バイトストリームをつくる
                final_buffer = BytesIO()

                # 画像をPNG形式でストリームに保存する
                background.save(final_buffer, "png")

        # 読み込まれるようにストリーム位置を0に返す
        final_buffer.seek(0)

        return final_buffer

    @commands.command(name="rank")
    async def mee6_rank(self, ctx, *, member: discord.Member = None):
        """アバターを丸にする"""

        # ユーザーが指定されていなかった場合、メッセージを送信したユーザーを使用します。
        member = member or ctx.author

        # 処理をしながら「入力中」を表示する
        async with ctx.typing():
            member_color = member.colour.to_rgb()

            # アバターデータを bytes として取得。
            avatar_bytes = await self.get_avatar(member)

            # partialオブジェクトを作る
            # fnが呼び出されると、avatar_bytesとmember_colorを引数として渡してself.processingを実行するのと同様の動作をします。
            fn = partial(await self.processing, avatar_bytes, member_color,member)

            # executorを使ってfnを別スレッドで実行します。
            # こうやって非同期的に関数が返すまで待つことができます
            # final_bufferはself.processingが返すバイトストリームになります。
            final_buffer = await self.bot.loop.run_in_executor(None, fn)

            # ファイル名「maru.png」の指定とfinal_bufferの内部でファイルを準備して
            file = discord.File(filename="maru.png", fp=final_buffer)

            # 最後にファイルをアップします。
            await ctx.send(file=file)


def setup(bot: commands.Bot):
    bot.add_cog(ImageCog(bot))
