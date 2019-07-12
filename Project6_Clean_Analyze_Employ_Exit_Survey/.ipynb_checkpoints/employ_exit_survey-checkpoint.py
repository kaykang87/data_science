#%% [markdown]

# # Analyzing Employ Exit Survey
# We are working with exit surveys from employees of the Department of Education, Training and Employment (DETE) and the Technical and Further Education(TAFE) institute in Queensland, Australia.
#
# Figure out if employees who only worked for the institute for a short period of time are resigning due to some kind of dissatisfaction and  also for the employees who have been there longer.
#
# Figure out if younger employees are resigning due to some kind of dissatisfaction and also for the older employees.

#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

# read in dataframe
dete_survey = pd.read_csv(
    "Projects\\Project6_Clean_Analyze_Employ_Exit_Survey\\dete_survey.csv"
)
# read in dataframe
tafe_survey = pd.read_csv(
    "Projects\\Project6_Clean_Analyze_Employ_Exit_Survey\\tafe_survey.csv"
)

#%%
# print info about dete survey
print(dete_survey.info(), "\n")
dete_survey.head()

#%%
# print info about tafe survey
print(tafe_survey.info(), "\n")
tafe_survey.head()

#%% [markdown]
# # Observations
# * The dete_survey dataframe contains 'not stated' values that indicate values that are missing and not represented as NaN
# * dete_survey and tafe_survey contain many columns that we don't need to complete our analysis
# * Each dataframe contains many of the same columns, but the names are different
# * There are multiple columns/answers that indicate an employee resigned because they were dissatisfied

#%% [markdown]
# # Identify Missing Values
# Correct the 'Not Stated' values and drop columns that are not needed

#%%
# read the data without 'Not Stated' values as 'NaN'
dete_survey = pd.read_csv(
    "Projects\\Project6_Clean_Analyze_Employ_Exit_Survey\\dete_survey.csv",
    na_values="Not Stated",
)
dete_survey.head()

#%%
# update and remove columns that are not needed
dete_survey_updated = dete_survey.drop(dete_survey.columns[28:49], axis=1)
tafe_survey_updated = tafe_survey.drop(tafe_survey.columns[17:66], axis=1)

# verify the updated columns
print(dete_survey_updated.columns, "\n")
print(tafe_survey_updated.columns)

#%% [markdown]
# # Rename Columns
# Standardize columns so that we can eventually combine dataframes
# clean up column names
dete_survey_updated.columns = (
    dete_survey_updated.columns.str.lower().str.strip().str.replace("\s+", "_")
)
dete_survey_updated.columns

#%%
# match the common columns of tafe_survey to the dete_survey_updated
mapping = {
    "Record ID": "id",
    "CESSATION YEAR": "cease_date",
    "Reason for ceasing employment": "separationtype",
    "Gender. What is your Gender?": "gender",
    "CurrentAge. Current Age": "age",
    "Employment Type. Employment Type": "employment_status",
    "Classification. Classification": "position",
    "LengthofServiceOverall. Overall Length of Service at Institute (in years)": "institute_service",
    "LengthofServiceCurrent. Length of Service at current workplace (in years)": "role_service",
}
# rename the tafe_survey columns according to the mapping
tafe_survey_updated = tafe_survey_updated.rename(mapping, axis=1)

tafe_survey_updated.columns

#%% [markdown]
# We have renamed the dete_survey columns to standardize them and matched the tafe_survey columns that held common data to dete_survey columns.

#%% [markdown]
# # Filter the Data
# Filter the data so that we can analyze only the survey respondents that resigned

#%%
# Check unique values for the 'separationtype' columns
tafe_survey_updated["separationtype"].value_counts()

#%%
# Check unique values for the 'separationtype' columns
dete_survey_updated["separationtype"].value_counts()

#%%
# update the columns in dete_survey_updated so that all reasons for resignation is assigned only as 'resignation'
dete_survey_updated["separationtype"] = (
    dete_survey_updated["separationtype"].str.split("-").str[0]
)

