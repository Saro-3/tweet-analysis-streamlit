import plotly.express as px
import streamlit as st
from search import search_file
import numpy as np
import pandas as pd

# Set up the page
st.set_page_config(page_title='Sentiment Analysis', 
                   layout="wide",
                   page_icon="Logo_of_Twitter.svg(1).jpg",
                   )
st.header('Sentiment Analysis 😊 😞 😐')
st.subheader('Classifying Tweets as Positive, Negative, or Neutral')

df = search_file()

if df is not None:
    # Display the dataframe
    st.write(df)

    # Define the colors for negative, positive, and neutral posts
    colors = np.array(['#F63366', '#32CD32', '#D3D3D3'])

    # Create and display a pie chart
    pie_chart = px.pie(df,
                   title='Total No. of Participants',
                   values=df['score'].abs(),
                   names='analysis',
                   color_discrete_sequence=colors)
    st.plotly_chart(pie_chart)

   # Create and display a line chart using px.line
    line_chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["Positive", "Neutral", "Negative"])
    line_chart = px.line(line_chart_data,
                        x=line_chart_data.index,
                        y=['Positive', 'Neutral', 'Negative'],
                        color_discrete_sequence=colors)  # Specify each column individually
    line_chart.update_layout(title_text='Sentiment Analysis Distribution')
    line_chart.update_xaxes(title_text='Sentiment')
    line_chart.update_yaxes(title_text='Score')
    st.plotly_chart(line_chart)
