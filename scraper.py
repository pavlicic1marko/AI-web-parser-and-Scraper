import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from html_parser import extract_body, clean_body_content, split_dom_content_by_length


def scrape_website(website):
    print("launching chrome browser")

    chrome_driver_path = "chromedriver.exe"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)
        print("page was loaded")
        html = driver.page_source

        html_body = extract_body(html)
        data = clean_body_content(html_body)
        data = split_dom_content_by_length(data)

        return data
    finally:
        driver.quit()
