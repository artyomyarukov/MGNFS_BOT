from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def glosses_balms_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Шоколад", callback_data=" glosses_balms_1")],
            [InlineKeyboardButton(text="Кокос", callback_data=" glosses_balms_2")],
            [InlineKeyboardButton(text="Вишневое благословение", callback_data=" glosses_balms_3")],
            [InlineKeyboardButton(text="Childhood dream", callback_data=" glosses_balms_4")],
            [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
        ]
    )
    return keyboard

def balms_in_iron_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Бальзам с запахом вишни", callback_data="balms_in_iron_01")],
            [InlineKeyboardButton(text="Бальзам с запахом шоколада", callback_data="balms_in_iron_02")],
            [InlineKeyboardButton(text="Бальзам с запахом пломбира", callback_data="balms_in_iron_03")],
            [InlineKeyboardButton(text="Бальзам с запахом кокоса", callback_data="balms_in_iron_04")],
            [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
        ]
    )
    return keyboard
def balms_in_stick_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Бальзам с запахом кокоса", callback_data="balms_in_stick_01")],
            [InlineKeyboardButton(text="Бальзам с запахом клюквы", callback_data="balms_in_stick_02")],
            [InlineKeyboardButton(text="Бальзам с запахом шоколада", callback_data="balms_in_stick_03")],
            [InlineKeyboardButton(text="Бальзам с запахом пломбира", callback_data="balms_in_stick_04")],
            [InlineKeyboardButton(text="Бальзам с запахом вишни", callback_data="balms_in_stick_05")],
            [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
        ]
    )
    return keyboard
def mask_for_lips_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
        ]
    )
    return keyboard