# -*- coding: utf-8 -*-
import pandas as pd
# pd.set_option("display.max_columns",10)
# Location of student and school data
school_data_to_load = ".\Resources\schools_complete.csv"
student_data_to_load = ".\Resources\students_complete.csv"
#
# District-Level summary report
# Read school and student data file and store into Pandas DataFrame
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
avgMathScore = student_df['math_score'].mean()
# Average Reading Score
avgReadingScore = student_df['reading_score'].mean()
# Percentage of students that passed math; score >= 70)
percPassMath = student_df['math_score'][student_df['math_score'] >= 70].count()/numStudents*100
# Percentage of students that passed reading. ; score >= 70)
percPassReading = student_df['reading_score'][student_df['reading_score'] >= 70].count()/numStudents*100
# Percentage Overall Passing (The percentage of students that passed math **and** reading.)
percPassBoth = student_df['math_score'][(student_df['math_score'] >= 70) & (student_df['reading_score'] >= 70)].count()/numStudents*100
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
print("PyCity District Summary Report")
print(districtResults_df)
#
# School-Level summary report
# Read and setup Pandas DataFrame Group-by school
school_grp = school_and_student_df.set_index('school_name').groupby(['school_name'])
# Setup series objects for school-report DataFrame
schoolType = school_df.set_index('school_name')['type']
schoolNumStudents = school_grp['Student ID'].count()
schoolBudget = school_df.set_index('school_name')['budget']
schoolPerStudentBudget = school_df.set_index('school_name')['budget']/school_df.set_index('school_name')['size']
schoolAvgMathScore = school_grp['math_score'].mean()
schoolAvgReadingScore = school_grp['reading_score'].mean()
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
# Display all district schools
print("PyCity Schools Summary Report")
print(schoolResults_df)
# Display top-5 performing schools in district based on % Overall Passing
print("Top 5 PyCity Schools by % Overall Passing")
print(schoolResults_df.sort_values('% Overall Passing', ascending=False).head())
# Display Bottom 5-performing schools in district based on % Overall Passing
print("Bottom 5 PyCity Schools by % Overall Passing")
print(schoolResults_df.sort_values('% Overall Passing', ascending=True).head())
#
# Display student math scores by grade; 9-12th
school9_grp = school_and_student_df[school_and_student_df['grade'] == '9th'].groupby('school_name')
school10_grp = school_and_student_df[school_and_student_df['grade'] == '10th'].groupby('school_name')
school11_grp = school_and_student_df[school_and_student_df['grade'] == '11th'].groupby('school_name')
school12_grp = school_and_student_df[school_and_student_df['grade'] == '12th'].groupby('school_name')
math_scores_df = pd.DataFrame({
        '9th Grade': school9_grp['math_score'].mean(),
        '10th Grade': school10_grp['math_score'].mean(),
        '11th Grade': school11_grp['math_score'].mean(),
        '12th Grade': school12_grp['math_score'].mean()},
        columns=['9th Grade','10th Grade','11th Grade','12th Grade'])
print("Student Average Math Scores by Grade")
print(math_scores_df)
#
# Display student Reading scores by grade; 9-12th
school9_grp = school_and_student_df[school_and_student_df['grade'] == '9th'].groupby('school_name')
school10_grp = school_and_student_df[school_and_student_df['grade'] == '10th'].groupby('school_name')
school11_grp = school_and_student_df[school_and_student_df['grade'] == '11th'].groupby('school_name')
school12_grp = school_and_student_df[school_and_student_df['grade'] == '12th'].groupby('school_name')
reading_scores_df = pd.DataFrame({
        '9th Grade': school9_grp['reading_score'].mean(),
        '10th Grade': school10_grp['reading_score'].mean(),
        '11th Grade': school11_grp['reading_score'].mean(),
        '12th Grade': school12_grp['reading_score'].mean()},
        columns=['9th Grade','10th Grade','11th Grade','12th Grade'])
