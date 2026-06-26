import _src.utils as utils

logger = None

def init():
    global logger
    logger = utils.logger.Logger()
    logger.init("start")

def token(bot):
    with open(bot.base_dir / "data" / "token", "r") as f:
        return f.read().strip()

async def setup_hook(bot):
    INITIAL_EXTENSIONS = []
    mod_path = bot.base_dir/ "_src" / "mod"
    for folder in mod_path.iterdir():
        if not folder.is_dir(): continue
        cog = folder / "cog.py"
        if cog.exists():
            INITIAL_EXTENSIONS.append(f"mod.{folder.name}.cog")
    for extension in INITIAL_EXTENSIONS:
        try:
            await bot.load_extension(extension)
            logger.info(f"Loaded extension: {extension}")
        except Exception as e:
            logger.error(f"Failed to load extension {extension}: {e}")
    synced = await bot.tree.sync()
    logger.info(f"Synced {len(synced)} slash commands")
    return