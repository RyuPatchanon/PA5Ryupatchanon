import streamlit as st
import pandas as pd
import openai
import json

def main():
    st.sidebar.header("OpenAI API Key")
    user_api_key = st.sidebar.text_input("Enter your OpenAI API Key")
    
    if user_api_key:
        client = openai.OpenAI(api_key=user_api_key)
        st.write("API Key Set Successfully!")

        st.title("Movie/Show Recommendation App")

        user_preference = st.text_input("Enter your preference:")
        prompt = f"Act as a movie enthusiast. You will receive a description of preference and you should give out movie or show recommendations based on the given preference. List the recommendations in a Json array, one recommendation per line. Each recommendation should have 4 fields: - 'Name' - the name of the recommended show or movie. - 'Reason' - The reason the movie or show is recommended based on user preference. - 'Genre' - the genre of the movie or show - 'Notable' - Notable actors or directors involved, list at most 3 names. Preference: {user_preference}"
        st.markdown('Input your preference for a movie or show. \nThe AI will give you suggestions on what to watch.')
        if st.button("Get Recommendations"):
            messages_so_far = [
                {"role": "system", "content": prompt},
                {'role': 'user', 'content': user_preference},]

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages_so_far)
            
            st.markdown('**AI response:**')
            suggestion_dictionary = response.choices[0].message.content

            sd = json.loads(suggestion_dictionary)
            suggestion_df = pd.DataFrame.from_dict(sd)
            st.table(suggestion_df)
    else:
        st.warning("Please enter your OpenAI API Key in the sidebar.")

    # Add custom CSS for background color and style
    st.markdown(
        """
        <style>
        body {
            background-color: #3F250B; /* Dark brown color */
            color: #ffffff;
            font-family: Arial, sans-serif;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()