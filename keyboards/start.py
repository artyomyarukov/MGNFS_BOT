from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Свой уникальный продукт", callback_data="unique_product")],
            [InlineKeyboardButton(text="Готовый продукт", callback_data="ready_product")]
        ]
    )
    return keyboard