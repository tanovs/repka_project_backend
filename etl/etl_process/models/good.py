from etl_process.models.association_tables import HorecaBasket
from etl_process.models.mixin import Base, TimeStampMixin, UUIDMixin
from sqlalchemy import BINARY, INTEGER, Column, ForeignKey
from sqlalchemy.orm import relationship


class Good(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'good'

    photo = Column('photo', BINARY)
    price = Column('price', INTEGER, nullable=False)
    volume = Column('volume', INTEGER, nullable=False)
    balance = Column('balance', INTEGER, nullable=False)
    calories = Column('calories', INTEGER, nullable=False)
    proteins = Column('proteins', INTEGER, nullable=False)
    fats = Column('fats', INTEGER, nullable=False)
    carbohydrates = Column('carbohydrates', INTEGER, nullable=False)

    supplier_id = Column('supplier_id', ForeignKey('supplier.id'))
    good_category = relationship('GoodCategory', uselist=False)
    good_tag = relationship('GoodTag', uselist=False)

    horecas = relationship(
        'Good',
        secondary=HorecaBasket,
        back_populates='goods',
    )
