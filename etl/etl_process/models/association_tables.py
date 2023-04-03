from etl_process.models.mixin import Base, UUIDMixin
from sqlalchemy import Column, ForeignKey


class SupplierCityTag(Base, UUIDMixin):
    __tablename__ = 'supplier_city_tag'

    supplier_id = Column('supplier_id', ForeignKey('supplier.id'))
    city_tag_id = Column('city_tag_id', ForeignKey('city_tag.id'))


class SupplierRegionTag(Base, UUIDMixin):
    __tablename__ = 'supplier_region_tag'

    supplier_id = Column(
        'supplier_id',
        ForeignKey('supplier.id'),
        primary_key=True,
    )
    region_tag_id = Column(
        'region_tag_id',
        ForeignKey('region_tag.id'),
        primary_key=True,
    )
