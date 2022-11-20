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
        #self.driver.implicitly_wait(5)
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

    def parsing(self):
        panel = self.driver.find_elements_by_class_name("cur-con-weather-card__panel")[0]
        current_location = self.driver.find_element_by_class_name("header-loc").text

        current_time = panel.find_element_by_class_name("cur-con-weather-card__subtitle").text
        current_real_feel = panel.find_element_by_class_name("real-feel").text.replace("RealFeel® ","")
        current_temp = panel.find_element_by_class_name("temp").text

        current_weather = self.driver.find_element_by_class_name("phrase").text

        panel = self.driver.find_elements_by_class_name("spaced-content")
        current_air_quality = panel[0].find_element_by_class_name("value").text
        current_aq_number = self.driver.find_element_by_class_name("aq-number").text

        current_wind = panel[1].find_element_by_class_name("value").text
        current_wind_gust = panel[2].find_element_by_class_name("value").text
        try :
            current_minutecast = self.driver.find_element_by_class_name("minutecast-banner__phrase").text
        except:
            current_minutecast = "None"

        self.driver.find_elements_by_class_name("subnav-item")[1].click()
        
        panel = self.driver.find_elements_by_class_name("hourly-card-nfl")
        hour = []
        count = 0
        for i in panel:
            if count > 0:
                i.click()

            hour_location = current_location
            hour_time = i.find_element_by_class_name("date").text
            print(count)
            hour_real_feel = i.find_element_by_class_name("real-feel__text").text.replace("RealFeel® ","")

            hour_temp = i.find_element_by_class_name("metric").text

            hour_weather = i.find_element_by_class_name("phrase").text

            self.wait.until(expc.presence_of_all_elements_located((By.CLASS_NAME, "hourly-content-container")))
            _panel = i.find_elements_by_class_name("hourly-content-container")[1]
            hour_air_quality = _panel.find_elements_by_tag_name("p")[4].text
            hour_wind = _panel.find_elements_by_tag_name("p")[0].text
            hour_wind_gust = _panel.find_elements_by_tag_name("p")[1].text
                
            hour_chunk = {
                "hour_location":hour_location,
                "hour_time":hour_time,
                "hour_temp":hour_temp,
                "hour_real_feel":hour_real_feel,
                "hour_weather":hour_weather,
                "hour_air_quality":hour_air_quality,
                "hour_wind":hour_wind,
                "hour_wind_gust": hour_wind_gust
            }

            hour.append(hour_chunk)
            count += 1

        result = {"current":{
            "current_location":current_location,
            "current_time":current_time,
            "current_temp":current_temp,
            "current_real_feel":current_real_feel,
            "current_weather":current_weather,
            "current_minutecast":current_minutecast,
            "current_air_quality":current_air_quality,
            "current_aq_number":current_aq_number,
            "current_wind":current_wind,
            "current_wind_gust": current_wind_gust
            },
            "hour":hour
        }

        return result

    def get_weather_content(self, location="", href=""):
        content = ""
        if location != "":
            self.driver.get("{}/en/search-locations?query={}".format(self.url, location))
            
        elif href != "":
            href = b64.Decode(href)
            self.driver.get("{}{}".format(self.url, href))
        
        else:
            content = False

        return self.parsing()

if __name__ == "__main__":
    AC = AccuWeather()
    content = AC.get_weather_content(location="Sinaksak")
    print(content)