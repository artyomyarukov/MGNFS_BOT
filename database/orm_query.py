from sqlalchemy.ext.asyncio import AsyncSession
from database.models import GlossesBalms, BalmInStick, BalmInIron, MaskForLip
from sqlalchemy import select
async def orm_add_product(session: AsyncSession, data: dict):
    # Проверка данных
    required_fields = ["category", "name", "price", "image"]
    if not all(field in data for field in required_fields):
        raise ValueError("Не все обязательные поля заполнены")

    # Определяем категорию
    category = data["category"]

    # Сопоставляем категорию с моделью
    model_mapping = {
        "Бальзамы в железной баночке": BalmInStick,
        "Бальзамы в стике": BalmInIron,
        "Маски для губ": MaskForLip,
    }

    # Выбираем модель по категории, по умолчанию — GlossesBalms
    model = model_mapping.get(category, GlossesBalms)

    # Создаем объект
    obj = model(
        category=category,
        name=data["name"],
        price=int(data["price"]),
        image=data["image"],
    )

    # Добавляем объект в сессию и сохраняем
    session.add(obj)
    await session.commit()

async def orm_get_glosses_balms(session: AsyncSession):
    query = select(GlossesBalms)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_balm_in_stick(session: AsyncSession):
    query = select(BalmInStick)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_balm_in_iron(session: AsyncSession):
    query = select(BalmInIron)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_mask_for_lip(session: AsyncSession):
    query = select(MaskForLip)
    result = await session.execute(query)
    return result.scalars().all()