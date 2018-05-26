import unicodecsv

with open('project_submissions.csv', 'rb') as f:
    reader = unicodecsv.DictReader(f)
    projectSubmissions = list(reader)

print(projectSubmissions[1])