from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd



df = pd.DataFrame()

url = "https://yandex.com/maps/"
location = "trabzon"
searchkey = "Mobilya mağazaları"

driver = webdriver.Firefox()
driver.get(url)

time.sleep(5)
search_textarea_xpath = '//input[@class="input__control _bold"]'
search_textarea = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, search_textarea_xpath))
)
search_textarea.send_keys(location, Keys.ENTER)

time.sleep(3)
search_textarea_xpath = '//input[@class="input__control _bold"]'
search_textarea = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, search_textarea_xpath))
)
search_textarea.clear()
search_textarea.send_keys(searchkey, Keys.ENTER)

time.sleep(3)

str_item_list = []
scroll_container = driver.find_element(By.CLASS_NAME, 'scroll__container')
last_position = driver.execute_script("return arguments[0].scrollTop;", scroll_container)
scrolling = True

while scrolling:
    
    items_xpath = '//div[@class="search-business-snippet-view__content"]'
    items = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, items_xpath))
    )
    
    for item in items:
        if not str(item) in str_item_list:
            item.click()
            str_item_list.append(str(item))
            time.sleep(0.2)
            title = item.find_element(By.XPATH, '//h1[@class="card-title-view__title"]').text
            try:
                address = item.find_element(By.XPATH, '//div[@class="business-contacts-view__address-link"]').text
            except:
                address = None
            try:
                card_phone_button = item.find_element(By.XPATH, '//div[@class="card-phones-view__more"]')
                card_phone_button.click()
                time.sleep(0.1)
                card_phone = item.find_element(By.XPATH, '//div[@class="card-phones-view__phone-number"]').text
                if "telefon" in df.columns:
                    if card_phone in list(df["telefon"]):
                        continue
                        
            except:
                card_phone = None
                
            df = pd.concat([
                df,
                pd.DataFrame({
                    "başlık" : [title],
                    "telefon" : [card_phone],
                    "adres" : [address]
                })
            ])
            
    driver.execute_script("arguments[0].scrollTop += 500;", scroll_container)
    curr_position = driver.execute_script("return arguments[0].scrollTop;", scroll_container)
    print(last_position, curr_position)
    
    if last_position == curr_position:
        scrolling = False

    last_position = curr_position
    time.sleep(1)



df.reset_index(drop=True, inplace=True)
df.to_excel(f"{location}.xlsx", index=False)


