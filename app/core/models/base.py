from datetime import datetime
from sqlalchemy import BigInteger, TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=func.now(), onupdate=func.now()
    )
