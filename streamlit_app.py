import streamlit as st

st.set_page_config(page_title="Redirecting...", page_icon="🔄")

st.markdown("""
    <meta http-equiv="refresh" content="0; URL=https://sitemap-url-extractor.netlify.app/">
    <script>
        window.location.href = "https://sitemap-url-extractor.netlify.app/";
    </script>
""", unsafe_allow_html=True)

st.write("If you are not redirected automatically, follow this [link to the new site](https://sitemap-url-extractor.netlify.app/).")
