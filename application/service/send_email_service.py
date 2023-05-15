import uuid
from dataclasses import dataclass

from fastapi import Depends, File
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from mail.mail import get_mail_config


@dataclass
class SendEmailService():
    mail_settings: ConnectionConfig

    async def send_email(self, file_content: File, supplier_id: uuid.UUID):
        message = MessageSchema(
            subject='Заявка на добавление товаров',
            recipients=['a.koreyba@repka.tech'],
            body=f'Необходимо добавить товары для пользователя с id {supplier_id}',
            subtype=MessageType.html,
            attachments=[file_content],
        )
        fm = FastMail(self.mail_settings)
        await fm.send_message(message=message)


def get_send_email_service(
    mail_settings: ConnectionConfig = Depends(get_mail_config),
) -> SendEmailService:
    return SendEmailService(mail_settings=mail_settings)