dete_survey_updated["separationtype"].value_counts()

#%%
# Select only the resignation separation types from each dataframe
# use df.copy() incase to avoid the SettingWithCopy Warning
dete_resignations = dete_survey_updated[
    dete_survey_updated["separationtype"] == "Resignation"
].copy()
tafe_resignations = tafe_survey_updated[
    tafe_survey_updated["separationtype"] == "Resignation"
].copy()

#%% [markdown]
# # Verify The Data
# clean and explore the data columns to make sure all the dates make sense
# * *cease_date* should come after the *start_date*
# * it is unlikely that the *start_date* was before the year 1940 since most people start working in their 20s

#%%
# check unique values in cease_date column within the filtered dataframe
dete_resignations["cease_date"].value_counts()

#%%
# extract only the years and convert it to float
dete_resignations["cease_date"] = dete_resignations["cease_date"].str.split("/").str[-1]
dete_resignations["cease_date"] = dete_resignations["cease_date"].astype("float")
dete_resignations["cease_date"].value_counts().sort_index()

#%%
tafe_resignations["cease_date"].value_counts().sort_index()

#%%
# check for outliers
dete_resignations["dete_start_date"].value_counts().sort_values()

#%%
# create a boxplot of the dete_start_date_column
sns.boxplot(dete_resignations["dete_start_date"])

#%% [markdown]
# The years don't completely align in both dataframes
# dete_survey has no resignations in 2011 while the tafe_survey has the most resignations in 2011. There are also couple more years that the dataframes don't have the matching years.

#%% [markdown]
# # Creating a New Column
# Create a column containing hte length of time an employee spent in their worksplace, or years or service, in both dataframes
# * End goal: Are employees who have only worked for the institutes for a short period of time resigning due to some kind of dissatisfaction? What about employees who have been at the job longer?
# * End goal: Are young employees resigning due to some kind of dissatisfaction? What about employees who are older?

#%%
# Calculate the length of time an employee spent in their respective workplace and create a new column
dete_resignations["institute_service"] = (
    dete_resignations["cease_date"] - dete_resignations["dete_start_date"]
)

dete_resignations["institute_service"].head()

#%% [markdown]
# # Identify Dissatisfied Employees
# Columns we will use to categorized dissatisfied employees:
#
# 1. tafe_survey_updated:
#   * contributing factors. dissatisfaction
#   * contributing factors. job dissatisfaction
#
# 2. dafe_survey_updated:
#   * job_dissatisfaction
#   * dissatisfaction_with_the_department
#   * physical_work_environment
#   * lack_of_recognition
#   * lack_of_job_security
#   * work_location
#   * employment_conditions
#   * work_life_balance
#   * workload

#%% [markdown]
# If the employee indicates any of the factors above caused them to resign, we'll mark them as dissatisfied in a new column. The dissatisfied column will contain following values:
# * True: Resigned due to dissatisfaction in some way
# * False: Resigned because of reason other than dissatisfaction
# * NaN

#%%
# check unique values
tafe_resignations["Contributing Factors. Dissatisfaction"].value_counts()
#%%
# check unique values

# Check the unique values
tafe_resignations["Contributing Factors. Job Dissatisfaction"].value_counts()

#%%
# check unique values of multiple columns
dissatisfied_columns = [
    "job_dissatisfaction",
    "dissatisfaction_with_the_department",
    "physical_work_environment",
    "lack_of_recognition",
    "lack_of_job_security",
    "work_location",
    "employment_conditions",
    "work_life_balance",
    "workload",
]
dete_resignations[dissatisfied_columns].apply(pd.Series.value_counts)

#%%
# update values in contributing factors columns to be True, False, or NaN
def update_vals(x):
    if x == "-":
        return False
    elif pd.isnull(x):
        return np.nan
    else:
        return True


