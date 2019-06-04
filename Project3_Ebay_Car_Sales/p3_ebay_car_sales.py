#!/usr/bin/env python
# coding: utf-8

# # Used Car Data from eBay Kleinanzeigen
#
# The aim of this project is to clean the data and analyze the included used car listing.

# In[1]:


import numpy as np
import pandas as pd

autos = pd.read_csv("Projects\Project3_Ebay_Car_Sales\\autos.csv",
                    encoding="Windows-1252")


# Print the autos data to inspect the data

# In[2]:


autos


# Use DataFrame.info() and DataFrame.head() methods to print information about the autos dataframe, as well as the first few rows.

# In[3]:


autos.info()
autos.head()


# Inspecting the data using the DataFrame.info() method, we can see that there are some columns with massing values. The columns with missing values are 'vehicleType', 'gearbox', 'model', 'fuelType', 'notRepairedDamage'. The autos dataframe has 5 columns with int data type and 15 columns with object data type.

# # Clean Columns

# In[4]:


autos.columns


# In[5]:


autos.columns = ['date_crawled', 'name', 'seller', 'offer_type', 'price', 'abtest',
                 'vehicle_type', 'registration_year', 'gearbox', 'power_ps', 'model',
                 'odometer', 'registration_month', 'fuel_type', 'brand',
                 'unrepaired_damage', 'ad_created', 'nr_of_pictures', 'postal_code',
                 'last_seen']
autos.head()


# Renamed multiple columns after inspecting the original column names using 'autos.columns'. All the camelcase names have been switched to snakecase. Column yearOfRegistration was renamed to registration_year. COlumn monthOfRegistration to registration_month. Column notRepairedDamage to unrepaired_damage. Column dateCreated to ad_created.

# # Initial Data Exploration and Cleaning

# In[6]:


autos.describe(include='all')


# The columns seller and offer_type seem to have the same values for all rows as it only 2 unique values. nr_of_pictures column is returning value of 0.0 for most statistics. postal_code and registration_year column also seems to need further investigation as the unique and top rows are missing values. price and odometer columns are numeric values stored as text.

# In[7]:


print(autos['seller'].value_counts())
print()
print(autos['offer_type'].value_counts())
print()
print(autos['nr_of_pictures'].value_counts())
print()
print(autos['postal_code'].value_counts().head())
print()
print(autos['registration_year'].value_counts().head())
print()
print(autos['price'].head())
print()
print(autos['odometer'].head())


# In[8]:


autos = autos.drop(["nr_of_pictures", "seller", "offer_type"], axis=1)
autos.columns


# Removed nr_of_pictures, seller, and offer_type columns from the dataframe because they either had 2 unique values or one values for all columns.

# # Cleaning Odometer and Price

# In[9]:


autos['price'] = (autos['price']
                  .str.replace('$', '')
                  .str.replace(',', '')
                  .astype(int)
                  )
autos['odometer'] = (autos['odometer']
                     .str.replace('km', '')
                     .str.replace(',', '')
                     .astype(int)
                     )
autos.rename({'odometer': 'odometer_km'}, axis=1, inplace=True)
print(autos['price'].head())
print(autos['odometer_km'].head())
print(autos.columns)


# Changed the text values to numeric values in the price and odometer column. Renamed the odometer column to odometer_km to specify the unit it is in.

# In[10]:


for column in ['odometer_km', 'price']:
    print(autos[column].unique().shape)
    print(autos[column].describe())
    print()
    print(autos[column].value_counts().sort_index(ascending=False).head(20))
    print()


# In[11]:


autos = autos[autos['price'].between(1, 351000)]
autos['price'].describe()


# Removed outliers that cost less than $1 and greater than $350000. The prices gradually increases upto 350000 and suddently jumps up which is suspicious. Although $1 car prices aren't realistic, because ebay is an auction site, there could be junk cars that are sold for that price.

# # Exploring the Date Columns

# In[12]:


autos[['date_crawled', 'ad_created', 'last_seen']][0:5]


# In[13]:


print(autos['date_crawled']
      .str[:10]
      .value_counts(normalize=True, dropna=False)
      .sort_index()
      )


# In[14]:


