from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

from database.orm_query import (
    orm_add_product,
    orm_get_glosses_balms,
    orm_get_balm_in_stick,
    orm_get_balm_in_iron,
    orm_get_mask_for_lip,
    orm_delete_product,
)
from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.reply import get_keyboard, ADMIN_KB, ASS_KB, BACK_KB
from keyboards.inline import start_keyboard

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

# Машина состояний (FSM) для добавления товара
class AddProduct(StatesGroup):
    category = State()
    name = State()
    price = State()
    image = State()

    texts = {
        'AddProduct:category': 'Выберите категорию заново',
        'AddProduct:name': 'Введите название заново:',
        'AddProduct:price': 'Введите стоимость заново:',
        'AddProduct:image': 'Этот стейт последний, поэтому...',
    }

# Состояния для удаления товара
class DeleteProduct(StatesGroup):
    category = State()
    product_name = State()

# Состояния для просмотра ассортимента
class ViewAssortment(StatesGroup):
    category = State()

# Хэндлер для команды /admin
@admin_router.message(Command("admin"))
async def admin_features(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)


@admin_router.message(F.text == "Вернуться в главное меню")
async def back_to_main_menu(message: types.Message, state: FSMContext):
    await state.clear()  # Очищаем состояние
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Свой уникальный продукт", callback_data="unique_product")],
            [InlineKeyboardButton(text="Готовый продукт", callback_data="ready_product")]
        ]
    )
    # Получаем инлайн-клавиатуру главного меню
    await message.answer(
        "Вы вернулись в главное меню",
        reply_markup=ReplyKeyboardRemove(),  # Удаляем клавиатуру админа
    )
    await message.answer("Выберите действие:", reply_markup=keyboard)  # Показываем инлайн-клавиатуру

# Хэндлер для начала удаления товара
@admin_router.message(F.text == "Удалить товар")
async def start_delete_product(message: types.Message, state: FSMContext):
    await message.answer("Выберите категорию товара для удаления:", reply_markup=ASS_KB)
    await state.set_state(DeleteProduct.category)

# Хэндлер для выбора категории при удалении товара
@admin_router.message(DeleteProduct.category, F.text)
async def choose_category_for_delete(message: types.Message, state: FSMContext):
    if message.text == "Назад к админ панели":  # Возврат в админ-панель
        await state.clear()
        await message.answer("Возвращаемся в админ-панель.", reply_markup=ADMIN_KB)
        return

    if message.text not in ["Блески-бальзамы", "Бальзамы в стике", "Бальзамы в железной баночке", "Маски для губ"]:
        await message.answer("Пожалуйста, выберите категорию из списка.", reply_markup=ASS_KB)
        return

    await state.update_data(category=message.text)
    await message.answer("Введите название товара для удаления:", reply_markup=BACK_KB)
    await state.set_state(DeleteProduct.product_name)

