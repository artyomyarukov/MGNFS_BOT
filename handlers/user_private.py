from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from database.models import GlossesBalms, BalmInIron, BalmInStick, MaskForLip
from filters.chat_types import ChatTypeFilter
from keyboards.main import main_keyboard
from keyboards.products import glosses_balms_keyboard, balms_in_iron_keyboard, balms_in_stick_keyboard, \
    mask_for_lips_keyboard, yes_no_back_keyboard, format_product_kb, aromat_kb
from utils.messages import get_product_added_message
from aiogram.types import InputMediaPhoto
from sqlalchemy import select
from sqlalchemy.orm import Session

router = Router()
from aiogram import Router, types, Bot
from aiogram.filters import Command, state
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.start import start_keyboard

router = Router()
router.message.filter(ChatTypeFilter(["private"]))

class Questionnaire(StatesGroup):
    dry_lips = State()
    cracked_lips = State()
    inflamed_lips = State()
    peeling_lips = State()
    chapped_lips = State()
    bite_lips = State()
    smoke = State()
    allergies = State()
    format_product = State()
    aromat = State()



@router.message(Command("start"))
async def cmd_start(message: Message):
    welcome_text = (
        "Что хочешь приобрести?"
    )
    await message.answer(welcome_text, reply_markup=start_keyboard())
