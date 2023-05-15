"""Add good tables

Revision ID: a703a1a2a083
Revises: 
Create Date: 2023-05-10 14:00:57.084210

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a703a1a2a083'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('create schema repka')
    op.create_table('category',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('category_name', sa.String(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.Column('modified', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    schema='repka'
    )
    op.create_table('good_tag',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('tag_name', sa.String(), nullable=False),
    sa.Column('category_id', sa.Uuid(), nullable=True),
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.Column('modified', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['repka.good_tag.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    schema='repka'
    )
    op.create_table('region',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('region_name', sa.String(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.Column('modified', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    schema='repka'
    )
    op.create_table('supplier',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('company_name', sa.String(), nullable=False),
    sa.Column('contact_name', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('company_address', sa.String(), nullable=False),
    sa.Column('website', sa.String(), nullable=True),
    sa.Column('social_network', sa.String(), nullable=True),
    sa.Column('delivery_time', sa.String(), nullable=True),
    sa.Column('delivery_day', sa.String(), nullable=True),
    sa.Column('min_price', sa.String(), nullable=True),
    sa.Column('OOO', sa.String(), nullable=True),
    sa.Column('OGRN', sa.String(), nullable=True),
    sa.Column('INN', sa.String(), nullable=True),
    sa.Column('bank_account', sa.String(), nullable=True),
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.Column('modified', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    schema='repka'
    )
    op.create_table('city',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('city_name', sa.String(), nullable=False),
    sa.Column('region_id', sa.Uuid(), nullable=True),
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.Column('modified', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['region_id'], ['repka.region.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    schema='repka'
    )
    op.create_table('good',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('photo', sa.LargeBinary(), nullable=True),
    sa.Column('price', sa.String(), nullable=False),
    sa.Column('valume', sa.String(), nullable=False),
    sa.Column('limit', sa.String(), nullable=True),
    sa.Column('calories', sa.String(), nullable=True),
    sa.Column('compound', sa.String(), nullable=True),
    sa.Column('expiration_day', sa.String(), nullable=True),
    sa.Column('supplier_id', sa.Uuid(), nullable=True),
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.Column('modified', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['supplier_id'], ['repka.supplier.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    schema='repka'
    )
    op.create_table('supplier_cert',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('certificate', sa.LargeBinary(), nullable=True),
    sa.Column('certificate_url', sa.String(), nullable=True),
    sa.Column('supplier_id', sa.Uuid(), nullable=True),
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.Column('modified', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['supplier_id'], ['repka.supplier.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    schema='repka'
    )
    op.create_table('supplier_region',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('supplier_id', sa.UUID(), nullable=True),
    sa.Column('region_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['region_id'], ['repka.region.id'], ),
    sa.ForeignKeyConstraint(['supplier_id'], ['repka.supplier.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='repka'
    )
    op.create_table('good_category',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('good_id', sa.UUID(), nullable=True),
    sa.Column('category_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['repka.category.id'], ),
    sa.ForeignKeyConstraint(['good_id'], ['repka.good.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='repka'
    )
    op.create_table('supplier_city',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('supplier_id', sa.UUID(), nullable=True),
    sa.Column('city_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['city_id'], ['repka.city.id'], ),
    sa.ForeignKeyConstraint(['supplier_id'], ['repka.supplier.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    schema='repka'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('supplier_city', schema='repka')
    op.drop_table('good_category', schema='repka')
    op.drop_table('supplier_region', schema='repka')
    op.drop_table('supplier_cert', schema='repka')
    op.drop_table('good', schema='repka')
    op.drop_table('city', schema='repka')
    op.drop_table('supplier', schema='repka')
    op.drop_table('region', schema='repka')
    op.drop_table('good_tag', schema='repka')
    op.drop_table('category', schema='repka')
    op.execute('drop schema repka')
    # ### end Alembic commands ###
