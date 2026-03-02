"""Car listing ORM model."""

from decimal import Decimal

from sqlalchemy import Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class Car(Base):
    """Car listing synchronized from an external source."""

    __tablename__ = "cars"
    __table_args__ = (UniqueConstraint("source_url", name="uq_cars_source_url"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    make: Mapped[str] = mapped_column(String(100), index=True)
    model: Mapped[str] = mapped_column(String(100), index=True)
    year: Mapped[int] = mapped_column(Integer, index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), index=True)
    color: Mapped[str] = mapped_column(String(50), index=True)
    source_url: Mapped[str] = mapped_column(String(500), unique=True, index=True)
