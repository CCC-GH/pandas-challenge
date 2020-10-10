# -*- coding: utf-8 -*-
# Dependencies and Setup
import pandas as pd
# File to Load (Remember to Change These)
school_data_to_load = ".\Resources\schools_complete.csv"
student_data_to_load = ".\Resources\students_complete.csv"
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
totalBudget = round(school_df['budget'].sum(),2)
# Average Math Score
avgMathScore = round(student_df['math_score'].mean(),6)
# Average Reading Score
avgReadingScore = round(student_df['reading_score'].mean(),6)
# Percentage of students that passed math; score >= 70)
percPassMath = round(student_df['math_score'][student_df['math_score'] >= 70].count()/numStudents*100,6)
# Percentage of students that passed reading. ; score >= 70)
percPassReading = round(student_df['reading_score'][student_df['reading_score'] >= 70].count()/numStudents*100,6)
# Percentage Overall Passing (The percentage of students that passed math **and** reading.)
percPassBoth = round(student_df['reading_score'][(student_df['math_score'] >= 70) & (student_df['reading_score'] >= 70)].count()/numStudents*100,6)
# Create a high level snapshot (in table form)
summaryResults_df = {'Total Schools':[numSchools],'Total Students':[numStudents],'Total Budget':[totalBudget],'Average Math Score':[avgMathScore],'Average Reading Score':[avgReadingScore],'% Passing Math':[percPassMath],'% Passing Reading':[percPassReading],'% Overall Passing':[percPassBoth]}
summaryResults_df
#
# School Summary
#
