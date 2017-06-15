'''read data from excel'''
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import xlrd
from gmail_send import SendGmail


def readfile(path):
    '''load file'''
    data = xlrd.open_workbook(path)
    table = data.sheet_by_index(0)

    nrows = table.nrows
    # ncols = table.ncols

    keys = table.row_values(0)
    mlist = []
    for i in range(1, nrows):
        row_values = table.row_values(i)
        ditem = {}
        index = 0
        for r_v in row_values:
            ditem[keys[index]] = r_v
            index += 1
        mlist.append(ditem)
    return mlist

def send_mails():
    '''send mails'''
    l_data = readfile('data.xlsx')
    for i in l_data:
        mail = SendGmail(**i)
        mail.get_content('mail.html')
        mail.send_mail()

if __name__ == '__main__':
    send_mails()
