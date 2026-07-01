import time

import _src.utils as utils

from . import dispatcher

logger = None

def init():
    global logger
    logger = utils.logger.Logger()
    logger.init("event")

async def on_ready(bot):
    logger.info(f"Bot is ready in %.2f seconds"%(time.perf_counter() - bot.start_time))
    logger.info(f"Logged in as {bot.user} | ID: {bot.user.id}")
    bot.start_time = None
    return

async def on_presence_update(before, after, bot):
    await dispatcher.on_presence_update(before, after, bot)
    if before.status != after.status: logger.info(f"{before.name}'s presence changes to : {after.status}")
    return

async def on_message(message, bot):
    if message.author.id == bot.user.id: return
    ctx = await bot.get_context(message)
    await bot.process_commands(message)
    if message.content.startswith("/"): return
    await dispatcher.on_message(message, bot)
    logger.info(f"Message received from {message.author}")
    return

async def on_reaction_add(reaction, user, bot):
    await dispatcher.on_reaction_add(reaction, user, bot)
    logger.info(f"Reaction added by {user}: {reaction.emoji}")
    return

async def on_voice_state_update(member, before, after, bot):
    await dispatcher.on_voice_state_update(member, before, after, bot)
    if before.channel is None and after.channel is not None:
        logger.info(f"{member.name} joined voice channel: {after.channel}")
    elif before.channel is not None and after.channel is None:
        logger.info(f"{member.name} left voice channel: {before.channel}")
    elif before.channel != after.channel:
        logger.info(f"{member.name} moved from voice channel {before.channel} to {after.channel}")
    return