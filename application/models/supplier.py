import uuid

from db.postgresql import Base
from models.good import Good
from models.order import Bucket
from models.mixin import TimeStampMixin, UUIDMixin
from sqlalchemy import Column, ForeignKey, LargeBinary, String, Table, Uuid
from sqlalchemy.orm import relationship
import sqlalchemy.dialects.postgresql as postgresql

# SupplierRegion = Table(
#     'supplier_region',
#     Base.metadata,
#     Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4, unique=True),
#     Column('supplier_id', ForeignKey('supplier.id')),
#     Column('region_id', ForeignKey('region.id')),
# )

class SupplierRegion(Base):
    __tablename__ = 'supplier_region'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4, unique=True)
    supplier_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('supplier.id'), primary_key=True)
    region_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('region.id'), primary_key=True)


class SupplierCity(Base):
    __tablename__ = 'supplier_city'
    
    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4, unique=True)
    supplier_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('supplier.id'), primary_key=True)
    city_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('city.id'), primary_key=True)



# SupplierCity = Table(
#     'supplier_city',
#     Base.metadata,
#     Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4, unique=True),
#     Column('supplier_id', ForeignKey('supplier.id')),
#     Column('city_id', ForeignKey('city.id')),
# )


class Region(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'region'

    region_name = Column(String, nullable=False)
    city = relationship('City', back_populates='region')
    supplier = relationship(
        'Supplier',
        secondary=SupplierRegion.__table__,
        back_populates='delivery_region',
    )


class City(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'city'

    city_name = Column(String, nullable=False)
    region_id = Column(Uuid, ForeignKey('region.id'))
    region = relationship('Region', back_populates='city')
    supplier = relationship(
        'Supplier',
        secondary=SupplierCity.__table__,
        back_populates='delivery_city',
    )


class Supplier(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'supplier'

    company_name = Column(String, nullable=False)  # Название компании
    contact_name = Column(String, nullable=False)  # Контактное лицо
    phone_number = Column(String, nullable=False)  # Номер телефона
    email = Column(String, nullable=False)  # email
    company_adress = Column(String)  # Адрес компании
    website = Column(String)  # Сайт
    social_network = Column(String)  # Cоциальные сети
    company_cover = Column(LargeBinary) #Обложка компании
    company_logo = Column(LargeBinary) #Лого компании
    delivery_region = relationship(
        'Region',
        secondary=SupplierRegion.__table__,
        back_populates='supplier',
    )  # Регион доставки
    delivery_city = relationship(
        'City',
        secondary=SupplierCity.__table__,
        back_populates='supplier',
    )  # Город доставки
    delivery_day_time = Column(String, nullable=False)  # Время и дни доставки
    estimated_delivery_time = Column(String, nullable=False)  # Сроки доставки
    min_price = Column(String, nullable=False)  # Минимальная цена заказа
    orders_day_time = Column(String, nullable=False) #Дни и время приема заявок
    ooo = Column(String, nullable=False)  # ООО/ИП/Самозанятость
    ogrn = Column(String, nullable=False)  # ОГРН
    inn = Column(String, nullable=False)  # ИНН
    certificate = relationship('SupplierCert', back_populates='supplier')
    good = relationship('Good', back_populates='supplier')
    bucket = relationship('Bucket', back_populates='supplier')


class SupplierCert(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'supplier_cert'

    certificate = Column(LargeBinary)  # Фотография сертификата
    certificate_url = Column(String)  # ссылка на сертификат
    supplier_id = Column(Uuid, ForeignKey('supplier.id'))
    supplier = relationship('Supplier', back_populates='certificate')
