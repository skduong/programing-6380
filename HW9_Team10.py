import numpy as np
import pandas as pd
import datetime

match = pd.read_excel('Match_History.xlsx')
students = pd.read_excel('Student.xlsx')
tutors = pd.read_excel('Tutor.xlsx')
studentsMatched = pd.merge(students, match, how='outer')

def q1(): #tutors with dropped status and certification after 4/1/2018
    return list(tutors['TutorID'][(tutors['TutorStatus'] == 'Dropped') & (tutors['CertDate'] > '2018-04-01')])

def q2(): #average length of tutoring
    start = match['StartDate'].apply(lambda x: x.date())
    end = match['EndDate'].apply(lambda x: x.date()).fillna(datetime.date.today())
    return np.mean(end - start).days
 
def q3(): #students matched in 2018 tutors with temp stop status
    merged = pd.merge(pd.merge(tutors, match.loc[match['StartDate'].dt.year==2018]), students)
    return list(merged.loc[merged['TutorStatus']=='Temp Stop']['StudentID'])

def q4(): #read score of students taught by tutors with dropped status
    return list(pd.merge(pd.merge(tutors.loc[tutors['TutorStatus']=='Dropped'], match), students)['ReadScore'])

def q5(): #tutors who taught 2+ students
    return list(np.unique(match['TutorID'])[np.unique(match['TutorID'], return_counts=True)[1]>1])
    
def q6(): #all students and their scores, tutors, tutor statuses
    merged = pd.merge(studentsMatched, tutors, how='left').set_index(['StudentID'])
    return merged[['ReadScore', 'TutorID', 'TutorStatus']]
    
def q7(): #all student groups and tutor count     
    merged = pd.merge(studentsMatched, tutors, how='left').set_index(['StudentGroup']).dropna(
        subset =['TutorID'])['TutorID'].sort_index().index.value_counts(sort=False)
    return pd.DataFrame(data={'StudentGroups': merged.index, 'NumberOfTutors': merged.values}).to_string(index=False)

def q8(): #active students who started in May or June
    merged = studentsMatched.dropna(subset= ['StartDate'])
    return list(merged.loc[(merged['EndDate'].isna()) & ((merged['StartDate'].dt.month == 5) | (merged['StartDate'].dt.month == 6))]['StudentID'])

def q9(): #students who have not been tutored
    return list(studentsMatched.loc[studentsMatched['MatchID'].isna()]['StudentID'])

def q10(): #tutors who did not tutor
     return list(tutors['TutorID'][~tutors['TutorID'].isin(match['TutorID'])].dropna())

#save Query 6 to Excel, also display all queries
q6().to_excel('Student_Tutor.xlsx')
print('Query 1:', q1(), '\nQuery 2:', q2(), 'days', '\nQuery 3:', q3(), '\nQuery 4:', q4(), '\nQuery 5:', q5(), 
      '\nQuery 6:', q6(), '\nQuery 7:', q7(), '\nQuery 8:', q8(), '\nQuery 9:', q9(), '\nQuery 10:', q10())