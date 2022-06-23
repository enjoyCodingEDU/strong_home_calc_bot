import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import math



import config as cfg



logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

bot = Bot(token=cfg.API_TOKEN)
dp = Dispatcher(bot, storage = storage)


#-----------database connect----------------------------------------------


#-------------------------------States-----------------------------
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    uy_nomi = State()
    kv_metr = State()
    necha_oyga = State()
    kv_narx = State()
    qavat = State()
    bosh_foiz = State()
    ism_familiya = State()


@dp.message_handler(commands=['newhome'])
async def user_register(message: types.Message):
        await message.answer("Uy nomi :")
        await UserState.uy_nomi.set()

@dp.message_handler(state=UserState.uy_nomi)
async def uynomi(message: types.Message, state: FSMContext):
        await state.update_data(uy_nomi=message.text)
        await message.answer("Uyning KV metri (faqat raqam): ")
        await UserState.next() # либо же UserState.adress.set()

@dp.message_handler(state=UserState.kv_metr)
async def kv_metr(message: types.Message, state: FSMContext):
        await state.update_data(kv_metr=float(message.text))
        await message.answer("Necha oyga (faqat raqam): ")
        await UserState.next()
        
@dp.message_handler(state=UserState.necha_oyga)
async def necha_oyga(message: types.Message, state: FSMContext):
        await state.update_data(necha_oyga=int(message.text))
        await message.answer("KV metr uchun narx( millionda, raqamni o'zi yetarli )\n( Masalan : 3.2 ):")
        await UserState.next()

@dp.message_handler(state=UserState.kv_narx)
async def kv_narx(message: types.Message, state: FSMContext):
        await state.update_data(kv_narx=float(message.text))
        await message.answer("Uyning qavati (faqat raqam) : ")
        await UserState.next()

@dp.message_handler(state=UserState.qavat)
async def qavat(message: types.Message, state: FSMContext):
        await state.update_data(qavat=int(message.text))
        await message.answer("Uyning boshlang'ich foizi (faqat raqam):")
        await UserState.next()

@dp.message_handler(state=UserState.bosh_foiz)
async def bosh_foiz(message: types.Message, state: FSMContext):
        await state.update_data(bosh_foiz=int(message.text))
        await message.answer("Mijoz F I SH si : ")
        await UserState.next()

@dp.message_handler(state=UserState.ism_familiya)
async def ism_familiya(message: types.Message, state: FSMContext):
        await state.update_data(ism_familiya=message.text)
        
        dt = await state.get_data()

        #keltirib chiqarilgan qiymatlar
        umumiy_narx = round((dt['kv_narx'] * dt['kv_metr']), 3)
        bosh_tulov = round(((umumiy_narx/100)* dt['bosh_foiz']), 3)
        qolgan_tulov = round((umumiy_narx - bosh_tulov), 3)
        har_oyga = round((qolgan_tulov / dt['necha_oyga']), 3)


        #finish message
        await message.answer(f"""
➖➖➖➖ *STRONG HOME* ➖➖➖➖

*Mijoz👤:*
  F I SH : *{dt['ism_familiya']}*

*Uy haqida🏡:*
  Uy raqami : *{dt['uy_nomi']}*📄
  Uyning maydoni : *{dt['kv_metr']} kv.metr*📏
  Uyning qavati : *{dt['qavat']} - qavat*🏢

*Uyning narxi haqida💸 :* 
  Uyning umumiy narxi : *{umumiy_narx} mln. so'm 💰*
  Uyga boshlang'ich to'lov ( *{dt['bosh_foiz']}%* ): *{bosh_tulov} mln. so'm🪙*
  Qolgan to'lov : *{qolgan_tulov} mln. so'm💵*
  Har kv metrga : *{dt["kv_narx"]} mln. so'm💳*
  Har oyga ( *{dt["necha_oyga"]} oy* ): *{har_oyga} mln. so'mdan⚖️*

➖➖➖➖ *STRONG HOME* ➖➖➖➖
    """, parse_mode="Markdown")
        await state.finish()

#-----------------------------------code------------------

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
        user_id = message.from_user.id
        first_name = message.from_user.first_name

        await message.answer(f"Salom {first_name}👋\nBotdan to'laqonli foydalanishingiz mumkin ✅\n\nYangi uyni hisoblash uchun - /newhome")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)