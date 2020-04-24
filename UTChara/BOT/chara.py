from discord.ext import commands,tasks
import discord
import ast
import datetime
import aiohttp
import re
import time
import asyncio
import random
import json
import Jinro.game as JinroGame

bot = commands.Bot(command_prefix="cs!",activety=discord.Game(name="きゃらちゃんのサーバー専属BOT"),help_command=None)

guilds = [648103908170006529,663967989187477506]
souls = ["決意","忍耐","勇気","誠実","不屈","正義","親切"]

f = open(r'Jinro/jinro_roles.json', 'r', encoding='utf-8')
jinro_json = json.load(f)

owners = [539787492711464960]
subowners = [508919483440693294,460208854362357770,561000119495819290]
hidden = [605188331642421272,691549557393326080]
operators = [690527190890053642,584008752005513216,404243934210949120,631786733511376916]
moderators = [491418194762792961,604872732961669120,421971957081309194,586157827400400907,475496066419130368]

def permission_owner():
    return owners
def permission_subowner():
    list_ = []
    [list_.append(c) for c in permission_owner()]
    [list_.append(c) for c in subowners]
    return list_
def permission_hidden():
    list_ = []
    [list_.append(c) for c in permission_subowner()]
    [list_.append(c) for c in hidden]
    return list_
def permission_operator():
    list_ = []
    [list_.append(c) for c in permission_hidden()]
    [list_.append(c) for c in operators]
    return list_
def permission_moderator():
    list_ = []
    [list_.append(c) for c in permission_operator()]
    [list_.append(c) for c in moderators]
    return list_

def is_owner():
    def predicate(ctx):
        return ctx.author.id in permission_owner()
    return commands.check(predicate)

def is_subowner():
    def predicate(ctx):
        return ctx.author.id in permission_subowner()
    return commands.check(predicate)

def is_hidden():
    def predicate(ctx):
        return ctx.author.id in permission_hidden()
    return commands.check(predicate)
        
def is_operator():
    def predicate(ctx):
        return ctx.author.id in permission_operator()
    return commands.check(predicate)

def is_moderator():
    def predicate(ctx):
        return ctx.author.id in permission_moderator()
    return commands.check(predicate)

@bot.event
async def on_ready():
    bot.load_extension("jishaku")
    print("------------------------")
    print('ログイン完了')
    print('verson 1.7.1')
    print(bot.user.name)
    print(bot.user.id)
    print('------------------------')
    game = discord.Game(f"prefix cs!|verson 1.7.1|heroku起動")
    await bot.change_presence(status=discord.Status.idle, activity=game)
    JinroGame.setup(bot)
    loop.start()
    looop.start()

