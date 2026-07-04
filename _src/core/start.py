"""
Application setup.

Provides utilities for loading the bot token and
loading extensions during startup.

"""
from discord.ext import commands

import _src.utils as utils

logger = None

def init():
    global logger
    logger = utils.logger.Logger()
    logger.init("start")

def token(bot):
    """Load the bot token from the data directory."""
    with open(bot.base_dir / "data" / "token", "r") as f:
        return f.read().strip()

async def setup_hook(bot):
    """Load extensions and synchronize application commands."""

    extensions = []
    mod_path = bot.base_dir/ "_src" / "mod"

    # Load all discovered extensions.
    for folder in mod_path.iterdir():
        if not folder.is_dir(): continue
        cog = folder / "cog.py"
        if cog.exists():
            extensions.append(f"_src.mod.{folder.name}.cog")
    for extension in extensions:
        try:
            await bot.load_extension(extension)
            logger.info(f"Loaded extension: {extension}")
        except commands.ExtensionNotFound:
            logger.info(f"Skipped extension: {extension} (not found)")
        except Exception as e:
            logger.error(f"Failed to load extension {extension}: {e}")

    synced = await bot.tree.sync()
    logger.info(f"Synced {len(synced)} slash commands")
    return