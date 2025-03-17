# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "005855E7D1C1A2B834C0984EFE2F8C49ADD9B777B0C3B6EA7E12ABBDD63A550F32713507F0D914782A3EB9FDDD41B303FF323EC5C62459A4CE7FA893712687046C10490CDA38F959717DDAEF5D9D0DABA40D14CD2F70D4B197B532A72ECAC00066D7F0240C3F37FE0AA54005F9EB43BBA828532563AA5D4CFBB51FB246E17F3DB1739A1BF19B5DC10D7520300A300FE5FCE86AA8DCE3CAFF499AD497A50878C77BE9054EB437520615B0BDB4C0DE34A1BBCAF1A82EE0B0C83DF4E5CA957DCB7DA9DA93EA1DB0447C8682487A7F9EE71F1BBF551A8C582E6E62E727F4744CE57FD325739CE51EBB4A97202E39445E9EE08D04718A164386A2BCC9C01CCCA3123F46AA2F5A31066D86FBC9C477A4EEFE6E9F1B860B8A9D1501E70A30B5D47B882942FD0A68B7D1BA55405D94318627F93BBA0D8BDA51A7282A46F265DEE8A40DABADC1F887C1D7AAE669AEF241D038E998FD0217EB13CFCA723D6469D5E61D6D1FD6"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
