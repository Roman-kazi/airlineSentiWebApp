import streamlit as st
import pandas as pd
#import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.title("Sentiment Analysis of Airline Tweets")
st.sidebar.title("Sentiment Analysis of Airline Tweets")

st.markdown("This is a streamlit dashbord to analyze sentiments of tweets 🐦 ")
st.markdown("Please use sidebar to access different features")
st.sidebar.markdown(" This is a streamlit dashbord to analyze sentiments of tweets 🐦?")

DATA_URL = ("Tweets.csv")

@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()

st.sidebar.subheader("Show a random tweet")
random_tweet = st.sidebar.radio('sentiment',('positive','neutral','negative'))

st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])
st.sidebar.markdown('### Number of tweets by sentiment')
select = st.sidebar.selectbox('Visualization',['Histogram','Pie Chart'],key=1)
sentiment_count = data['airline_sentiment'].value_counts()

# Creating a tidy dataframe
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index,'Tweets':sentiment_count.values})

if not st.sidebar.checkbox("Hide",False):
    st.markdown("Number of tweets by sentiment")
    if select == "Histogram":
        fig = px.bar(sentiment_count,x='Sentiment',y='Tweets',height=500,color='Tweets')
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count,values='Tweets',names='Sentiment')
        st.plotly_chart(fig)


        #map
st.sidebar.subheader("Hour of Tweet")
hour = st.sidebar.slider("Hour of day",0,23)
#number = st.sidebar.number_input("Number input",min_value=101,max_value=1001)
modified_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox("Close",False,key='1'):
    st.markdown("Tweets location based on hour of day")
    st.markdown('### %i tweets between %i:00 hours and %i:00'%(len(modified_data),hour,(hour+1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)

st.sidebar.subheader("Sentiments by airlines")
choice = st.sidebar.multiselect('Pick airlines',('Virgin America', 'United', 'Southwest', 'Delta', 'US Airways','American'))

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data,x='airline',y='airline_sentiment',histfunc='count',color='airline_sentiment',
    facet_col='airline_sentiment',labels={'airline_sentiment':'tweets'},height=600,width=500)
    st.plotly_chart(fig_choice)

st.sidebar.header("WordCloud")

word_sentiment = st.sidebar.radio('Sentiment for wordcloud',('positive','neutral','negative'))

if not st.sidebar.checkbox('Hide',True,key=3):
    st.subheader("WordCloud for %s sentiment"%(word_sentiment))
    df = data[data['airline_sentiment'] == word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', height=640, width=500).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()
