from aiogram import Bot, Dispatcher, F
import asyncio
from aiogram.types import (Message, ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
from models import bot_token, craete_table, connect, register, get_user
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class Register(StatesGroup):
    full_name = State()
    phone = State()
    address = State()

bot = Bot(token=bot_token)

dp = Dispatcher()


@dp.message(F.text == '/start')
async def start(message: Message):  #type hint
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Regiter', style='danger'), KeyboardButton(text='About us')],
            [KeyboardButton(text='My Profile')],
        ], resize_keyboard=True
    )
    await message.answer('Salom', reply_markup=markup)


@dp.message(F.text == 'My Profile')
async def start(message: Message, state: FSMContext):  #type hint
    user =   await get_user(message.from_user.id)
    
    print(user['full_name'], 'fulname')
    if not user:
        await message.answer('u dont have profile yet') 
        return
    await message.answer(f"Usernam: {user['full_name']}")
    

@dp.message(F.text == 'Regiter')
async def start(message: Message, state: FSMContext):  #type hint
    if  await get_user(message.from_user.id):
        await message.answer('U aready registered')
        return
    await message.answer('Send ur fullname plz')
    await state.set_state(Register.full_name)

@dp.message(Register.full_name)
async def geting_name(message: Message, state: FSMContext):
    if len(message.text)<3:
        await message.answer('Name shoudl be more then 3 letters or equal')
        return
    await state.update_data(full_name=message.text)
    contact = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Send ur number', request_contact=True)]
        ], resize_keyboard=True, one_time_keyboard=True
    )
    await message.answer('Now Enter ur phone', reply_markup=contact)
    await state.set_state(Register.phone)


@dp.message(Register.phone, F.contact)
async def getting_contact(message: Message, state:FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    print(message.text, message.contact)
    
    await message.answer('Now Enter ur addrsse')
    await state.set_state(Register.address)

    
@dp.message(Register.address)
async def getting_contact(message: Message, state:FSMContext):
    data = await state.get_data()
    print(data)
    user = message.from_user
    await register(user.id, user.username, data['full_name'], data['phone'], message.text)
    await message.answer('Regisered successfullyt')
    await state.clear()



async def main():
    print('started bot')
    await connect()
    await craete_table()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())