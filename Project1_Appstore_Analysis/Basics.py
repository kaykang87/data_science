#%% [markdown]
# # Profitable Apps That Attracts More Users
# 
# We only build aps that are free to download and install, and our main source of revenue consists of in-app ads. Source of revenue is mostly influenced by the number of users who uses the app.
# 
# The goal for this project is to analyze data to help developers understand what kinds of apps are likely to attract more users to increase our revenue.

#%%
from csv import reader
# Open AppleStore Data and Separate Data from Header
opened_file = open('AppleStore.csv')
read_file = reader(opened_file)
apple_list = list(read_file)
apple_header = apple_list[0]
apple_data = apple_list[1:]

# Open AndroidStore Data and Separate Data from Header
opened_file = open('googleplaystore.csv')
read_file = reader(opened_file)
android_list = list(read_file)
android_header = android_list[0]
android_data = android_list[1:]


#%%
# Function to return wanted data interval and number of rows and columns based on user's request
def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]
    for row in dataset_slice:
        print(row)
        print('\n')
    print('Number of rows:', len(dataset))
    #print('Number of columns:', len(dataset[0]))

print(apple_header)
print('\n')
explore_data(apple_data, 0, 3, True)
print('\n')

print(android_header)
print('\n')
explore_data(android_data, 0, 3, True)
print('\n')


#%%
print(android_header)
print('\n')
# The data with incorrect information. It is missing data and has columns shifted.
print(android_data[10472])
print('\n')
print('Number of Android Data Before Deletion of Invalid Row', len(android_data))
del android_data[10472]
print('Number of Android Data After Deletion of Invalid Row', len(android_data))

#%% [markdown]
# Row 10472 had invalid data. It was missing the category section which resulted in the shift of other columns. It caused the data to have rating of 19, which is not possible since the highest rating in the app store is 5.

#%%
# Finding Duplicate Data In Google Play Store
unique_list = []
duplicate_list = []

for row in android_data:
    name = row[0]
    if name in unique_list:
        duplicate_list.append(name)
    else:
        unique_list.append(name)

print('Number of duplicate apps:', len(duplicate_list))

#%% [markdown]
# After finding the duplicate apps, we will try to keep the one with the latest updated information. This can be based on number of installs. The data with the most installs will be kept. 
# 
# This can be done by creating a dictionary
# * Create a dictionary where each key is the unique app name, and value is the number of installs of that app
# * Use the dictionary to create a new data set, which will have only one entry per app (and we only select the apps with the highest number of installs)
# 
# Android data should only include unique apps. To count the number of unique apps, we need to substract the duplicate apps from the android data.

#%%
print('Expected number of unique apps:', len(android_data) - 1181)

#%% [markdown]
# Let's start by building the dictionary to keep only the apps with the most amount of installs. The dictionary will loop through each app and overwrite the existing value for the app name when it finds the number of installs with higher number than the existing value.

#%%
reviews_max = {}

for app in android_data:
    name = app[0]
    n_reviews = float(app[3])
    
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
        
    elif name not in reviews_max:
        reviews_max[name] = n_reviews

print('Actual Number of unique apps:', len(reviews_max))        

#%% [markdown]
# Now, let's use the reviews_max dictionary to remove the duplicates. For the duplicate cases, we'll only keep the entries with the highest number of reviews. In the code cell below:
# 
# We start by initializing two empty lists, android_clean and already_added.
# We loop through the android data set, and for every iteration:
# We isolate the name of the app and the number of reviews.
# We add the current row (app) to the android_clean list, and the app name (name) to the already_cleaned list if:
# The number of reviews of the current app matches the number of reviews of that app as described in the reviews_max dictionary; and
# The name of the app is not already in the already_added list. **We need to add this supplementary condition to account for those cases where the highest number of reviews of a duplicate app is the same for more than one entry (for example, the Box app has three entries, and the number of reviews is the same). If we just check for reviews_max[name] == n_reviews, we'll still end up with duplicate entries for some apps.**

#%%
android_clean = []
already_added = []
for app in android_data:
    name = app[0]
    n_reviews = float(app[3])
    
    if (n_reviews == reviews_max[name]) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)


#%%
explore_data(android_clean, 0, 3, True)

#%% [markdown]
# We have 9659 apps as expected.
#%% [markdown]
# We will remove non-english apps by using the [ASCII](https://en.wikipedia.org/wiki/ASCII) system. English uses number that is equal to or less than 127 so we will use this number to create a condition to figure out if the language is english or not. 

#%%
def check_language(string):
    for character in string:
        if ord(character) > 127:
            return False
    return True

