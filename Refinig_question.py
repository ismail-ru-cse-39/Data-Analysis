# -*- coding: utf-8 -*-
"""
Created on Thu May 31 01:06:18 2018

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
project_submissions = read_csv('project_submissions.csv')

#daily_engagement = read_csv('daily_engagement.csv')
for engagement_record in daily_engagement:
    engagement_record['account_key'] = engagement_record['acct']
    del[engagement_record['acct']]
    
unique_engagement_students = get_unique_data(daily_engagement)


udacity_test_accounts = set()
for enrollment in enrollments:
    if enrollment['is_udacity'] == 'True':
        udacity_test_accounts.add(enrollment['account_key'])
print(len(udacity_test_accounts))

#function to remove udacity accounts
 
def remove_udacity_accounts(data):
    non_udacity_data = []
    for data_point in data:
        if data_point['account_key'] not in udacity_test_accounts:
            non_udacity_data.append(data_point)
    return non_udacity_data

non_udacity_enrollments = remove_udacity_accounts(enrollments)
non_udacity_engagement = remove_udacity_accounts(daily_engagement)
non_udacity_submissions = remove_udacity_accounts(project_submissions)

print(len(non_udacity_enrollments))
print(len(non_udacity_engagement))
print(len(non_udacity_submissions))


paid_students = {}

cnt = 0;
for enrollment in non_udacity_enrollments:
    if enrollment['is_canceled'] == 'False' or (enrollment['days_to_cancel'] != '' and int(enrollment['days_to_cancel']) > 7):
        account_key = enrollment['account_key']
        enrollment_date = enrollment['join_date']
        paid_students[account_key] = enrollment_date

print(len(paid_students))
#print(cnt)
