import uuid

from db.postgresql import Base
from models.good import Good
from models.mixin import TimeStampMixin, UUIDMixin
from sqlalchemy import Column, ForeignKey, LargeBinary, String, Table, Uuid
from sqlalchemy.orm import relationship

SupplierRegion = Table(
    'supplier_region',
    Base.metadata,
    Column('id', Uuid, primary_key=True, nullable=False, default=uuid.uuid4()),
    Column('supplier_id', ForeignKey('supplier.id')),
    Column('region_id', ForeignKey('region.id')),
)


SupplierCity = Table(
    'supplier_city',
    Base.metadata,
    Column(
        'id',
        Uuid,
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
        unique=True,
    ),
    Column('supplier_id', ForeignKey('supplier.id')),
    Column('city_id', ForeignKey('city.id')),
)


class Region(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'region'

    region_name = Column(String, nullable=False)
    city = relationship('City', back_populates='region')
    supplier = relationship(
        'Supplier',
        secondary=SupplierRegion,
        back_populates='delivery_region',
    )


class City(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'city'

    city_name = Column(String, nullable=False)
    region_id = Column(Uuid, ForeignKey('region.id'))
    region = relationship('Region', back_populates='city')
    supplier = relationship(
        'Supplier',
        secondary=SupplierCity,
        back_populates='delivery_city',
    )


class Supplier(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'supplier'

    company_name = Column(String, nullable=False)  # Название компании
    contact_name = Column(String, nullable=False)  # Контактное лицо
    phone_number = Column(String, nullable=False)  # Номер телефона
    email = Column(String, nullable=False)  # email
    company_address = Column(String, nullable=False)  # Адрес компании
    website = Column(String)  # Сайт
    social_network = Column(String)  # Cоциальные сети
    delivery_region = relationship(
        'Region',
        secondary=SupplierRegion,
        back_populates='supplier',
    )  # Регион доставки
    delivery_city = relationship(
        'City',
        secondary=SupplierCity,
        back_populates='supplier',
    )  # Город доставки
    delivery_time = Column(String)  # Время доставки
    delivery_day = Column(String)  # Сроки доставки
    min_price = Column(String)  # Минимальная цена заказа
    OOO = Column(String)  # ООО/ИП/Самозанятость
    OGRN = Column(String)  # ОГРН
    INN = Column(String)  # ИНН
    bank_account = Column(String)  # Расчетный счет
    certificate = relationship('SupplierCert', back_populates='supplier')
    good = relationship('Good', back_populates='supplier')


class SupplierCert(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'supplier_cert'

    certificate = Column(LargeBinary)  # Фотография сертификата
    certificate_url = Column(String)  # ссылка на сертификат
    supplier_id = Column(Uuid, ForeignKey('supplier.id'))
    supplier = relationship('Supplier', back_populates='certificate')
