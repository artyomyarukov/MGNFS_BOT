from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Свой уникальный продукт", callback_data="unique_product")],
            [InlineKeyboardButton(text="Готовый продукт", callback_data="ready_product")],
            [InlineKeyboardButton(text="Открыть корзину 🛒", callback_data="cart")]
        ]
    )
    return keyboard