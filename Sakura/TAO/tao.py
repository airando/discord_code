import json
import re

f = open(r"training.json","r",encoding="utf-8")
training_json = json.load(f)

@bot.event
async def on_message(message):
    if message.content.startswith("::t") and message.author.id != bot.user.id:
        def check(msg):
            if len(msg.embeds) != 0 and msg.author.id in [688300266331701273,526620171658330112] and msg.channel.id == message.channel.id:return True
            return False
        try:
            msg = await bot.wait_for('message', check=check, timeout=20.0)
        except:
            pass
        else:
            description = msg.embeds[0].description
            if description is not discord.Embed.Empty and description.endswith("」の読み方をひらがなで答えなさい。"):
                quiz = re.search(r"(「*)((.+)*)(」の読み方をひらがなで答えなさい。*)", description)
                if quiz:
                    answer = training_json[quiz.group(2)]
                    if message.author.mobile_status != discord.Status.offline:
                        await msg.channel.send(f"この問題の答えは")
                        await msg.channel.send(f"||`{answer}`||")
                        await msg.channel.send(f"です！")
                    else:
                        embed = discord.Embed(description=f"この問題の答えは||`{answer}`||です！")
                        embed.set_footer(icon_url=msg.author.avatar_url, text="TAOのトレーニング")
                        await msg.channel.send(embed=embed)