print("Student Average Reading Scores by Grade")
print(reading_scores_df)
#
# Scores by school spending
# Setup 4 spending bins
spending_bin = [0, 585, 630, 645, 675]
spending_bin_name = ["<$584", "$585-629", "$630-644", "$645-675"]
# Setup measures
school_and_student_df['avg_budget'] = school_and_student_df['budget'] / school_and_student_df['size']
school_and_student_df['Spending Ranges (Per Student)'] = pd.cut(school_and_student_df["avg_budget"], spending_bin, labels = spending_bin_name)
spending_grp = school_and_student_df.groupby('Spending Ranges (Per Student)')
spendingNumStudents = spending_grp['Student ID'].count()
spendingAvgMathScore = spending_grp['math_score'].mean()
spendingAvgReadingScore = spending_grp['reading_score'].mean()
spendingPercPassMath = school_and_student_df[school_and_student_df['math_score'] >= 70].groupby('Spending Ranges (Per Student)')['math_score'].count()/spendingNumStudents*100
spendingPercPassReading = school_and_student_df[school_and_student_df['reading_score'] >= 70].groupby('Spending Ranges (Per Student)')['reading_score'].count()/spendingNumStudents*100
spendingPercBoth = school_and_student_df[(school_and_student_df['math_score'] >= 70) & (school_and_student_df['reading_score'] >= 70)].groupby('Spending Ranges (Per Student)')['Student ID'].count()/spendingNumStudents*100
spendingSchool_df = pd.DataFrame({
        "Average Math Score": spendingAvgMathScore,
        "Average Reading Score": spendingAvgReadingScore,
        "% Passing Math": spendingPercPassReading,
        "% Passing Reading": spendingPercPassReading,
        "% Overall Passing": spendingPercBoth
    },
    columns=["Average Math Score", "Average Reading Score", "% Passing Math", "% Passing Reading", "% Overall Passing"])
print("Scores by School Spending")
print(spendingSchool_df)
#
# Scores by school size
# Setup 3 size bins
size_bin = [0, 1000, 2000, 5000]
size_bin_name = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]
# Setup measures
school_and_student_df['School Size'] = pd.cut(school_and_student_df["size"], size_bin, labels = size_bin_name)
size_grp = school_and_student_df.groupby('School Size')
sizeNumStudents = size_grp['Student ID'].count()
sizeAvgMathScore = size_grp['math_score'].mean()
sizeAvgReadingScore = size_grp['reading_score'].mean()
sizePercPassMath = school_and_student_df[school_and_student_df['math_score'] >= 70].groupby('School Size')['math_score'].count()/sizeNumStudents*100
sizePercPassReading = school_and_student_df[school_and_student_df['reading_score'] >= 70].groupby('School Size')['reading_score'].count()/sizeNumStudents*100
sizePercBoth = school_and_student_df[(school_and_student_df['math_score'] >= 70) & (school_and_student_df['reading_score'] >= 70)].groupby('School Size')['Student ID'].count()/sizeNumStudents*100
sizeSchool_df = pd.DataFrame({
        "Average Math Score": sizeAvgMathScore,
        "Average Reading Score": sizeAvgReadingScore,
        "% Passing Math": sizePercPassReading,
        "% Passing Reading": sizePercPassReading,
        "% Overall Passing": sizePercBoth
    },
    columns=["Average Math Score", "Average Reading Score", "% Passing Math", "% Passing Reading", "% Overall Passing"])
print("Scores by School Size")
print(sizeSchool_df)
#
# Scores by school type
# Setup measures
type_grp = school_and_student_df.groupby('type')
typeNumStudents = type_grp['Student ID'].count()
typeAvgMathScore = type_grp['math_score'].mean()
typeAvgReadingScore = type_grp['reading_score'].mean()
typePercPassMath = school_and_student_df[school_and_student_df['math_score'] >= 70].groupby('type')['math_score'].count()/typeNumStudents*100
typePercPassReading = school_and_student_df[school_and_student_df['reading_score'] >= 70].groupby('type')['reading_score'].count()/typeNumStudents*100
typePercBoth = school_and_student_df[(school_and_student_df['math_score'] >= 70) & (school_and_student_df['reading_score'] >= 70)].groupby('type')['Student ID'].count()/typeNumStudents*100
typeSchool_df = pd.DataFrame({
        "Average Math Score": typeAvgMathScore,
        "Average Reading Score": typeAvgReadingScore,
        "% Passing Math": typePercPassReading,
        "% Passing Reading": typePercPassReading,
        "% Overall Passing": typePercBoth
    },
    columns=["Average Math Score", "Average Reading Score", "% Passing Math", "% Passing Reading", "% Overall Passing"])
print("Scores by School Type")
print(typeSchool_df)
