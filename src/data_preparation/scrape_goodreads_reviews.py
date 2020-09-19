# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 16:12:37 2020
@author: ejgen

------ What is this file? ------
                
Lorem dolor ipsum sit amet

"""

#%% --- Import required packages ---

import os
from bs4 import BeautifulSoup
import requests # To request for an HTML file
from selenium import webdriver # For webscraping
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pathlib import Path # To wrap around filepaths
import pandas as pd
from urllib.request import urlopen
import time

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Prepare URL's to be searched ---

initial_http = "https://www.goodreads.com/"
search_https = ["https://www.goodreads.com/book/show/2517",
                "https://www.goodreads.com/book/show/11691",
                "https://www.goodreads.com/book/show/6282753",
                "https://www.goodreads.com/book/show/11690",
                "https://www.goodreads.com/book/show/11692",
                "https://www.goodreads.com/book/show/11693",
                "https://www.goodreads.com/book/show/28718879",
                "https://www.goodreads.com/book/show/24997390",
               "https://www.goodreads.com/book/show/11694",
               "https://www.goodreads.com/book/show/270872"]
               
                
                
# search_url = requests.get(search_http, headers={
#             'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
#         })

#%% --- Initialize the Chrome web driver ---

#Access the options for Chrome webdrivers
# option = webdriver.ChromeOptions()

#Add some exceptions to deactivate images and javascript
#This way, the page will load faster.
# prefs = {'profile.default_content_setting_values': {'images':2}}
# option.add_experimental_option('prefs', prefs)

#Initiate the Google Chrome webdriver with options.
#driver = webdriver.Chrome("selenium chrome driver/chromedriver.exe", options=option)

#%% --- Next Page Test ---
all_reviews = []

## password id

login_id = "ejgscrape@protonmail.com"
login_password = "ejgscrapegoodreads"

#Initiate the Google Chrome webdriver with options.
#driver = webdriver.Chrome("selenium chrome driver/chromedriver.exe", options=option)
driver = webdriver.Firefox(executable_path="firefox_driver/geckodriver.exe")
driver.get(initial_http)
time.sleep(5)
login_id_field = driver.find_element_by_id("userSignInFormEmail").send_keys(login_id)
login_password_field = driver.find_element_by_id("user_password").send_keys(login_password)
login_button = driver.find_element_by_class_name("gr-button").click()

for search_http in search_https:
    driver.get(search_http)
    time.sleep(5)
    
    from selenium.webdriver.common.action_chains import ActionChains
    
    reviews = []
    
    i = 0
    while i <= 10:
        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser").find(id="bookReviews")
        for review in soup.find_all(class_="review"):
            try:  # Get user / reviewer id
                user_id = review.find(class_="user").get("href")[11:].split("-")[0]
                #Get user name
                user_name = review.find(class_ = "user").get_text()
                # Get full review text even the hidden parts, and remove spaces and newlines
                comment = review.find(class_="readable").find_all("span")[-1].get_text(". ", strip=True)
                date = review.find(class_="reviewDate").get_text()
                user_data = [user_id, user_name, comment, date]
                reviews.append(user_data)
                
            except Exception:
                print("OOOPs!")
        
        
        
        #ActionChains(driver).move_to_element(driver.find_element_by_class_name('next_page')).perform()
        #next_button = driver.find_element_by_class_name('next_page')
        next_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'next_page')))
        #BAR BLOCKS IT
        #ActionChains(driver).move_to_element(next_button).perform()
        #next_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.class, 'next_page')))
        #next_button.click()
        try:
            driver.execute_script("arguments[0].click();", next_button)
        except:
            next_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'next_page')))
            driver.execute_script("arguments[0].click();", next_button)
        
        time.sleep(3)
        i += 1
    
    all_reviews.append(reviews)


driver.close()
#%% --- Write the data into a pandas DataFrame object. ---

reviews_df = pd.DataFrame.from_records(all_reviews,
                                       columns = ["user_id", "user_name",
                                                  "comment", "comment_date"])

#%% --- Save the data ---

output_fp = Path("../../data/raw/goodreads_reviews_raw.csv")
reviews_df.to_csv(output_fp, encoding = "utf-8", index = False)

            
            