from fastapi_mail import ConnectionConfig

mail: ConnectionConfig = None


def get_mail_config() -> ConnectionConfig:
    return mail
