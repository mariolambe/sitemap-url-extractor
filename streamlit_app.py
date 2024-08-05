import streamlit as st
import streamlit.components.v1 as components
import requests
from pathlib import Path
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

index = Path(st.__file__).parent / "static" / "index.html"
html = index.read_text()

html = html.replace("<head>", """<head>
<meta name="google-adsense-account" content="ca-pub-2331172121439147">
""".replace("\n", ""))

index.write_text(html)



# JavaScript to inject meta tags into the head
inject_meta_tags = """
<script>
document.addEventListener('DOMContentLoaded', function() {
    var head = document.head;

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

col1,
