#!/usr/bin/env python
# coding: utf-8
#%% [markdown]
# # ASK HN vs. SHOW HN Comments
#
# We are going to compare two different types of posts(Ask HN or Show HN) to see wich posts receives more comments on average. We are also interested in if posts created at a certain time receive more comments on average.

# In[1]:
from csv import reader

opened_file = open("Projects\\Project2_Exploring_Hacker_News_Posts\\hacker_news.csv")
read_file = reader(opened_file)
hn = list(read_file)
hn[:5]


# In[2]:
# extract the first row of data
headers = hn[0]
# remove the headers from the list
hn = hn[1:]

print(headers)
print(hn[:5])


# In[3]:
ask_posts = []  # list to hold 'ask hn' posts
show_posts = []  # list to hold 'show hn' posts
other_posts = []  # list to hold all other posts

# for loop to append specific posts to its matching lists
for post in hn:
    title = post[1]
    if title.lower().startswith("ask hn"):
        ask_posts.append(post)
    elif title.lower().startswith("show hn"):
        show_posts.append(post)
    else:
        other_posts.append(post)

print("ask_posts has a total of", len(ask_posts), "posts")
print("show_posts has a total of", len(show_posts), "posts")
print("show_posts has a total of", len(other_posts), "posts")


# In[4]:
# Calculate the average number of comments `Ask HN` posts receive.
total_ask_comments = 0

for post in ask_posts:
    total_ask_comments += int(post[4])

avg_ask_comments = total_ask_comments / len(ask_posts)
print("Ask posts receive average of", avg_ask_comments, "comments")

# Calculate the average number of comments 'Show HN' posts receive
total_show_comments = 0
for post in show_posts:
    total_show_comments += int(post[4])

avg_show_comments = total_show_comments / len(show_posts)
print("Show posts receive average of", avg_show_comments, "comments")


# In average, ask posts receive more comments. Ask posts receive a total of about 14 comments per post while the show posts receive an average of about 10 comments per post.

# ## Finding the Amount of Ask Posts and Comments by Hour Created
# We will analyze how many posts were posted during a speicific time and how many comments those posts received.

# In[5]:
# import datetime module as dt
import datetime as dt
import operator

result_list = []

# append created_at column and comments column to result_list[]
# as a list[] with two elements
for post in ask_posts:
    created = post[6]
    comments = int(post[4])
    result_list.append([created, comments])

posts_by_hour = {}
comments_by_hour = {}
date_format = "%m/%d/%Y %H:%M"
# loop through result_list[] and parse the date to create a datetime object
for row in result_list:
    created_time = row[0]
    comments = row[1]
    # extract the %H(Hour) from the datetime object
    created_hour = dt.datetime.strptime(created_time, date_format).strftime("%H")
    if created_hour in posts_by_hour:
        posts_by_hour[created_hour] += 1
        comments_by_hour[created_hour] += comments
    else:
        posts_by_hour[created_hour] = 1
        comments_by_hour[created_hour] = comments

print("Number of Posts During a Speicific Hour")
print("------------------------------------------")
print(sorted(zip(posts_by_hour.keys(), posts_by_hour.values())))
print("\n")

print("Number of Comments During a Speicific Hour")
print("------------------------------------------")
print(sorted(zip(comments_by_hour.keys(), comments_by_hour.values())))

#%%[markdown]
# ## Calculate Average Number of Comments by the Hour for Ask HN Posts

# In[9]:
avg_by_hour = []
for hour in comments_by_hour:
    avg_by_hour.append([hour, comments_by_hour[hour] / posts_by_hour[hour]])

# sort the list using the itemgetter method from the operator module
sorted(avg_by_hour, key=operator.itemgetter(1), reverse=True)

# We will sort the above list using a different method to swap positions of the elements to make it easier to identify the hours with the highest values.

# In[10]:
swap_avg_by_hour = []
for row in avg_by_hour:
    swap_avg_by_hour.append([row[1], row[0]])
sorted_swap = sorted(swap_avg_by_hour, reverse=True)
sorted_swap


# In[14]:
print("Top 5 Hours for Ask Posts Comments")
for avg, hr in sorted_swap[:5]:
    template = "{hr}: {avg:.2f} average comments per post"
    output = template.format(
        hr=dt.datetime.strptime(hr, "%H").strftime("%H:%M"), avg=avg
    )
    print(output)

#%%[markdown]
# ## Conclusion
# From the above analysis, it seems like the most comments per post is received around 15:00 or 3:00 p.m. with an average of 38.59 comments per post. Overall, it seems like the best timeframe to post to receive the most comments is between 3-4 p.m. as these two timeframe receives total of 45 comments on average. If the post can't be made during this timeframe, the second best option will be around 8-9p.m. as it receives a total of about 38 comments on average.
