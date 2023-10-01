from db.postgresql import Base
from models.mixin import TimeStampMixin, UUIDMixin
from sqlalchemy import Column, Uuid, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Order(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'orders_info'

    company_name = Column(String)
    delivery_city_region = Column(String)
    delivery_adress = Column(String)
    contact_name = Column(String)
    contact_phone = Column(String)
    contact_email = Column(String)
    ooo = Column(String)
    inn = Column(String)
    bank_account = Column(String)
    bank_name = Column(String)

    bucket = relationship('Bucket', back_populates='info')


class Bucket(Base, UUIDMixin):
    __tablename__ = 'bucket'

    supplier_id = Column(Uuid, ForeignKey('supplier.id'))
    info_id = Column(Uuid, ForeignKey('orders_info.id'))
    good_id = Column(Uuid, ForeignKey('good.id'))
    amount = Column(Integer, nullable=False)
    supplier = relationship('Supplier', back_populates='bucket')
    good = relationship('Good', back_populates='bucket')
    info = relationship('Order', back_populates='bucket')
