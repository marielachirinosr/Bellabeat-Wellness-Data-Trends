import pandas as pd 
import numpy as np

# Read CSV 
general_activity = pd.read_csv ('Fitabase Data 4.12.16-5.12.16/dailyActivity_merged.csv')
sleep_day_info = pd.read_csv ('Fitabase Data 4.12.16-5.12.16/sleepDay_merged.csv')
weight_log = pd.read_csv ('Fitabase Data 4.12.16-5.12.16/weightLogInfo_merged.csv')

# Summary information CSV
print(general_activity.describe())
print(general_activity.info())
print(sleep_day_info.describe())
sleep_day_info.info()
print(weight_log.describe())
weight_log.info()

# Date format
general_activity['ActivityDate'] = pd.to_datetime(general_activity['ActivityDate'], format='%m/%d/%Y').dt.date
sleep_day_info['SleepDay'] = pd.to_datetime(sleep_day_info['SleepDay'], format='%m/%d/%Y %I:%M:%S %p').dt.date
weight_log['Date'] = pd.to_datetime(weight_log['Date'], format='%m/%d/%Y %I:%M:%S %p').dt.date

# Print number of duplicate rows before removal
duplicate_count = sleep_day_info.duplicated().sum()
duplicate_count_general = general_activity.duplicated().sum()
duplicate_count_weight_log = weight_log.duplicated().sum()
print("Number of duplicate rows before removal:", duplicate_count, duplicate_count_general, duplicate_count_weight_log)

# Remove duplicate rows based on all columns
sleep_day_info = sleep_day_info.drop_duplicates()

# Merge dataframes
general_activity = pd.merge(general_activity, sleep_day_info[['Id', 'SleepDay', 'TotalSleepRecords', 'TotalMinutesAsleep', 'TotalTimeInBed']],
                            how='left', left_on=['Id', 'ActivityDate'], right_on=['Id', 'SleepDay'])

general_activity = pd.merge(general_activity, weight_log[['Id', 'Date', 'WeightKg', 'WeightPounds', 'BMI', 'Fat']],
                            how='left', left_on=['Id', 'ActivityDate'], right_on=['Id', 'Date'])

# Drop redundant columns
general_activity = general_activity.drop(columns=['SleepDay', 'Date'])

# Replace NaN values with actual NaN
general_activity = general_activity.replace('NaN', np.nan)

# Add day of the week column
general_activity['DayOfWeek'] = pd.to_datetime(general_activity['ActivityDate']).dt.dayofweek

# Add user type column
general_activity['UserType'] = np.select(
    [
    (general_activity['TotalSteps'] >= 10000),
    (general_activity['TotalSteps'] >= 7500) & (general_activity['TotalSteps'] <= 9999),
    (general_activity['TotalSteps'] >= 5000) & (general_activity['TotalSteps'] <= 7499),
    (general_activity['TotalSteps'] < 5000)
    ],
    ['Highly Active', 'Somewhat Active', 'Low Active', 'Sedentary'], #source https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3197470/
    default='Other'
)

# Create a new column with TimeHoursAsleep 
general_activity['TotalHoursAsleep'] = general_activity['TotalMinutesAsleep'] / 60
general_activity['TotalHourInBed'] = general_activity['TotalTimeInBed'] / 60
general_activity['SedentaryHours'] = general_activity['SedentaryMinutes'] / 60
general_activity['VeryActiveHours'] = general_activity['VeryActiveMinutes'] / 60

# Total of users by combination with sleep and heart rate
total_unique_users = general_activity['Id'].nunique()
print("Total number of unique users:", total_unique_users)

users_per_sleep = general_activity.groupby(['Id', 'TotalMinutesAsleep']).size().reset_index(name='UserCount')
total_unique_users_combination_sleep = users_per_sleep['Id'].nunique()
print("Total number of unique users with sleep records:", total_unique_users_combination_sleep)

users_per_weight = general_activity.groupby(['Id', 'WeightKg']).size().reset_index(name='UserCount')
total_unique_users_combination_weight = users_per_weight['Id'].nunique()
print("Total number of unique users with weight records:", total_unique_users_combination_weight)

user_type_counts = general_activity['UserType'].value_counts()

# Print or display the counts
print(user_type_counts)

# Organize CSV
general_activity = general_activity[['Id','ActivityDate', 'DayOfWeek', 'UserType', 'TotalSteps' , 'TotalDistance' , 'TrackerDistance' , 'LoggedActivitiesDistance' , 'VeryActiveDistance' , 'ModeratelyActiveDistance', 'LightActiveDistance' , 'SedentaryActiveDistance' , 'VeryActiveMinutes' ,'VeryActiveHours', 'FairlyActiveMinutes', 'LightlyActiveMinutes', 'SedentaryMinutes' , 'SedentaryHours', 'Calories' , 'TotalSleepRecords' , 'TotalMinutesAsleep' , 'TotalHoursAsleep',  'TotalTimeInBed','TotalHourInBed', 'WeightKg' , 'WeightPounds' , 'BMI' , 'Fat']]

# Export to CSV
general_activity.to_csv('general_daily_activity.csv', index=False, na_rep='NaN')

# Displaying the result
print(general_activity)