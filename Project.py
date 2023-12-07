import streamlit as st
import pandas as pd
import openai

# Set up your OpenAI API key
def set_openai_key(api_key):
    openai.api_key = api_key

def generate_recommendations(preference):
    # GPT-3 prompt to generate recommendations
    prompt = f"Act as a movie enthusiast. You will receive a description of preference and you should give out movie or show recommendations based on the given preference. List the recommendations in a 4 column table, one recommendation per line. Each recommendation should have 4 fields: - 'Name' - the name of the recommended show or movie. - 'Reason' - The reason the movie or show is recommended based on user preference. - 'Genre' - the genre of the movie or show - 'Notable' - Notable actors or directors involved, list at most 3 names. Preference: {preference}"
    
    # Use GPT-3 to generate recommendations
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    
    recommendations = response.choices[0].text.strip().split("\n")
    recommendations = [rec.split(",") for rec in recommendations]
    
    return recommendations

def main():
    st.sidebar.header("OpenAI API Key")
    api_key = st.sidebar.text_input("Enter your OpenAI API Key")

    if api_key:
        set_openai_key(api_key)
        st.write("API Key Set Successfully!")

        st.title("Movie/Show Recommendation App")

        preference = st.text_input("Enter your preference:")

        if st.button("Get Recommendations"):
            recommendations = generate_recommendations(preference)
            df = pd.DataFrame(recommendations, columns=["Name", "Reason", "Genre", "Notable"])
            st.dataframe(df)
    else:
        st.warning("Please enter your OpenAI API Key in the sidebar.")

if __name__ == "__main__":
    main()