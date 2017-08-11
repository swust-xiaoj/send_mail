'''read data from excel'''
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from email.mime.application import MIMEApplication
import os
import configparser

import re
import xlrd

from gmail_send import SendGmail


def readfile(path, start, step):
    '''load file'''
    datafile = os.path.join(os.path.dirname(__file__), path)
    data = xlrd.open_workbook(datafile)
    sheets = data.sheets()
    mlist = []
    keys = []
    regrex = r'([\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+)'
    new_start = start + step
    for s_l in sheets:
        table = s_l

        nrows = table.nrows
        if nrows <= new_start:
            new_start = nrows

        keys = table.row_values(0)
        for i in range(start, new_start):
            row_values = table.row_values(i)
            ditem = {}
            index = 0
            for r_v in row_values:
                ditem[keys[index]] = r_v
                index += 1
            isvalid = re.search(regrex, ditem['to_addr'], re.M|re.I)
            if isvalid:
                mlist.append(ditem)
            else:
                print(ditem['to_addr'] + ' is invalid email address....')
    return keys[3:], mlist, new_start

def add_attachment(attachment_file):
    '''add xlsx file'''
    attachmentfile = os.path.join(os.path.dirname(__file__), attachment_file)
    att = MIMEApplication(open(attachmentfile, 'rb').read())
    att.add_header('Content-Disposition', 'attachment', filename=attachment_file)
    return att

def add_html(htmltmpfile):
    '''html template'''
    htmlfile = os.path.join(os.path.dirname(__file__), htmltmpfile)
    file = open(htmlfile, 'r', encoding='utf8')
    content = file.read()
    return content

def send_mails(language, conf):
    '''send mails'''

    start = int(conf['common_conf']['start'])
    step = int(conf['common_conf']['step'])

    conf = conf[language + '_conf']
    receive_list = conf['receive_list_file']
    attachment_file = conf['attachment_file']
    htmltmpfile = conf['mail_content_file']
    subject = conf['mail_subject']

    l_keys, l_data, new_start = readfile(receive_list, start, step)

    if len(l_data) == 0:
        print('email empty!!!!')
        return

    if attachment_file != 'none':
        attachment = add_attachment(attachment_file)
    else:
        attachment = ''
    htmltmp = add_html(htmltmpfile)
    for i in l_data:
        mail = SendGmail(subject, **i)
        mail.add_content(htmltmp, attachment, l_keys)
        mail.send_mail()
    set_conf(str(new_start))

def read_conf():
    '''read config file'''
    conf_parser = configparser.ConfigParser()
    config_file = os.path.join(os.path.dirname(__file__), 'mail.conf')
    conf_parser.read(config_file, 'utf-8')
    zh_conf = dict(conf_parser.items('zh'))
    en_conf = dict(conf_parser.items('en'))
    common_conf = dict(conf_parser.items('common'))
    return {
        'zh_conf': zh_conf,
        'en_conf': en_conf,
        'common_conf': common_conf,
    }
def set_conf(start):
    '''set new start to config file'''
    conf_parser = configparser.ConfigParser()
    config_file = os.path.join(os.path.dirname(__file__), 'mail.conf')
    conf_parser.read(config_file, 'utf-8')
    conf_parser.set('common', 'start', start)
    with open('mail.conf', 'w+', encoding='utf-8') as f:
        conf_parser.write(f)


if __name__ == '__main__':
    CONF = read_conf()
    send_mails(CONF['common_conf']['language'], CONF)