print(autos['date_crawled']
      .str[:10]
      .value_counts(normalize=True, dropna=False)
      .sort_values(ascending=False)
      )


# The site was crawled daily for about a month. The distribution is roughly normal.

# In[15]:


print(autos['last_seen']
      .str[:10]
      .value_counts(normalize=True, dropna=False)
      .sort_index())


# In[16]:


print(autos['last_seen']
      .str[:10]
      .value_counts(normalize=True, dropna=False)
      .sort_values(ascending=False))


# The last seen values includes listings of cars that were removed because it was sold. The values have gradually increased until the last date of crawling. It indicates that the auction period was probably for about a month until it was sold off or the listing for the auction has ended. There are least chance of the car getting sold off. The cars sale goes up as the the auction gets close to the end or the listing ends because of the duration limit of the ebay.

# In[17]:


print(autos['ad_created']
      .str[:10]
      .value_counts(normalize=True, dropna=False)
      .sort_index())


# ad_created dates span for about a year. It seems like most of the ads are created during March and falls off during other months.

# # Dealing with Incorrect Registration Year Data

# In[18]:


autos['registration_year'].describe()


# There are odd values within the registration_year column. Year 1000 was before any cars were even created and year 9999 is thounsands of years later in to the future

# In[19]:


autos['registration_year'].describe()


# In[20]:


print((autos["registration_year"].between(1900, 2019)).sum() / autos.shape[0])
(~autos["registration_year"].between(1900, 2019)).sum() / autos.shape[0]


# Given that the registration year between 1900 and 2016 is close to 100% of the data, it seems to be safe to remove anything beyond that.

# In[21]:


autos.loc[(autos['registration_year'] < 1900), 'registration_year']


# In[22]:


autos.loc[(autos['registration_year'] > 2019), 'registration_year']


# After reviewing the registration year, it seems reasonable to remove the cars that has the registration year prior to 1900 becaue the cars were invented in the late 1800s. Also because the current year is 2019, cars registered after this year can be removed as it is not possible to have a registration year of the future.

# In[23]:


autos = autos[autos['registration_year'].between(1900, 2019)]
autos['registration_year'].value_counts(normalize=True).head(50).sort_index()


# It seems that vehical registration started booming starting in the early 1990s. Late 1990s and early 2000s are where we see the most registration of vehicles.

# # Exploring Price by Brand

# In[24]:


autos['brand'].value_counts(normalize=True)


# It seems like the most popular brands are european car brands. Volkswagen is by far the most popular brand. There are brands with such a small value of percentage so we will limit our analysis to brands representing more than 5%.

# In[25]:


brand_counts = autos['brand'].value_counts(normalize=True)
common_brands = brand_counts[brand_counts > .05].index
print(common_brands)


# In[26]:


brand_mean_prices = {}

for brand in common_brands:
    brand_only = autos[autos['brand'] == brand]
    mean = brand_only['price'].mean()
    brand_mean_prices[brand] = int(mean)

brand_mean_prices


# Of the most 5 popular brands, it seems like Audi, BMW, and Benz are the most expensive. Volkswagen has a middle ground price among these top brands which suggests that consumers prefer the cars that are priced in a middle.

# # Exploring Mileage

# In[28]:


brand_mean_mileage = {}

for brand in common_brands:
    brand_only = autos[autos['brand'] == brand]
    mean_mileage = brand_only['odometer_km'].mean()
    brand_mean_mileage[brand] = int(mean_mileage)

brand_mean_mileage


# In[42]:


mean_price = pd.Series(brand_mean_prices).sort_values(ascending=False)
mean_mileage = pd.Series(brand_mean_mileage).sort_values(ascending=False)
print(mean_price)
print(mean_mileage)


# Converted the dictionaries average price and mileage to pandas Series by using the consturctor. The converted series will be entered into a new dataframe 'brand_info'.

# In[44]:


brand_info = pd.DataFrame(mean_price, columns=['mean_price'])
brand_info


# In[43]:


brand_info['mean_mileage'] = mean_mileage
brand_info


# It seems like the average mileage is about similar among all brands but there are big price differences. Even though Ford and Opel have similar or even less mileage than the top 3 brands, they are far less expensive.