print(check_language('Instagram'))
print(check_language('안녕'))
print(check_language('Instachat 😜'))
print(check_language('Docs To Go™ Free Office Suite'))

#%% [markdown]
# The function checks the language to a certain point but because it doesn't recognize some symbols and emojis, it returns false even if the app is using english. To prevent some data loss of these english apps that includes certain symbols, we'll only remove an app if its name has more than three characters with corresponding numbers failing outside the ASCII range.

#%%
def check_language(string):
    non_ascii = 0
    for character in string:
        if ord(character) > 127:
            non_ascii +=1
    if non_ascii > 3:
        return False
    else:
        return True

print(check_language('Instagram'))
print(check_language('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(check_language('Instachat 😜'))
print(check_language('Docs To Go™ Free Office Suite'))


#%%
android_english_app = []
android_nonenglish_app = []
for app in android_clean:
    name = app[0]
    if check_language(name):
        android_english_app.append(app)
    else:
        android_nonenglish_app.append(app)

ios_english_app = []
ios_nonenglish_app = []
for app in apple_data:
    name = app[1]
    if check_language(name):
        ios_english_app.append(app)
    else:
        ios_nonenglish_app.append(app)
        
explore_data(android_english_app, 0, 3, True)
print('\n')
explore_data(android_nonenglish_app, 0, 3, True)
print('\n')
explore_data(ios_english_app, 0, 3, True)   
print('\n')
explore_data(ios_nonenglish_app, 0, 1, True)  
print('\n')


#%%
android_free_app = []
ios_free_app = []
for app in android_english_app:
    price = app[7]
    if price == '0':
        android_free_app.append(app)
for app in ios_english_app:   
    price = app[4]
    if price == '0.0':
        ios_free_app.append(app)

print('Number of Free Android Apps:', len(android_free_app))        
print('Number of Free iOS Apps:', len(ios_free_app))

#%% [markdown]
# Among the cleaned data, we need to find the most popular genre in each app store. This information will provide us with the knowledge of which genre is the most popular and possibly most profitable.
# 
# To minimize risks and overhead, our validation strategy for an app idea is comprised of three steps:
# 
# 1. Build a minimal Android version of the app, and add it to Google Play.
# 2. If the app has a good response from users, we then develop it further.
# 3. If the app is profitable after six months, we also build an iOS version of the app and add it to the App Store.

#%%
def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])

def freq_table(dataset, index): 
    frequency_table = {}
    total = 0
    for app in dataset:
        total += 1
        value = app[index]
        if value in frequency_table:
            frequency_table[value] +=1
        else:
            frequency_table[value] = 1

    freq_table_percentages = {}
    for key in frequency_table:
        percentage = (frequency_table[key] / total) * 100
        freq_table_percentages[key] = percentage 
    
    return freq_table_percentages

#%% [markdown]
# We will now analyze the prime_genre column of the iOS App Store.

#%%
print('iOS Prime Genres')
print('---------------------------')
display_table(ios_free_app, -5)

#%% [markdown]
# We can see that among the free English apps, more than a half (58.16%) are games. Entertainment apps are close to 8%, followed by photo and video apps, which are close to 5%. Only 3.66% of the apps are designed for education, followed by social networking apps which amount for 3.29% of the apps in our data set.
# 
# The general impression is that App Store (at least the part containing free English apps) is dominated by apps that are designed for fun (games, entertainment, photo and video, social networking, sports, music, etc.), while apps with practical purposes (education, shopping, utilities, productivity, lifestyle, etc.) are more rare. However, the fact that fun apps are the most numerous doesn't also imply that they also have the greatest number of users — the demand might not be the same as the offer.
# 
# We will now analyze the Category and Genres column of the Google Play Data Set

#%%
print('Android Genres')
print('---------------------------')
display_table(android_free_app, -4)
print('\n')
print('Android Category')
print('---------------------------')
display_table(android_free_app, 1)

#%% [markdown]
# The landscape seems significantly different on Google Play: there are not that many apps designed for fun, and it seems that a good number of apps are designed for practical purposes (family, tools, business, lifestyle, productivity, etc.). However, if we investigate this further, we can see that the family category (which accounts for almost 19% of the apps) means mostly games for kids.
# 
# The difference between the Genres and the Category columns is not crystal clear, but one thing we can notice is that the Genres column is much more granular (it has more categories). We're only looking for the bigger picture at the moment, so we'll only work with the Category column moving forward.
# 
# Up to this point, we found that the App Store is dominated by apps designed for fun, while Google Play shows a more balanced landscape of both practical and for-fun apps. Now we'd like to get an idea about the kind of apps that have most users.
#%% [markdown]
# To figure out which genre is the most popular, we can calculate the average number of installs or the average number of user ratings for the app. To calculate the average number of user ratings for each genre, we'll need to use a for loop inside of another for loop. The first for loop will loop through each genre in the dictionary. The second for loop will loop through the genres in the dataset to match the genre in the dictionary. If the match is found, it will tally up the ratings and the number of apps in that genre to calculate the average rating.

