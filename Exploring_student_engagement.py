# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 11:40:25 2018
Exploring student engagement
code started from 171

@author: Ismail
"""




import unicodecsv
from datetime import datetime as dt

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


#Fixing data type
#Takes a date as string return a python datetyme object
#if there is no datetyme returns none
    
def parse_date(date):
    if date == '':
        return None
    else:
        return dt.strptime(date, '%Y-%m-%d')


#Take an empty string or with number
#Return int value

def parse_maybe_int(i):
    if i == '':
        return None
    else:
        return int(i)

#Clean up the data types in the enrollments table

for enrollment in enrollments:
    enrollment['cancel_date'] = parse_date(enrollment['cancel_date'])
    enrollment['days_to_cancel'] = parse_maybe_int(enrollment['days_to_cancel'])
    enrollment['is_canceled'] = enrollment['is_canceled'] == 'True'
    enrollment['is_udacity'] = enrollment['is_udacity'] == 'True'
    enrollment['join_date'] = parse_date(enrollment['join_date'])


#Clean up the data type in engagement table
    
for engagement_record in daily_engagement:
    engagement_record['lessons_completed'] = int(float(engagement_record['lessons_completed']))
    engagement_record['num_courses_visited'] = int(float(engagement_record['num_courses_visited']))
    engagement_record['projects_completed'] = int(float(engagement_record['projects_completed']))
    engagement_record['total_minutes_visited'] = float(engagement_record['total_minutes_visited'])
    engagement_record['utc_date'] = parse_date(engagement_record['utc_date'])

#Clean up the data type in the submission table

for submission in project_submissions:
    submission['completion_date'] = parse_date(submission['completion_date'])
    submission['creation_date'] = parse_date(submission['creation_date'])


#daily_engagement = read_csv('daily_engagement.csv')
for engagement_record in daily_engagement:
    engagement_record['account_key'] = engagement_record['acct']
    del[engagement_record['acct']]
    
unique_engagement_students = get_unique_data(daily_engagement)


udacity_test_accounts = set()
for enrollment in enrollments:
    if enrollment['is_udacity'] == True:
        udacity_test_accounts.add(enrollment['account_key'])
#print(len(udacity_test_accounts))

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

#print(len(non_udacity_enrollments))
#print(len(non_udacity_engagement))
#print(len(non_udacity_submissions))


paid_students = {}

#cnt = 0;
for enrollment in non_udacity_enrollments:
    if not enrollment['is_canceled']  or  enrollment['days_to_cancel'] > 7:
        account_key = enrollment['account_key']
        enrollment_date = enrollment['join_date']
        
        if account_key not in paid_students or enrollment_date > paid_students[account_key]:
            paid_students[account_key] = enrollment_date

print(len(paid_students))
#print(cnt)

#Getting data from first week
        

#Takes a student's join date and the date of a specific engagement record
#and returns True if that engagement record happened within one week
#of the student joining
def within_one_week(join_date, engagement_date):
    time_delta = engagement_date - join_date
    return  time_delta.days < 7

#Remove data point corresponds to any student who cancel trial

def remove_free_trial_cancel(data):
    new_data = []
    for data_point in data:
        if data_point['account_key'] in paid_students:
            new_data.append(data_point)
    return new_data

paid_enrollments = remove_free_trial_cancel(non_udacity_enrollments)
paid_engagement = remove_free_trial_cancel(non_udacity_engagement)
paid_submissions = remove_free_trial_cancel(non_udacity_submissions)

print(len(paid_enrollments))
print(len(paid_engagement))
print(len(paid_submissions))

 #create a list of rows from the engagement table including only rows
 #where the students is one of the paid students we just found
 #the date is within one week of the student's join date
 
paid_engagement_in_first_week = []

for engagement_record in paid_engagement:
    account_key = engagement_record['account_key']
    join_date = paid_students[account_key]
    engagement_record_date = engagement_record['utc_date']
    
    if within_one_week(join_date, engagement_record_date):
        paid_engagement_in_first_week.append(engagement_record)

print(len(paid_engagement_in_first_week))


        

#EXPLORING STUDENT ENGAGEMENT

from collections import defaultdict

engagement_by_account = defaultdict(list)
for engagement_record in paid_engagement_in_first_week:
    account_key = engagement_record['account_key']
    engagement_by_account[account_key].append(engagement_record)

total_minutes_by_account = {}

for account_key, engagement_for_student in engagement_by_account.items():
    total_minutes = 0
    for engagement_record in engagement_for_student:
        total_minutes += engagement_record['total_minutes_visited']
    total_minutes_by_account[account_key] = total_minutes

total_minutes = list(total_minutes_by_account.values())#numpy class is written for python 2 
                                                        #but in python 3 .values returns a dictionary
                                                        #so we have to convert it into list

import numpy as np

#mean_of_minutes = np.mean(total_minutes)
print()
print('Mean:', np.mean(total_minutes))
print('standard deviation:',np.std(total_minutes))
print('Minimum:', np.min(total_minutes))
print('Maximum:', np.max(total_minutes))
