# %%
import pandas as pd
import matplotlib.pyplot as plt

# %% [markdown]
# # Introduction
# Visualize the gender gap across college degrees. Generate line charts to compare across all degree categories.

# %% [markdown]
# Compare each degrees within the STEM category

# %%
women_degrees = pd.read_csv('percent-bachelors-degrees-women-usa.csv')
cb_dark_blue = (0/255, 107/255, 164/255)
cb_orange = (255/255, 128/255, 14/255)
stem_cats = ['Engineering', 'Computer Science', 'Psychology',
             'Biology', 'Physical Sciences', 'Math and Statistics']
lib_arts_cats = ['Foreign Languages', 'English', 'Communications and Journalism',
                 'Art and Performance', 'Social Sciences and History']
other_cats = ['Health Professions', 'Public Administration',
              'Education', 'Agriculture', 'Business', 'Architecture']

fig = plt.figure(figsize=(18, 3))

# use for loop to graph different degrees against 'Year'
for sp in range(0, 6):
    ax = fig.add_subplot(1, 6, sp+1)
    ax.plot(women_degrees['Year'], women_degrees[stem_cats[sp]],
            c=cb_dark_blue, label='Women', linewidth=3)
    ax.plot(women_degrees['Year'], 100-women_degrees[stem_cats[sp]],
            c=cb_orange, label='Men', linewidth=3)
    ax.set_xlim(1968, 2011)
    ax.set_ylim(0, 100)
    ax.set_title(stem_cats[sp])
    ax.tick_params(bottom="off", top="off", left="off", right="off")

    for key, spine in ax.spines.items():
        spine.set_visible(False)
    """
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)    
    ax.spines["bottom"].set_visible(False)
    """
    if sp == 0:
        ax.text(2005, 87, 'Men')
        ax.text(2002, 8, 'Women')
    elif sp == 5:
        ax.text(2005, 62, 'Men')
        ax.text(2001, 35, 'Women')

# %% [markdown]
# ## Compare STEM to Other Degree Categories
# Compare other degree categories to the stem degrees by organizing them into a column.
# Export to a file.
# %%
fig = plt.figure(figsize=(15, 25))

# Generate first column of line charts
# use for loop to graph different degrees against 'Year'
for sp in range(0, 18, 3):
    # divides the subplot by 3 to match the index of the degree list. plots graph into 1, 4, 7, 11, 15
    cat_index = int(sp/3)
    ax = fig.add_subplot(6, 3, sp+1)
    ax.plot(women_degrees['Year'], women_degrees[stem_cats[cat_index]],
            c=cb_dark_blue, label='Women', linewidth=3)
    ax.plot(women_degrees['Year'], 100-women_degrees[stem_cats[cat_index]],
            c=cb_orange, label='Men', linewidth=3)

    ax.set_xlim(1968, 2011)
    ax.set_ylim(0, 100)
    ax.set_title(stem_cats[cat_index])
    ax.tick_params(bottom="off", top="off", left="off",
                   right="off", labelbottom='off')
    ax.set_yticks([0, 100])
    ax.axhline(50, c=(171/255, 171/255, 171/255), alpha=0.3)

    for key, spine in ax.spines.items():
        spine.set_visible(False)
    """
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)    
    ax.spines["bottom"].set_visible(False)
    """
    if cat_index == 0:
        ax.text(2005, 87, 'Men')
        ax.text(2003, 8, 'Women')
    elif cat_index == 5:
        ax.text(2005, 62, 'Men')
        ax.text(2003, 35, 'Women')
        ax.tick_params(labelbottom='on')

# chart for male and female in liberal arts category
for sp in range(1, 16, 3):
    # calculate to the index matches the list. plots into 2,5,8,11,14
    cat_index = int((sp-1)/3)
    ax = fig.add_subplot(6, 3, sp+1)
    ax.plot(women_degrees['Year'], women_degrees[lib_arts_cats[cat_index]],
            c=cb_dark_blue, label='Women', linewidth=3)
    ax.plot(women_degrees['Year'], 100-women_degrees[lib_arts_cats[cat_index]],
            c=cb_orange, label='Men', linewidth=3)

    for key, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xlim(1968, 2011)
    ax.set_ylim(0, 100)
    ax.set_title(lib_arts_cats[cat_index])
    ax.tick_params(bottom="off", top="off", left="off",
                   right="off", labelbottom='off')
    ax.set_yticks([0, 100])
    ax.axhline(50, c=(171/255, 171/255, 171/255), alpha=0.3)

    if cat_index == 0:
        ax.text(2005, 75, 'Women')
        ax.text(2003, 20, 'Men')
        ax.tick_params(labelbottom='on')

# chart for all other categories
for sp in range(2, 18, 3):
    cat_index = int((sp-2)/3)
    ax = fig.add_subplot(6, 3, sp+1)
    ax.plot(women_degrees['Year'], women_degrees[other_cats[cat_index]],
            c=cb_dark_blue, label='Women', linewidth=3)
    ax.plot(women_degrees['Year'], 100-women_degrees[other_cats[cat_index]],
            c=cb_orange, label='Men', linewidth=3)

    for key, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xlim(1968, 2011)
    ax.set_ylim(0, 100)
    ax.set_title(other_cats[cat_index])
    ax.tick_params(bottom="off", top="off", left="off",
                   right="off", labelbottom='off')
    ax.set_yticks([0, 100])
    ax.axhline(50, c=(171/255, 171/255, 171/255), alpha=0.3)

    if cat_index == 0:
        ax.text(2003, 90, 'Women')
        ax.text(2005, 5, 'Men')
    elif cat_index == 5:
        ax.text(2005, 62, 'Men')
        ax.text(2003, 30, 'Women')
        ax.tick_params(labelbottom='on')

fig.savefig('gender_degrees.png')
