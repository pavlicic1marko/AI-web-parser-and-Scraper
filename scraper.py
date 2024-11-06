import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from html_parser import extract_body, clean_body_content
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from dotenv import load_dotenv
import os

load_dotenv()


SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")

def scrape_website(website_url, use_proxy):
    if(use_proxy):
        return scrape_website_with_remote_connection(website_url)
    else:
        return scrape_website_without_proxy(website_url)

def scrape_website_without_proxy(website):
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

        return data
    finally:
        driver.quit()


def scrape_web_element(website, css_selector):
    print("launching chrome browser")

    chrome_driver_path = "chromedriver.exe"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)
        print("page was loaded")
        html = driver.find_elements(By.CSS_SELECTOR,css_selector)

        return  [i.text  for  i in html]
    finally:
        driver.quit()




def scrape_website_with_remote_connection(website):
    print("Connecting to Scraping Browser...")
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        driver.get(website)
        print("Waiting captcha to solve...")
        solve_res = driver.execute(
            "executeCdpCommand",
            {
                "cmd": "Captcha.waitForSolve",
                "params": {"detectTimeout": 10000},
            },
        )
        print("Captcha solve status:", solve_res["value"]["status"])
        print("Navigated! Scraping page content...")
        html = driver.page_source

        html_body = extract_body(html)
        data = clean_body_content(html_body)

        return data

