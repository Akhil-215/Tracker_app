from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options

def initiate_driver():
    # Set up options for Chrome (optional: for headless mode)
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (optional)
    options.add_argument("--disable-gpu") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")


    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service= service, options= options)
    
    return driver

def get_top20(driver, index):
    driver.get("https://www.nseindia.com/market-data/live-equity-market")

    refresh_button = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'freezed-row')))
    select_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'equitieStockSelect')))

    select = Select(select_element)
    select.select_by_value(index)

    time.sleep(2)

    volume_element = driver.find_element(By.ID, 'equityStockTablecol9')
    volume_element.click()
    time.sleep(1)    
    volume_element.click()
    time.sleep(1)

    top20_indices = {
        'SYMBOL': [],
        'Volume': []
    }

    for i in range(2, 21):
        symbol = driver.find_element(By.XPATH, f'//*[@id="equityStockTable"]/tbody/tr[{i}]/td[1]').text.strip()
        volume = driver.find_element(By.XPATH, f'//*[@id="equityStockTable"]/tbody/tr[{i}]/td[10]').text.strip().replace(',', '')

        top20_indices['SYMBOL'].append(symbol)
        top20_indices['Volume'].append(int(volume))
    return top20_indices

def main(index):
    driver = initiate_driver()
    top20 = get_top20(driver, index)
    return top20

if __name__ == "__main__":
    index = "NIFTY 100"
    top20 =  main(index)
    print(top20)