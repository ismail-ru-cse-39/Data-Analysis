# -*- coding: utf-8 -*-
"""
Created on Tue May 29 21:26:00 2018

@author: Ismail
"""

# -*- coding: utf-8 -*-
"""
Created on Mon May 28 23:43:00 2018

@author: Ismail
"""

import unicodecsv

def read_csv(filename):
    with open(filename, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)

def get_unique_data(data):
    unique_students = set()
    for data_point in data:
        unique_students.add(data_point['account_key'])
    return unique_students

enrollments = read_csv('enrollments.csv')
daily_engagement = read_csv('daily_engagement.csv')

#daily_engagement = read_csv('daily_engagement.csv')
for engagement_record in daily_engagement:
    engagement_record['account_key'] = engagement_record['acct']
    del[engagement_record['acct']]
    
unique_engagement_students = get_unique_data(daily_engagement)

num_prob_students = 0

for enrollment in enrollments:
    student = enrollment['account_key']
    if (student not in unique_engagement_students and
        enrollment['join_date'] != enrollment['cancel_date']):
        print (enrollment)
        num_prob_students += 1

print(num_prob_students)