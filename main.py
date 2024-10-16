import streamlit as st
from scraper import scrape_website

st.title("AI Web Scraper")
url = st.text_input("Enter a website URL:")

if st.button("Scraper Site"):
    st.write("Scraping...")
    result = scrape_website(url)
    print(result)



