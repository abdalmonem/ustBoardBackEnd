from flask import current_app
from flask_jwt_extended import get_current_user
from random import randint
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from . import api

def send_verfy_mail(_to, _from, confirmation):
    html = "\
        <body float:\"right\">\
            <h4>مرحبًا عزيزي المستخدم</h4>\
            <div>هذه الرسالة تم إنشاؤها لإستكمال عملية الإنضمام للتطبيق عبر تأكيد حسابك بإدخال</div>\
            <div>الأرقام التالية:</div\
            <strong>" + str(confirmation) + "</strong><br>\
            <p>فريق إدارة اللوحة الذكية.</p>\
        </body>"

    message = MIMEMultipart('alternative')
    message['Subject'] = 'تأكيد الحساب'
    message['From'] = _from
    message['To'] = _to

    html_part = MIMEText(html, 'html')
    message.attach(html_part)
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(current_app.config['SMTP_SERVER'], current_app.config['PORT'])
        server.ehlo()
        server.starttls(context=context) # Secure the connection
        server.ehlo()
        server.login(message['From'], current_app.config['UST_PASSWORD']) # Mail & Password

        server.sendmail(message['From'], message['To'], message.as_string())
    except Exception as e:
        return {"msg": e}
