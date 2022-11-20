from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as expc
import Base64DecodeEncode as b64

class AccuWeather:
    def __init__(self):
        self.url = "https://www.accuweather.com"
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)
        self.search = 0
        self.query = ""
    
    def search_location(self, location):
        if self.query == location:
            return self.search
        else:
            self.driver.get("{}/en/search-locations?query={}".format(self.url, location))
            arraySearch = []
            if self.driver.title == "Find Your Location's Weather Forecast | AccuWeather":
                loop = True
                while loop:
                    try:
                        self.wait.until(expc.text_to_be_present_in_element((By.CLASS_NAME, "sm-text"), "Show more locations"))
                        elements = self.driver.find_element_by_class_name("locations-list-show-button")
                        self.driver.execute_script("arguments[0].click()", elements)
                    except:
                        loop = False
                
                self.search = self.driver.find_element_by_class_name("locations-list")
                self.search = self.search.find_elements_by_tag_name("a")
            
                j = 0
                for i in self.search:
                    arraySearch.append({"No":j, "Value":i.text, "href":b64.Encode(i.get_attribute("href").replace(self.url,""))})
                    j += 1

                self.search = arraySearch
                self.query = location

            else:
                self.search = False
                self.query = location


        return self.search

    def get_weather_content(self, location="", href=""):
        content = ""
        if location != "":
            self.driver.get("{}/en/search-locations?query={}".format(self.url, location))
            
        elif href != "":
            self.driver.get("{}{}".format(self.url, href))
        
        else:
            content = False

        

if __name__ == "__main__":
    AC = AccuWeather()
    while True:
        query = input("Masukkan Query : ")
        print(AC.search_location(query))