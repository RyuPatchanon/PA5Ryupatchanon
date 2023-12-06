import streamlit as st
import openai
import pandas as pd
from newspaper import Article

# Set up the OpenAI API key input in the sidebar
st.sidebar.title('OpenAI API Key')
api_key = st.sidebar.text_input('Enter your OpenAI API Key:', type='password')

# Set the OpenAI API key
openai.api_key = api_key

def extract_text_from_url(article_url):
    article = Article(article_url)
    article.download()
    article.parse()
    return article.text

def summarize_text(text):
    response = openai.Completion.create(
        engine="davinci",
        prompt=text,
        max_tokens=150  # Adjust this parameter to control the length of the summary
    )
    return response.choices[0].text.strip()

def main():
    st.title('Article Text Extractor and Summarizer')

    # Input field for article URL
    article_url = st.text_input('Enter the URL of the news article:')

    if st.button('Extract and Summarize'):
        if article_url:
            try:
                extracted_text = extract_text_from_url(article_url)
                summary = summarize_text(extracted_text)

                st.subheader('Extracted Text:')
                st.write(extracted_text)

                st.subheader('Summary:')
                st.write(summary)

                # Display the extracted text and summary in a Pandas DataFrame
                df = pd.DataFrame({'Extracted Text': [extracted_text], 'Summary': [summary]})
                st.subheader('DataFrame:')
                st.write(df)
            except Exception as e:
                st.error('An error occurred. Please check the URL or try again.')
                st.error(f'Error details: {str(e)}')

if __name__ == '__main__':
    main()
