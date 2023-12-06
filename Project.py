import streamlit as st
import openai
import pandas as pd
import json

# Set up the OpenAI API key input in the sidebar
st.sidebar.title('OpenAI API Key')
api_key = st.sidebar.text_input('Enter your OpenAI API Key:', type='password')

# Set the OpenAI API key
openai.api_key = api_key

def get_recommendations(user_preferences):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Recommend movies or shows based on my preferences."},
            {"role": "user", "content": user_preferences}
        ]
    )
    return response.choices[0].message['content']

def format_recommendations(recommendations):
    recommendations_list = []
    # Split the recommendations by lines
    recommendation_lines = recommendations.splitlines()
    for line in recommendation_lines:
        # Split each line into name and reason
        name, reason = line.split(' - ')
        # Create a dictionary for each recommendation
        recommendation = {'Name': name.strip(), 'Reason': reason.strip()}
        recommendations_list.append(recommendation)
    return recommendations_list

def main():
    st.title('Movie or Show Recommendation Generator')

    # Input field for user preferences
    user_preferences = st.text_area('Enter your movie or show preferences:')

    if st.button('Get Recommendations'):
        if user_preferences:
            try:
                recommendations = get_recommendations(user_preferences)
                recommendations_list = format_recommendations(recommendations)

                st.subheader('Recommendations:')
                st.json(recommendations_list)
            except Exception as e:
                st.error('An error occurred. Please try again.')
                st.error(f'Error details: {str(e)}')

if __name__ == '__main__':
    main()
