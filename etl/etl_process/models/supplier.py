from etl_process.models.mixin import Base, TimeStampMixin, UUIDMixin
from etl_process.models.tags import SupplierCityTag, SupplierRegionTag
from sqlalchemy import BINARY, INTEGER, TEXT, UUID, Column, ForeignKey
from sqlalchemy.orm import relationship


class Supplier(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'supplier'

    password = Column('pasword', TEXT, nullable=False)
    company_name = Column('company_name', TEXT, nullable=False)
    contact_name = Column('contact_name', TEXT, nullable=False)
    contact_adress = Column('contact_adress', TEXT, nullable=False)
    phone_number = Column('phone_number', TEXT, nullable=False)
    email = Column('email', TEXT, nullable=False)
    site = Column('site', TEXT, default=None)
    social_network = Column('social_network', TEXT, default=None)
    delivery_min_price = Column('delivery_min_price', INTEGER, default=None)
    estimate_delivery_time_from = Column(
        'estimate_delivery_time_from',
        INTEGER,
        default=None,
    )
    estimate_delivery_time_to = Column(
        'estimate_delivery_time_to',
        INTEGER,
        default=None,
    )
    delivery_day = Column('delivery_day', TEXT, default=None)
    delivery_time = Column('delivery_time', TEXT, default=None)
    application_day = Column('application_day', TEXT, default=None)
    application_time = Column('application_time', TEXT, default=None)
    ooo = Column('ooo', TEXT, nullable=False)
    ogrn = Column('ogrn', TEXT, nullable=False)
    inn = Column('inn', TEXT, nullable=False)
    bank_account = Column('bank_account', TEXT, nullable=False)

    city_tags = relationship(
        'CityTag',
        secondary=SupplierCityTag,
        back_populates='suppliers',
    )
    region_tags = relationship(
        'RegionTag',
        secondary=SupplierRegionTag,
        back_populates='suppliers',
    )
    certificate = relationship('SupplierCert')


class SupplierCert(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'supplier_cert'

    certificate = Column('certificate', BINARY, nullable=False)
    certificate_url = Column('certificate_url', TEXT)
    supplier_id = Column(UUID, ForeignKey('supplier.id'))
