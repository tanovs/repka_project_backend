from etl_process.models.association_tables import (SupplierCityTag,
                                                   SupplierRegionTag)
from etl_process.models.mixin import Base, TimeStampMixin, UUIDMixin
from sqlalchemy import TEXT, Column, ForeignKey
from sqlalchemy.orm import relationship


class CityTag(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'city_tag'

    city = Column('city', TEXT, nullable=False)
    suppliers = relationship(
        'Supplier',
        secondary=SupplierCityTag,
        back_populates='city_tags',
    )


class RegionTag(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'region_tag'

    region = Column('region', TEXT, nullable=False)
    suppliers = relationship(
        'Supplier',
        secondary=SupplierRegionTag,
        back_populates='region_tags',
    )


class CategoryTag(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'category_tag'

    category = Column('category', TEXT, nullable=False)
    category_tags = relationship('GoodTag')


class GoodTag(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'good_tag'

    good_tag = Column('good_tag', TEXT, nullable=False)
    category_tag_id = Column('category_tag_id', ForeignKey('category_tag.id'))
