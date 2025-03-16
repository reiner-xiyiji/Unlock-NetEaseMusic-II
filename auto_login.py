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
    browser.add_cookie({"name": "MUSIC_U", "value": "008A0AA2173BEBA359D48BD910115E315445BCA02D70CE1F93CC87EE6BB7D4B97B3B24DB99265CECA51645D4F6F111CF07AA1FE5736B840296A09BDFC443BBC758B7DDE55EA00E657823915BBBD964E1541C434CB3D0459626FDBBD1F8E4C0A3DEAB155FA0CE55818F81751BDAE840983F10FE8B6219F5B5B01C95BEF8F1BE3D70BD757CEF0E3809CA5A6112C7786ACDB95F6D9037796D21BE25AE3E475762D7296C4469C17F47C53F378D5D2E72ECB1790C24803D3621B8F2E250F5165811A54EAD11CA5A0324AA4ACCF05EDA34082EDEF8AB1C9BD16624A7CE8AF19D1CB3CA70EEAC449661E9F77C8506BBF9A2842712EFF149DA7570FBE4DB82C5B57EDE6AE022589631735D8F0579B80CE004F5A04FC48E68B8FCDAC3F8814EA3A0700E72008C7D9F110AB16689AB5D21D1BC819E1C8BDB672492F7E4FC20C716C9EDEBDEF9D1E234D4EBA0BF820A3549974C970236EBC0DB52360B3A6EFDA858E92CDAF9FC31A70829E8067A7ED5B11610E403EE3C"})
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
