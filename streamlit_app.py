import streamlit as st
import requests
from bs4 import BeautifulSoup

# Set page configuration
st.set_page_config(page_title="Sitemap URL Extractor", page_icon="😎", layout="wide")

def extract_urls_from_sitemap(sitemap_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    try:
        response = requests.get(sitemap_url, headers=headers, timeout=60)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'xml')
        urls = [loc.text for loc in soup.find_all('loc')]
        return urls
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching the sitemap: {e}")
        return []

# Inject meta title and description
meta_tags = """
<head>
<title>Sitemap URL Extractor [Free Tool]</title>
<meta name="description" content="Extract URLs from sitemap XML files with this easy-to-use Streamlit app. Enter the URL of a sitemap XML file and get all contained URLs.">
</head>
"""
st.markdown(meta_tags, unsafe_allow_html=True)

st.title('Sitemap URL Extractor 😎')
st.subheader('Extract URLs from your sitemap XML files easily')

# Define sidebar text
SIDEBAR_TEXT = """
### About the Sitemap URL Extractor
The Sitemap URL Extractor is a Streamlit app that helps you extract URLs from sitemap XML files.

Simply enter the URL of a sitemap XML file, click "Go", and the app will extract all the URLs contained in the file.

It works also with sitemap index file (example: [Google Sitemap](https://www.google.com/sitemap.xml)).

If you want to explore alternative ways (for example via Google sheets, Screaming Frog, command line) check out this article on [**How to extract URLs from sitemaps**](https://www.mariolambertucci.com/how-to-extract-urls-from-sitemaps/).
"""

# Add sidebar text
st.sidebar.markdown(SIDEBAR_TEXT)

# Define sidebar subheader text
SIDEBAR_SUBHEADER_TEXT = """
### About Author
SEO Specialist [**Mario Lambertucci**](https://www.linkedin.com/in/mariolambertucci/)
"""

# Add sidebar subheader text
st.sidebar.subheader(SIDEBAR_SUBHEADER_TEXT)

# Main content
st.write('Enter the URL of your sitemap XML file below and click "Go" to extract all URLs.')
st.write('For example, try this [Google Sitemap](https://www.google.com/sitemap.xml)')

col1, col2 = st.columns([3, 1])
with col1:
    sitemap_url = st.text_input('Enter Sitemap URL:', placeholder="Enter your sitemap URL here", key='sitemap')
    if st.button('Go', key='go'):
        with st.spinner('Extracting URLs...'):
            urls = extract_urls_from_sitemap(sitemap_url)
        if urls:
            st.success(f'Extracted {len(urls)} URLs:')
            st.code('\n'.join(urls), language='')

            # Download button
            st.download_button(label='Download URLs', data='\n'.join(urls), file_name='urls.txt', mime='text/plain', key='download')
        else:
            st.warning("No URLs found or there was an error with the sitemap.")

# Hide Streamlit's default menu and footer
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)




