from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import InputMediaPhoto  # Для создания медиагруппы

from database.orm_query import orm_get_glosses_balms, orm_get_balm_in_stick, orm_get_balm_in_iron, orm_get_mask_for_lip
from filters.chat_types import ChatTypeFilter
from keyboards.main import main_keyboard
from keyboards.products import glosses_balms_keyboard, balms_in_iron_keyboard, balms_in_stick_keyboard, \
    mask_for_lips_keyboard, yes_no_back_keyboard, format_product_kb, aromat_kb
from keyboards.reply import ASS_KB
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
    color_product = State()  # Новое состояние для выбора цвета
    aromat = State()


welcome_text = (
    "Давай выберем формат твоего продукта"
)


@router.message(Command("start"))
async def cmd_start(message: Message):
    file_path = "GUID.pdf"
    # Отправляем файл
    await message.answer_document(
        document=FSInputFile(file_path),  # Используем FSInputFile для загрузки файла
        caption="Памятка покупателю",  # Подпись к файлу
    )
    await message.answer(welcome_text, reply_markup=start_keyboard())


@router.callback_query(lambda query: query.data == "unique_product")
async def start_questionnaire(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text("Испытываете ли вы сухость губ?", reply_markup=yes_no_back_keyboard())
    await state.set_state(Questionnaire.dry_lips)


@router.callback_query(Questionnaire.dry_lips)
async def process_dry_lips(query: CallbackQuery, state: FSMContext):
    if query.data == "back":
        await query.message.edit_text(welcome_text, reply_markup=start_keyboard())
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
    await query.message.edit_text("Часто ли у вас воспаляется кожа на губах и в уголках губ?",
                                  reply_markup=yes_no_back_keyboard())
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
        await query.message.edit_text("Часто ли у вас воспаляется кожа на губах и в уголках губ?",
                                      reply_markup=yes_no_back_keyboard())
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


@router.callback_query(Questionnaire.allergies)
async def process_allergies(query: CallbackQuery, state: FSMContext):
    if query.data == "back":
        await query.message.edit_text("Курите ли вы?", reply_markup=yes_no_back_keyboard())
        await state.set_state(Questionnaire.smoke)
        return
    await state.update_data(allergies=query.data)
    await query.message.edit_text("Теперь выберем формат продукта", reply_markup=format_product_kb())
    await state.set_state(Questionnaire.format_product)
def color_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="01", callback_data="color_01")],
        [InlineKeyboardButton(text="02", callback_data="color_02")],
        [InlineKeyboardButton(text="03", callback_data="color_03")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]
    ])
    return keyboard


@router.callback_query(Questionnaire.format_product)
async def process_format_product(query: CallbackQuery, state: FSMContext):
    if query.data == "back":
        await query.message.edit_text("Есть ли у вас аллергия?", reply_markup=yes_no_back_keyboard())
        await state.set_state(Questionnaire.allergies)
        return
    await state.update_data(format_product=query.data)

    # Создаем медиагруппу с фотографиями
    media_group = [
        InputMediaPhoto(media=FSInputFile("color_1.jpg"), caption="Цвет 01"),
        InputMediaPhoto(media=FSInputFile("color_2.jpg"), caption="Цвет 02"),
        InputMediaPhoto(media=FSInputFile("color_3.jpg"), caption="Цвет 03")
    ]

    # Отправляем медиагруппу
    await query.message.answer_media_group(media=media_group)

    # Отправляем сообщение с выбором цвета
    await query.message.answer("Теперь выберете цвет продукта", reply_markup=color_keyboard())
    await state.set_state(Questionnaire.color_product)


@router.callback_query(Questionnaire.color_product)
async def process_color_product(query: CallbackQuery, state: FSMContext):
    if query.data == "back":
        # Возвращаем пользователя к выбору формата продукта
        await query.message.edit_text("Теперь выберем формат продукта", reply_markup=format_product_kb())
        await state.set_state(Questionnaire.format_product)
        return

    await state.update_data(color_product=query.data)

    # Переход к выбору аромата
    await query.message.answer("Теперь выберем аромат продукта", reply_markup=aromat_kb())
    await state.set_state(Questionnaire.aromat)


