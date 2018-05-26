# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 10:12:35 2018

@author: Ismail
"""

import unicodecsv

with open('daily_engagement.csv', 'rb') as f:
    reader = unicodecsv.DictReader(f)
    dailyEngagement = list(reader)

print(dailyEngagement[0])