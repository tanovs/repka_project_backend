from etl_process.models.association_tables import (SupplierCityTag,
                                                   SupplierRegionTag)
from etl_process.models.mixin import Base, TimeStampMixin, UUIDMixin
from sqlalchemy import TEXT, Column
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
