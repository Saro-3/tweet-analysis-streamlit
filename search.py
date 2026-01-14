import pandas as pd
from textblob import TextBlob
import chardet
import streamlit as st


# Define sentiment scoring functions
def score(x):
    return TextBlob(str(x)).sentiment.polarity

def analyze(x):
    if x >= 0.5:
        return 'POSITIVE😊'
    elif x <= -0.5:
        return 'NEGATIVE😞'
    else:
        return 'NEUTRAL😐'

@st.cache_data(ttl=None, persist=True)
def load_data(uploaded_file):
    # Detect file encoding
    rawdata = uploaded_file.read()
    result = chardet.detect(rawdata)
    encoding = result['encoding']

    # Reset the cursor of the file
    uploaded_file.seek(0)
    
    # Load the CSV file
    try:
        df = pd.read_csv(uploaded_file, encoding=encoding, on_bad_lines='warn')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(uploaded_file, encoding='ISO-8859-1', on_bad_lines='warn')
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, encoding='latin1', on_bad_lines='warn')

    # Remove unnecessary columns
    if 'Unnamed: 0' in df.columns:
        df.drop('Unnamed: 0', axis=1, inplace=True)

    return df



def search_file():
    # Create an expander for the file uploader
    with st.expander("Upload a file"):
    # File uploader
     uploaded_file = st.file_uploader("Choose a file", type=['csv'])

    if uploaded_file is not None:
        df = load_data(uploaded_file)

        # Print column names
        st.write(f"Columns in the dataframe: {df.columns.tolist()}")

        # Check if 'Tweets' column exists
        if 'Tweets' in df.columns:
            # Convert 'Tweets' column to string
            df['Tweets'] = df['Tweets'].astype(str)

            # Apply sentiment analysis
            df['score'] = df['Tweets'].apply(score)
            df['analysis'] = df['score'].apply(analyze)

            # Add a search bar
            search_term = st.text_input('Enter a search term:')
            if search_term:
                search_terms = search_term.lower().split()
                df = df[df['Tweets'].apply(lambda x: any(term in x.lower().split() for term in search_terms))]
            
            # Check if 'analysis' column exists before plotting
            if 'analysis' in df.columns:
                # Add your plotting code here
                pass
            else:
                st.write("The 'analysis' column does not exist in the dataframe. Please check your sentiment analysis function.")
        else:
            st.write("The 'Tweets' column does not exist in the uploaded file. Please specify the correct column name.")

        return df
