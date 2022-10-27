from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
import csv


START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"

browser = webdriver.Chrome("chromedriver.exe")
browser.get(START_URL)
time.sleep(10)

stars_data = []



def scrape():

        soup = BeautifulSoup(browser.page_source)
        star_table = soup.find('table')
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


new_stars_data = []

def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
      
        soup = BeautifulSoup(page.content, "html.parser")

        temp_list = []

        for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}):
            td_tags = tr_tag.find_all("td")
          
            for td_tag in td_tags:
                try: 
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
                    
        new_stars_data.append(temp_list)

    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

#Calling method

for index, data in enumerate(stars_data):
    scrape_more_data(data[5])
    print(f"scraping at hyperlink {index+1} is completed.")

print(new_stars_data[0:10])

final_planet_data = []

for index, data in enumerate(stars_data):
    new_stars_data_element = new_stars_data[index]
    new_stars_data_element = [elem.replace("\n", "") for elem in new_stars_data_element]
    new_stars_data_element = new_stars_data_element[:7]
    final_planet_data.append(data + new_stars_data_element)

with open("final1.csv", "w") as f:
        csvwriter = csv.writer(f)
     
        csvwriter.writerows(final_planet_data)
