import streamlit as st
from scraper import scrape_website


st.title("AI Web Scraper")
url = st.text_input("Enter a website URL:")

if st.button("Scraper Site"):
    st.write("Scraping...")
    result = scrape_website(url)

    st.session_state.dom_content = result #store in session

    with st.expander("View DOM Content"):  # toggle UI button
        st.text_area("DOM Content", result, height=300)  # to display in UI