@bot.command()
async def help(ctx):
    embed = discord.Embed(title=f"**{bot.user.name}のこまんど**",
    color=0xffff00)
    embed.add_field(name="何かわからないのかい", value="コマンド一覧", inline=False)
    embed.add_field(name="**help**", value="いまのやつ", inline=False)
    embed.add_field(name="**info**", value="**BOTの説明的な？**", inline=False)
    embed.add_field(name="**admin**", value="運営一覧", inline=False)
    embed.add_field(name="**admin commands**", value="admin command一覧", inline=False)
    embed.add_field(name="**support**", value="チャンネルサポートコマンドの一覧が表示されます", inline=False)
    embed.add_field(name="**kick**", value="**cs!kick [ID or MENTION] [reason]**\nキック権限有する", inline=False)
    embed.add_field(name="**ban**", value="**cs!ban [ID or MENTION] [reason]**\nBAN権限有する", inline=False)
    embed.add_field(name="**unban**", value="**cs!unban [ID or MENTION] [reason]**\nBAN権限有する", inline=False)
    embed.add_field(name="**apurge**", value="**全部メッセージ消します。**\n管理者権限有する", inline=False)
    embed.add_field(name="**purge**", value="**cs!purge [int]**\nメッセージ管理権限有する", inline=False)
    embed.add_field(name="**soul**", value="貴様のソウルを私自ら直々に判定してやる、《決意,忍耐,勇気,誠実,不屈,親切,正義》のロールを必ず作ってください", inline=False)
    embed.add_field(name="**soul2**", value="決意を抱け", inline=False)
    embed.add_field(name="**soul-reset**", value="ソウル役職を全メンバーから剥奪します\n鯖所有権あればいけます", inline=False)
    embed.add_field(name="**ping**", value="BOTの速さを計ります", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def about(ctx):
    embed = discord.Embed(title=f"**BOTの概要**",color=0xffff00)
    embed.add_field(name="**これは**", value="**専属BOTです**", inline=False)
    embed.add_field(name="**ログ**", value="**入退室ログは公式サーバーおよび公式サーバー2ndのみ有効**", inline=False)
    embed.add_field(name="**ほかのサーバーで使うには**", value="**運営のオーナーに連絡を**", inline=False)
    embed.add_field(name="**運営**", value="**cs!adminで表示されます**", inline=False)
    await ctx.send(embed=embed)

@bot.group()
async def admin(ctx):
    if ctx.invoked_subcommand:return
    owner = [bot.get_user(c) for c in owners]
    subowner = [bot.get_user(c) for c in subowners]
    operator = [bot.get_user(c) for c in operators]
    moderator = [bot.get_user(c) for c in moderators]
    des = "**__OWNER__**\n" + '\n'.join(f'{c} ({c.id})' for c in owner)
    des += "\n\n**__SUB OWNER__**\n" + '\n'.join(f'{c} ({c.id})' for c in subowner)
    des += "\n\n**__OPERATOR__**\n" + '\n'.join(f'{c} ({c.id})' for c in operator)
    des += "\n\n**__MODERATORS__**\n" + '\n'.join(f'{c} ({c.id})' for c in moderator)
    embed = discord.Embed(title="運営一覧",description=des,color=0xffff00)
    await ctx.send(embed=embed)

@admin.command(name="commands")
async def admin_cmd(ctx):
    ok = bot.get_emoji(654634589444374529)
    no = bot.get_emoji(655358129391009812)
    des = f"{ok}...使用可能\n{no}...使用不可能"
    def check(role):
        inv = {'owner':permission_owner(),'subowner':permission_subowner(),'hidden':hidden,
                'operator':permission_operator(),'moderator':permission_moderator(),'id':ctx.author.id,
                }
        if eval(f"id in {role} and not id in hidden",inv):return ok
        else:return no
    embed = discord.Embed(title=f"**{bot.user.name}運営専用こまんど**,c=charaです",description=des,color=0xffff00)
    embed.add_field(name="**capurge**", value=f"{check('operator')}**メッセージ全部消える\nOPERATOR以上**", inline=False)
    embed.add_field(name="**cpurge**", value=f"{check('moderator')}**cs!cpurge [int]\nMODERATOR以上**", inline=False)
    embed.add_field(name="**say**", value=f"{check('moderator')}**cs!say [しゃべらせたい文]\nMODERATOR以上**", inline=False)
    embed.add_field(name="**ckick**", value=f"{check('moderator')}**cs!ckick [ID or MENTION] [reason]**\n**MODERATOR以上が可能**", inline=False)
    embed.add_field(name="**cban**", value=f"{check('operator')}**cs!cban [ID or MENTION] [reason]**\n**OPERATOR以上**", inline=False)
    embed.add_field(name="**cunban**", value=f"{check('operator')}**cs!cunban [ID or MENTION] [reason]**\n**OPERATOR以上**", inline=False)
    embed.add_field(name="**eval**", value=f"{check('subowner')}**コードを評価します\nSUB OWNER以上が使用可能**", inline=False)
    embed.add_field(name="**csoul-reset**", value=f"{check('subowner')}**ソウル役職を全メンバーから剥奪します\nSUB OWNER以上**", inline=False)
    embed.add_field(name="**jsk**", value=f"{check('owner')}**jishakuを実行します(BOT OWNER限定)**", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"**このBOTについて**",
    color=0xffff00)
    embed.set_thumbnail(url=ctx.bot.user.avatar_url_as(static_format="png"))
    embed.add_field(name="**Prefix**", value="**cs!**", inline=False)
    embed.add_field(name="バージョン", value="**ver 1.7.1**", inline=False)
    embed.add_field(name="更新内容", value="**ADMINコマンド作成、コマンドを全サーバー使用可**", inline=False)
    embed.add_field(name="次の更新内容", value="**人狼ゲーム作るってどっかの誰かが言ってた**", inline=False)
    embed.add_field(name="作成者", value="<@!539787492711464960>", inline=False)
    embed.add_field(name="サポーター", value="みんな！", inline=False)
    embed.add_field(name="使用言語", value="**Python**", inline=False)
    embed.add_field(name="最後に", value="専属BOTだ、以後お見知りおきを", inline=False)
    await ctx.send(embed=embed)

@bot.group()
async def support(ctx):
    if ctx.invoked_subcommand:return
    embed = discord.Embed(title=f"**なにがわからないのかな\n例cs!support boost**",color=0xffff00)
    embed.add_field(name="**boost**", value="**ブーストするとどうなるの?**", inline=False)
    embed.add_field(name="**legend**", value="**LEGENDARY MEMBERってなんや**", inline=False)
    embed.add_field(name="**second**", value="**セカンドサーバーってなに**", inline=False)
    embed.add_field(name="**event**", value="**イベントはどうすれば参加できるの?**", inline=False)
    embed.add_field(name="**partner**", value="**サーバー提携するには？**", inline=False)
    embed.add_field(name="**global**", value="**グローバルチャットって何？**", inline=False)
    await ctx.send(embed=embed)

@support.command()
async def boost(ctx):
    embed = discord.Embed(title=f"**Boost**", color=0xffff00)
    embed.add_field(name="ブーストするとどうなるの?", value="ブーストをしたらブーストした回数xAvaire経験値10000もらえます。ランキングが有利になりますよ", inline=False)
    await ctx.send(embed=embed)

@support.command()
async def legend(ctx):
    embed = discord.Embed(title=f"**Legend**",color=0xffff00)
    embed.add_field(name="**LEGENDARY MEMBER**って?", value="レジェメンは特別な人に贈られます。サーバーに凄い貢献してる人とか。ほしかったら頑張ってね！", inline=False)
    await ctx.send(embed=embed)

@support.command()
async def second(ctx):
    embed = discord.Embed(title=f"**second**",color=0xffff00)
    embed.add_field(name="セカンドサーバーとは", value="メインサーバーとは別にある鯖です。統合雑談とセカンドの雑談はリンクしています。", inline=False)
    await ctx.send(embed=embed)

@support.command()
async def event(ctx):
    embed = discord.Embed(title=f"**Event**",color=0xffff00)
    embed.add_field(name="イベントはいつ開催されるの？", value="イベントは唐突に開かれて唐突に終わります。機会を逃さないようにお知らせ通知をONにしておこう！", inline=False)
    await ctx.send(embed=embed)

@support.command()
async def partner(ctx):
    embed = discord.Embed(title=f"**Partner**",color=0xffff00)
    embed.add_field(name="パートナー提携はどうしたらできるの", value="パートナー提携するには条件があり鯖人数がBOTを抜かして500人いること、鯖作成から3か月たっていることです、TAO-Partnerはそれにくわえて一番高いチャンネルのレベルが10万をこえていることです", inline=False)
    await ctx.send(embed=embed)

@support.command(name="global")
async def global_(ctx):
    embed = discord.Embed(title=f"**Global**",color=0xffff00)
    embed.add_field(name="グローバルチャットって何？", value="グローバルチャットとは\nパブリックチャットと呼ばれており様々なサーバーのユーザーと雑談を共有することができます。\nそのため参加の際にはほかのサーバーに失礼のないようお願いします。", inline=False)
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(context, exception):
    if isinstance(exception, commands.CommandNotFound):
        e = discord.Embed(title="おや？", description="コマンドが違うらしいな・・・\n`cs!help`でかくにんしてみてはどうだろうか", color=0xffff00)
        await context.send(embed=e)
    elif isinstance(exception, commands.CommandOnCooldown):
        e = discord.Embed(description=f"クールダウンだよ。**{int(exception.retry_after*100)/100}s**待ってね",color=0xffff00)
        await context.send(embed=e)
    elif isinstance(exception, commands.CheckFailure):
        e = discord.Embed(description="君はこのコマンドを使用できないようだ", color=0xffff00)
        await context.send(embed=e)
    elif isinstance(exception, commands.MissingRequiredArgument):
        e = discord.Embed(description="パラメータが足りてないようだよ。", color=0xffff00)
        await context.send(embed=e)
    else:
        embed = discord.Embed(title='予期しないエラーが発生しました！',description=f"```py\n{exception}```",color=0xFFFF00)
        embed.add_field(name="Class",value=f"{exception.__class__}")
        await context.send(embed=embed)

@bot.command()
async def purge(ctx,limit):
    if ctx.author.guild_permissions.manage_messages is True:
        await ctx.channel.purge(limit=int(limit))
    else:
        m = discord.Embed(title="だれ？", description=f"おまえだれだ", color=0xffff00)
        await ctx.send(embed=m)

@bot.command()
async def apurge(ctx):
    if ctx.author.guild_permissions.administrator is True:
        await ctx.send("メッセージ決意...")
        await ctx.channel.purge(limit=None)
    else:
        m = discord.Embed(title="だれ？", description=f"おまえだれだ", color=0xffff00)
        await ctx.send(embed=m)

@bot.command()
async def kick(ctx, member:discord.Member=None, reason=None):
    if ctx.author.guild_permissions.kick_members is True:
        await ctx.guild.kick(member, reason=reason)
        l = discord.Embed(title="ユーザーが追放されました！ / User has Sayonara!!", description=f"実行者：{ctx.author.name}\n{member.mention} を追放した。\n理由：{reason}", color=0xffff00)
        await ctx.send(embed=l)
    else:
        m = discord.Embed(title="だれ？", description=f"おまえだれだ", color=0xffff00)
        await ctx.send(embed=m)

@bot.command()
async def ban(ctx, user:discord.User=None, reason=None):
    if ctx.author.guild_permissions.ban_members is True:
        await ctx.guild.ban(user, reason=reason)
        l = discord.Embed(title="ユーザーが死にました！ / User has dead!!", description=f"実行者：{ctx.author.name}\n{user.mention} を決意した。\n理由：{reason}", color=0xffff00)
        await ctx.send(embed=l)
    else:
        m = discord.Embed(title="だれ？", description=f"おまえだれだ", color=0xffff00)
        await ctx.send(embed=m)

@bot.command()
async def unban(ctx, user:discord.User=None, reason=None):
    if ctx.author.guild_permissions.ban_members is True:
        await ctx.guild.unban(user, reason=reason)
        l = discord.Embed(title="ユーザーが復活しました！ / User is back!!", description=f"実行者：{ctx.author.name}\n{user.mention} が決意を抱いた。\n理由：{reason}", color=0xffff00)
        await ctx.send(embed=l)
    else:
        m = discord.Embed(title="だれ？", description=f"おまえだれだ", color=0xffff00)
        await ctx.send(embed=m)

async def DeadGetEmbed(member):
    des = f"{member}さん...なんで...\nこんなことになるなんて..."
    des += "まさか死ぬとは思わないじゃないか...さよなら...ｶﾜｲｿ"
    embed = discord.Embed(title="ユーザーが死にました！ / User has dead!!", description=des, color=0xffff00)
    embed.set_footer(text=f"只今の生存数:{len(member.guild.members)}")
    return embed

async def JoinGetEmbed(member):
    if member.guild.id == 648103908170006529:
        second = ""
        rule = bot.get_channel(659936250391822346)
        roles = bot.get_channel(659936254338531341)
    elif member.guild.id == 663967989187477506:
        second = "2nd "
        rule = bot.get_channel(692342312381972490)
        roles = bot.get_channel(692342336033783838)
    else:return discord.Embed()
    des = f"{member} さん！ようこそきゃらちゃんの部屋‼＠公式サーバー {second}へ！\n"
    des += f"{rule.mention}でしっかりルールの確認をしましょう！\n"
    des += f"また{roles.mention}で必要な役職を受け取りましょう！\n"
    des += f"よかったらコマンド部屋で`cs!soul`ってうってみてね！"
    embed = discord.Embed(title="ユーザーが参加しました！ / User has Joined!", description=des, color=0xffff00)
    embed.set_footer(text=f"只今の人数:{len(member.guild.members)}")
    return embed

async def OtherGetEmbed(member,join=True):
    if isinstance(member,discord.Member):
        if join is True:
            title = "ユーザーが参加しました！ / User has Joined!"
            des = f"[{chr(129351 + guilds.index(member.guild.id))}]{member} さんが"
            des += f"[{member.guild.name}](https://discordapp.com/channels/{member.guild.id}/{discord.utils.get(await member.guild.webhooks(),name='SyncChat').channel.id})"
            des += "に参加しました！"
            text = "Welcome to Chara’s Server!!"
        else:
            title = "ユーザーが死にました！ / User has dead!!"
            des = f"[{chr(129351 + guilds.index(member.guild.id))}]{member} さんが"
            des += f"[{member.guild.name}](https://discordapp.com/channels/{member.guild.id}/{discord.utils.get(await member.guild.webhooks(),name='SyncChat').channel.id})"
            des += "で死にました！"
            text = discord.Embed.Empty
        embed = discord.Embed(title=title,description=des,color=0x0088FF)
        embed.set_footer(text=text)
        return embed

async def UserGetProfile(member):
    embed = discord.Embed(color=discord.utils.get(member.guild.roles,name="MEMBER").color)
    embed.set_author(name="User Info")
    if member.is_avatar_animated():embed.set_thumbnail(url=member.avatar_url)
    else:embed.set_thumbnail(url=member.avatar_url_as(format='png'))
    embed.add_field(name="Name",value=str(member))
    embed.add_field(name="ID",value=str(member.id))
    embed.add_field(name="Bot",value=str(member.bot))
    embed.add_field(name="Status",value=str(member.status),inline=False)
    if member.activities:
        embed.add_field(name=f"Activities({len(member.activities)})",value="\n".join(c.name for c in member.activities))
    else:embed.add_field(name="Activities(0)",value="None")
    return embed

@bot.event
async def on_member_join(member):
    webhook = discord.utils.get(await member.guild.webhooks(),name="SyncChat")
    if webhook is None:return
    def get_role(name):
        return discord.utils.get(member.guild.roles,name=name)
    if member.bot:
        await member.add_roles(get_role("BOT"))
    else:
        if get_role("人狼ゲーム"):await member.add_roles(get_role("人狼ゲーム"))
        await member.add_roles(get_role("お知らせ通知ON"),get_role("MEMBER"))
        if member.guild.id == 648103908170006529:second = ""
        else:second = "2nd "
        des = f"こんにちは！きゃらちゃんの部屋＠公式サーバー!! {second}の専属BOTです！\n"
        des += f"この度はきゃらちゃんの部屋@公式サーバー!! {second}に参加していただきありがとうございます！\n"
        des += "ゆっくりしていってください！！\n何かわからないときはどうぞ！\n"
        des += f"{bot.get_user(539787492711464960)}\n||即抜けは悲しい...||"
        embed = discord.Embed(title="ようこそ きゃらちゃんの部屋@公式サーバー!!へ！ / Welcome to Chara‘s Server!!",description=des, color=0xffff00)
        embed.set_footer(text="Welcome to Chara’s Server!!")
        await member.send(embed=embed)
        for guild in bot.guilds:
            webhook = discord.utils.get(await guild.webhooks(),name="SyncChat")
            if webhook is not None:
                if guild.id == member.guild.id:embeds = [await JoinGetEmbed(member),await UserGetProfile(member)]
                else:embeds = [await OtherGetEmbed(member)]
                await webhook.send(username="[♾️] System Message",avatar_url="https://bit.ly/2QLUbaM",embeds=embeds)

@bot.event
async def on_member_remove(member):
    webhook = discord.utils.get(await member.guild.webhooks(),name="SyncChat")
    if webhook is None:return
    for guild in bot.guilds:
        webhook = discord.utils.get(await guild.webhooks(),name="SyncChat")
        if webhook is not None:
            if guild.id == member.guild.id:embeds = [await DeadGetEmbed(member),await UserGetProfile(member)]
            else:embeds = [await OtherGetEmbed(member,join=False)]
            await webhook.send(username="[♾️] System Message",avatar_url="https://bit.ly/2QLUbaM",embeds=embeds)

no, ok = '👎', '👍'

def predicate(message, author, bot):
    def check(reaction, users):
        if reaction.message.id != message.id or users == bot.user or author != users:
            return False
        if reaction.emoji == ok or reaction.emoji == no:
            return True
        return False
    return check

@bot.command()
@commands.cooldown(type=commands.BucketType.user,per=30,rate=1)
async def soul(ctx):
    author = ctx.author
    reactions = [chr(127462 + i) for i in range(1)]
    role_list = [discord.utils.get(ctx.guild.roles,name=role) for role in souls[1:]]
    if [c for c in ctx.author.roles if c in role_list]:
        return await ctx.send(embed=discord.Embed(description=f"Chara「また{ctx.author.mention}か、きみはソウルを判定してもらったはずだ。\n\nそれともそのソウルが不満か？\n\n私に会いにきた？\n\nそ、そんなこと言って...\n\nべ、別に嬉しいわけじゃないぞ！決意なんか絶対あげないからな！\n\nさっさと消えな！！」", color=0xffff00))
    else:
        e = discord.Embed(description=f"Chara「ほう、{ctx.author.mention}のソウルが何かわからない。そしてソウルを知りたい。\n\nならば私が判定してやろう,一回判定したら次はないぞ。それでもいいなら進め。\n\n貴様のソウルはいずれかのものになるはずだ。\n\n忍耐,勇気,誠実,不屈,親切,正義\n決意はないぞ、私だけのものだ。\nでは貴様のソウルを判定してやる。\n希望のソウルにならなくても怒るんじゃないぞ。」", color=0xffff00)
        msg = await ctx.send(embed=e)
        [await msg.add_reaction(c) for c in [no, ok]]
        try:
            reaction, user = await bot.wait_for("reaction_add", check=predicate(msg, author, bot), timeout=20)
        except ValueError:
            return
        else:
            if reaction.emoji == no:
                e = discord.Embed(description=f"Chara「{ctx.author.mention}そうか、ソウルはわからないままでいいのだな。\n\nそれもいいだろう。またきたまえ。」", color=0xffff00)
                return await ctx.send(embed=e)
            e = discord.Embed(description=f"Chara「{ctx.author.mention}5秒ほどまちな,すぐに貴様のソウルを特定してやろう。\n\n別に貴様のためにやってるわけじゃない,貴様に頼まれたからやっているのだ。\n\n決してそこは勘違いするんじゃない。」", color=0xffff00)
            await ctx.send(embed=e)
            await asyncio.sleep(5)
            r = random.choice(role_list[:-1])
            await author.add_roles(r)
            msg = await ctx.send(embed=discord.Embed(description=f"Chara「{ctx.author.mention}のソウルは\n{r.mention}みたいだな。\n\n自分のソウルがしれてよかったな。\n\n次このコマンドを使っても意味はないぞ。\n\n\nでは、ごきげんよう」", color=0xffff00))
            [await msg.add_reaction(c) for c in reactions]
            def check(r,u):
                if u == ctx.author and r.emoji in reactions and r.message.id == msg.id:return True
                return False
            try:
                reaction,user = await bot.wait_for("reaction_add",check=check,timeout=20)
            except asyncio.TimeoutError:return
            else:
                if reaction.emoji == reactions[0]:
                    content = [f"[`{i+1}`] {m.mention}" for i,m in zip(range(len(r.members)),r.members)]
                    list_ = []
                    while content:
                        list_.append(content[:30])
                        content = content[30:]
                    def check(reaction,user):
                            if (reaction.emoji == "⏭" or reaction.emoji == "⏮") and user == ctx.author and reaction.message.id == msg.id:return True
                            return False
                    def embed(description):
                        return discord.Embed(title="クランメンバー一覧",description="\n".join(description))
                    count = 0
                    msg = await ctx.send(embed=embed(list_[0]))
                    while not bot.is_closed():
                        if count > 0:
                            await msg.add_reaction("⏮")
                        if count < len(list_)-1:
                            await msg.add_reaction("⏭")
                        try:
                            reaction,user = await bot.wait_for("reaction_add",check=check,timeout=20.0)
                        except asyncio.TimeoutError:return await msg.clear_reactions()
                        else:
                            if reaction.emoji == "⏭":
                                count += 1
                            if reaction.emoji == "⏮":
                                count -= 1
                            await msg.edit(embed=embed(list_[count]))
                            await msg.clear_reactions()

@bot.command()
async def soul2(ctx):
    role = discord.utils.find(lambda r: r.name == "決意", ctx.guild.roles)
    if role in ctx.author.roles:
        msg = await ctx.send(embed=discord.Embed(description=f"Chara「ほう、{ctx.author.mention}は決意のソウルをもっているのか。\n\n\nならば貴様にはすべてのソウルを授けよう...」", color=0xffff00))
        [await ctx.author.add_roles(discord.utils.get(ctx.guild.roles,name=c)) for c in souls]
        await asyncio.sleep(5)
        await msg.edit(embed=discord.Embed(description=f"Chara「{ctx.author.mention}にすべてのソウルをさずけた...\nどんなことにも耐え忍び、何事も実行できる勇気を持ち,\n誠実であり決して屈することなく\nやさしい正義感の持ち主になり,\nだれよりも強く決意を抱き続けよ」", color=0xffff00))
    else:
        e = discord.Embed(description=f"{ctx.author.mention}は決意で満たされていない...\nでなおしな", color=0xffff00)
        await ctx.send(embed=e)

 
@bot.command(name='in')
async def in_(ctx):
    await ctx.send('..in')

@bot.command()
async def st(ctx):
    await ctx.send('..st')

@bot.command()
async def atk(ctx):
    await ctx.send('..atk')

@tasks.loop(seconds=10.0)
async def loop():
    role = bot.get_guild(648103908170006529).get_role(680573212446425141)
    channel = bot.get_channel(680573946974044227)
    key = "AIzaSyBxmY6diRxybaE7wONZusXZNWXYHXzXRdw"
    url = f'https://www.googleapis.com/youtube/v3/search?key={key}&channelId=UCPZDqfGwTfWiWhssUArk4ow&part=snippet,id&order=date&maxResults=10'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                js = await r.json()
                new = [c for c in js['items'] if c['id']['kind'] == 'youtube#video'][0]
                msgs = []
                for msg in await channel.history(limit=10).flatten():
                    if msg.author == bot.user and msg.embeds and msg.embeds[0].url == 'https://youtu.be/' + new['id']['videoId']:
                        msgs.append(msg)
                if not msgs:
                    embed = discord.Embed(title=new['snippet']['title'],url='https://youtu.be/' + new['id']['videoId'],color=0xff0000)
                    embed.set_thumbnail(url=new['snippet']['thumbnails']['high']['url'])
                    embed.set_author(name="YouTube")
                    embed.set_footer(text=new['snippet']['publishedAt'])
                    await channel.send(f'{role.mention}\n新しい動画が投稿されました！！みんなみてね！',embed=embed)


@bot.command(name="soul-reset")
async def soul_reset(ctx):
    if ctx.channel.type is not discord.ChannelType.private:
        if ctx.author == ctx.guild.owner:
            embed = discord.Embed(description="Reset the Soul!!",color=0xffff00)
            embed.set_image(url="https://i.pinimg.com/originals/d4/11/94/d4119472e9cd7949f4e4185a7ef8bea9.gif")
            await ctx.send(embed=embed)
            roles = [discord.utils.get(ctx.guild.roles,name=c) for c in souls]
            for role in roles:
                for member in role.members:
                    await member.remove_roles(role)
            send_msg = await ctx.send(embed=discord.Embed(color=0xffff00))
            msg = ['リ', 'セ', 'ッ', 'ト', '完', '了', '!', '!']
            for i in range(len(msg)):
                if send_msg is not None:await send_msg.edit(embed=discord.Embed(description="".join(msg[:(i+1):]),color=0xffff00))
                await asyncio.sleep(0.3)

async def process_commands(message):
    if message.author.bot:return
    if message.channel.type is discord.ChannelType.private:return
    ctx = await bot.get_context(message)
    await bot.invoke(ctx)

@bot.event
async def on_message(message):
    if message.channel.type is discord.ChannelType.private:return
    if message.channel.type is not discord.ChannelType.private:
        if message.channel.name == "チャンネル編集":
            if not message.author.bot and message.content is not None:
                name = message.content.lower().replace(" ","-")
                msg = await message.channel.send(embed=discord.Embed(description=f"`{name}`というチャンネルを作成しますか？", color=0xffff00))
                [await msg.add_reaction(c) for c in ["✅","❌"]]
                try:reaction,user = await bot.wait_for("reaction_add",check=lambda r,u:r.message.id == msg.id and u == message.author and r.emoji in ["✅","❌"])
                except asyncio.TimeoutError:return await msg.delete()
                else:
                    if reaction.emoji == "✅":
                        if message.channel.category is not None:
                            if len(message.channel.category.channels) < 50:
                                channel = await message.guild.create_text_channel(name=name,category=message.channel.category)
                                await channel.set_permissions(message.author, read_messages=True,send_messages=True,manage_channels=True,manage_messages=True,manage_roles=True)
                                await msg.edit(embed=discord.Embed(description=f"チャンネルを作成しました。{channel.mention}", color=0xffff00))
                            else:
                                await msg.edit(embed=discord.Embed(description="このカテゴリー内のチャンネル数が50のため、作成できませんでした。", color=0xffff00))
                        else:
                            await msg.edit(embed=discord.Embed(description="このチャンネルにカテゴリーが存在しないため、作成できませんでした。", color=0xffff00))
                    else:
                        await msg.edit(embed=discord.Embed(description="チャンネルは作成されませんでした。", color=0xffff00))
                    return await msg.clear_reactions()

    if discord.utils.get(await message.channel.webhooks(),name="SyncChat") is not None:
        if isinstance(message.author,discord.Member):
            mark = chr(129351 + guilds.index(message.guild.id))
            if message.author.is_avatar_animated:avatar_url = message.author.avatar_url
            else:avatar_url = message.author.avatar_url_as(format="png")
            if message.content:
                content = message.content.replace("@everyone", "`@ everyone`").replace("@here", "`@ here`")
                for ids in message.raw_mentions:
                    user = bot.get_user(ids)
                    if user:
                        content = re.sub(f"<@{ids}>", f"`@ {user}`", content)
                        content = re.sub(f"<@!{ids}>", f"`@ {user}`", content)
                    for idss in message.raw_role_mentions:
                        role = message.guild.get_role(idss)
                        if role is None:
                            content = content.replace(f"<@&{idss}>", "`@unknown-role`")
                        else:
                            content = content.replace(f"<@&{idss}>", f"`@ {role.name}`")
            else:content = None
            for guild in bot.guilds:
                if guild.id != message.guild.id:
                    webhook = discord.utils.get(await guild.webhooks(),name="SyncChat")
                    if webhook is not None:
                        await webhook.send(content=content, username=mark + str(message.author),avatar_url=avatar_url,embeds=message.embeds[:10:],files=[await c.to_file() for c in message.attachments[:10:]])
    await process_commands(message)
    

@tasks.loop(minutes=1)
async def looop():
    guild = bot.get_guild(648103908170006529)
    now = datetime.datetime.now()
    channels = guild.text_channels
    time_ = [i for i in range(0, 1440, 60) if i > len(channels)][0]
    times = [i - len(channels) for i in range(0, 1440, time_) if i - len(channels) > 0]
    list_ = []
    for _time in times:
        hours = 0
        minutes = _time
        for i in range(_time):
            if not i % 60 and minutes > 59:
                hours += 1
                minutes -= 60
        if len(str(hours)) == 1: hours = f"0{hours}"
        if len(str(minutes)) == 1: minutes = f"0{minutes}"
        list_.append(f"{hours}:{minutes}")
    if now.strftime("%H:%M") in list_:
        users = []
        bots = []
        for channel in guild.text_channels:
            for message in await channel.history(limit=10000).flatten():
                if not message.author.bot:
                    if not users or not message.author.id in [c[0] for c in users]:users.append([message.author.id,0])
                    [c for c in users if c[0] == message.author.id][0][1] += 1
                if message.author.bot:
                    if not bots or not message.author.id in [c[0] for c in bots]:bots.append([message.author.id,0])
                    [c for c in bots if c[0] == message.author.id][0][1] += 1
        dict_users = dict(users)
        dict_bots = dict(bots)
        user_ranking = []
        bot_ranking = []
        for ranking, dict_, members in zip([user_ranking, bot_ranking], [dict_users, dict_bots], [users, bots]):
            for user in members:
                id = user[0]
                try:await bot.fetch_user(id)
                except:continue
                else:
                    count = user[1]
                    if not ranking:ranking.append(id)
                    else:
                        for i,n in zip(ranking,range(len(ranking))):
                            if not id in ranking:
                                c = dict_[i]
                                if c <= count:ranking.insert(n,id)
                        if not id in ranking:ranking.append(id)
        for type_,ranking,dict_,id in zip(["ユーザー","ボット"],[user_ranking,bot_ranking],[dict_users,dict_bots],[687144773257265175,687144755523617071]):
            message = await bot.get_channel(684384306071863322).fetch_message(id)

            rank = "\n".join([f"[`{i+1}`] {await bot.fetch_user(c)}{''.join('　' for e in range(25-len(str(await bot.fetch_user(c)))))}{dict_[c]}" for i,c in zip(range(20),ranking[:20:])])
            embed = discord.Embed(title=f"{type_}ランキングtop20({time_}分更新)",description=rank,color=0xffff00)
            embed.set_footer(text=f"最終更新時刻:{now:%F.%T}")
            await message.edit(content=None,embed=embed)

@bot.command(name='ping',description='BOTの速度を測ることができる',pass_context=True)
async def ping(ctx):
    before = time.monotonic()

    msg = await ctx.send(
         embed=discord.Embed(
            title="きゃらちゃんの鯖専属BOTの反応速度", description="計測中・・・", color=0xffff00
        )
    )

    return await msg.edit(
        embed=discord.Embed(
            title="きゃらちゃんの鯖専属BOTの反応速度", description=f"Pingを取得したよ～\nPong!`{int((time.monotonic() - before) * 1000)}ms`", color=0xffff00
        )
    )

#人狼系コマンド
@bot.command(name='roles')
async def jinro_roles(ctx):
    if ctx.guild.id != guilds[0]:return
    embed = discord.Embed(description="\n".join(f'[`{n+1}`]{c["役職名"]}' for n,c in zip(range(len(jinro_json)),jinro_json)),color=0xFF0000)
    embed.set_footer(text="詳細を見たい役職の番号を送信してください。")
    await ctx.send(embed=embed)
    def check(msg):
        if msg.author == ctx.author and msg.channel == ctx.channel:
            try:int(msg.content)
            except ValueError:return False
            else:
                if int(msg.content) > 0 and int(msg.content) <= len(jinro_json):return True
                return False
        return False
    try:msg = await bot.wait_for('message',check=check,timeout=60.0)
    except asyncio.TimeoutError:return
    else:
        count = int(msg.content)
        role = jinro_json[count-1]
        embed = discord.Embed(color=0xFF0000).set_author(name=f"役職『{role['役職名']}』")
        [embed.add_field(name=c[0],value=c[1]) for c in list(role.items())]
        await ctx.send(embed=embed)

#運営用コマンド
@bot.command()
@is_moderator()
async def say(ctx, *, text):
    await ctx.send(text)
    await ctx.message.delete()

@bot.command()
@is_moderator()
async def cpurge(ctx,limit):
    await ctx.channel.purge(limit=int(limit))

@bot.command()
@is_operator()
async def capurge(ctx):
    await ctx.send("メッセージ決意...")
    await ctx.channel.purge(limit=None)

@bot.command()
@is_moderator()
async def ckick(ctx, member:discord.Member=None, reason=None):
    if member is None:return
    embed = discord.Embed(description="ユーザーを追放するための権限が足りていません！",color=0xFFFF00)
    if member.top_role.position > ctx.guild.me:return await ctx.send(embed=embed)
    if member == ctx.guild.owner:return await ctx.send(embed=embed)
    if member == ctx.author or member == ctx.guild.me:
        return await ctx.send(embed=discord.Embed(description="自身を追放することはできません！",color=0xFFFF00))
    await ctx.guild.kick(member, reason=reason)
    l = discord.Embed(title="ユーザーが追放されました！ / User has Sayonara!!", description=f"実行者：{ctx.author.name}\n{member.mention} を追放した。\n理由：{reason}", color=0xffff00)
    await ctx.send(embed=l)

@bot.command()
@is_operator()
async def cban(ctx, user:discord.User=None, reason=None):
    if user is None:return
    embed = discord.Embed(description="ユーザーをBANするための権限が足りていません！",color=0xFFFF00)
    if user in list(await ctx.guild.bans()):return await ctx.send(embed=embed)
    if user.id == ctx.guild.owner.id:return await ctx.send(embed=embed)
    if user.id == ctx.author.id or user.id == bot.user.id:
        return await ctx.send(embed=discord.Embed(description="自身をBANすることはできません！",color=0xFFFF00))
    await ctx.guild.ban(user, reason=reason)
    l = discord.Embed(title="ユーザーが死にました！ / User has dead!!", description=f"実行者：{ctx.author.name}\n{user.mention} を決意した。\n理由：{reason}", color=0xffff00)
    await ctx.send(embed=l)

@bot.command()
@is_operator()
async def cunban(ctx, user:discord.User=None, reason=None):
    if user is None:return
    embed = discord.Embed(description="ユーザーをUNBANするための権限が足りていません！",color=0xFFFF00)
    if ctx.guild.get_member(user.id):
        if ctx.guild.get_member(user.id).top_role > ctx.guild.me.top_role.position:
            return await ctx.send(embed=embed)
    if not user in list(await ctx.guild.bans()):return await ctx.send(embed=embed)
    await ctx.guild.unban(user, reason=reason)
    l = discord.Embed(title="ユーザーが復活しました！ / User is back!!", description=f"実行者：{ctx.author.name}\n{user.mention} が決意を抱いた。\n理由：{reason}", color=0xffff00)
    await ctx.send(embed=l)

@bot.command(name="csoul-reset")
@is_hidden()
async def csoul_reset(ctx):
    if ctx.channel.type is not discord.ChannelType.private:
        embed = discord.Embed(description="Reset the Soul!!",color=0xffff00)
        embed.set_image(url="https://i.pinimg.com/originals/d4/11/94/d4119472e9cd7949f4e4185a7ef8bea9.gif")
        await ctx.send(embed=embed)
        roles = [discord.utils.get(ctx.guild.roles,name=c) for c in souls]
        for role in roles:
            for member in role.members:
               await member.remove_roles(role)
        send_msg = await ctx.send(embed=discord.Embed(color=0xffff00))
        msg = ['リ', 'セ', 'ッ', 'ト', '完', '了', '!', '!']
        for i in range(len(msg)):
            if send_msg is not None:await send_msg.edit(embed=discord.Embed(description="".join(msg[:(i+1):]),color=0xffff00))
            await asyncio.sleep(0.3)

@bot.command(name="eval")
@is_hidden()
async def eval_(ctx, *, cmd):
    def get_role(name):
        return discord.utils.get(ctx.guild.roles,name=name)
    def get_channel(name):
        return discord.utils.get(ctx.guild.channels,name=name)
    def get_member(name):
        return discord.utils.get(ctx.guild.members,name=name)
    try:
        fn_name = "_eval_expr"
        cmd = cmd.strip("` ")
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
        body = f"async def {fn_name}():\n{cmd}"
        parsed = ast.parse(body)
        env = {
                'bot': ctx.bot,
                'discord': discord,
                'asyncio':asyncio,'random':random,'datetime':datetime,'re':re,
                'commands': commands,'tasks':tasks,
                'get_role':get_role, 'get_channel':get_channel, 'get_member':get_member,
                'ctx': ctx,
                '__import__': __import__
            }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)
        await eval(f"{fn_name}()", env)
        if ctx.message is not None:await ctx.message.add_reaction("✅")
    except Exception as e:
        await ctx.send(e)
        if ctx.message is not None:await ctx.message.add_reaction("‼")
 
loop.stop()
looop.stop()
