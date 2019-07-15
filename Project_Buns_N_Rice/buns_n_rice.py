#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#%%
# read in dataframe
hourly_sales = pd.read_csv(
    "Projects\Project_Buns_N_Rice\Hourly Sales Performance by Revenue Class.csv"
)

#%%
# drop the unneeded columns and make the changes in the dataframe itself by using inplace=True
cols = [0, 1, 5, 6, 7, 11, 12, 13, 20, 21]
hourly_sales.drop(hourly_sales.columns[cols], axis="columns", inplace=True)
hourly_sales.head()

#%%
# check for missing values
hourly_sales.isnull().sum()

#%%
# check the unique value of hours and drop the values that are outside the range of operating hours of the store
print(hourly_sales["create_hour_ordinal"].value_counts())

hourly_sales_up = hourly_sales[
    (hourly_sales["create_hour_ordinal"] != 16)
    & (hourly_sales["create_hour_ordinal"] != 5)
]
print(hourly_sales_up["create_hour_ordinal"].value_counts().sort_index())

#%%
# create a pivot table to get total sales of individual hours
pivot_table = hourly_sales_up.pivot_table(
    index="create_hour_ordinal", values="c_ticketitem_net_price", aggfunc=np.sum
)
pivot_table.plot(kind="bar")

#%%
# Create a pivot table to get the sum of sales based on specific hours of each day
# pivot_table = hourly_sales_up.pivot_table(values='c_ticketitem_net_price', index=['create_hour_ordinal', 'create_day'], aggfunc=np.sum)
pivot_table = hourly_sales_up.pivot_table(
    index="create_hour_ordinal",
    columns="create_day",
    values="c_ticketitem_net_price",
    aggfunc=np.sum,
)

pivot_table = pivot_table.reindex_axis(
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], axis=1
)

pivot_table

#%%
# create a bar plot that shows the sum of sales based on specific hours of each day
pivot_table.plot(
    kind="bar",
    width=0.8,
    ylim=(0, 5000),
    yticks=[500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000],
).legend(loc="center left", bbox_to_anchor=(1, 0.5))

#%%
# stacked bar plot of the above code
pivot_table.plot(kind="bar", stacked=True, width=0.8).legend(
    loc="center left", bbox_to_anchor=(1, 0.5)
)

#%%
# create a pivot table to see total itemgroup sales per hour
pivot_table = hourly_sales_up.pivot_table(
    index="create_day",
    columns="ItemGroup",
    values="c_ticketitem_net_price",
    aggfunc=np.sum,
)

# drop unused columns
pivot_table.drop(
    ["**Dine In**", "--To Go--", "No Item Group"], axis="columns", inplace=True
)

# reorder the pivot table
pivot_table = pivot_table.reindex_axis(
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
)

pivot_table

#%%
# create a bar plot to see total itemgroup sales per hour
pivot_table.plot(kind="bar", width=0.9).legend(
    loc="center left", bbox_to_anchor=(1, 0.5)
)

#%%
# calculate how many each categories sold during specific hour
hourly_cat = {}
for h in hourly_sales_up["create_hour_ordinal"].unique():
    selected_rows = hourly_sales_up[hourly_sales_up["create_hour_ordinal"] == h]
    cat_sum = selected_rows["ItemGroup"].value_counts()
    hourly_cat[h] = cat_sum

for key in hourly_cat:
    print(f"Sales at {key}")
    print(hourly_cat[key])
    print("\n")