tafe_resignations["dissatisfied"] = (
    tafe_resignations[
        [
            "Contributing Factors. Dissatisfaction",
            "Contributing Factors. Job Dissatisfaction",
        ]
    ]
    .applymap(update_vals)
    .any(1, skipna=False)
)

tafe_resignations_up = tafe_resignations.copy()

# check unique values after the updates
tafe_resignations_up["dissatisfied"].value_counts(dropna=False)

#%%
# Update the values in columns related to dissatisfaction to be either True, False, or NaN by uaing any() function
dete_resignations["dissatisfied"] = dete_resignations[
    [
        "job_dissatisfaction",
        "dissatisfaction_with_the_department",
        "physical_work_environment",
        "lack_of_recognition",
        "lack_of_job_security",
        "work_location",
        "employment_conditions",
        "work_life_balance",
        "workload",
    ]
].any(1, skipna=False)
dete_resignations_up = dete_resignations.copy()
dete_resignations_up["dissatisfied"].value_counts(dropna=False)

#%% [markdown]
# # Combining the Data
# Add an institute column so that we can differentiate the data from each survey after we combine them. Then, combine the dataframes and drop any remaining columns we don't need

#%%
# Add an institute column
dete_resignations_up["institute"] = "DETE"
tafe_resignations_up["institute"] = "TAFE"

#%%
# combine the dataframes
combined = pd.concat(
    [dete_resignations_up, tafe_resignations_up], ignore_index=True, sort=True
)
combined.head()

#%%
# verify the number of not null values in each column
combined.notnull().sum().sort_values()

#%%
# drop columns with less than 500 non null values
combined_updated = combined.dropna(thresh=500, axis=1).copy()
combined_updated.notnull().sum().sort_values()

#%% [markdown]
# # Clean the Service Column
# Clean the institute_service column and categorize employees according to the following definitions
#
# * New : Less than 3 years in the workplace
# * Experienced: 3-6 years in the workplace
# * Established: 7-10 years in the workplace
# * Veteran: 11 or more years in the workplace

#%%
# check unique values
combined_updated["institute_service"].value_counts(dropna=False)

#%%
# Extract(one or more digits) the years of service and Save it to a new column
combined_updated["institute_service_up"] = (
    combined_updated["institute_service"].astype("str").str.extract(r"(\d+)")
)
# convert the type to float
combined_updated["institute_service_up"] = combined_updated[
    "institute_service_up"
].astype("float")
# Check the years extracted are correct
combined_updated["institute_service_up"].value_counts().sort_index()

#%%
# function to convert years of service to categories
def transform_service(val):
    if val >= 11:
        return "Veteran"
    elif 7 <= val < 11:
        return "Established"
    elif 3 <= val < 7:
        return "Experienced"
    elif pd.isnull(val):
        return np.nan
    else:
        return "New"


# create a new column to save the categories that has been returned by applying the transform_service function to the 'institute_service_up' column
combined_updated["service_cat"] = combined_updated["institute_service_up"].apply(
    transform_service
)

combined_updated["service_cat"].value_counts()

#%% [markdown]
# # Analysis Of Dissatisfaction Based On Years of Service

#%%
# unique values
combined_updated["dissatisfied"].value_counts(dropna=False)

#%%
# replace missing values in dissatisfied column with the most frequent value(False)
combined_updated["dissatisfied"] = combined_updated["dissatisfied"].fillna(False)
combined_updated["dissatisfied"].value_counts(dropna=False)

#%%
# calculate percentage of employees who resigned due to dissatisfaction in each category
dis_pct = combined_updated.pivot_table(index="service_cat", values="dissatisfied")

# Plot the results
dis_pct.plot(kind="bar", rot=30)

#%% [markdown]
# From the graph, employees with 7 or more years(Established & Veteran) of service are more likely to resign due to some kind of dissatisfaction

#%%
combined_updated["institute_service_up"].isnull().sum()
# drop the missing rows
combined_updated.dropna()

#%% [markdown]
# # Analysis Of Dissatisfaction Based On Age

