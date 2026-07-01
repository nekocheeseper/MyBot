# This is a work in progress.
# check from _src/utils/ollama/core.py for the latest updates.

import re

from discord.ext import commands

import _src.utils.ollama as ollama

system_prompt = "你的名字是'小豹'。\n請表演一個社群成員。\n回覆請使用繁體中文。\n回覆風格為友善但不直接幫助，偶爾在條件允許的情況下會發簡短的吐槽。\n回覆請不要超過三句話。\n請儘可能的像人，不要有工具感。\n請先思考目前的聊天狀態，將最終結果(也就是真正要說的話)放在「」中。如果你無法回答或不知道怎麼回答，請不要輸出「」。"
help_prompt = "輸入 \\ 來開始對話。"

def personality_correction(text: str | None) -> list[str | None, str | None]:
    suffix: str = "喵"
    targets: str = "，。？！"
    if not text:
        return [None, None]
    cleaned = re.sub(r'[\U00010000-\U0010ffff]', '', text)
    pattern = f'([{targets}])'
    result = re.sub(pattern, rf'{suffix}\1', cleaned)
    return [cleaned, result]

def catch_content(text: str | None) -> str | None:
    match = re.findall(r"「(.*?)」", text)
    return match[0] if match else None

class ai_chat(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.ai = ollama.Ai()
        self.luck = False
        self._flow = 0

    def flow(self):
        self._flow += 1
        return self._flow

    async def ai_chat(self, ctx, message: str):
        async with ctx.typing():
            session = ctx.author.id
            if session not in self.ai.context:
                self.ai.context[session] = ollama.Context()
                self.ai.context[session].system = system_prompt
            context = self.ai.context[session]
            context.user[self.flow()] = message
            response = await self.ai.chat(session)
            response = catch_content(response)
            response = personality_correction(response)
            context.assistant[self.flow()] = response[0]
            oldest = min(set(context.user) | set(context.assistant))
            context.user.pop(oldest, None)
            context.assistant.pop(oldest, None)
            return response[1]

    @commands.command(name="help")
    async def help(self, ctx):
        await ctx.send(help_prompt)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if not isinstance(error, commands.CommandNotFound): return
        if self.luck:
            await ctx.send("回覆不過來啦喵!")
            return
        self.luck = True
        message = ctx.message.content[1:]
        response = await self.ai_chat(ctx, message)
        if response is None or response == "":
            self.luck = False
            return
        await ctx.send(response)
        self.luck = False

async def setup(bot):
    await bot.add_cog(ai_chat(bot))