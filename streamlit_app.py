import streamlit as st
import requests
from bs4 import BeautifulSoup

def extract_urls_from_sitemap(sitemap_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(sitemap_url, headers=headers, timeout=30)
    soup = BeautifulSoup(response.content, 'xml')
    urls = []
    for loc in soup.find_all('loc'):
        urls.append(loc.text)
    return urls

st.set_page_config(page_title="Sitemap URL Extractor", page_icon=":memo:", layout="wide")
st.header('Sitemap URL Extractor :sunglasses:')

# Define sidebar text
SIDEBAR_TEXT = """
### About the Sitemap URL Extractor
The Sitemap URL Extractor is a Streamlit app that helps you extract URLs from sitemap XML files. 

Simply enter the URL of a sitemap XML file, click "Go", and the app will extract all the URLs contained in the file.

It works also with sitemap index file (example: https://www.google.com/sitemap.xml). 

In case of questions, reach out via email: mariolambertucci@gmail.com
"""

# Add sidebar text
st.sidebar.markdown(SIDEBAR_TEXT)

col1, col2 = st.columns([2, 1])
with col1:
    sitemap_url = st.text_input('Enter sitemap URL:', key='sitemap')
    if st.button('Go', key='go'):
        urls = extract_urls_from_sitemap(sitemap_url)
        st.write(f'Extracted {len(urls)} URLs:')
        download_button = st.download_button(label='Download URLs', data='\n'.join(urls), file_name='urls.txt', mime='text/plain', key='download')
        if download_button:
            st.write('Download successful.')
        with st.container():
            st.code('\n'.join(urls), language='')
        download_button = st.download_button(label='Download URLs', data='\n'.join(urls), file_name='urls.txt', mime='text/plain', key='download1')
        if download_button:
            st.write('Download successful.')

# Add some custom CSS to style the output container
st.markdown("""
<style>
    .output-container {
        background-color: #d8d8d8;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)
