from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from loader import dp

@dp.message_handler(CommandStart())
async def hi(message: Message):
    
    with open('/home/ubuntu/Cryptonews_bot/ids_added.txt', 'r') as l:
        ids = l.readlines()
        ids_list = list(map(lambda x: x.strip('\n'), ids))

    with open('/home/ubuntu/Cryptonews_bot/ids_added.txt', 'a') as q:
        if str(message.from_user.id) not in ids_list:
            q.write(f'{message.from_user.id}\n')
            await message.answer('''Привет! 👾 Этот бот автоматически рассылает новости о криптовалютах по мере их поступления.\n\n👀 Ну получается ждём, чё...''')
