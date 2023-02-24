#!/usr/bin/env python3

"""
gitlab-webhook-telegram
"""

import asyncio
import os

from classes.app import App
from classes.bot import Bot
from classes.context import Context


async def main() -> None:
    directory = os.getenv("GWT_DIR", "./configs/")
    context = Context(directory)
    context.get_config()
    context.migrate_table_config()
    bot = Bot(token=context.config["telegram-token"], context=context)
    app = App(bot=bot, context=context)
    async with bot.application:
        await bot.run()
        await app.run()
        await bot.application.updater.stop()
        await bot.application.stop()
        await bot.application.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
