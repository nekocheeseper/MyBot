"""
Core initialization.

Initializes the shared resources required by the application
before the Discord bot starts running.

"""
import pathlib
import time

import _src.utils as utils

from . import event, start

logger = None

def init(bot):
    """Initialize the application's core components."""
     
    global logger

    # Store shared runtime information.
    bot.base_dir = pathlib.Path.cwd()
    bot.start_time = time.perf_counter()

    # Initialize the logging system.
    utils.logger.init(bot.base_dir, "mybot")
    logger = utils.logger.Logger()
    logger.init("core")
    logger.info("logger is ready")

    # Initialize core modules.
    start.init()
    event.init()

    logger.info("core initialized in %.2f seconds"%(time.perf_counter() - bot.start_time))
    return