#%%
# Clean the Age Column
combined_updated["age"] = combined_updated["age"].astype("str").str.extract(r"(\d+)")

# convert the age column to float
combined_updated['age'] = combined_updated['age'].astype('float')

# check unique values
combined_updated['age'].value_counts()

#%%
# function to convert age to categories
def transform_age(val):
       if val >= 50:
              return "Old"
       elif 40 <= val <= 50:
              return "Middle Aged"
       elif pd.isnull(val):
              return np.nan
       else:
              return "Young"

# Create a new column to save the age categories
combined_updated['age_cat'] = combined_updated['age'].apply(transform_age)

combined_updated['age_cat'].value_counts()       

#%%
dis_age = combined_updated.pivot_table(
    index="age_cat", values="dissatisfied"
)

# Plot the results
dis_age.plot(kind="bar", rot=30)

#%%
ax = sns.barplot(x='age_cat', y='institute_service_up', hue='dissatisfied', data=combined_updated)

#%%
ax = sns.barplot(x='service_cat', y='institute_service_up', hue='dissatisfied', data=combined_updated)

#%%
# Calculate each gender within the each age category
young_fem = combined_updated[(combined_updated['age_cat'] == 'Young') & (combined_updated['gender'] == 'Female') & (combined_updated['dissatisfied'] == True)]
young_male = combined_updated[(combined_updated['age_cat'] == 'Young') & (combined_updated['gender'] == 'Male') & (combined_updated['dissatisfied'] == True)]

middle_fem = combined_updated[(combined_updated['age_cat'] == 'Middle Aged') & (combined_updated['gender'] == 'Female') & (combined_updated['dissatisfied'] == True)]
middle_male = combined_updated[(combined_updated['age_cat'] == 'Middle Aged') & (combined_updated['gender'] == 'Male') & (combined_updated['dissatisfied'] == True)]

old_fem = combined_updated[(combined_updated['age_cat'] == 'Old') & (combined_updated['gender'] == 'Female') & (combined_updated['dissatisfied'] == True)]
old_male = combined_updated[(combined_updated['age_cat'] == 'Old') & (combined_updated['gender'] == 'Male') & (combined_updated['dissatisfied'] == True)]

print(young_fem.shape[0], 'dissatisfied young females')
print(young_male.shape[0], 'dissatisfied young males')
print()
print(middle_fem.shape[0], 'dissatisfied middle aged females')
print(middle_male.shape[0], 'dissatisfied middle aged males')
print()
print(old_fem.shape[0], 'dissatisfied old females')
print(old_male.shape[0], 'dissatisfied old males')

#%% [markdown]
# From the above bar plot, it shows that age group between 20-40 is the most dissatisfied
# Among the different age groups, it seems like females are more dissatisfied compared to man

#%% [markdown]
# Perform Data Analysis With FacetGrid

#%%
g = sns.FacetGrid(
    combined_updated,
    col="dissatisfied",
    hue="gender",
    legend_out=True,
    size = 4
)
g.map(sns.kdeplot, "age", shade=True).add_legend()

#%%
g = sns.FacetGrid(
    combined_updated,
    col="dissatisfied",
    hue="gender",
    legend_out=True,
    size = 4
)
g.map(sns.kdeplot, "institute_service_up", shade=True).add_legend()

#%%
g = sns.FacetGrid(
    combined_updated,
    col="dissatisfied",
    row='service_cat',
    hue="gender",
    legend_out=True,
    size = 4
)
g.map(sns.kdeplot, "age", shade=True).add_legend()

#%% [markdown]
# # Conclusion
# From the analysis, we can make a conclusion that veteran and established employees are more likely to resign due to dissatisfaction. 
# Also, older employees with more experience are more likely to be dissatisfied compared to younger employees. 
# Females seem to be more likely to resign due to dissatisfaction compared to males. Among the females, younger females are more likely to resign due to dissatisfaction.
# As employees gain experience, it might be likely that they are having dissatisfaction due to lack of promotions. 

#%%
