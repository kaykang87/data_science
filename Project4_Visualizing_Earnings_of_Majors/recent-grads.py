# %%
from pandas.plotting import scatter_matrix
import pandas as pd
import matplotlib.pyplot as plt

# %% [markdown]
## Introduction
# This project will compare the earnings based on different college majors

# %% [markdown]
# Overview of data

# %%
recent_grads = pd.read_csv(
    "./Project4_Visualizing_Earnings_of_Majors/recent-grads.csv")
recent_grads.describe()

# %% [markdown]
# Observing through the data
# Displays the first row of the data along with first 5 rows and last 5 rows.
# Drops the missing values and compares it to the original data

# %%
# print first row
print(recent_grads.iloc[0])
print()
# print first 5 rows
print(recent_grads.head())
print()
# print last 5 rows
print(recent_grads.tail())
print()
# count of rows
raw_data_count = recent_grads.shape[0]
recent_grads = recent_grads.dropna()
# count of rows after dropping missing values
cleaned_data_count = recent_grads.shape[0]
print("raw data count", raw_data_count)
print("cleaned_data_count", cleaned_data_count)

# %%[markdown]
## Creating Scatter Plots

# %%
ax = recent_grads.plot(x='Sample_size', y='Employed', kind='scatter')
ax.set_title('Employed vs. Sample_size')

ax1 = recent_grads.plot(x='Sample_size', y='Median', kind='scatter')
ax1.set_title('Median vs. Sample_size')

ax2 = recent_grads.plot(x='Sample_size', y='Unemployment_rate', kind='scatter')
ax2.set_title('Unemployment_rate vs. Sample_size')

ax3 = recent_grads.plot(x='Full_time', y='Median', kind='scatter')
ax2.set_title('Median vs. Full_time')

ax4 = recent_grads.plot(x='ShareWomen', y='Unemployment_rate', kind='scatter')
ax4.set_title('Unemployment_rate vs. Sharewomen')

ax5 = recent_grads.plot(x='Men', y='Median', kind='scatter')
ax5.set_title('Median vs. Men')

ax6 = recent_grads.plot(x='Women', y='Median', kind='scatter')
ax6.set_title('Median vs. Women')


# %% [markdown]
## Pandas, Histograms
# Creating multiple histograms using a for-loop

# %%
cols = ["Sample_size", "Median", "Employed", "Full_time",
        "ShareWomen", "Unemployment_rate", "Men", "Women"]
fig = plt.figure(figsize=(10, 35))
for r in range(1, 9):
    ax = fig.add_subplot(8, 1, r)
    ax = recent_grads[cols[r-1]].plot(kind='hist', rot=40)

# %%
# %% [markdown]
## Pandas, Scatter Matrix Plot

# %%
scatter_matrix(recent_grads[['Sample_size', 'Median']], figsize=(6, 6))


# %%
scatter_matrix(
    recent_grads[['Sample_size', 'Median', 'Unemployment_rate']], figsize=(10, 10))

# %% [markdown]
## Pandas, Bar Plots

# %%
recent_grads[:10].plot.bar(x='Major', y='ShareWomen', legend=False)
recent_grads[163:].plot.bar(x='Major', y='ShareWomen', legend=False)
