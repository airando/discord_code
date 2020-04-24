import discord
import json
import datetime,re,asyncio,random
from discord.ext import commands

class JinroGame(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.dead = "Dead"
        self.player = "客"
        self.spectator = "観戦"
        f = open(r'Jinro/setting.json', 'r', encoding='utf-8')
        self.setting = json.load(f)
        f = open(r'Jinro/roles.json', 'r', encoding='utf-8')
        self.jinro_roles = json.load(f)

    async def update(self,jinro):
        f = open(r'Jinro/playing.json', 'w', encoding='utf-8')
        json.dump(jinro, f, indent=4)

    async def members_update(self,jinro):
        f = open(r'Jinro/members.json', 'w', encoding='utf-8')
        json.dump(jinro, f, indent=4)

    def predicate(self,ctx,emojis,message):
        def check(reaction,user):
            if reaction.emoji in emojis and user == ctx.author:
                if reaction.message.id == message.id:return True
                return False
            return False
        return check

    def using(self):
        f = open(r'Jinro/playing.json', 'r', encoding='utf-8')
        playing = json.load(f)
        return playing

    async def get_time(self,seconds):
        if not isinstance(seconds,int):return None
        seconds = 90
        minute = int(seconds / 60)/10
        second = int(seconds % 60)/10
        return f"{minute}:{second}".replace('.','')

    async def send(self,webhooks,message,url=None,name='執事'):
        if url is None:url = self.bot.get_emoji(702519622343196683).url
        for webhook in webhooks:
           await webhook.send(message,username=name,avatar_url=url)

    async def process_commands(self,message):
        if message.author.bot:return
        if message.channel.type is discord.ChannelType.private:return
        if message.guild.id != 694952646901235792:return
        ctx = await self.bot.get_context(message)
        await self.bot.invoke(ctx)

    async def check(self):
        f = open(r'Jinro/members.json', 'r', encoding='utf-8')
        members_dict = json.load(f)
        wolves = [c for c in members_dict['roles']['人狼'] if members_dict['members'][c]['Dead'] is False]
        people = [c for c in list(members_dict['members'].values()) if members_dict['members'][c]['Dead'] is False and not c in wolves]
        if len(wolves) >= people:
            return "人狼"
        if len(wolves) == 0:
            if people == 0:return "全滅"
            return "村人"
        return None

    async def night(self,day,timeout=90):
        color = 0xFF0000
        guild = self.bot.get_guild(694952646901235792)
        time_channel = self.bot.get_channel(702493994138992651)
        remain_channel = self.bot.get_channel(702495647961710632)
        cafeteria = discord.utils.get(category.text_channels,name='食堂')
        category = self.bot.get_channel(699653796653170768)
        def get_role(name):
            return discord.utils.get(guild.roles,name=name)
        f = open(r'Jinro/members.json', 'r', encoding='utf-8')
        members_dict = json.load(f)
        if members_dict['time'] == "夜":
            [await c.edit(name="処理中…") for c in [time_channel,remain_channel]]
            fortunes = member_dict['roles']['占い師']
            psychics = member_dict['roles']['霊能者']
            wolves = member_dict['roles']['人狼']
            hunters = member_dict['roles']['狩人']
            for fortune in fortunes:
                if members_dict['members'][fortune]['Dead'] is not False:continue
                member = guild.get_member(fortune)
                channel = self.bot.get_channel(member_dict['members'][fortune]['private'])
                users = []
                if day == 1:
                    for id in members_dict['占']['白']:
                        mem = guild.get_member(id)
                        if mem is not None or mem.id == member.id:users.append(mem)
                    user = random.choice(users)
                    embed = discord.Embed(description="1日目占い結果(ランダム):\n『{user}』:白",color=color)
                    await channel.send(member.mention,embed=embed)
                else:
                    for id in list(members_dict['members'].keys()):
                        mem = guild.get_member(id)
                        if mem is None or mem.id == member.id:continue
                        if members_dict['members'][id]['Dead'] is False:users.append(mem)
                    embed = discord.Embed(description="占い先を指定してください。",color=color)
                    emojis = [chr(127462 + i) for i in range(len(users))]
                    embed.add_field(name="選択欄",value="\n".join(e + u.mention for e,u in zip(emojis,users)))
                    msg = await channel.send(member.mention,embed=embed)
                    [await msg.add_reaction(c) for c in emojis]
            for psychic in psychics:
                if members_dict['members'][spychic]['Dead'] is not False:continue
                member = guild.get_member(psychic)
                channel = self.bot.get_channel(member_dict['members'][psychic]['private'])
                users = []
                if day == 1:
                    embed = discord.Embed(description="1日目は能力を発動することはできません。",color=color)
                    await channel.send(member.mention,embed=embed)
                else:
                    for id in list(members_dict['members'].keys()):
                        mem = guild.get_member(id)
                        if mem is None:continue
                        if members_dict['members'][id]['Dead'] is not False:
                            if members_dict['members'][id]['Dead']['day'] == day:
                                jinro_role = [c for c in self.jinro_roles if role == list(c.values())[0]][0]
                                users.append([mem,jinro_role['霊能結果']])
                    des = "```\n" + "\n".join(f'{c[0]}:{c[1]}' for c in users) + "```"
                    embed = discord.Embed(description="霊能結果:\n" + des,color=color)
                    await channel.send(member.mention,embed=embed)
            channel = discord.utils.get(category.text_channels,name="人狼チャット")
            if day == 1:
                embed = discord.Embed(description="1日目は自動で『執事』を襲撃します。",color=color)
                await channel.send(','.join([bot.get_user(c).mention for c in wolves]),embed=embed)
            else:
                wolf_users = []
                for id in list(members_dict['members'].keys()):
                    if not id in wolves:
                        mem = guild.get_member(id)
                        if mem is None:continue
                        if members_dict['members'][id]['Dead'] is False:
                            wolf_users.append(mem)
                embed = discord.Embed(description="襲撃先を指定してください。",color=color)
                wolf_emojis = [chr(127462 + i) for i in range(len(wolf_users))]
                embed.add_field(name="選択欄",value="\n".join(e + str(u) for e,u in zip(emojis,wolf_users)))
                wolf_message = await channel.send(','.join([bot.get_user(c).mention for c in wolves]),embed=embed)
                [await wolf_message.add_reaction(c) for c in wolf_emojis]
            hunter_msgs = []
            for hunter in hunters:
                if members_dict['members'][hunter]['Dead'] is not False:continue
                member = guild.get_member(hunter)
                channel = self.bot.get_channel(member_dict['members'][hunter]['private'])
                users = []
                if day == 1:
                    embed = discord.Embed(description="1日目は能力を発動することはできません。",color=color)
                    await channel.send(member.mention,embed=embed)
                else:
                    for id in list(members_dict['members'].keys()):
                        mem = guild.get_member(id)
                        if mem is None or mem.id == member.id:continue
                        if members_dict['members'][id]['Dead'] is False:users.append(mem)
                    embed = discord.Embed(description="護衛先を指定してください。",color=color)
                    emojis = [chr(127462 + i) for i in range(len(users))]
                    embed.add_field(name="選択欄",value="\n".join(e + str(u) for e,u in zip(emojis,users)))
                    msg = await channel.send(member.mention,embed=embed)
                    [await msg.add_reaction(c) for c in emojis]
                    hunter_msgs.append([msg,users,emojis])
            await time_channel.edit(name=f"{day}日目 | 夜")
            await remain_channel.edit(name=f"残り | {self.get_time(timeout)}")
            await cafeteria.send(embed=discord.Embed(description="夜になりました。\n能力を持ってる方は能力を実行してください。",color=color))
            for i in range(timeout):
                await asyncio.sleep(1)
                if not (i + 1) % 30:
                    await remain_channel.edit(name=f"残り | {self.get_time(timeout-(i+1))}")
                if (i + 1) >= timeout - 10:
                    await remain_channel.edit(name=f"残り | {self.get_time(timeout-(i+1))}")
            [await c.edit(name="処理中…") for c in [time_channel,remain_channel]]
            if day == 1:
                members_dict['time'] = "昼"
                await self.members_update(members_dict)
                return None
            def predicate(user):
                return user.id in wolves
            reaction_dict = {}
            for reaction in list(msg.reaction):
                reaction_dict[reaction.emoji] = len(await reaction.users().filter(predicate).flatten())
            emojis = []
            for reaction in list(msg.reactions):
                if reaction_dict[reaction.emoji] == 0:continue
                if not emojis:emojis.append([reaction.emoji])
                else:
                    for n,emoji in zip(range(len(emojis)),emojis):
                        if reaction_dict[emoji[0]] == reaction_dict[reaction.emoji]: emoji.append(reaction.emoji)
                        elif reaction_dict(emoji[0]) < reaction_dict[reaction.emoji]: emojis.insert(n,[reaction.emoji])
                        else:continue
                        break
                    if not [c for c in emojis if [e for e in c if c == reaction.emojis]]:emojis.append([reaction.emojis])
            target = None
            if emojis:
                target = wolf_users[wolf_emojis.index(random.choice(emojis[0]))].id
            hunter_ = []
            for hunt in hunter_msgs:
                msg = hunt[0]
                def predicate(user):
                    return user.id == members_dict['channels'][msg.channel.id]['member']
                emojis = [c.emoji for c in msg.reactions if len(await reaction.users().filter(predicate).flatten()) > 0]
                if emojis:hunter_.append(hunt[1][hunt[2].index(emojis[0])].id)
            members_dict['time'] = "昼"
            await self.members_update(members_dict)
            if target in hunter_:return None
            else:
                members_dict['members'][target]['Dead'] = {'day':day}
                return target

    async def noon(self,day,target,timeout=300):
        color = 0xFF0000
        guild = self.bot.get_guild(694952646901235792)
        time_channel = self.bot.get_channel(702493994138992651)
        remain_channel = self.bot.get_channel(702495647961710632)
        category = self.bot.get_channel(699653796653170768)
        cafeteria = discord.utils.get(category.text_channels,name='食堂')
        def get_role(name):
            return discord.utils.get(guild.roles,name=name)
        f = open(r'Jinro/members.json', 'r', encoding='utf-8')
        members_dict = json.load(f)
        if members_dict['time'] == "昼":
            if target is None:
                if day == 2:description = "『執事』が無残な姿で発見されました。"
                else:description = "昨夜に襲撃された人はいませんでした。"
            else:
                member = guild.get_member(target)
                await member.add_roles(get_role(self.dead))
                description = f"『{member}』が無残な姿で発見されました。"
            await time_channel.edit(name=f"{day}日目 | 昼")
            await cafeteria.set_permissions(get_role(self.player),send_messages=True)
            des = description + "\n\n昼になりました。これから5分間話し合ってください。"
            await cafeteria.send(get_role(self.player).mention,embed=discord.Embed(description=des,color=color))
            await remain_channel.edit(name=f"残り | {self.get_time(timeout)}")
            for i in range(timeout-60):
                await asyncio.sleep(1)
                if not (i + 1) % 30:
                    await remain_channel.edit(name=f"残り | {self.get_time(timeout-(i+1))}")
            embed = discord.Embed(description="残り時間を延長しますか？",color=color)
            embed.set_footer(text="残り時間が0秒になった時に過半数の人が延長を希望した場合延長します。")
            embed.add_field(name="選択欄",value=chr(127462) + "はい")
            send_msg = await cafeteria.send(get_role(self.player).mention,embed=embed)
            await send_msg.add_reaction(chr(127462))
            for i in range(60):
                await asyncio.sleep(1)
                if not (i + 1) % 30:
                    await remain_channel.edit(name=f"残り | {self.get_time(60-(i+1))}")
                if (i + 1) >= timeout - 10:
                    await remain_channel.edit(name=f"残り | {self.get_time(60-(i+1))}")
            def predicate(user):
                return get_role(self.player) in guild.get_member(user.id).roles
            users = [c.users().filter(predicate).flatten() for c in send_msg.reactions if c.emoji == chr(127462)][0]
            if len(users) > len(get_role(self.player)):
                embed = discord.Embed(title="残り時間が延長されました。")
                embed.add_field(name="延長を希望したメンバー",value="\n".join(f"`{c}`" for c in zip(range(len(users)),users)))
                await cafeteria.send(get_role(self.player).mention,embed=embed)
                for i in range(180):
                    await asyncio.sleep(1)
                    if not (i + 1) % 30:
                        await remain_channel.edit(name=f"残り | {self.get_time(180-(i+1))}")
                    if (i + 1) >= timeout - 10:
                        await remain_channel.edit(name=f"残り | {self.get_time(180-(i+1))}")
            members_dict['time'] = "投票"
            await self.members_update(members_dict)

    async def vote(self,day,timeout=60):
        color = 0xFF0000
        guild = self.bot.get_guild(694952646901235792)
        time_channel = self.bot.get_channel(702493994138992651)
        remain_channel = self.bot.get_channel(702495647961710632)
        category = self.bot.get_channel(699653796653170768)
        private_category = self.bot.get_channel(699654333083549726)
        cafeteria = discord.utils.get(category.text_channels,name='食堂')
        jinro_chat = discord.utils.get(category.text_channels,name="人狼チャット")
        def get_role(name):
            return discord.utils.get(guild.roles,name=name)
        f = open(r'Jinro/members.json', 'r', encoding='utf-8')
        members_dict = json.load(f)
        if members_dict['time'] == "投票":
            await cafeteria.set_permissions(get_role(self.player),send_messages=False)
            await time_channel.edit(name=f"{day}日目 | 投票")
            await remain_channel.edit(name=f"残り | {self.get_time(timeout)}")
            des = "投票を開始します。個人チャンネルにて投票を行ってください。"
            await cafeteria.send(embed=discord.Embed(description=des,color=color))
            channels = {}
            msgs = []
            for channel in private_category.text_channels:
                if channel.id in members_dict['channels'].keys():
                    member = guild.get_member(members_dict['channels'][c.id]['member'])
                    if members_dict['members'][member.id]['Dead'] is not False:continue
                    channels[channel.id] = member.id
                    embed = discord.Embed(description="投票先を指定してください。",color=color)
                    embed.set_footer(text="残り時間0秒まで何度でも選びなおせます。")
                    users = []
                    for id in members_dict['members'].keys():
                        if id != member.id:
                            mem = guild.get_member(id)
                            if mem is None:continue
                            if members_dict['members'][id]['Dead'] is False:users.append(mem)
                    emojis = [chr(127462 + i) for i in range(len(users))]
                    embed.add_field(name="選択欄",value='\n'.join(e + str(m) for e,m in zip(emojis,users)))
                    msg = await channel.send(member.mention,embed=embed)
                    [await msg.add_reaction(c) for c in emojis]
                    msgs.append([msg,users,emojis])
            for i in range(timeout):
                await asyncio.sleep(1)
                if not (i + 1) % 10:
                    await remain_channel.edit(name=f"残り | {self.get_time(timeout-(i+1))}")
                if (i + 1) >= timeout - 10:
                    await remain_channel.edit(name=f"残り | {self.get_time(timeout-(i+1))}")
            [await c.edit(name=f"処理中…") for c in [time_channel,remain_channel]]
            voting = {"無投票":0}#{user.id:int[投票数]}
            voting_ = []#[user.id(1st),user.id(2nd)]
            for msg in msgs:
                msg_,users,emojis = msg
                channel = mag_.channel
                member = guild.get_member(members_dict['channels'][channel.id]['member'])
                def predicate(user):
                    return user == member
                emoji = [c.emoji for c in msg_.reactions if len(await c.users().filter(predicate).flatten()) > 0][0]
                if not emoji:
                    voting["無投票"] += 1
                    continue
                user = users[emojis.index(emoji)]
                if not user.id in voting.keys():voting[user.id] = 0
                voting[user.id] += 1
            for vote_ in voting.keys():
                if not voting:voting_.append([vote_])
                else:
                    for i,_vote in zip(range(len(voting_)),voting_):
                        if voting[_vote] == voting[vote_]:voting_[i].append(vote_)
                        elif voting[_vote] > voting[vote_]:voting_.insert(i,[vote_])
                        else:continue
                        break
                    if [c for c in voting_ if [e for e in c if e == vote_]]:
                        voting_.append([vote_])
            user = guild.get_member(random.choice(voting_[0]))
            await user.add_roles(get_role(self.dead))
            if user.id in members_dict['roles']['人狼']:
                await jinro_chat.set_permissions(user,read_messages=False)
            member_dict['members'][user.id]['Dead'] = {'day':day}
            embed = discord.Embed(description=f"『{user}』が処刑されました。",color=color)
            embed.add_field(name="投票結果",value="\n".join(f"{c} -> {voting[c]}" for c in voting_))
            await cafeteria.send(get_role(self.player).mention,embed=embed)
            members_dict['time'] = "夜"
            await self.members_update(members_dict)
            

    @commands.command(name='start')
    async def start(self,ctx):
        guild = self.bot.get_guild(694952646901235792)
        def get_role(name):
            return discord.utils.get(guild.roles,name=name)
        color = 0xFFFF00
        if not self.using:
            return await ctx.send(embed=discord.Embed(description="ゲームが開始済みです！",color=color))
        await self.update({'ゲームスタート':True})
        if ctx.author.voice is None:
            await self.update({})
            embed = discord.Embed(description="あなたはボイスチャンネルに接続していません",color=color)
            return await ctx.send(embed=embed)
        vc = self.bot.get_channel(702103120083288136)
        channel = ctx.author.voice.channel
        if channel is not vc:return await self.update(None)
        members = channel.members
        if len(members) != 9:
            await self.update({})
            embed = discord.Embed(description="人数が`9人`ではないため、開始できません。",color=color)
            return await ctx.send(embed=embed)
        roles = []
        for role in list(self.setting.keys()):
            for i in range(int(self.setting[role]['members']['count'])):
                roles.append(role)
        [await c.edit(mute=True,deafen=True) for c in members]
        embed = discord.Embed(description="開始の準備をします。しばらくお待ちください。",color=color)
        await ctx.send(embed=embed)
        time_channel = self.bot.get_channel(702493994138992651)
        remain_channel = self.bot.get_channel(702495647961710632)
        [await c.edit(name="準備中…") for c in [time_channel,remain_channel]]
        [await c.remove_roles(get_role(self.player)) for c in get_role(self.player).members]
        [await c.remove_roles(get_role(self.dead)) for c in get_role(self.dead).members]
        [await c.add_roles(get_role(self.player)) for c in members]
        category = self.bot.get_channel(699653796653170768)
        private_category = self.bot.get_channel(699654333083549726)
        [await c.delete() for c in private_category.text_channels]
        members_dict = {'members':{},'channels':{},'roles':{},
            '占':{'白':[],'黒':[],'他':[]},'霊':{'白':[],'黒':[],'他':[]},'time':'夜'}
        for member in members:
            ch = await private_category.create_text_channel(name=member.name)
            await ch.set_permissions(guild.default_role,read_messages=False)
            await ch.set_permissions(member,add_reactions=False,read_messages=True,send_messages=True)
            role = random.choice(roles)
            jinro_role = [c for c in self.jinro_roles if role == list(c.values())[0]][0]
            des = f"陣営: {jinro_role['陣営']}\n占い結果: {jinro_role['占い結果']}\n霊能結果: {jinro_role['霊能結果']}"
            des += f"\n勝利条件: {jinro_role['勝利条件']}"
            embed = discord.Embed(title=f"あなたの役職は『{role}』です。",description=des,color=color)
            embed.add_field(name="能力",value=jinro_role["能力"])
            await ch.send(member.mention,embed=embed)
            members_dict['members'][member.id] = {'private':ch.id,"role":role,"Dead":False}
            members_dict['channels'][ch.id] = {'member':member.id,"role":role}
            if role in list(members_dict['roles'].keys()): members_dict['roles'][role].append(member.id)
            else:members_dict['roles'][role] = [member.id]
            for target,kind in zip(['占い結果','霊能結果'],['占','霊']):
                target_ = jinro_role[target]
                if target_ == '白':members_dict[kind]['白'].append(member.id)
                elif target_ == '黒':members_dict[kind]['黒'].append(member.id)
                else:members_dict[kind]['他'].append(member.id)
        [await c.delete() for c in category.text_channels]
        cafeteria = await category.create_text_channel(name="食堂")
        await cafeteria.set_permissions(get_role(self.player),read_messages=True,send_messages=False)
        await cafeteria.set_permissions(get_role(self.spectator),read_messages=True,send_messages=False)
        await cafeteria.set_permissions(get_role(self.dead),read_messages=False,send_messages=False)
        await cafeteria.set_permissions(guild.default_role,read_messages=False,send_messages=False)
        jinro_room = await category.create_text_channel(name="人狼チャット")
        await jinro_room.set_permissions(get_role(self.player),read_messages=False,send_messages=False)
        await jinro_room.set_permissions(get_role(self.spectator),read_messages=True,send_messages=False)
        await jinro_room.set_permissions(get_role(self.dead),read_messages=False,send_messages=False)
        await jinro_room.set_permissions(guild.default_role,read_messages=False,send_messages=False)
        cemetery = await category.create_text_channel(name="墓場")
        await cemetery.set_permissions(get_role(self.player),read_messages=False,send_messages=False)
        await cemetery.set_permissions(get_role(self.spectator),read_messages=True,send_messages=False)
        await cemetery.set_permissions(get_role(self.dead),read_messages=True,send_messages=True)
        await cemetery.set_permissions(guild.default_role,read_messages=False,send_messages=False)
        webhooks = [await c.create_webhook(name=c.name,avatar=await guild.me.avatar_url_as(format='png').read()) for c in [cafeteria,jinro_room,cemetery]]
        await self.members_update(members_dict)
        embed = discord.Embed(description="ゲームを開始します。",color=0xFF0000)
        await cemetery.send(embed=embed)
        await self.send(webhooks,"おやおやお客様、私はこの館で執事をしております。")
        await self.send(webhooks,"この館には『人狼』という人の化けた狼がいるという噂がありますので、お気をつけください。")
        await self.send(webhooks,"ではおやすみなさいませ。")
        embed = discord.Embed(title="1日目 | 夜",description="能力を持っている方は能力を実行してください。",color=0xFF0000)
        await cemetery.send(embed=embed)
        for id in members_dict['roles']['人狼']:
            member = guild.get_member(id)
            if member:await jinro_room.set_permissions(member,read_messages=True,send_messages=True)
        target = await self.night(1,30)
        day = 2
        while not bot.is_closed():
            await self.noon(day,target)
            await self.vote(day)
            if self.check() is not None:
                await cafeteria.send(embed=discord.Embed(description=f"『{check}』の勝利！",color=color))
                return await self.update({})
            target = await self.night(day)
            if self.check() is not None:
                await cafeteria.send(embed=discord.Embed(description=f"『{check}』の勝利！",color=color))
                return await self.update({})
            day += 1

    @commands.Cog.listener()
    async def on_reaction_add(self,reaction,user):
        message = reaction.message
        guild = self.bot.get_guild(694952646901235792)
        if message.channel.category_id == 699654333083549726:
            if message.author is message.guild.me:
                f = open(r'Jinro/members.json', 'r', encoding='utf-8')
                members_dict = json.load(f)
                channel = message.channel
                if not channel in list(members_dict['channels'].keys()):return
                if user.id != members_dict['channels'][channel.id]['member']:return
                if user.id in members_dict['roles']['占い師']:
                    if not message.embeds:return
                    embed = message.embeds[0]
                    if embed.description == "占い先を指定してください。":
                        if len(embed.fields) == 1:
                            await message.clear_reactions()
                            await message.edit(embed=discord.Embed(description="占い結果が出るまでお待ち下さい🔮",color=0xFF0000))
                            value = embed.fields[0].value
                            split = value.splitlines()[[c.emoji for c in message.reactions].index(reaction.emoji)]
                            id = re.search("<@([0-9]*)>",split)
                            if id is None:
                                id = re.search("<@!([0-9]*)>",split)
                            if id is not None:
                                member = guild.get_member(int(id.group(1)))
                                if member is None:return
                                role = members_dict['members'][member.id]['role']
                                future = [c for c in self.jinro_roles if role == list(c.values())[0]][0]['占い結果']
                                await channel.send(user.mention,embed=discord.Embed(description=f"『{member}』:{future}",color=0xFF0000))
                for reaction_ in message.reactions:
                    if reaction_.emoji != reaction.emoji:
                        users = await reaction_.users().flatten()
                        if user in users:await message.remove_reaction(reaction_.emoji,user)

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.channel.type is discord.ChannelType.private:return
        if message.guild.id != 694952646901235792:return
        if self.using is None:return
        if isinstance(message.author,discord.User):return

        if message.channel.category_id == 699653796653170768:
            async def get_webhook(name):
                webhooks = []
                for webhook in list(await message.guild.webhooks()):
                    if webhook.name == name:
                        if webhook.channel.category is message.channel.category:
                            webhooks.append(webhook)
                if webhooks:return webhooks[0]
                return None
            cafeteria = await get_webhook("食堂")
            jinro_room = await get_webhook("人狼チャット")
            cemetery = await get_webhook("墓場")
            webhooks = [cafeteria,jinro_room,cemetery]
            if [c for c in webhooks if c is None]:return
            if message.channel is cafeteria.channel:
                for webhook in webhooks:
                    if webhook.channel is message.channel:continue
                    name,url = str(message.author),message.author.avatar_url_as(format='png')
                    await webhook.send(message.content,username=name,avatar_url=url,embeds=message.embeds,files=[await c.to_file() for c in message.attachments])

        await self.process_commands(message)
        

            

def setup(bot):
    bot.add_cog(JinroGame(bot))
