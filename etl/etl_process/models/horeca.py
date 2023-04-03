from etl_process.models.association_tables import HorecaBasket, HorecaFavourite
from etl_process.models.mixin import Base, TimeStampMixin, UUIDMixin
from sqlalchemy import TEXT, Column, ForeignKey
from sqlalchemy.orm import relationship


class Horeca(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'horeca'

    password = Column('password', TEXT, nullable=False)
    name = Column('name', TEXT, nullable=False)
    company_name = Column('company_name', TEXT, nullable=False)
    phone_number = Column('phone_number', TEXT, nullable=False)
    email = Column('email', TEXT, nullable=False)
    ooo = Column('ooo', TEXT)
    inn = Column('inn', TEXT)
    bank_account = Column('bank_account', TEXT)

    restaurants = relationship('Restaurant')
    suppliers = relationship(
        'Supplier',
        secondary=HorecaFavourite,
        back_populates='horecas',
    )
    goods = relationship(
        'Good',
        secondary=HorecaBasket,
        back_populates='horecas',
    )


class Restaurant(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'restaurant'

    restaurant_name = Column('restaurant_name', TEXT, nullable=False)
    restaurant_theme = Column('restaurant_theme', TEXT)
    horeca_id = Column('horeca_id', ForeignKey('horeca.id'))

    adresses = relationship('RestaurantAdress')


class RestaurantAdress(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'restaurant_adress'

    adress = Column('adress', TEXT, nullable=False)
    restaurant_id = Column('restaurant_id', ForeignKey('restaurant.id'))
