import streamlit as st
import matplotlib.pyplot as plt
import preprocessor, helper


st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    # fetch unique users in the chat
    user_list = df['users'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis", user_list)

    # button to show analysis
    if st.sidebar.button("Show Analysis"):

        num_messages, words, links, num_media_messages = helper.fetchStats(selected_user, df)
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

        with col1:
            st.header("Total Message")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Total Links")
            st.title(links)
            
        with col4:
            st.header("Media Shared")
            st.title(num_media_messages)


        # Monthly Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt. subplots()
        ax.plot(timeline['time'], timeline[ 'message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # Daily Timeline
        st. title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index.astype(str), busy_day.values)  
            plt.xticks(rotation='vertical')
            ax.set_ylabel('Message Count') 
            ax.set_xlabel('Day of the Week')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index.astype(str), busy_month.values, color='orange') 
            plt.xticks(rotation='vertical')
            ax.set_ylabel('Message Count') 
            ax.set_xlabel('Month')
            st.pyplot(fig)


        # finding the busiest users in the group
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)


        # WordCloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        # Most common words
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Emoji analyser
        st.title("Emoji Analyser")
        emoji_df = helper.emoji_helper(selected_user, df)

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        
        with col2:
            fig, ax = plt.subplots()
            ax.pie(
                emoji_df['Count'],
                labels=emoji_df['Emoji'],  
                autopct='%1.1f%%'
            )
            st.pyplot(fig)