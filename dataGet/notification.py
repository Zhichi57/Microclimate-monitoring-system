from django.core.mail import BadHeaderError, send_mail, get_connection

from vkr import settings


def send_email(danger_temp, danger_humidity, temperature, humidity, time, email_address):
    text_mail = ''
    if danger_temp:
        text_mail += 'Неправильная температура:\n{}\n'.format(temperature)
    if danger_humidity:
        text_mail += 'Неправильная влажность:\n{}\n'.format(humidity)
    text_mail += 'Время получения:\n{}'.format(time)
    connection = get_connection(
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        use_tls=True
    )

    send_mail(
        settings.EMAIL_SUBJECT,
        text_mail,
        settings.DEFAULT_FROM_EMAIL,
        [email_address],
        connection=connection,
    )
