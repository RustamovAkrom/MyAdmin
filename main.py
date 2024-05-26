from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.client.session.aiohttp import AiohttpSession
import logging
import asyncio
import config
import time

# start time bot
time_start = time.time()

session = AiohttpSession(proxy="http://proxy.server:3128")
bot = Bot(token = config.BOT_TOKEN, session=session)
dp = Dispatcher()


class MessageSendState(StatesGroup):
    message_text = State()


@dp.message(Command(commands=["start"]))
async def start(message: types.Message):
    await message.reply(f"Salom 🙋‍♂️ {message.from_user.first_name} murojat va habarlarizni faqat matin korinishda kiriting boshqa (rasim, gif, ovozli habar, ...) lar qabul qilinmaydi. --> /help")


@dp.message(Command(commands=["help"]))
async def help(message: types.Message):
    await message.reply(config.COMMANDS)


@dp.message(Command(commands=["send_message"]))
async def send_message(message: types.Message, state: FSMContext):
    await message.answer("Habarizni kiriting agar siz bilan 24 sogat ichida jovob yozishmasa shahsiy akauntimga habarizni qoldirishiz munkin\n\t https://t.me/RustamovAkrom2007")
    await message.answer("Habar qoldiring iltimos hamma savolizni bitta yakka tarizda kiriting: 👇")
    await state.set_state(MessageSendState.message_text)


@dp.message(MessageSendState.message_text)
async def sending_on_group(message: types.Message, state: FSMContext):

    await state.update_data(message_text = message.text)

    if not message.text:
        await message.answer("Iltimos yozma tarizda kiriting !.")
        return sending_on_group
    
    await bot.send_message(config.GROUP_ID, config.SEND_GROUP_TEXT(
        message.from_user.first_name,
        message.from_user.last_name,
        f"https:/t.me/{message.from_user.username}",
        message.text
    ))
    await state.clear()
    await message.answer("Habariz qabul qilindi javobni kuting.")
    

async def main():
    try:
        await dp.start_polling(bot)

    except Exception as e:
        print(f"There is an exeptino - {e}")


if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")

        time_end = time.time()
        result_time = int(time_end) - int(time_start)

        with open("time.txt", "w") as f:
            f.write(f"bot working time: {str(result_time)} secund")