# Хэндлер для удаления товара по названию
@admin_router.message(DeleteProduct.product_name, F.text)
async def delete_product_by_name(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text == "Назад":  # Возврат к выбору категории
        await state.set_state(DeleteProduct.category)
        await message.answer("Выберите категорию товара для удаления:", reply_markup=ASS_KB)
        return

    product_name = message.text.strip()
    if not product_name:
        await message.answer("Пожалуйста, введите корректное название товара.", reply_markup=BACK_KB)
        return

    data = await state.get_data()
    category = data["category"]

    try:
        await orm_delete_product(session, product_name, category)
        await message.answer(f"Товар '{product_name}' успешно удален из категории {category}.", reply_markup=ADMIN_KB)
        await state.clear()  # Очищаем состояние после успешного удаления
    except ValueError as e:
        await message.answer(f"Ошибка: {str(e)}\nПопробуйте ввести название еще раз или нажмите 'Назад'.", reply_markup=BACK_KB)
    except Exception as e:
        await message.answer(f"Произошла ошибка при удалении товара: {str(e)}\nПопробуйте ввести название еще раз или нажмите 'Назад'.", reply_markup=BACK_KB)

# Хэндлер для начала просмотра ассортимента
@admin_router.message(F.text == "Ассортимент")
async def start_view_assortment(message: types.Message, state: FSMContext):
    await message.answer("Выберите категорию для просмотра ассортимента:", reply_markup=ASS_KB)
    await state.set_state(ViewAssortment.category)

# Хэндлер для выбора категории при просмотре ассортимента
@admin_router.message(ViewAssortment.category, F.text)
async def choose_category_for_view(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text == "Назад к админ панели":  # Возврат в админ-панель
        await state.clear()
        await message.answer("Возвращаемся в админ-панель.", reply_markup=ADMIN_KB)
        return

    if message.text not in ["Блески-бальзамы", "Бальзамы в стике", "Бальзамы в железной баночке", "Маски для губ"]:
        await message.answer("Пожалуйста, выберите категорию из списка.", reply_markup=ASS_KB)
        return

    # Сохраняем выбранную категорию
    await state.update_data(category=message.text)

    # Получаем товары из выбранной категории
    if message.text == "Блески-бальзамы":
        products = await orm_get_glosses_balms(session)
    elif message.text == "Бальзамы в стике":
        products = await orm_get_balm_in_stick(session)
    elif message.text == "Бальзамы в железной баночке":
        products = await orm_get_balm_in_iron(session)
    elif message.text == "Маски для губ":
        products = await orm_get_mask_for_lip(session)

    if not products:
        await message.answer("Товары в этой категории отсутствуют.", reply_markup=ASS_KB)
        return

    # Выводим товары
    for product in products:
        await message.answer_photo(
            photo=product.image,
            caption=f"Категория: {product.category}\nНазвание: {product.name}\nЦена: {int(product.price)} руб.",
        )

    await message.answer("Выберите следующее действие:", reply_markup=ASS_KB)

# Хэндлер для добавления товара
@admin_router.message(StateFilter(None), F.text == "Добавить товар")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer("Выберите категорию товара", reply_markup=ASS_KB)
    await state.set_state(AddProduct.category)

# Хэндлер для отмены и сброса состояния
@admin_router.message(StateFilter('*'), Command("отмена"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)

# Хэндлер для возврата на шаг назад
@admin_router.message(StateFilter('*'), Command("назад"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AddProduct.category:
        await message.answer('Предыдущего шага нет. Выберите категорию или напишите "отмена".', reply_markup=ASS_KB)
        return

    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n{AddProduct.texts[previous.state]}", reply_markup=BACK_KB if previous != AddProduct.category else ASS_KB)
            return
        previous = step
#выбор категории
@admin_router.message(AddProduct.category, F.text)
async def add_category(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await back_step_handler(message, state)
        return
    elif message.text == "Назад к админ панели":  # Обработка кнопки "Назад к админ панели"
        await state.clear()
        await message.answer("Возвращаемся в админ-панель.", reply_markup=ADMIN_KB)
        return

    if message.text not in ["Блески-бальзамы", "Бальзамы в стике", "Бальзамы в железной баночке", "Маски для губ"]:
        await message.answer("Пожалуйста, выберите категорию из списка.", reply_markup=ASS_KB)
        return

    await state.update_data(category=message.text)
    await message.answer("Введите название товара", reply_markup=BACK_KB)
    await state.set_state(AddProduct.name)


# Хэндлер для ввода названия товара
@admin_router.message(AddProduct.name, F.text)
async def add_name(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await back_step_handler(message, state)
        return

    if len(message.text) >= 100:
        await message.answer("Название товара не должно превышать 100 символов. Введите заново.")
        return

    await state.update_data(name=message.text)
    await message.answer("Введите цену", reply_markup=BACK_KB)
    await state.set_state(AddProduct.price)

# Хэндлер для ввода цены
@admin_router.message(AddProduct.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await back_step_handler(message, state)
        return

    try:
        int(message.text)
    except ValueError:
        await message.answer("Введите корректное значение цены.")
        return

    await state.update_data(price=message.text)
    await message.answer("Загрузите изображение товара", reply_markup=BACK_KB)
    await state.set_state(AddProduct.image)

# Хэндлер для загрузки изображения
@admin_router.message(AddProduct.image, F.photo)
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()

    try:
        await orm_add_product(session, data)
        await message.answer("Товар добавлен", reply_markup=ADMIN_KB)
        await state.clear()
    except Exception as e:
        await message.answer(f"Ошибка добавления товара: {str(e)}")
        await state.clear()