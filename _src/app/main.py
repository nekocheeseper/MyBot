import discord
import discord.ext.commands

import _src.core as core

bot = discord.ext.commands.Bot(command_prefix = "\\", help_command = None, intents = core.intents)

core.init(bot)

@bot.event
async def setup_hook():
    await core.setup_hook(bot)
    return

@bot.event
async def on_ready():
    await core.event.on_ready(bot)
    return

@bot.event
async def on_presence_update(before, after):
    await core.event.on_presence_update(before, after, bot)
    return

@bot.event
async def on_message(message):
    await core.event.on_message(message, bot)
    return

@bot.event
async def on_reaction_add(reaction, user):
    await core.event.on_reaction_add(reaction, user, bot)
    return

@bot.event
async def on_voice_state_update(member, before, after):
    await core.event.on_voice_state_update(member, before, after, bot)
    return

bot.run(core.token(bot), log_formatter = core.utils.logger.ColourFormatter())