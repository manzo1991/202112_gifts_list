from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import jinja2
import os
import smtplib

from typing import (
    Dict,
    List,
)

from utils.secrets import DICT_PASSWORDS


def send_mail(
        data: Dict,
        list_recipients: List,
        sender: str = DICT_PASSWORDS['sender'],
        list_recipients_copy: List = [],
        subject: str = "Christmas Gifts List 2022",
        template_name: str = DICT_PASSWORDS['template_name'],
        smpt_server: str = DICT_PASSWORDS['smpt_server'],
        port_number_server: int = DICT_PASSWORDS['port_number_server'],
        username: str = DICT_PASSWORDS['username'],
        password: str = DICT_PASSWORDS['password'],
):
    template_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '../templates',
    )
    template_loader = jinja2.FileSystemLoader(searchpath=template_path)
    template_env = jinja2.Environment(loader=template_loader)

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = ','.join(list_recipients)
    msg["Cc"] = ','.join(list_recipients_copy)
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = subject

    template_raw = template_env.get_template(f'{template_name}.html')
    kwargs = data.get('kwargs', {})
    body = template_raw.render(data, **kwargs)
    msg.attach(MIMEText(body, "html"))

    smtp = smtplib.SMTP(
        smpt_server,
        port_number_server,
    )
    smtp.ehlo()
    smtp.starttls()

    smtp.login(
        username,
        password,
    )
    smtp.sendmail(
        sender,
        list_recipients + list_recipients_copy,
        msg.as_string(),
    )
    smtp.close()
