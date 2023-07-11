import uuid

from db.postgresql import Base
from models.mixin import TimeStampMixin, UUIDMixin
from sqlalchemy import Column, ForeignKey, LargeBinary, String, Table, Uuid
from sqlalchemy.orm import relationship

GoodCategory = Table(
    'good_category',
    Base.metadata,
    Column('id', Uuid, primary_key=True, nullable=False, default=uuid.uuid4()),
    Column('good_id', ForeignKey('good.id')),
    Column('category_id', ForeignKey('category.id')),
)


class Good(Base, TimeStampMixin, UUIDMixin):
    __tablename__ = 'good'

    name = Column(String, nullable=False)  # наименование товара
    photo = Column(LargeBinary)  # фото товара
    price = Column(String, nullable=False)  # цена товара
    volume = Column(String, nullable=False)  # объем товара
    limit = Column(String)  # остаток товара
    calories = Column(String)  # КБЖУ
    compound = Column(String)  # Состав
    expiration_day = Column(String)  # Срок годности и условия хранения
    category = relationship(
        'Category',
        secondary=GoodCategory,
        back_populates='good',
    )
    supplier_id = Column(Uuid, ForeignKey('supplier.id'))
    supplier = relationship('Supplier', back_populates='good')


class Category(Base, TimeStampMixin, UUIDMixin):
    __tablename__ = 'category'

    category_name = Column(String, nullable=False)
    file_path = Column(String)
    tag = relationship('Tag', back_populates='category')
    good = relationship(
        'Good',
        secondary=GoodCategory,
        back_populates='category',
    )


class Tag(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'tag'

    tag_name = Column(String, nullable=False)
    category_id = Column(Uuid, ForeignKey('category.id'))
    category = relationship('Category', back_populates='tag')
