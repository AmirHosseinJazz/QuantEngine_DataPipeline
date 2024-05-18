from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

import os
import time
import shutil
import zipfile
import pandas as pd

def handle_cookies(driver):
    try:
        driver.find_element(By.ID,'onesignal-slidedown-allow-button').click()
    except:
        pass
    try:
        driver.find_element(By.ID,'cookie_action_close_header').click()
    except:
        pass

def get_asset_history(asset='EUR/USD'):
    current_dir = os.getcwd()

    # Set the download directory to the current directory
    download_dir = current_dir


    chrome_options = webdriver.ChromeOptions()
    preferences = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,  # Disable download prompt
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True  # You can disable this if it interferes with automation
    }
    chrome_options.add_experimental_option("prefs", preferences)
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
    driver.maximize_window()
    already=[]
    driver.get("https://www.histdata.com/download-free-forex-data/?/metatrader/1-minute-bar-quotes")
    handle_cookies(driver)
    asset_button=driver.find_element(By.XPATH,'//strong[text()="{}"]/parent::a'.format(asset))
    action_asset_button=ActionChains(driver)
    action_asset_button.move_to_element(asset_button).perform()
    asset_button.click()
    loa=[x.get_attribute('href') for x  in driver.find_elements(By.XPATH,'//a[contains(@href,"download-free-forex-historical-data")]')]
    handle_cookies(driver)
    for i in loa[:]:
        handle_cookies(driver)
        if i not in already:
            print('Downloading '+i)
            already.append(i)
            driver.get(i)
            time.sleep(3)
            handle_cookies(driver)
            try:
                # delete element
                driver.execute_script("document.getElementById('cookie-law-info-bar').remove();")
            except:
                pass

            button=driver.find_element(By.ID,'a_file')
            actions=ActionChains(driver)
            actions.move_to_element(button).perform()
            button.click()
        else:
            print('Already Downloaded')
    time.sleep(20)
    driver.quit()
    ####
    current_dir = os.getcwd()
    output_directory = current_dir+'/destination'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Folder '{output_directory}' created successfully.")
    else:
        print(f"Folder '{output_directory}' already exists.")

    # Search for zip files in the directory
    zip_files = [file for file in os.listdir(current_dir) if file.endswith(".zip")]

    # Unzip each zip file and delete it afterwards
    for zip_file in zip_files:
        zip_path = os.path.join(current_dir, zip_file)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_directory)
        os.remove(zip_path)

    print("All zip files have been unzipped and deleted.")
    ####
    # read all the csv files in the destination folder and concatenate them
    csv_files = [file for file in os.listdir(output_directory) if file.endswith(".csv")]
    df_list = []
    for csv_file in csv_files:
        df = pd.read_csv(os.path.join(output_directory, csv_file),header=None)
        df.columns=['date','time','open','high','low','close','volume']
        df['datetime']=pd.to_datetime(df['date']+' '+df['time'])
        df=df[['datetime','open','high','low','close','volume']]
        df=df.drop_duplicates(subset=['datetime'],keep='first')

        df_list.append(df)
    #### delete the destination folder
    shutil.rmtree(output_directory)
    print(f"Folder '{output_directory}' has been deleted successfully.")
    return df_list
