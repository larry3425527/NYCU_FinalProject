from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

import time

# Create options for setting Chrome driver arguments
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)  # Create a new instance of the Chrome driver
driver.get('https://medlineplus.gov/healthtopics.html')  # Navigate to a website

# Extract information from the page
ul_element = driver.find_element(By.CSS_SELECTOR, 'ul.indent#bodyMaps')
li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
hrefs = [li.find_element(By.TAG_NAME, 'a').get_attribute('href') for li in li_elements]

print(len(hrefs))
# print(hrefs[0])

driver.close()  # Close the browser

# Start to scrap second layer of the website
subhrefs = []

for href in hrefs:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(href)

    li_elements = driver.find_elements(By.CSS_SELECTOR, 'li.item')
    for li in li_elements:
        subhrefs.append(li.find_element(By.TAG_NAME, 'a').get_attribute('href'))
    li_elements = driver.find_elements(By.CSS_SELECTOR, 'li.item break')
    for li in li_elements:
        subhrefs.append(li.find_element(By.TAG_NAME, 'a').get_attribute('href'))
        
    driver.close()
    
    time.sleep(1)
    
print(len(subhrefs))

set_hrefs = set(subhrefs)
print(len(set_hrefs))

# Start to scrap third layer of the website
output_dir = "text/"
cnt = 0

for href in set_hrefs:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(href)
    # print(href)
    
    div_element = driver.find_element(By.ID, 'topic-summary')
    div_text = div_element.text
    
    fopen = output_dir + "{}.txt".format(cnt)
    
    with open(fopen, 'w') as f:
        f.write(div_text)
    
    cnt = cnt + 1
    
    driver.close()
    
    time.sleep(1)
