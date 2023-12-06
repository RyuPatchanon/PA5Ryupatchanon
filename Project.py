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

def summarize_text_with_gpt3(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Summarize the text."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message['content']

def main():
    st.title('Article Text Extractor and Summarizer with OpenAI GPT-3')

    # Input field for article URL
    article_url = st.text_input('Enter the URL of the news article:')

    if st.button('Extract and Summarize'):
        if article_url:
            try:
                extracted_text = extract_text_from_url(article_url)
                summary = summarize_text_with_gpt3(extracted_text)

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