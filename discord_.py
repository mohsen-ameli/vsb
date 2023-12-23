from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from functions import *
import os

if __name__ == "__main__":
    try:
        service = Service(executable_path=os.getenv("CHROME_DRIVER_PATH"))
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("start-maximized")
        driver = webdriver.Chrome(service=service, options=options)

        # get initial info from VSB site
        get_info_vsb(driver)

        # start the discord bot
        run_discord_bot(driver)
    except KeyboardInterrupt as e:
        print("exiting...")
    except Exception as e:
        print(e)