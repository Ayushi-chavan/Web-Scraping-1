from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import csv

START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"

browser = webdriver.Chrome("chromedriver.exe")
browser.get(START_URL)
time.sleep(10)

headers = ["name", "distance","mass","radius"]

def scrape():

        soup = BeautifulSoup(browser.page_source)
        for th_tag in soup.find_all("th", attrs={"class","tabindex","role","title"}):
            tr_tags = th_tag.find_all("tr")
            temp_list = []
            for index, tr_tag in enumerate(tr_tags):
                if index == 0:
                    temp_list.append(tr_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(tr_tag.contents[0])
                    except:
                        temp_list.append("")

                         # Get Hyperlink Tag
            hyperlink_th_tag = tr_tags[0]

            temp_list.append("https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"+ hyperlink_th_tag.find_all("a", href=True)[0]["href"])
            
        print(f"Page scraping completed")


# Calling Method
scrape()