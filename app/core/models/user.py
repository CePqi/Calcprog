from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import TEXT, LargeBinary
from .base import Base

class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(TEXT, nullable=False, unique=True)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    def __repr__(self) -> str:
        return f"<User email={self.email}, password={self.password}>"