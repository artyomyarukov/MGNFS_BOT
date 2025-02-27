from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# клава для готовых продуктов
def main_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Блеск-бальзам (15 гр)", callback_data="glosses_balms")],
            [InlineKeyboardButton(text="Бальзам в железной баночке (15 гр)", callback_data="balms_in_iron")],
            [InlineKeyboardButton(text="Бальзам в стике (5 гр)", callback_data="balms_in_stick")],
            [InlineKeyboardButton(text="Маска для губ", callback_data="mask_for_lips")],
            [InlineKeyboardButton(text="Назад", callback_data="back_to_start")]
        ]
    )
    return keyboard