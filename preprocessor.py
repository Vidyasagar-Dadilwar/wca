import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[AP]M\s-\s'

    messages = re.split(pattern, data)[1:]

    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Remove non-breaking spaces and trailing " - "
    df['message_date'] = df['message_date'].str.replace('\u202f', ' ', regex=True).str.strip().str.rstrip(' - ')

    # Convert message_date to datetime
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p', errors='coerce')

    if df['message_date'].isna().any():
        print("Some rows could not be parsed. Review the following rows:")
        # print(df[df['message_date'].isna()])
    else:
        print("All dates parsed successfully")

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['users'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    mean_date = df['date'].dropna().mean()
    df['date'].fillna(mean_date, inplace=True)

    df['year'] = df['date'].dt.year.astype(int)
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day.astype(int)
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour.astype(int)
    df['minute'] = df['date'].dt.minute.astype(int)
    df['only_date'] = df['date'].dt.date

    return df