'''using python send gmail'''
# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
class SendGmail(object):
    '''send mail via gmail'''
    def __init__(self):
        self._from_addr = input('From:')
        self._password = input('Password:')
        self._to_addr = input('To:')
        self._smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        self._msg = MIMEMultipart('alternative')
        self._msg['From'] = self._format_addrs('<%s>' % self._from_addr) # 发件人
        self._msg['To'] = self._format_addrs('<%s>' % self._to_addr) # 收件人
        subject = 'hello python'
        self._msg['Subject'] = Header(subject, 'utf-8').encode() # 主题

    def get_content(self, mail_tmp_path='mail.html'):
        '''get mail content'''
        page = mail_tmp_path
        file = open(page, 'r', encoding='utf8')
        content = file.read()
        content = content.replace('<#send_name#>', self._from_addr)
        content = content.replace('<#name#>', self._to_addr)
        self._msg.attach(MIMEText(content, 'html', 'utf-8'))

    def send_mail(self):
        '''send mail'''
        server = self._smtp_server
        server.ehlo()
        server.starttls()
        server.login(self._from_addr, self._password)
        server.sendmail(self._from_addr, [self._to_addr], self._msg.as_string())
        print('success send to %s!' % self._to_addr)
        server.quit()
    @classmethod
    def _replace_tmp(cls, string):
        pass
    @classmethod
    def _format_addrs(cls, string):
        '''format addr'''
        name, addr = parseaddr(string)
        return formataddr((Header(name, 'utf-8').encode(), addr))

if __name__ == '__main__':
    MESSAGE = SendGmail()
    MESSAGE.get_content()
    MESSAGE.send_mail()
