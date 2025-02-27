from string import punctuation

from aiogram import F, Bot, types, Router
from aiogram.filters import Command, BaseFilter

from filters.chat_types import ChatTypeFilter

ALLOWED_CHAT_IDS = [-4612151315]
class AllowedChatFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return message.chat.id in ALLOWED_CHAT_IDS


user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(["group", "supergroup"]), AllowedChatFilter())
user_group_router.edited_message.filter(ChatTypeFilter(["group", "supergroup"]), AllowedChatFilter())


@user_group_router.message(Command("admin"))
async def get_admins(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)
    #просмотреть все данные и свойства полученных объектов
    #print(admins_list)
    # Код ниже это генератор списка, как и этот x = [i for i in range(10)]
    admins_list = [
        member.user.id
        for member in admins_list
        if member.status == "creator" or member.status == "administrator"
    ]
    bot.my_admins_list = admins_list
    if message.from_user.id in admins_list:
        await message.delete()
    #print(admins_list)


def clean_text(text: str):
    return text.translate(str.maketrans("", "", punctuation))


