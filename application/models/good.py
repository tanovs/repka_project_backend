import uuid

from db.postgresql import Base
from models.mixin import TimeStampMixin, UUIDMixin
from sqlalchemy import Column, ForeignKey, LargeBinary, String, Table, Uuid, Boolean, Integer
from sqlalchemy.orm import relationship


class Tag(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'tag'

    tag_name = Column(String, nullable=False)
    category_id = Column(Uuid, ForeignKey('category.id'))
    category = relationship('Category', back_populates='tag')

class Good(Base, TimeStampMixin, UUIDMixin):
    __tablename__ = 'good'

    name = Column(String, nullable=False)  # наименование товара
    photo = Column(LargeBinary)  # фото товара
    price = Column(String, nullable=False)  # цена товара
    volume = Column(String, nullable=False)  # объем товара
    balance = Column(String, nullable=False)  # остаток товара
    calories = Column(String)  # КБЖУ
    compound = Column(String)  # Состав
    expiration_day = Column(String)  # Срок годности и условия хранения
    producer = Column(String)
    sample = Column(Boolean, server_default=None)
    sample_amount = Column(Integer)
    supplier_id = Column(Uuid, ForeignKey('supplier.id'))
    tag_id = Column(Uuid, ForeignKey(Tag.id))
    supplier = relationship('Supplier', back_populates='good')
    tag = relationship('Tag')
    bucket = relationship('Bucket', back_populates='good')


class Category(Base, TimeStampMixin, UUIDMixin):
    __tablename__ = 'category'

    category_name = Column(String, nullable=False)
    file_path = Column(String)
    tag = relationship('Tag', back_populates='category')