@router.callback_query(lambda query: query.data == "unique_product")
async def start_questionnaire(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text("Испытываете ли вы сухость губ?", reply_markup=yes_no_back_keyboard())
    await state.set_state(Questionnaire.dry_lips)

@router.callback_query(Questionnaire.dry_lips)
async def process_dry_lips(query: CallbackQuery, state: FSMContext):
    if query.data == "back":
        await query.message.edit_text("Что хочешь приобрести?", reply_markup=start_keyboard())
        await state.clear()
        return
    await state.update_data(dry_lips=query.data)
    await query.message.edit_text("Трескаются ли у вас губы?", reply_markup=yes_no_back_keyboard())
    await state.set_state(Questionnaire.cracked_lips)

@router.callback_query(Questionnaire.cracked_lips)
async def process_cracked_lips(query: CallbackQuery, state: FSMContext):
    if query.data == "back":
        await query.message.edit_text("Испытываете ли вы сухость губ?", reply_markup=yes_no_back_keyboard())
        await state.set_state(Questionnaire.dry_lips)
        return
    await state.update_data(cracked_lips=query.data)
    await query.message.edit_text("Часто ли у вас воспаляется кожа на губах и в уголках губ?", reply_markup=yes_no_back_keyboard())
    await state.set_state(Questionnaire.inflamed_lips)

@router.callback_query(Questionnaire.inflamed_lips)
async def process_inflamed_lips(query: CallbackQuery, state: FSMContext):
    if query.data == "back":
        await query.message.edit_text("Трескаются ли у вас губы?", reply_markup=yes_no_back_keyboard())
        await state.set_state(Questionnaire.cracked_lips)
        return
    await state.update_data(inflamed_lips=query.data)
    await query.message.edit_text("Присутствует ли у вас на губах шелушения?", reply_markup=yes_no_back_keyboard())
    await state.set_state(Questionnaire.peeling_lips)

@router.callback_query(Questionnaire.peeling_lips)
async def process_peeling_lips(query: CallbackQuery, state: FSMContext):
    if query.data == "back":
        await query.message.edit_text("Часто ли у вас воспаляется кожа на губах и в уголках губ?", reply_markup=yes_no_back_keyboard())
        await state.set_state(Questionnaire.inflamed_lips)
        return
    await state.update_data(peeling_lips=query.data)
    await query.message.edit_text("Обветриваются ли у вас губы?", reply_markup=yes_no_back_keyboard())
    await state.set_state(Questionnaire.chapped_lips)

@router.callback_query(Questionnaire.chapped_lips)
async def process_chapped_lips(query: CallbackQuery, state: FSMContext):
    if query.data == "back":
        await query.message.edit_text("Присутствует ли у вас на губах шелушения?", reply_markup=yes_no_back_keyboard())
        await state.set_state(Questionnaire.peeling_lips)
        return
    await state.update_data(chapped_lips=query.data)
    await query.message.edit_text("Кусаете ли вы губы?", reply_markup=yes_no_back_keyboard())
    await state.set_state(Questionnaire.bite_lips)

@router.callback_query(Questionnaire.bite_lips)
async def process_bite_lips(query: CallbackQuery, state: FSMContext):
    if query.data == "back":
        await query.message.edit_text("Обветриваются ли у вас губы?", reply_markup=yes_no_back_keyboard())
        await state.set_state(Questionnaire.chapped_lips)
        return
    await state.update_data(bite_lips=query.data)
    await query.message.edit_text("Курите ли вы?", reply_markup=yes_no_back_keyboard())
    await state.set_state(Questionnaire.smoke)

@router.callback_query(Questionnaire.smoke)
async def process_smoke(query: CallbackQuery, state: FSMContext):
    if query.data == "back":
        await query.message.edit_text("Кусаете ли вы губы?", reply_markup=yes_no_back_keyboard())
        await state.set_state(Questionnaire.bite_lips)
        return
    await state.update_data(smoke=query.data)
    await query.message.edit_text("Есть ли у вас аллергия?", reply_markup=yes_no_back_keyboard())
    await state.set_state(Questionnaire.allergies)

'''
@router.callback_query(Questionnaire.allergies)
async def process_allergies(query: CallbackQuery, state: FSMContext):
    if query.data == "back":
        await query.message.edit_text("Курите ли вы?", reply_markup=yes_no_back_keyboard())
        await state.set_state(Questionnaire.smoke)
        return
    await state.update_data(allergies=query.data)
    data = await state.get_data()
    user_name = query.from_user.full_name
    user_id = query.from_user.username if query.from_user.username else f"ID: {query.from_user.id}"
    # Преобразуем ответы в читаемый формат
    responses = {
        "dry_lips": "Сухость губ",
        "cracked_lips": "Трескаются ли губы",
        "inflamed_lips": "Воспаление кожи на губах",
        "peeling_lips": "Шелушение губ",
        "chapped_lips": "Обветривание губ",
        "bite_lips": "Кусание губ",
        "smoke": "Курение",
        "allergies": "Аллергии"
    }

    formatted_responses = []
    for key, value in data.items():
        question = responses.get(key, key)  # Получаем понятный текст вопроса
        answer = "Да" if value == "yes" else "Нет"  # Преобразуем ответ в "Да" или "Нет"
        formatted_responses.append(f"{question}: {answer}")

    # Собираем итоговое сообщение
    response_message = f"Ответы пользователя @{user_id} ({user_name}):\n" + "\n".join(formatted_responses)

    await query.message.edit_text("Спасибо за ответы! Ваши данные сохранены.\nСкоро с вами свяжется менеджер для уточнения деталей и оформления заказа.\nПо всем вопросам писать @splvll или @itskkira\nЖелаете ли еще что-нибудь выбрать?",reply_markup=start_keyboard())
    await state.clear()
    # Отправка данных в определенный чат
    await query.bot.send_message(chat_id=-4612151315, text=response_message)
    
'''
@router.callback_query(Questionnaire.allergies)
async def process_allergies(query: CallbackQuery, state: FSMContext):
    if query.data == "back":
        await query.message.edit_text("Курите ли вы?", reply_markup=yes_no_back_keyboard())
        await state.set_state(Questionnaire.smoke)
        return
    await state.update_data(allergies=query.data)
    await query.message.edit_text("Теперь выберем формат продукта", reply_markup=format_product_kb())
    await state.set_state(Questionnaire.format_product)

@router.callback_query(Questionnaire.format_product)
async def process_allergies(query: CallbackQuery, state: FSMContext):
    if query.data == "back":
        await query.message.edit_text("Есть ли у вас аллергия", reply_markup=yes_no_back_keyboard())
        await state.set_state(Questionnaire.allergies)
        return
    await state.update_data(format_product=query.data)
    await query.message.edit_text("Теперь выберем аромат продукта", reply_markup=aromat_kb())
    await state.set_state(Questionnaire.aromat)


@router.callback_query(Questionnaire.aromat)
async def process_allergies(query: CallbackQuery, state: FSMContext):
    if query.data == "back":
        await query.message.edit_text("Теперь выберем формат продукта", reply_markup=format_product_kb())
        await state.set_state(Questionnaire.format_product)
        return
    await state.update_data(aromat=query.data)
    data = await state.get_data()
    user_name = query.from_user.full_name
    user_id = query.from_user.username if query.from_user.username else f"ID: {query.from_user.id}"
    # Преобразуем ответы в читаемый формат
    responses = {
        "dry_lips": "Сухость губ",
        "cracked_lips": "Трескаются ли губы",
        "inflamed_lips": "Воспаление кожи на губах",
        "peeling_lips": "Шелушение губ",
        "chapped_lips": "Обветривание губ",
        "bite_lips": "Кусание губ",
        "smoke": "Курение",
        "allergies": "Аллергии",
        "format_product": "Формат продукта",
        "aromat": "Аромат"
    }
    formatted_responses = []
    for key, value in data.items():
        question = responses.get(key, key)# Получаем понятный текст вопроса
        answer = "Да"
        if value == "no":
            answer = "Нет"
        if value == "f_cherry":
            answer = "Вишня"
        if value == "f_plombir":
            answer = "Пломбир"
        if value == "f_granat_kl":
            answer = "Гранат-клюква"
        if value == "f_no_aromat":
            answer = "Без запаха"
        if value == "f_glosses_balms":
            answer = "Блес-бальзам"
        if value == "f_balms_in_iron":
            answer = "Бальзам в железной баночке"
        if value == "f_balms_in_stick":
            answer = "Бальзам в стике"
        if value == "f_mask_for_lips":
            answer = "Маска для губ"
        formatted_responses.append(f"{question}: {answer}")

    # Собираем итоговое сообщение
    response_message = f"Ответы пользователя @{user_id} ({user_name}):\n" + "\n".join(formatted_responses)

    await query.message.edit_text(
        "Спасибо за ответы! Ваши данные сохранены.\nСкоро с вами свяжется менеджер для уточнения деталей и оформления заказа.\nПо всем вопросам писать @splvll или @itskkira\nЖелаете ли еще что-нибудь выбрать?",
        reply_markup=start_keyboard())
    await state.clear()
    # Отправка данных в определенный чат
    await query.bot.send_message(chat_id=-4612151315, text=response_message)

#хэндлеры для обработки готовых продуктов
@router.callback_query(lambda query: query.data in ["ready_product"])
async def choose_product_type(query: CallbackQuery):
    await query.message.edit_text("Выберите продукт", reply_markup=main_keyboard())





