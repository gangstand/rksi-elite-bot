from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import markups as nav
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
import sqlite3


conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()
bot = Bot(token='5181540972:AAFRALZvnARj6hAQ4ykpXaYhD-fuKdtRwq0')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

group_list = {'btn_is_11': 'ИС-11', 'btn_is_12': 'ИС-12', 'btn_is_13': 'ИС-13', 'btn_is_14': 'ИС-14',
              'btn_is_15': 'ИС-15',
              'btn_is_16': 'ИС-16', 'btn_is_17': 'ИС-17', 'btn_is_18': 'ИС-18', 'btn_sa_11': 'СА-11',
              'btn_sa_12': 'СА-12',
              'btn_sa_13': 'СА-13', 'btn_sa_14': 'СА-14', 'btn_sa_15': 'СА-15', 'btn_sa_16': 'СА-16',
              'btn_sa_17': 'СА-17',
              'btn_ibt_11': 'ИБТ-11', 'btn_ibt_12': 'ИБТ-12', 'btn_ibt_13': 'ИБТ-13', 'btn_ibt_14': 'ИБТ-14',
              'btn_iba_11': 'ИБА-11', 'btn_iba_12': 'ИБА-12', 'btn_iba_13': 'ИБА-13', 'btn_iba_14': 'ИБА-14'}

button1 = KeyboardButton('Информационные системы и программирование (ИС)')
button2 = KeyboardButton('Сетевое и системное администрирование (СА)')
button3 = KeyboardButton('Обеспечение информационной безопасности телекоммуникационных систем (ИБТ)')
button4 = KeyboardButton('Обеспечение информационной безопасности автоматизированных систем (ИБА)')

markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    button1).add(button2).add(button3).add(button4)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Выберите специальность студента", reply_markup=markup)


class Form(StatesGroup):
    group = State()
    name = State()
    username = State()


@dp.message_handler(text='Информационные системы и программирование (ИС)')
async def group_is(message: types.Message):
    await message.reply("Выберите группу студента", reply_markup=nav.mainMenuIS)


@dp.message_handler(text='Сетевое и системное администрирование (СА)')
async def group_sa(message: types.Message):
    await message.reply("Выберите группу студента", reply_markup=nav.mainMenuSA)


@dp.message_handler(text='Обеспечение информационной безопасности телекоммуникационных систем (ИБТ)')
async def group_ibt(message: types.Message):
    await message.reply("Выберите группу студента", reply_markup=nav.mainMenuIBT)


@dp.message_handler(text='Обеспечение информационной безопасности автоматизированных систем (ИБА)')
async def group_iba(message: types.Message):
    await message.reply("Выберите группу студента", reply_markup=nav.mainMenuIBA)


@dp.callback_query_handler(text_contains="btn")
async def group_messange(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = call.data
    print(call.data)
    await Form.next()
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer("Введите ФИО студента")
    await Form.name.set()


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await Form.next()
    await message.reply("Введите ФИО родителя студента и номер телефона")


@dp.message_handler(state=Form.username)
async def process_age(message: types.Message, state: FSMContext):
    await Form.next()
    await state.update_data(age=message.text)
    async with state.proxy() as data:
        data['username'] = message.text
        await bot.send_message(message.chat.id, md.text("ФИО: " + md.text(data['name']),
                                                        "\nФИО родителя и номер: " + md.text(data['username']),
                                                        "\nГруппа: " + md.text(data['group']),
                                                        "\nЕсли ввели неверные данные введите команду /start"))
        print(md.text(data['name']))
        print(md.text(data['username']))
        cursor.execute('INSERT INTO Students(FIO, groupa, FIO_p) VALUES (?, ?, ?)',
                       (md.text(data['name']), md.text(data['group']), md.text(data['username'])))
        conn.commit()
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
