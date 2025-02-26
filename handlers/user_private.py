from aiogram import Router, types
from aiogram.types import Message, CallbackQuery

from filters.chat_types import ChatTypeFilter
from keyboards.main import main_keyboard
from keyboards.products import glosses_balms_keyboard, balms_in_iron_keyboard, balms_in_stick_keyboard,mask_for_lips_keyboard
from utils.messages import get_product_added_message

router = Router()
from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.start import start_keyboard

router = Router()
router.message.filter(ChatTypeFilter(["private"]))


@router.message(Command("start"))
async def cmd_start(message: Message):
    welcome_text = (
        "Что хочешь приобрести?"
    )
    await message.answer(welcome_text, reply_markup=start_keyboard())



#хэндлеры для обработки готовых продуктов
@router.callback_query(lambda query: query.data in ["ready_product"])
async def choose_product_type(query: CallbackQuery):
    await query.message.edit_text("Выберите продукт", reply_markup=main_keyboard())



# после того как нажали что именно выбрать
# надо доделать клавы для отделльных товаров
@router.callback_query(lambda query: query.data in ["glosses_balms","balms_in_iron","balms_in_stick","mask_for_lips"])
async def choose_product_type(query: CallbackQuery):
    if query.data == "glosses_balms":
        await query.message.edit_text("Выберите бальзам:", reply_markup=glosses_balms_keyboard())
    elif query.data == "balms_in_iron":
        await query.message.edit_text("Выберите бальзам:", reply_markup=balms_in_iron_keyboard())
    elif query.data == "balms_in_stick":
        await query.message.edit_text("Выберите бальзам:", reply_markup=balms_in_stick_keyboard())
    elif query.data == "mask_for_lips":
        await query.message.edit_text("Выберите маску для губ:", reply_markup=mask_for_lips_keyboard())






