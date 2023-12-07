import streamlit as st
import openai
import pandas as pd

# Set up the OpenAI API key input in the sidebar
st.sidebar.title('OpenAI API Key')
user_api_key = st.sidebar.text_input("OpenAI API key", type="password")
client = openai.OpenAI(api_key=user_api_key)

def get_recommendations(user_preference):
    response = client.chat.completion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": user_preference},
            {"role": "user", "content": ""}
        ]
    )
    return response.choices[0].message['content']

def format_recommendations(recommendations):
    recommendations_list = []
    # Split the recommendations by lines
    recommendation_lines = recommendations.splitlines()
    for line in recommendation_lines:
        # Split each line into name and summary
        name, summary = line.split(' - ')
        # Create a dictionary for each recommendation
        recommendation = {'Name': name.strip(), 'Summary': summary.strip()}
        recommendations_list.append(recommendation)
    return recommendations_list

def main():
    st.title('Movie or Show Recommendation Generator')

    # Input field for user preferences
    user_preference = st.text_area('Enter your preference:')

    if st.button('Get Recommendations'):
        if user_preference:
            try:
                recommendations = get_recommendations(user_preference)
                recommendations_list = format_recommendations(recommendations)

                # Display the recommendations in a Pandas DataFrame with 2 columns
                df = pd.DataFrame(recommendations_list)
                st.write(df)
            except Exception as e:
                st.error('An error occurred. Please try again.')
                st.error(f'Error details: {str(e)}')

if __name__ == '__main__':
    main()