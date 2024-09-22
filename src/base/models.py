from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

FK = ForeignKey
mc = mapped_column


class BaseDBModel(DeclarativeBase):
    """
    Базовая модель от нее наследуются все модели в проекте.
    Служит так же для соединения всех данных таблиц между собой в проекте (metadata)
    """

    id: Mapped[int] = mc(primary_key=True)
