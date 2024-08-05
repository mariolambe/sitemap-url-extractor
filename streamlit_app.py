import streamlit as st
import streamlit.components.v1 as components
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

# JavaScript to inject meta tags into the head
inject_meta_tags = """
<script>
document.addEventListener('DOMContentLoaded', function() {
    var head = document.head;

    var title = document.createElement('title');
    title.textContent = 'Sitemap URL Extractor [Free Tool]';
    head.appendChild(title);

    var metaDescription = document.createElement('meta');
    metaDescription.name = 'description';
    metaDescription.content = 'Extract URLs from sitemap XML files with this easy-to-use Streamlit app. Enter the URL of a sitemap XML file and get all contained URLs.';
    head.appendChild(metaDescription);

    var metaAdsense = document.createElement('meta');
    metaAdsense.name = 'google-adsense-account';
    metaAdsense.content = 'ca-pub-2331172121439147';
    head.appendChild(metaAdsense);
});
</script>
"""

# Inject the JavaScript into the Streamlit app
components.html(inject_meta_tags, height=0)

st.title('Sitemap URL Extractor 😎')
st.subheader('Extract URLs from your sitemap XML files easily')

# Define sidebar text
SIDEBAR_TEXT = """
### About the Sitemap URL Extractor
The Sitemap URL Extractor is a Streamlit app that helps you extract URLs from sitemap XML files.

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

# Initialize session state
if 'go' not in st.session_state:
    st.session_state['go'] = False

# Main content
st.write('Enter the URL of your sitemap XML file below and click "Go" to extract all URLs.')

# Function to handle automatic fill and submit
def autofill_and_submit():
    st.session_state.sitemap = "https://www.google.com/sitemap.xml"
    st.session_state.go = True

st.button("Try this Google Sitemap", on_click=autofill_and_submit)

col1, col2 = st.columns([3, 1])
with col1:
    sitemap_url = st.text_input('Enter Sitemap URL:', placeholder="Enter your sitemap URL here", key='sitemap')
    go_button_clicked = st.button('Go', key='go_button')

    # Check if 'Go' button is clicked or autofill was triggered
    if go_button_clicked or st.session_state.go:
        with st.spinner('Extracting URLs...'):
            urls = extract_urls_from_sitemap(sitemap_url)
            st.session_state.go = False  # Reset the 'go' state
        if urls:
            st.success(f'Extracted {len(urls)} URLs:')
            st.text_area('Extracted URLs', '\n'.join(urls), height=200)

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







