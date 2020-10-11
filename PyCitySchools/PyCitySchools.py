# -*- coding: utf-8 -*-
import pandas as pd
# File to Load (Remember to Change These)
school_data_to_load = ".\Resources\schools_complete.csv"
student_data_to_load = ".\Resources\students_complete.csv"
#
# Report at district level
#
# Read School and Student Data File and store into Pandas DataFrames
school_df = pd.read_csv(school_data_to_load)
student_df = pd.read_csv(student_data_to_load)
# Combine the data into a single dataset.  
school_and_student_df = pd.merge(student_df, school_df, how="left", on=["school_name", "school_name"])
# Total Schools
numSchools = school_df['School ID'].count()
# Total Students
numStudents = student_df['Student ID'].count()
# Total Budget
totalBudget = school_df['budget'].sum()
# Average Math Score
avgMathScore = round(student_df['math_score'].mean(),6)
# Average Reading Score
avgReadingScore = round(student_df['reading_score'].mean(),6)
# Percentage of students that passed math; score >= 70)
percPassMath = round(student_df['math_score'][student_df['math_score'] >= 70].count()/numStudents*100,6)
# Percentage of students that passed reading. ; score >= 70)
percPassReading = round(student_df['reading_score'][student_df['reading_score'] >= 70].count()/numStudents*100,6)
# Percentage Overall Passing (The percentage of students that passed math **and** reading.)
percPassBoth = round(student_df['math_score'][(student_df['math_score'] >= 70) & (student_df['reading_score'] >= 70)].count()/numStudents*100,6)
# Create a high level snapshot (in table form)
districtResults_df = pd.DataFrame({
                    'Total Schools':[numSchools],
                       'Total Students':[numStudents],
                       'Total Budget':[totalBudget],
                       'Average Math Score':[avgMathScore],
                       'Average Reading Score':[avgReadingScore],
                       '% Passing Math':[percPassMath],
                       '% Passing Reading':[percPassReading],
                       '% Overall Passing':[percPassBoth]},
                      columns=['Total Schools','Total Students','Total Budget','Average Math Score','Average Reading Score','% Passing Math','% Passing Reading','% Overall Passing'])                       
# Format Total Students with commas and Budget as money
districtResults_df['Total Students'] = districtResults_df['Total Students'].astype(int).map('{:,}'.format)
districtResults_df['Total Budget'] = districtResults_df['Total Budget'].astype(float).map('${:,.2f}'.format)
print(districtResults_df)
#
# School Summary Report
#
# Setup Group by school
schoolGrp = school_and_student_df.set_index('school_name').groupby(['school_name'])
schoolType = school_df.set_index('school_name')['type']
schoolNumStudents = schoolGrp['Student ID'].count()
schoolBudget = school_df.set_index('school_name')['budget']
schoolPerStudentBudget = school_df.set_index('school_name')['budget']/school_df.set_index('school_name')['size']
schoolAvgMathScore = schoolGrp['math_score'].mean()
schoolAvgReadingScore = schoolGrp['reading_score'].mean()
schoolPercPassMath = school_and_student_df[school_and_student_df['math_score'] >= 70].groupby('school_name')['Student ID'].count()/schoolNumStudents*100
schoolPercPassReading = school_and_student_df[school_and_student_df['reading_score'] >= 70].groupby('school_name')['Student ID'].count()/schoolNumStudents*100
schoolPercPassBoth = school_and_student_df[(school_and_student_df['math_score'] >= 70) & (school_and_student_df['reading_score'] >= 70)].groupby('school_name')['Student ID'].count()/schoolNumStudents*100
schoolResults_df = pd.DataFrame({
                    'School Type':schoolType,
                       'Total Students':schoolNumStudents,
                       'Total School Budget':schoolBudget,
                       'Per Student Budget':schoolPerStudentBudget,
                       'Average Math Score':schoolAvgMathScore,
                       'Average Reading Score':schoolAvgReadingScore,
                       '% Passing Math':schoolPercPassMath,
                       '% Passing Reading':schoolPercPassReading,
                       '% Overall Passing':schoolPercPassBoth,},
                      columns=['School Type','Total Students','Total School Budget','Per Student Budget','Average Math Score','Average Reading Score','% Passing Math','% Passing Reading','% Overall Passing'])                       
# Format Budget metrics as money$
schoolResults_df['Total School Budget'] = schoolResults_df['Total School Budget'].astype(float).map('${:,.2f}'.format)
schoolResults_df['Per Student Budget'] = schoolResults_df['Per Student Budget'].astype(float).map('${:,.2f}'.format)
# District schools
schoolResults_df
# Top 5 performing schools
print(schoolResults_df.sort_values('% Overall Passing', ascending=False).head())
# Bottom 5 performing schools
print(schoolResults_df.sort_values('% Overall Passing', ascending=True).head())