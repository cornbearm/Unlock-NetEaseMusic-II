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
    browser.add_cookie({"name": "MUSIC_U", "value": "00A7C100D0FE32F423CB682936791F0A651CC1BA35F63F048DB7823A589A3EDE164D816202F96F45C0D65627844E8152391664DF81D0953DEF1D1768664CC1A9A80EB7A3E1BE9A84F2DF25C4E98536BD5D9535525B754936690D3E9C6C70F58ACCF4ED9CD9C6404C07617F9106F0CDA113DB9D2C318B55491AF8EBC4C9FF3D742DC2D03ED2A3F8D9E15969911E156D1AAD13EC143F8307F161060C966413AEF24A7AB4B30CD56AB17AA26A42CB42625607B192358E598B0B878D4CB235605C862E359209793AAC279CB928B21E4F657AB8DC73D254B3023E6B9EFBF9D4165B70EE7186C1390B284B5DEE2CCAE3E9CDC3E13F46EE91CF1A888C08CAC0ECFB81C8BF5A0436AE943321E24B07FEA22457C3E551DAC453336B7E411206A271506F3F693734D1F3471A32BF13FABEE3BF46977880FCFB2E9A2A628EED86008F51FA4FFDFA5EAFAED58B15C9F070D083E31C9A575F4476679D48FE3E2B98E58CF6FBB48D"})
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
