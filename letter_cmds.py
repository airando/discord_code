"""
大文字小文字を区別させずにコマンドを呼び出すコード
"""

"""
===================================
"""
#Cogではない場合

async def process_commands(message):
    if message.author.bot:return
    ctx = await bot.get_context(message)
    if ctx.prefix is not None:
        ctx.command = self.all_commands.get(ctx.invoked_with.lower())
        await bot.invoke(ctx)

@bot.event
async def on_message(message):
    await process_commands(message)

"""
===================================
"""
#Cogの場合

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="::")

    async def process_commands(self, message):
        if message.author.bot:return
        ctx = await self.get_context(message)
        if ctx.prefix is not None:
            ctx.command = self.all_commands.get(ctx.invoked_with.lower())
            await self.invoke(ctx)

    async def on_message(self,message):
        await self.process_commands(message)

"""
===================================
"""

