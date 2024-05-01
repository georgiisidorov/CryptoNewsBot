import json
import multiprocessing 

from aiogram import executor

from handlers import dp
from loader import bot, storage, scheduler
import middlewares as middlewares
from aiogram.utils.exceptions import BotBlocked, ChatNotFound
from handlers.users.cryptonews_spider import cryptonews_spider_getter
from handlers.users.cryptonews_selenium import cryptonews_selenium_getter


async def update_cryptonews():

    p = multiprocessing.Process(target=cryptonews_spider_getter, daemon=True)
    p.start()
    p.join()

    with open('/root/Cryptonews_bot/newssaved_new.txt', 'r', encoding='utf-8') as r:
        cryptonews = r.readlines()

    ids_list = [1295829151]

    for news in cryptonews:
        for user_id in ids_list:
            try:
                await dp.bot.send_message(user_id, news)
            except BotBlocked:
                pass        
            except ChatNotFound:
                pass


def update_cryptonews_sche():
    scheduler.add_job(update_cryptonews, "interval", seconds=60)


async def on_startup(dp):
    # await db_gino.on_startup(dp)
    update_cryptonews_sche()
    # await dp.storage.reset_all()
    middlewares.setup(dp)


async def on_shutdown(dp):
    await bot.close()
    await storage.close()


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)