#%%
ios_genres = freq_table(ios_free_app, -5)

for genre in ios_genres:
    total = 0
    len_genre = 0
    for app in ios_free_app:
        genre_app = app[-5]
        if genre_app == genre:
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    avg_n_ratings = total / len_genre
    print(genre, ':', avg_n_ratings)

#%% [markdown]
# We can see that navigation app has the most number of ratings so let's analyze what is included in that genre. We will also look at the Entertainment genre because it is a very popular category in the Android app store. It seems like it is uncharacteristic for this genre to have such a little number of ratings so we'll see if there are potential in this genre.

#%%
for app in ios_free_app:
    if app[-5] == 'Navigation':
        print(app[1], ':', app[5]) # print name and number of ratings
print('\n')                
for app in ios_free_app:
    if app[-5] == 'Entertainment':
        print(app[1], ':', app[5])        

#%% [markdown]
# The Navigation genre in the Apple app store seems very skewed because it is heavily dominated by two apps(Waze and Google Maps). The Entertainment genre seems to have potential because they are less skewed and iOS app store has such a little number of reviews compared to Android app store.

#%%
android_category = freq_table(android_free_app, 1)

for category in android_category:
    total = 0
    len_category = 0
    for app in android_free_app:
        category_app = app[1]
        if category_app == category:
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)

#%% [markdown]
# On average, communication apps have the most installs: 38,456,119. This number is heavily skewed up by a few apps that have over one billion installs (WhatsApp, Facebook Messenger, Skype, Google Chrome, Gmail, and Hangouts), and a few others with over 100 and 500 million installs. Let's analyze the communication category in the android app store.

#%%
for app in android_free_app:
    if app[1] == 'COMMUNICATION':
        print(app[0], ':', app[5])


#%%
for app in android_free_app:
    if app[1] == 'COMMUNICATION' and (app[5] == '1,000,000,000+'
                                      or app[5] == '500,000,000+'
                                      or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


#%%
under_100_m = []

for app in android_free_app:
    n_installs = app[5]
    n_installs = n_installs.replace(',', '')
    n_installs = n_installs.replace('+', '')
    if (app[1] == 'COMMUNICATION') and (float(n_installs) < 100000000):
        under_100_m.append(float(n_installs))
        
sum(under_100_m) / len(under_100_m)

#%% [markdown]
# If we removed communications app that has over 100m installs, the average number of install is reduced drastically because it is heavily skewed by few apps. 

#%%
for app in android_free_app:
    if app[1] == 'ENTERTAINMENT':
        print(app[0], ':', app[5])

#%% [markdown]
# The Entertainment category seems to be dominated by streaming services. There are some niche apps, such as drawing, that has over 10 million installs but not many. There are a lot of apps that are targeted towards kids. 

#%%
for app in android_free_app:
    if app[1] == 'ENTERTAINMENT' and (app[5] == '1,000,000,000+'
                                            or app[5] == '500,000,000+'
                                            or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])

#%% [markdown]
# Entertainment apps that are extremely popular with over 100m installs are pretty balanced. There are couple streaming apps along with review and information providing app for movies and tv shows. Interestingly, there are also apps that doesn't provide streaming services. Talking angela and Talking Ben The Dog are interactive apps for kids. From these top apps in this category, it shows that ENTERTAINMENT category is used by Adults and Kids at the same time.

#%%
for app in android_free_app:
    if app[1] == 'ENTERTAINMENT' and (app[5] == '1,000,000+'
                                            or app[5] == '5,000,000+'
                                            or app[5] == '10,000,000+'
                                            or app[5] == '50,000,000+'):
        print(app[0], ':', app[5])

#%% [markdown]
# Most apps within 1,000,000+ and 50,000,000+ are streaming apps. There are some variation because some picture and image manipulating tools but it is heavily dominated by streaming services. 
#%% [markdown]
# # Conclusion
# In this project, we analyzed data about the App Store and Google Play mobile apps with the goal of recommending an app profile that can be profitable for both markets.
# 
# Although Communication and Navigation category has the most number of installs in google play store and iOS store, it seems like the Entertainment category has more potential for success. It is able to target both adults and kids and is less dominated by couple apps. It seems like users download multiple Entertainment apps for their needs compared to Communication and Navigation where users only use the top apps in the store.

