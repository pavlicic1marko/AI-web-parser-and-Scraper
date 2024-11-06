import streamlit as st
from scraper import scrape_website, scrape_website_with_remote_connection
from html_parser import split_dom_content_by_length
from llama_ai import parse_with_ollama


st.title("AI Web Scraper")
url = st.text_input("Enter a website URL:")
use_proxy = st.checkbox("use proxy when scraping")


if st.button("Scraper Site"):
    st.write("Scraping...")
    st.write("use proxy:" + str(use_proxy))
    result = scrape_website_with_remote_connection(url)

    st.session_state.dom_content = result #store in session

    with st.expander("View DOM Content"):  # toggle UI button
        st.text_area("DOM Content", result, height=300)  # to display in UI



if "dom_content" in st.session_state:
    parse_description = st.text_area("describe what you want to parse")

    if st.button("Parse content"):
        if parse_description:
            st.write("Parsing the content")

            dom_chunks = split_dom_content_by_length(st.session_state.dom_content)
            results = parse_with_ollama(dom_chunks,parse_description)
            st.write(results)