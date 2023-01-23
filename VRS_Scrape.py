from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import json
import time

def launch_driver():
    with open("settings.json", "r") as f:
        settings = json.load(f)
    options = Options()
    options.binary_location = settings["FirefoxPath"]
    fp = webdriver.FirefoxProfile(settings["FirefoxProfile"])
    driver = webdriver.Firefox(firefox_profile=fp,options=options)
    driver.execute_script("return navigator.userAgent")
    driver.set_window_size(2560,1440)
    driver.get(settings["VRSLink"])
    return driver

def main():
    driver = launch_driver()
    load_more_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='default-button load-more']")))
    load_all_entries(load_more_button)
    time.sleep(5)
    table = driver.find_elements(By.XPATH, "//tr[@data-vrs-widget='trWrapper']")
    data_frame = pd.DataFrame(columns=["Track", "Car", "Season", "Sessions", "Total Laps", "Driving Time"])
    for i, entry in enumerate(table):
        if i == 0:
            continue
        elif i == len(table) - 1:
            break
        elements = entry.find_elements(By.XPATH, ".//td")
        row_dict = {}
        row_dict["Track"] = elements[0].find_element(By.XPATH, ".//div/span[@class='IRGHJVC-id-b']").get_attribute("title")
        row_dict["Car"] = elements[1].find_element(By.XPATH, ".//div/span[@class='IRGHJVC-id-b']").get_attribute("title")
        row_dict["Season"] = elements[2].find_element(By.XPATH, ".//div/h3/span").text
        row_dict["Sessions"] = int(elements[3].find_element(By.XPATH, ".//div/h3").text)
        row_dict["Total Laps"] = int(elements[4].find_element(By.XPATH, ".//div/h3").text)
        row_dict["Driving Time"] = float(elements[5].find_element(By.XPATH, ".//div/h3").text)
        if "Season" not in row_dict["Season"]:
            row_dict["Season"] = "2023 Season 1"
        data_frame = data_frame.append(row_dict, ignore_index=True)
    print(data_frame)
    data_frame.to_csv("vrs_data.csv")

def load_all_entries(load_more_button):
    try:
        while(True):
            load_more_button.click()
    except:
        print("No more load more buttons")
    #result = driver.get_attribute("outerHTML")
    #print(result)

if __name__ == "__main__":
    main()