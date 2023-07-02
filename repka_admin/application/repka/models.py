import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampMixin(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class SupplierRegion(UUIDMixin):
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    region = models.ForeignKey('Region', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "repka\".\"supplier_region"


class SupplierCity(UUIDMixin):
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "repka\".\"supplier_city"



class Region(UUIDMixin, TimeStampMixin):
    region_name = models.TextField(_('region_name'))

    class Meta:
        db_table = "repka\".\"region"
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"
    
    def __str__(self) -> str:
        return self.region_name


class City(UUIDMixin, TimeStampMixin):
    city_name = models.TextField(_('city_name'))
    region = models.ForeignKey('Region', on_delete=models.CASCADE)

    class Meta:
        db_table = "repka\".\"city"
        verbose_name = "Город"
        verbose_name_plural = "Города"
    
    def __str__(self) -> str:
        return self.city_name


class Supplier(UUIDMixin, TimeStampMixin):
    company_name = models.TextField(_('company_name'))  # Название компании
    contact_name = models.TextField(_('contact_name'))  # Контактное лицо
    phone_number = models.TextField(_('phone_number'))  # Номер телефона
    email = models.TextField(_('email'))  # email
    company_adress = models.TextField(_('company_adress'), blank=True)  # Адрес компании
    website = models.TextField(_('website'), blank=True)  # Сайт
    social_network = models.TextField(_('social_network'), blank=True)  # Cоциальные сети
    delivery_region = models.ManyToManyField(Region, through='SupplierRegion')# Регион доставки
    delivery_city = models.ManyToManyField(City, through='SupplierCity')  # Город доставки
    delivery_time = models.TextField(_('delivery_time'))  # Время доставки
    delivery_day = models.TextField(_('delivery_day'))  # Сроки доставки
    min_price = models.TextField(_('min_price'))  # Минимальная цена заказа
    ooo = models.TextField(_('OOO'), blank=True)  # ООО/ИП/Самозанятость
    ogrn = models.TextField(_('OGRN'), blank=True)  # ОГРН
    inn = models.TextField(_('INN'), blank=True)  # ИНН
    class Meta:
        db_table = "repka\".\"supplier"
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"
    
    def __str__(self) -> str:
        return self.company_name


class SupplierCert(UUIDMixin, TimeStampMixin):
    certificate = models.ImageField(_('certificate'), blank=True)  # Фотография сертификата
    certificate_url = models.TextField(_('certificate_url'), blank=True)  # ссылка на сертификат
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)

    class Meta:
        db_table = "repka\".\"supplier_cert"
        verbose_name = "Сертификат поставщика"
        verbose_name_plural = "Сертификаты поставщиков"
    
    def __str__(self) -> str:
        return self.certificate

class GoodCategory(UUIDMixin):
    good = models.ForeignKey('Good', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "repka\".\"good_category"
    

class Category(TimeStampMixin, UUIDMixin):
    category_name = models.TextField(_('category_name'))

    class Meta:
        db_table = "repka\".\"category"
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    
    def __str__(self) -> str:
        return self.category_name


class Tag(UUIDMixin, TimeStampMixin):
    tag_name = models.TextField(_('tag_name'))
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        db_table = "repka\".\"tag"
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
    
    def __str__(self) -> str:
        return self.tag_name

class Good(TimeStampMixin, UUIDMixin):
    name = models.TextField(_('name'))  # наименование товара
    photo = models.ImageField(_('photo'))  # фото товара
    price = models.TextField(_('price'))  # цена товара
    volume = models.TextField(_('volume'))  # объем товара
    balance = models.TextField(_('balance'))  # остаток товара
    calories = models.TextField(_('calories'), blank=True)  # КБЖУ
    compound = models.TextField(_('compound'), blank=True)  # Состав
    expiration_day = models.TextField(_('expiration_day'), blank=True)  # Срок годности и условия хранения
    category = models.ManyToManyField(Category, through='GoodCategory')
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)

    class Meta:
        db_table = "repka\".\"good"
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
    
    def __str__(self) -> str:
        return self.name

