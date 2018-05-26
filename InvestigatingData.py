# -*- coding: utf-8 -*-
"""
Created on Fri May 25 14:05:29 2018

@author: Ismail
"""

import unicodecsv

def read_csv(filename):
    with open(filename, 'rb') as f:
        reader = unicodecsv.DictReader(f);
        
        return list(reader)

enrollments = read_csv('enrollments.csv')
daily_engagement = read_csv('daily_engagement.csv')
project_submissions = read_csv('project_submissions.csv')

#investigating the data

#for enrollments.csv

length_enrollments = len(enrollments)

unique_enrolled_students = set()

for enrollment in enrollments:
    unique_enrolled_students.add(enrollment['account_key'])

length_unique_enrolled_students = len(unique_enrolled_students)

print('Length of enrollments:')
print(length_enrollments)
print('Length of unique enrolled students:')
print(length_unique_enrolled_students)
print()

#for daily_engagement.csv

length_daily_engagement = len(daily_engagement)

unique_engagement_students = set()

for engagement_record in daily_engagement:
    unique_engagement_students.add(engagement_record['acct'])

length_unique_engagement_students = len(unique_engagement_students)

print('Length of daily_engagement: ')
print(length_daily_engagement)
print('Length of unique_engagement_students: ')
print(length_unique_engagement_students)
print()

#for project_submissions.csv

length_project_submissions = len(project_submissions)

unique_project_submitters = set()

for submission in project_submissions:
    unique_project_submitters.add(submission['account_key'])

length_unique_project_submitters = len(unique_project_submitters)

print('Length of project_submissions: ')
print(length_project_submissions)
print('Length of unique_project_submitters: ')
print(length_unique_project_submitters)



    