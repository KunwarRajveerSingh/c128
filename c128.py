from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

Start_url = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome("chromedriver")

browser.get(Start_url)
headers = ["name","Light_Years_from_Earth","Planet_Mass","Stellar_Magnitude","Discovery_Date","Hyper_Link","Planet_Type","Planet_radius","Orbital_radius","Orbital_period","eccentricity"]
planet_data = []
new_Planet_Data = []
time.sleep(10)
def scrape():
    
    for i in range(1,428):
        while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source,"html.parser")
            currentPageNumber = int(soup.find_all("input",attrs={"class","Page_Number"})[0].get("value"))
            if currentPageNumber < i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif currentPageNumber > i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break
        for ul_tag in soup.find_all("ul",attrs={"class","exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            Hyper_Link_li_tag = li_tags[0]
            temp_list.append("https://exoplanets.nasa.gov" + Hyper_Link_li_tag.find_all("a",href = True)[0]["href"])
            planet_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print("PageDone",i)

    

def ScrapeMoreData(Hyper_Link):
    try:
        page = requests.get(Hyper_Link)
        soup = BeautifulSoup(page.content,"html.parser")
        temp_list = []

        for trtag in soup.find_all("tr",attrs={"class","fact_row"}):
            td_tags = trtag.find_all('td')
            for tdtag in td_tags:
                try:
                    temp_list.append(tdtag.find_all("div",attrs={"class","value"})[0].contents[0])
                except:
                    temp_list.append("")
        new_Planet_Data.append(temp_list)
    except:
        time.sleep(1)
        ScrapeMoreData(Hyper_Link)
                     

scrape()
for index,data in enumerate(planet_data):
    ScrapeMoreData(data[5])
    print("pageDone2",index + 1)
final_Planet_Data = []
for index,data in enumerate(planet_data):
    new_Planet_Data_element = new_Planet_Data[index]
    new_Planet_Data_element = [elem.replace("\n","") for elem in new_Planet_Data_element]
    new_Planet_Data_element = new_Planet_Data_element[:7]
    final_Planet_Data.append(data + new_Planet_Data_element)
with open("final.csv","w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(headers)
        csv_writer.writerows(final_Planet_Data)