@router.callback_query(Questionnaire.aromat)
async def process_aromat(query: CallbackQuery, state: FSMContext):
    if query.data == "back":
        # Удаляем предыдущее сообщение (если нужно)
        await query.message.delete()

        # Создаем медиагруппу с фотографиями
        media_group = [
            InputMediaPhoto(media=FSInputFile("color_1.jpg"), caption="Цвет 01"),
            InputMediaPhoto(media=FSInputFile("color_2.jpg"), caption="Цвет 02"),
            InputMediaPhoto(media=FSInputFile("color_3.jpg"), caption="Цвет 03")
        ]

        # Отправляем медиагруппу
        await query.message.answer_media_group(media=media_group)

        # Отправляем сообщение с выбором цвета
        await query.message.answer("Теперь выберете цвет продукта", reply_markup=color_keyboard())
        await state.set_state(Questionnaire.color_product)
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
        "color_product": "Цвет продукта",
        "aromat": "Аромат"
    }
    formatted_responses = []
    for key, value in data.items():
        question = responses.get(key, key)
        answer = "Да" if value == "yes" else "Нет"
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
        if value == "color_01":
            answer = "01"
        if value == "color_02":
            answer = "02"
        if value == "color_03":
            answer = "03"
        formatted_responses.append(f"{question}: {answer}")

    # Собираем итоговое сообщение
    response_message = f"Ответы пользователя @{user_id} ({user_name}):\n" + "\n".join(formatted_responses)

    await query.message.edit_text(
        "Спасибо за ответы! Ваши данные сохранены.\nСкоро с вами свяжется менеджер для уточнения деталей и оформления заказа.\nПо всем вопросам писать @splvll или @itskkira\nЖелаете ли еще что-нибудь выбрать?",
        reply_markup=start_keyboard())
    await state.clear()
    # Отправка данных в определенный чат
    await query.bot.send_message(chat_id=-4612151315, text=response_message)
# Состояния для выбора готового продукта


from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class RProduct(StatesGroup):
    category_state = State()
    product_state = State()
    count = State()


# Хэндлер для выбора готового продукта
@router.callback_query(lambda query: query.data == "ready_product")
async def choose_product_type(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text("Выберите формат продукта", reply_markup=main_keyboard())
    await state.set_state(RProduct.category_state)


# Хэндлер для обработки выбора категории
@router.callback_query(RProduct.category_state)
async def handle_category_selection(query: CallbackQuery, state: FSMContext, session: AsyncSession):
    if query.data == "back_to_start":
        await query.message.edit_text(welcome_text, reply_markup=start_keyboard())
        await state.clear()
        return

    await state.update_data(category_state=query.data)

    if query.data == "glosses_balms":
        products = await orm_get_glosses_balms(session)
    elif query.data == "balms_in_iron":
        products = await orm_get_balm_in_iron(session)
    elif query.data == "balms_in_stick":
        products = await orm_get_balm_in_stick(session)
    elif query.data == "mask_for_lips":
        products = await orm_get_mask_for_lip(session)
    else:
        await query.answer("Неизвестная категория.")
        return

    if not products:
        await query.message.delete()
        await query.message.answer("Товары в этой категории отсутствуют. Выберите другую категорию:",
                                   reply_markup=main_keyboard())
        await state.set_state(RProduct.category_state)
        return

    for product in products:
        await query.message.answer_photo(
            photo=product.image,
            caption=f"Продукт: {product.category}\nНазвание: {product.name}\nЦена: {int(product.price)} руб.",
        )

    product_buttons = [
        [InlineKeyboardButton(text=product.name, callback_data=f"product_{product.name}")]
        for product in products
    ]
    product_buttons.append([InlineKeyboardButton(text="Назад", callback_data="ready_product")])

    products_kb = InlineKeyboardMarkup(inline_keyboard=product_buttons)

    await query.message.answer("Что хотите заказать?", reply_markup=products_kb)
    await state.set_state(RProduct.product_state)


# Хэндлер для обработки выбора товара
@router.callback_query(RProduct.product_state)
async def handle_product_selection(query: CallbackQuery, state: FSMContext):
    if query.data == "ready_product":
        await choose_product_type(query, state)
        return

    product_id = query.data.replace("product_", "")
    await state.update_data(product_id=product_id)

    # Создаем клавиатуру с кнопкой "Назад"
    back_button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back_to_product")]
    ])
    await query.message.delete()
    await query.message.answer("Укажите количество")
    await state.set_state(RProduct.count)


# Хэндлер для ввода количества
@router.message(RProduct.count)
async def handle_count_input(message: types.Message, state: FSMContext):
    try:
        count = int(message.text)
        if count <= 0:
            await message.answer("Количество должно быть больше нуля. Попробуйте снова.")
            return
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число.")
        return

    await state.update_data(count=count)
    data = await state.get_data()
    category = data.get("category_state")
    product_id = data.get("product_id")
    count = data.get("count")
    # Словарь для перевода категорий на русский
    category_translations = {
        "glosses_balms": "Блески и бальзамы",
        "balms_in_iron": "Бальзамы в железной упаковке",
        "balms_in_stick": "Бальзамы в стике",
        "mask_for_lips": "Маски для губ",
    }

    # Переводим категорию на русский
    category_ru = category_translations.get(category, category)
    username = message.from_user.username
    if not username:  # Если username отсутствует, используем first_name
        username = message.from_user.first_name

    target_chat_id = -4612151315
    await message.bot.send_message(
        chat_id=target_chat_id,
        text=f"Новый заказ:\nПользователь: @{username}\n"
             f"Категория: {category_ru}\nИмя товара: {product_id}\nКоличество: {count}"
    )

    await state.clear()
    await message.answer(
        "Ваш заказ успешно отправлен!\nСкоро с вами свяжеться менеджер\nПо всем вопросам писать - @itskkira или @splvll\nЖелаете ли заказать что-ниубудь еще? ",
        reply_markup=start_keyboard())
