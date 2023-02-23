import streamlit as st
import requests
from bs4 import BeautifulSoup
import pyperclip

def extract_urls_from_sitemap(sitemap_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(sitemap_url, headers=headers, timeout=30)
    soup = BeautifulSoup(response.content, 'xml')
    urls = []
    for loc in soup.find_all('loc'):
        urls.append(loc.text)
    return urls

st.set_page_config(page_title="Sitemap URL Extractor", page_icon=":memo:", layout="wide")
st.header('Sitemap URL Extractor emojis :sunglasses:')

col1, col2 = st.columns([2, 1])
with col1:
    sitemap_url = st.text_input('Enter sitemap URL:', key='sitemap')
    if st.button('Go', key='go'):
        urls = extract_urls_from_sitemap(sitemap_url)
        st.write(f'Extracted {len(urls)} URLs:')
        with st.container():
            st.code('\n'.join(urls), language='')
        copy_button = st.button(f'Copy All ({len(urls)})', key='copy')
        if copy_button:
            pyperclip.copy('\n'.join(urls))
            st.success('All URLs copied to clipboard!')

# Add some custom CSS to style the output container
st.markdown("""
<style>
    .output-container {
        background-color: #f1f1f1;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)
