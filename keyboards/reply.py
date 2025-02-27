from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_keyboard(
        *btns: str,
        placeholder: str = None,
        request_contact: int = None,
        request_location: int = None,
        sizes: tuple[int] = (2,),
):

    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(btns, start=0):

        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))

        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True, input_field_placeholder=placeholder)



ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Удалить товар",
    "Ассортимент",
    "Вернуться в главное меню",  # Новая кнопка
    placeholder="Выберите действие",
    sizes=(2,2),
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
