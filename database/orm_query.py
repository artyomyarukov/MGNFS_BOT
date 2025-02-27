from sqlalchemy.ext.asyncio import AsyncSession
from database.models import GlossesBalms, BalmInStick, BalmInIron, MaskForLip
from sqlalchemy import select,delete
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
async def orm_delete_product(session: AsyncSession, product_name: str, category: str):
    """
    Удаляет товар из базы данных по его названию и категории.
    """
    if category == "Блески-бальзамы":
        query = delete(GlossesBalms).where(GlossesBalms.name == product_name)
    elif category == "Бальзамы в стике":
        query = delete(BalmInStick).where(BalmInStick.name == product_name)
    elif category == "Бальзамы в железной баночке":
        query = delete(BalmInIron).where(BalmInIron.name == product_name)
    elif category == "Маски для губ":
        query = delete(MaskForLip).where(MaskForLip.name == product_name)
    else:
        raise ValueError("Неверная категория товара")

    result = await session.execute(query)
    await session.commit()

    # Проверяем, был ли удален хотя бы один товар
    if result.rowcount == 0:
        raise ValueError("Товар с таким названием не найден в указанной категории.")
async def orm_get_product_by_id(session: AsyncSession, product_id: int, category: str):
    """
    Получает товар по его ID и категории.
    """
    if category == "Блески-бальзамы":
        query = select(GlossesBalms).where(GlossesBalms.id == product_id)
    elif category == "Бальзамы в стике":
        query = select(BalmInStick).where(BalmInStick.id == product_id)
    elif category == "Бальзамы в железной баночке":
        query = select(BalmInIron).where(BalmInIron.id == product_id)
    elif category == "Маски для губ":
        query = select(MaskForLip).where(MaskForLip.id == product_id)
    else:
        raise ValueError("Неверная категория товара")

    result = await session.execute(query)
    return result.scalars().first()