from django.contrib import admin
from .models import Region, City, Category, Tag, Supplier, Good, SupplierCert, SupplierCity, SupplierRegion, GoodCategory

class SupplierCityInline(admin.TabularInline):
    model = SupplierCity

class SupplierRegionInline(admin.TabularInline):
    model = SupplierRegion

class GoodCategoryInline(admin.TabularInline):
    model = GoodCategory

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('region_name', 'created', 'modified')
    list_filter = ('created', 'modified')
    search_fields = ('region_name',)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('city_name', 'region', 'created', 'modified')
    list_filter = ('created', 'modified')
    search_fields = ('city_name',)
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'created', 'modified')
    list_filter = ('created', 'modified')
    search_fields = ('category_name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_name', 'category', 'created', 'modified')
    list_filter = ('created', 'modified')
    search_fields = ('tag_name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    inlines = (SupplierCityInline, SupplierRegionInline, )

    list_display = (
        'company_name', 'contact_name', 'phone_number',
        'email', 'company_adress', 'website', 'social_network', 
        'delivery_time', 'delivery_day', 'get_regions', 'get_cities', 'min_price', 'ooo',
        'ogrn', 'inn', 'created', 'modified',
    )
    list_filter = ('created', 'modified')
    search_fields = ('company_name',)

    @admin.display(description='region')
    def get_regions(self, obj):
        return [region.region_name for region in obj.delivery_region.all()]
    
    @admin.display(description='city')
    def get_cities(self, obj):
        return [city.city_name for city in obj.delivery_city.all()]


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    inline = (GoodCategoryInline, )

    list_display = (
        'name', 'photo', 'price', 'volume', 'balance', 'calories',
        'compound', 'expiration_day', 'supplier', 'created', 'modified',
    )
    list_filter = ('created', 'modified')
    search_fields = ('name',)

@admin.register(SupplierCert)
class SupplierCertAdmin(admin.ModelAdmin):
    list_display = (
        'certificate', 'certificate_url', 'supplier', 'created', 'modified',
    )
    list_filter = ('created', 'modified')