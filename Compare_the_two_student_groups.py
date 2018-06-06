# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 18:01:58 2018
Compare the student groups
Code start from line 325
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
    return  time_delta.days < 7 and time_delta.days >= 0 #Debugging data analysis code solution


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


#NUMBER OF VISITS IN FIRST WEEK

for engagement_record in paid_engagement:
    if engagement_record['num_courses_visited'] > 0:
        engagement_record['has_visited'] = 1
    else:
        engagement_record['has_visited'] = 0



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

#DEBUGGING DATA ANALYSIS CODE SOLUTION

student_with_maximum_minutes = None
max_minutes = 0

for student,total_minutes in total_minutes_by_account.items():
    if total_minutes > max_minutes:
        max_minutes = total_minutes
        student_with_max_minutes = student

print()
print()
print('Debugging data analysis code solution:')
print()
print('Maximum minutes:', max_minutes)

"""
for engagement_record in paid_engagement_in_first_week:
    if engagement_record['account_key'] == student_with_max_minutes:
        print(engagement_record)
        """


#LESSON COMPLETED FOR FIRST WEEK
print()
print()
print('Lesson completed in first week:')

def group_data(data, key_name):
    grouped_data = defaultdict(list)
    
    for data_point in data:
        key = data_point[key_name]
        grouped_data[key].append(data_point)
    return grouped_data

engagement_by_account = group_data(paid_engagement_in_first_week, 'account_key')

def sum_grouped_items(grouped_data, field_name):
    summed_data ={}
    
    for key, data_points in grouped_data.items():
        total = 0
        for data_point in data_points:
            total += data_point[field_name]
        summed_data[key] = total
    return summed_data

total_minutes_by_account = sum_grouped_items(engagement_by_account, 'total_minutes_visited')


def describe_data(data):
    print('Mean:', np.mean(data))
    print('Standard deviation:', np.std(data))
    print('Minimum:', np.min(data))
    print('Maximum:',np.max(data))

total_minutes = list(total_minutes_by_account.values())
describe_data(total_minutes)

print()
lesson_completed_by_account = sum_grouped_items(engagement_by_account, 'lessons_completed')

describe_data(list(lesson_completed_by_account.values()))


#some code from Number of visits in first week

print()
print()
print('Number of visits in first week : ')
print()
days_visited_by_account = sum_grouped_items(engagement_by_account, 'has_visited')

describe_data(list(days_visited_by_account.values()))


#SPLITITNG OUT PASSING STUDENTS

print()
print()
print('Splitting out passing students:')
print()


subway_project_lesson_keys = ['746169184', '3176718735']

pass_subway_project = set()

for submission in paid_submissions:
    project = submission['lesson_key']
    rating = submission['assigned_rating']
    
    if project in subway_project_lesson_keys and (rating == 'PASSED' or rating == 'DISTINCTION'):
        pass_subway_project.add(submission['account_key'])

print('Length of pass_subway_project:', len(pass_subway_project)) 


passing_engagement = []
non_passing_engagement = []

for engagement_record in paid_engagement_in_first_week:
    if engagement_record['account_key'] in pass_subway_project:
        passing_engagement.append(engagement_record)
    else:
        non_passing_engagement.append(engagement_record)
    
print('Length of passing_engagement:', len(passing_engagement))
print('Length of non_passing_engagement:', len(non_passing_engagement))



#COMPARE THE TWO STUDENT GROUPS
print()
print()
print('Compare the two student groups:')
print()
passing_engagement_by_account = group_data(passing_engagement, 'account_key')

non_passing_engagement_by_account = group_data(non_passing_engagement, 'account_key')

print('Non_passing_students:')
non_passing_minutes = sum_grouped_items(non_passing_engagement_by_account, 'total_minutes_visited')
describe_data(list(non_passing_minutes.values()))

print('Passing_students:')
passing_minutes = sum_grouped_items(passing_engagement_by_account, 'total_minutes_visited')
describe_data(list(passing_minutes.values()))

print()
print('For lessons completed:')


print('Non_passing_students:')
non_passing_minutes = sum_grouped_items(non_passing_engagement_by_account, 'lessons_completed')
describe_data(list(non_passing_minutes.values()))

print('Passing_students:')
passing_minutes = sum_grouped_items(passing_engagement_by_account, 'lessons_completed')
describe_data(list(passing_minutes.values()))

print()
print('For has_visited:')

print('Non_passing_students:')
non_passing_minutes = sum_grouped_items(non_passing_engagement_by_account, 'has_visited')
describe_data(list(non_passing_minutes.values()))

print('Passing_students:')
passing_minutes = sum_grouped_items(passing_engagement_by_account, 'has_visited')
describe_data(list(passing_minutes.values()))