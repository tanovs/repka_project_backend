import uuid
from dataclasses import dataclass

from fastapi import Depends, File
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from mail.mail import get_mail_config


@dataclass
class SendEmailService():
    mail_settings: ConnectionConfig

    async def send_email_add_goods(self, content: File, supplier_id: uuid.UUID):
        message = MessageSchema(
            subject='Заявка на добавление товаров',
            recipients=['a.koreyba@repka.tech'],
            body=f'Необходимо добавить товары для пользователя с id {supplier_id}',
            subtype=MessageType.html,
            attachments=[content],
        )
        fm = FastMail(self.mail_settings)
        await fm.send_message(message=message)
    
    async def send_email_add_supplier(self, company_name: str, email: str, url: str):
        with open('/home/tania/repka_project/application/src/supplier_add_template', 'r') as templ_file:
            template = templ_file.read()
        template = template.format(
            company_name=company_name,
            profile_url=url,
            email=email
        )
        message = MessageSchema(
            subject='Ваша компания зарегестрирована в сервисе Repka',
            recipients=[email],
            body=template,
            subtype=MessageType.html,
        )
        fm = FastMail(self.mail_settings)
        await fm.send_message(message=message)
    
    async def send_email_horeca(self, data, email: str):
        body = '''Добрый день! Вы соверишили заказ на платформе repka.tech. Детали заказа:'''
        message = MessageSchema(
            subject='Подтверждение заказа',
            recipients=[email], # Заменить на почту horeca
            body=body,
            subtype=MessageType.html,
        )
        fm = FastMail(self.mail_settings)
        await fm.send_message(message=message)
    
    async def send_email_supplier(self, data, email: str):
        body = '''Добрый день! Компания ... сделала заказ на сайте repka.tech. Детали заказа: Для подтверждения заказа необходимо связаться с компанией .... контакты:'''
        message = MessageSchema(
            subject='Подтверждение заказа',
            recipients=[email], # Заменить на почту horeca
            body=body,
            subtype=MessageType.html,
        )
        fm = FastMail(self.mail_settings)
        await fm.send_message(message=message)


def get_send_email_service(
    mail_settings: ConnectionConfig = Depends(get_mail_config),
) -> SendEmailService:
    return SendEmailService(mail_settings=mail_settings)
