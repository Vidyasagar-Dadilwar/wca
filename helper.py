import re
import emoji
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd

extractor = URLExtract()


def fetchStats(selected_user, df):
    # Fetch the stats for the selected user
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    # fetch no. of messages
    num_messages = df.shape[0]

    num_media_messages = df[df['message'] == "<Media omitted>\n"].shape[0]

    # fetch no. of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch no. of links shared
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), len(links), num_media_messages
    

def most_busy_users(df):
    x = df['users'].value_counts().head()
    df = round ((df ['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
    columns={'index': 'name', 'user': 'percent' })
    return x, df

# function to create wordcloud
def create_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    f = open('stop_words_hinglish.txt', 'r')
    stop_words = f.read()
    # removing group notifications
    temp = df[df['users'] != 'group_notification']
    # removing media omitted
    temp = temp[temp['message'] != "<Media omitted>\n"]

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc


def most_common_words(selected_user, df):

    # reading stop_words file containing hinglish stop words
    f = open('stop_words_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    # removing group notifications
    temp = df[df['users'] != 'group_notification']
    # removing media omitted
    temp = temp[temp['message'] != "<Media omitted>\n"]

    # taking most common words
    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)


    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df 


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis = []

    for message in df[ 'message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    
    emoji_counts = Counter(emojis)
    total_count = sum(emoji_counts.values())
    
    # Separate emojis based on the 2% threshold
    above_threshold = {k: v for k, v in emoji_counts.items() if v / total_count > 0.02}
    below_threshold = {k: v for k, v in emoji_counts.items() if v / total_count <= 0.02}

    # Add "Others" category
    if below_threshold:
        above_threshold['Others'] = sum(below_threshold.values())
    
    emoji_df = pd.DataFrame(above_threshold.items(), columns=['Emoji', 'Count'])
    return emoji_df



def monthly_timeline(selected_user, df) :
    if selected_user != 'Overall':
        df = df[df[ 'users'] == selected_user]

    df['month_num'] = df['date'].dt.month

    timeline = df.groupby(['year', 'month_num', 'month']). count() [ 'message' ].reset_index()

    time = []

    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    
    timeline['time'] = time
    return timeline


def daily_timeline(selected_user, df) :
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def week_activity_map(selected_user,df) :
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    return df ['month'].value_counts()