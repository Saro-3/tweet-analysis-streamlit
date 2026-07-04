import plotly.express as px
import streamlit as st
from search import search_file
import numpy as np
import pandas as pd

# Set up the page
st.set_page_config(page_title='Sentiment Analysis', 
                   layout="wide",
                   page_icon="assets/logo/twitter-logo.png",
                   )
st.title('🐦Sentiment Analysis')
st.markdown(
    "Analyze tweets and classify them into **Positive**, **Negative**, or **Neutral** sentiments."
)

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

    # Create and display a line chart from the uploaded data
    line_chart_data = (
        df["analysis"]
        .value_counts()
        .rename_axis("analysis")
        .reset_index(name="count")
    )
    line_chart = px.line(line_chart_data,
                        x="analysis",
                        y="count",
                        markers=True,
                        color_discrete_sequence=colors)  # Specify each column individually
    line_chart.update_layout(title_text='Sentiment Analysis Distribution')
    line_chart.update_xaxes(title_text='Sentiment')
    line_chart.update_yaxes(title_text='Tweet count')
    st.plotly_chart(line_chart)
