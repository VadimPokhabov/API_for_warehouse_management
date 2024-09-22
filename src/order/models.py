from datetime import date
from enum import Enum
from sqlalchemy import func, Enum as EnumType
from sqlalchemy.orm import Mapped
from src.base.models import BaseDBModel, mc


class Status(str, Enum):
    one_hour = 'В процессе'
    one_day = 'Отправлен'
    seven_days = 'Доставлен'


class Order(BaseDBModel):
    __tablename__ = "order"
    create_date: Mapped[date] = mc(server_default=func.now())
    status: Mapped[str] = mc(EnumType(Status), nullable=True)
