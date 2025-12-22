import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from html_parser import extract_body, clean_body_content

def scrape_website_without_proxy(website):
    options = Options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:



        driver.get(website)

        input_field = driver.find_element(By.XPATH, "//input[@placeholder='Унесите пословно име / Назив']")
        time.sleep(10)

        # Unesi tekst
        input_field.send_keys("KOMERCPRODUKT DOO")
        time.sleep(10)

        # Pritisni Enter
        input_field.send_keys(Keys.ENTER)

        # Sačekaj da vidiš rezultat
        time.sleep(2)

        button = driver.find_element(By.XPATH, "//button[@class='ResultItem_link__XQU5w']")
        button.click()


        time.sleep(2)

        # Find the <p> element that contains the text
        paragraph = driver.find_element(By.XPATH, "//p[contains(text(), 'Подаци о адресама')]")

        # Click it
        paragraph.click()
        # Find the element that contains the email
        time.sleep(1)

        email = driver.find_element(By.XPATH, "//td[text()='Е-пошта']/following-sibling::td//span").text
        # Extract the email text
        print("Email:", email)

        print("page was loaded")
        time.sleep(100)

    finally:
        driver.quit()

scrape_website_without_proxy("https://pretraga.apr.gov.rs/search")