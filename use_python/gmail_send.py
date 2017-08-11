'''using python send gmail'''
# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
import datetime
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
class SendGmail(object):
    '''send mail via gmail'''
    def __init__(self, subject='', **kw):
        self._params = kw
        self._smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        self._msg = MIMEMultipart('alternative')
        self._msg['From'] = self._format_addrs('<%s>' % self._params['from_addr'])
        self._msg['To'] = self._format_addrs('<%s>' % self._params['to_addr'])
        self._msg['Subject'] = Header(subject, 'utf-8').encode()
        self._msg['date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def add_content(self, content='', attachment='', l_keys=''):
        '''add html template and attachment file'''
        if l_keys != '':
            for i in l_keys:
                content = content.replace('<#' + i + '#>', str(self._params[i]))
        self._msg.attach(MIMEText(content, 'html', 'utf-8'))
        if attachment != '':
            self._msg.attach(attachment)

    def send_mail(self):
        '''send mail'''
        try:
            server = self._smtp_server
            server.ehlo()
            server.starttls()
            server.login(self._params['from_addr'], self._params['password'])
            server.sendmail(self._params['from_addr'], [self._params['to_addr']], self._msg.as_string())
            server.quit()
            print(self._params['to_addr'] + ' send success ...')
        except:
            print(self._params['to_addr'] + ' send failed....')

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
    MESSAGE.add_content()
    MESSAGE.send_mail()
