from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.orm_query import (
    orm_add_product,
    orm_get_glosses_balms,
    orm_get_balm_in_stick,
    orm_get_balm_in_iron,
    orm_get_mask_for_lip,
)
from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.reply import get_keyboard

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

# Клавиатуры
ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Удалить товар",
    "Ассортимент",
    placeholder="Выберите действие",
    sizes=(2, 1),
)

ASS_KB = get_keyboard(
    "Блески-бальзамы",
    "Бальзамы в железной баночке",
    "Бальзамы в стике",
    "Маски для губ",
    "Назад к админ панели",
    placeholder="Выберите категорию",
    sizes=(2, 2),
)

BACK_KB = get_keyboard(
    "Назад",
    placeholder="Вернуться назад",
    sizes=(1,),
)

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

# Хэндлер для команды /admin
@admin_router.message(Command("admin"))
async def admin_features(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)
@admin_router.message(F.text=="Назад к админ панели")
async def admin_features(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)


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

# Хэндлеры для добавления товара (FSM)
@admin_router.message(AddProduct.category, F.text)
async def add_category(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await back_step_handler(message, state)
        return

    await state.update_data(category=message.text)
    await message.answer("Введите название товара", reply_markup=BACK_KB)
    await state.set_state(AddProduct.name)

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

@admin_router.message(AddProduct.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await back_step_handler(message, state)
        return

    try:
        float(message.text)
    except ValueError:
        await message.answer("Введите корректное значение цены.")
        return

    await state.update_data(price=message.text)
    await message.answer("Загрузите изображение товара", reply_markup=BACK_KB)
    await state.set_state(AddProduct.image)

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

# Хэндлеры для просмотра ассортимента
@admin_router.message(F.text == "Ассортимент")
async def view_assortment(message: types.Message):
    await message.answer("Выберите категорию для просмотра ассортимента:", reply_markup=ASS_KB)

@admin_router.message(F.text == "Блески-бальзамы")
async def view_glosses_balms(message: types.Message, session: AsyncSession):
    products = await orm_get_glosses_balms(session)
    if not products:
        await message.answer("Товары в этой категории отсутствуют.", reply_markup=ASS_KB)
        return

    for product in products:
        await message.answer_photo(
            photo=product.image,
            caption=f"Категория: {product.category}\nНазвание: {product.name}\nЦена: {int(product.price)} руб.",  # Преобразуем цену в int
        )
    await message.answer("Выберите следующее действие:", reply_markup=ASS_KB)

@admin_router.message(F.text == "Бальзамы в стике")
async def view_balm_in_stick(message: types.Message, session: AsyncSession):
    products = await orm_get_balm_in_stick(session)
    if not products:
        await message.answer("Товары в этой категории отсутствуют.", reply_markup=ASS_KB)
        return

    for product in products:
        await message.answer_photo(
            photo=product.image,
            caption=f"Категория: {product.category}\nНазвание: {product.name}\nЦена: {int(product.price)} руб.",  # Преобразуем цену в int
        )
    await message.answer("Выберите следующее действие:", reply_markup=ASS_KB)

@admin_router.message(F.text == "Бальзамы в железной баночке")
async def view_balm_in_iron(message: types.Message, session: AsyncSession):
    products = await orm_get_balm_in_iron(session)
    if not products:
        await message.answer("Товары в этой категории отсутствуют.", reply_markup=ASS_KB)
        return

    for product in products:
        await message.answer_photo(
            photo=product.image,
            caption=f"Категория: {product.category}\nНазвание: {product.name}\nЦена: {int(product.price)} руб.",  # Преобразуем цену в int
        )
    await message.answer("Выберите следующее действие:", reply_markup=ASS_KB)

@admin_router.message(F.text == "Маски для губ")
async def view_mask_for_lip(message: types.Message, session: AsyncSession):
    products = await orm_get_mask_for_lip(session)
    if not products:
        await message.answer("Товары в этой категории отсутствуют.", reply_markup=ASS_KB)
        return

    for product in products:
        await message.answer_photo(
            photo=product.image,
            caption=f"Категория: {product.category}\nНазвание: {product.name}\nЦена: {int(product.price)} руб.",  # Преобразуем цену в int
        )
    await message.answer("Выберите следующее действие:", reply_markup=ASS_KB)