import requests
from suppliers.model import AddSupplierRequest

def add_suppliers() -> dict:
    company_name = {1: 'ООО «ВКУСНЫЕ ИСТОРИИ»', 2: 'ООО ПК "Заготпром"', 3: 'ferro', 4: 'ИП ТУЧИН'}
    contact_name = {1: 'Дарья Зеленцова', 2: 'Александр', 3: 'Владимир', 4: 'Тучин Антон'}
    phone_number = {1: '89296037090', 2: '+79535464073', 3: '+79955944083', 4: '89257728738'}
    email = {1: 'd.zelentsova@fresco.team', 2: 'avs@zagotprom.ru', 3: 'connect@pastaferro.ru', 4: 'Anton_tuchin@mail.ru'}
    company_adress = {1: '141544, Московская обл., г.о. Химки, д. Рузино, ул. Малинская, д.2.', 2: 'Республика Карелия, Кондопожский р-он, пос. Березовка, ул. Новая 8Б. Самовывоз со склада в Пушкино (МО)', 3: 'улица Малая Посадская, д. 17, корп./ст. ЛИТЕРА В, кв./оф. ПОМЕЩ. 9-Н, ПОМЕЩЕНИЕ № 6, г. Санкт – Петербург', 4: 'г. Красногорск, ул. Ленина, 29'}
    website = {1: 'https://fresco.team/', 2: 'https://zagotprom.com/', 3: '', 4: 'https://kingsvanilla.ru/'}
    social_network = {1: '', 2: '', 3: '@pastaferro', 4: '@kings_vanilla'}
    delivery_day_time = {1: 'с 8 до 20, с пн по вс', 2: 'Пн-Пт', 3: 'С понедельника по пятницу 10:00-20:00', 4: 'Пн-пт, 09.00-17.00'}
    estimated_delivery_time = {1: '2 дня', 2: '10 дней', 3: '72 часа', 4: '72 часа'}
    min_price = {1: '30 000р.', 2: 'Зависит от региона доставки', 3: '3500', 4: '150'}
    orders_day_time = {1: 'с 8 до 12, с пн по вс', 2: 'Пн-Пт 09.00-17.00', 3: 'В любой день 10:00-20:00', 4: 'Пн-Пт, 09.00-17.00'}
    ooo = {1: 'ООО', 2: 'ООО', 3: 'ООО', 4: 'ИП'}
    ogrn = {1: '1187746995072', 2: '1131001000338', 3: '1237800094597', 4: '32250810029502'}
    inn = {1: '7730248208', 2: '1001266608', 3: '7813674418', 4: '502498463424'}

    results = {}
    for i in range(1, 5):
        supplier = AddSupplierRequest(
            company_name=company_name[i],
            contact_name=contact_name[i],
            phone_number=phone_number[i],
            email=email[i],
            company_adress=company_adress[i],
            website=website[i],
            social_network=social_network[i],
            delivery_day_time=delivery_day_time[i],
            estimated_delivery_time=estimated_delivery_time[i],
            min_price=min_price[i],
            orders_day_time=orders_day_time[i],
            ooo=ooo[i],
            ogrn=ogrn[i],
            inn=inn[i],
        )
        resp = requests.post('http://89.208.198.57:8080/api/v1/supplier/add', data=supplier.json())
        results[i] = resp.json()['supplier_uuid']
    return results