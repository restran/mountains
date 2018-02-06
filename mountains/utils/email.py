# -*- coding: utf-8 -*-
# created by restran on 2016/07/02
from __future__ import unicode_literals, absolute_import, print_function

import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

from mountains import BytesIO, PY2

logger = logging.getLogger(__name__)


class EmailHandler(object):
    def __init__(self, mail_from, password, smtp_server, smtp_port=25):
        """
        :param mail_from: 发件人
        :param password: 发件人密码
        :param smtp_server: SMTP服务器地址
        :param smtp_port: SMTP服务器端口，SSL 方式是 465
        :return:
        """

        self.mail_from = mail_from
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_mail_ssl(self, mail_to_list, subject, content, file_name_list):
        self.do_send_mail(True, mail_to_list, subject, content, file_name_list)

    def send_mail(self, mail_to_list, subject, content, file_name_list):
        self.do_send_mail(False, mail_to_list, subject, content, file_name_list)

    def do_send_mail(self, is_ssl, mail_to_list, subject, content, file_name_list):
        """
        发送邮件
        :param is_ssl: 使用SSL的方式发生
        :param mail_to_list: 收件人列表
        :param subject: 邮件主题
        :param content: 邮件正文
        :param file_name_list: 附近的文件路径列表
        :return:
        """
        if is_ssl:
            smtp = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
        else:
            smtp = smtplib.SMTP(self.smtp_server, self.smtp_port)
        smtp.ehlo(name='foxmail')
        # 调用login时，如果没有调用过 echlo 会自动调用该方法，但是默认使用的name为计算机名
        # 如果计算机名有中文，就会返回503方法未实现的异常
        smtp.login(self.mail_from, self.password)
        msg = MIMEMultipart()
        msg['From'] = self.mail_from
        msg['To'] = ', '.join(mail_to_list)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        # 如果 content 是 html，则需要设置 _subtype='html'
        # 默认情况下 _subtype='plain'，即纯文本
        msg.attach(MIMEText(content, _charset='utf-8'))
        for fn in file_name_list:
            part = MIMEText(open(fn, 'rb').read(), 'base64', 'utf-8')
            part["Content-Type"] = 'application/octet-stream'
            basename = os.path.basename(fn)
            if PY2:
                basename = basename.encode('gb2312')
            # 文件名使用 gb2312 编码，否则会没有附件
            part.add_header('Content-Disposition', 'attachment', filename=('gb2312', '', basename))
            msg.attach(part)
        smtp.sendmail(self.mail_from, mail_to_list, msg.as_string())
        smtp.close()


class PostfixEmailHandler(object):
    def __init__(self, mail_from, smtp_server='localhost', smtp_port=25):
        self.mail_from = mail_from
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_email(self, mail_to, subject, content, content_type='plain', files=None):
        """
        :param content_type: 如果 text 是html，则需要设置 _subtype='html'
        :param mail_to:
        :param subject:
        :param content:
        :param files: (f_name, f_data)
        :return:
        """
        assert type(mail_to) == list
        server = self.smtp_server
        if files is None:
            files = []

        msg = MIMEMultipart()
        msg['From'] = self.mail_from
        msg['To'] = ', '.join(mail_to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        # 如果 text 是html，则需要设置 _subtype='html'
        # 默认情况下 _subtype='plain'，即纯文本
        msg.attach(MIMEText(content, _subtype=content_type, _charset='utf-8'))

        for fn, fd in files:
            part = MIMEText(fd, 'base64', 'utf-8')
            part["Content-Type"] = 'application/octet-stream'
            basename = fn
            if PY2:
                basename = basename.encode('gb2312')
            # 文件名使用 gb2312 编码，否则会没有附件
            part.add_header('Content-Disposition', 'attachment', filename=('gb2312', '', basename))
            msg.attach(part)
        smtp = smtplib.SMTP(server, port=self.smtp_port)
        smtp.sendmail(self.mail_from, mail_to, msg.as_string())
        smtp.close()


def main():
    handler = EmailHandler('mail_from@example.com', 'password', 'smtp.example.com', 465)
    mail_to_list = ['example@test.com']
    subject = 'Python 发送邮件测试'
    content = '这是用 Python 自动发送的邮件，请勿回复'
    # 附件存放在当前文件夹
    file_name_list = ['test.rar']
    handler.send_mail_ssl(mail_to_list, subject, content, file_name_list)
    print('邮件发送成功')

    mail_to_list = ['mail_from@example.com']
    subject = 'Python 发送邮件测试'
    content = '这是用 Python 自动发送的邮件，请勿回复'
    bio = BytesIO()
    bio.write(b'123')
    bio.getvalue()
    files = [
        ('test中文3.txt', bio.getvalue()),
    ]
    handler = PostfixEmailHandler('mail_from@example.com')
    handler.send_email(mail_to_list, subject, content, files=files)


if __name__ == '__main__':
    main()
