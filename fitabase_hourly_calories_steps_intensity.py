import pandas as pd
from fitabase_general_activity import general_activity

# Read CSV
hourly_calories = pd.read_csv('Fitabase Data 4.12.16-5.12.16/hourlyCalories_merged.csv')
hourly_steps = pd.read_csv('Fitabase Data 4.12.16-5.12.16/hourlySteps_merged.csv')
hourly_intensities = pd.read_csv('Fitabase Data 4.12.16-5.12.16/hourlyIntensities_merged.csv')

# Summary information CSV
print(hourly_calories.describe())
print(hourly_calories.info())
print(hourly_steps.describe())
print(hourly_steps.info())
print(hourly_intensities.describe())
print(hourly_intensities.info())

# Date format
hourly_calories['ActivityHour'] = pd.to_datetime(hourly_calories['ActivityHour'], format='%m/%d/%Y %I:%M:%S %p')
hourly_steps['ActivityHour'] = pd.to_datetime(hourly_steps['ActivityHour'], format='%m/%d/%Y %I:%M:%S %p')
hourly_intensities['ActivityHour'] = pd.to_datetime(hourly_intensities['ActivityHour'], format='%m/%d/%Y %I:%M:%S %p')

# Print number of duplicate rows before removal
duplicate_count_intensities = hourly_intensities.duplicated().sum()
duplicate_count_calories = hourly_calories.duplicated().sum()
duplicate_count_steps = hourly_steps.duplicated().sum()
print("Number of duplicate rows before removal:", duplicate_count_intensities, duplicate_count_calories, duplicate_count_steps)

# Merge dataframes
df_merge = pd.merge(hourly_calories, hourly_steps, 
                    how='left', on=['Id', 'ActivityHour'])

df_merge = pd.merge(df_merge, hourly_intensities, 
                    how='left', on=['Id', 'ActivityHour'])




# Add day of the week column
df_merge['DayOfWeek'] = pd.to_datetime(df_merge['ActivityHour']).dt.dayofweek

# Convert to datatime type
df_merge['ActivityHour'] = pd.to_datetime(df_merge['ActivityHour']) 

# Extract date and time into separate columns
df_merge['Date'] = df_merge['ActivityHour'].dt.date
df_merge['Time'] = df_merge['ActivityHour'].dt.time

# Assuming 'Id' and 'Date' are the common columns for merging
df_merge = pd.merge(df_merge, general_activity[['Id', 'ActivityDate', 'UserType']], 
                      how='inner', left_on=['Id', 'Date'], right_on=['Id', 'ActivityDate'])

# Drop redundant columns
df_merge = df_merge.drop(columns=['ActivityHour'])

# Organize df_merge columns
df_merge = df_merge[['Id','Date', 'Time', 'DayOfWeek', 'UserType', 'Calories', 'StepTotal', 'TotalIntensity', 'AverageIntensity']]

# Displaying the result
print(df_merge)

# Export to CSV
df_merge.to_csv('hourly_activity.csv', index=False, na_rep='NaN')
