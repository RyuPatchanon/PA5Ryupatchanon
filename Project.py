import streamlit as st
import openai
import json
import pandas as pd

# Get the API key from the sidebar called OpenAI API key
user_api_key = st.sidebar.text_input("OpenAI API key", type="password")

client = openai.chat.completion.create(api_key=user_api_key)

prompt = """Act as a movie enthusiast. You will receive a 
            a description of preference and you should give out movie or show recommendations based on the given preference.
            List the recommendations in a 4 column table, one recommendation per line.
            Each recommendation should have 4 fields:
            - "Name" - the name of the recommended show or movie.
            - "Reason" - The reason the movie or show is recommended based on user preference.
            - "Genre" - the genre of the movie or show
            - "Notable" - Notable actors or directors involved, list at most 3 names
            Don't say anything at first. Wait for the user to say something.
        """

st.title('Movie/Show Recommendations')
st.markdown('Enter your preferences, and the AI will provide recommendations.')

user_preference = st.text_area("Enter your preferences:", "I enjoy action-packed movies with suspense.")

# submit button after preference input
if st.button('Get Recommendations'):
    response = client.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {'role': 'user', 'content': user_preference},
        ]
    )
    
    # Show the response from the AI in a box
    st.markdown('**AI Recommendations:**')
    recommendation_dictionary = response['choices'][0]['message']['content']

    rec = json.loads(recommendation_dictionary)
    recommendation_df = pd.DataFrame.from_dict(rec)

    st.table(recommendation_df)