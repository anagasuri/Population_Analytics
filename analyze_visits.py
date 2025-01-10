# Using the cleaned data and insurance category file from Question 1:

# 1. Load and structure the data:
#    - Read the processed CSV file
#    - Convert visit_date to datetime
#    - Sort by patient_id and visit_date
import pandas as pd

# read in cleaned csv file
df = pd.read_csv("ms_data.csv")

# add names to each column
df.columns = ['patient_id','visit_date','age','education_level','walking_speed']

# convert visit date to datetime
df['visit_date'] = pd.to_datetime(df['visit_date'])

# sort by patient_id and visit_date
df = df.sort_values(['patient_id', 'visit_date']).reset_index(drop=True)

# 2. Add insurance information:
#    - Read insurance types from `insurance.lst`
#    - Randomly assign (but keep consistent per patient_id)
#    - Generate visit costs based on insurance type:
#      - Different plans have different effects on cost
#      - Add random variation

import random
import numpy as np 

# Read in insurance.lst
dfIns = pd.read_csv('insurance.lst')
insTypes = dfIns['insurance_type'].tolist() 

# Initialize an empty dictionary to map random insurance to each patient_id
patientInsDict = {}

# Populate the dictionary with patient_id as keys and random insurance types as values
for ids in df['patient_id'].unique():
    patientInsDict[ids] = random.choice(insTypes)

# Add the mapped insurance types to the DataFrame
df['insurance_type'] = df['patient_id'].map(patientInsDict)

# insurance costs 
insCosts = {'Lower': 1, 'Middle': 2, 'Highest': 3}

# insurance by season
seasonsCategory = {1: 'Winter', 2:'Winter', 3:'Spring', 4:'Spring',
                    5:'Spring', 6:'Summer', 7:'Summer', 8:'Summer', 
                    9: 'Fall', 10:'Fall', 11:'Fall', 12:'Winter'} 

# map visit_date to season
df['season'] = df['visit_date'].dt.month.map(seasonsCategory) 

# assign cost to insurance type 
df['visit_cost'] = df['insurance_type'].map(insCosts) + np.random.uniform(-10, 10, size=len(df))

# 3. Calculate summary statistics:
#    - Mean walking speed by education level
#    - Mean costs by insurance type
#    - Age effects on walking speed

meanWalkingSpeed = df.groupby('education_level')['walking_speed'].mean()
print(meanWalkingSpeed)

meanInsType = df.groupby('insurance_type')['visit_cost'].mean()
print(meanInsType)

effectAgeOnSpeed = df['age'].corr(df['walking_speed'])
print(effectAgeOnSpeed)

df.to_csv("ms_data_edited.csv", index=False)