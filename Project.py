import streamlit as st
import pandas as pd
import openai

def main():
    st.sidebar.header("OpenAI API Key")
    user_api_key = st.sidebar.text_input("Enter your OpenAI API Key")
    
    if user_api_key:
        client = openai.OpenAI(api_key=user_api_key)
        st.write("API Key Set Successfully!")

        st.title("Movie/Show Recommendation App")

        user_preference = st.text_input("Enter your preference:")
        prompt = f"Act as a movie enthusiast. You will receive a description of preference and you should give out movie or show recommendations based on the given preference. List the recommendations in a 4 column table, one recommendation per line. Each recommendation should have 4 fields: - 'Name' - the name of the recommended show or movie. - 'Reason' - The reason the movie or show is recommended based on user preference. - 'Genre' - the genre of the movie or show - 'Notable' - Notable actors or directors involved, list at most 3 names. Preference: {user_preference}"
        st.markdown('Input your preference for movie or show. \n\
            The AI will give you suggestions on what to watch.')
        if st.button("Get Recommendations"):
            messages_so_far = [
                {"role": "system", "content": prompt},
                {'role': 'user', 'content': user_preference},]

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages_so_far)
            
            recommendations = response.choices[0].text.strip().split("\n")
            recommendations = [rec.split(",") for rec in recommendations]
            df = pd.DataFrame(recommendations, columns=["Name", "Reason", "Genre", "Notable"])
            st.dataframe(df)
    else:
        st.warning("Please enter your OpenAI API Key in the sidebar.")

if __name__ == "__main__":
    main()