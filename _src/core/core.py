import pathlib
import time

import _src.utils as utils

from . import event, start

logger = None

def init(bot):
    global logger
    bot.base_dir = pathlib.Path.cwd()
    bot.start_time = time.perf_counter()
    utils.logger.init(bot.base_dir, "mybot")
    logger = utils.logger.Logger()
    logger.init("core")
    logger.info("logger is ready")
    start.init()
    event.init()
    logger.info("core initialized in %.2f seconds"%(time.perf_counter() - bot.start_time))
    return