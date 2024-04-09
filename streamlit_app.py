import streamlit as st
import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def extract_urls_from_sitemap_async(sitemap_url):
    async with aiohttp.ClientSession() as session:
        response_text = await fetch_url(session, sitemap_url)
        soup = BeautifulSoup(response_text, 'xml')
        urls = [loc.text for loc in soup.find_all('loc')]
        return urls

async def main():
    sitemap_url = st.text_input('Enter sitemap URL:', key='sitemap')
    if st.button('Go', key='go'):
        st.write('Extracting URLs...')
        urls = await extract_urls_from_sitemap_async(sitemap_url)
        st.write(f'Extracted {len(urls)} URLs:')
        st.write(urls)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
