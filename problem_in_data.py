# -*- coding: utf-8 -*-
"""
Created on Mon May 28 23:08:23 2018

this code will delete value with 'acct' key in dictionary
and store with key 'account_key'

@author: Ismail
"""

import unicodecsv

def read_csv(filename):
    with open(filename, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)

#daily_engagement = list()
daily_engagement = read_csv('daily_engagement.csv')
for engagement_record in daily_engagement:
    engagement_record['account_key'] = engagement_record['acct']
    del[engagement_record['acct']]