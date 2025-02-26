from sqlalchemy import DateTime, Integer, String, Text, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(150), nullable=False)


class GlossesBalms(Base):
    __tablename__ = 'glosses_balms'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String(150), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)  # Изменено на Integer
    image: Mapped[str] = mapped_column(String(150))


class BalmInStick(Base):
    __tablename__ = 'balm_in_sticks'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String(150), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)  # Изменено на Integer
    image: Mapped[str] = mapped_column(String(150))


class BalmInIron(Base):
    __tablename__ = 'balm_in_irons'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String(150), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)  # Изменено на Integer
    image: Mapped[str] = mapped_column(String(150))


class MaskForLip(Base):
    __tablename__ = 'mask_for_lips'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String(150), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)  # Изменено на Integer
    image: Mapped[str] = mapped_column(String(150))