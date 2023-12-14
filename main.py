from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from dotenv import load_dotenv
import os

load_dotenv()

url = "https://schedulebuilder.yorku.ca/vsb/criteria.jsp?access=0&lang=en&tip=0&page=results&scratch=0&term=2023102119"
course_name = "LE-EECS-2101-3.00-EN"
course_term = "Term W"
course_section = "Section N"
username = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")

try:
    service = Service(executable_path="chromedriver.exe")
    options = Options()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(service=service, options=options) 

    # Go to VSB (Which redirects to York's login page)
    driver.get(url)

    # Login
    driver.find_element(By.ID, "mli").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password + Keys.ENTER)

    # Wait for the duo mobile iframe to load
    sleep(3)

    # Wait for the duo mobile iframe to load
    WebDriverWait(driver, 5).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "duo_iframe"))
    )

    # Click on send me a push
    driver.find_element(By.CSS_SELECTOR, "#auth_methods > fieldset > div.row-label.push-label > button").click()
    driver.find_elements(By.TAG_NAME, "button")[0].click()
    
    sleep(20)

except KeyboardInterrupt as e:
    print("exiting...")
except Exception as e:
    print(e)
    # driver.quit()


info = {}

while True:
    try:
        # Search for course
        driver.find_element(By.ID, "code_number").send_keys(course_name + Keys.ENTER)

        # Select term
        term = driver.find_element(By.CSS_SELECTOR, "#requirements > div:nth-child(3) > div.courseDiv.bc1.bd1 > div:nth-child(12) > select")
        term.click()
        terms = term.text.split("\n")
        term.find_elements(By.TAG_NAME, "option")[terms.index(course_term)].click()

        # Select section
        section = driver.find_element(By.CSS_SELECTOR, "#requirements > div:nth-child(3) > div.courseDiv.bc1.bd1 > div:nth-child(13) > select")
        section.click()
        sections = section.text.split("\n")
        section.find_elements(By.TAG_NAME, "option")[sections.index(course_section)].click()

        # Get the course information
        courses = driver.find_elements(By.CLASS_NAME, "course_box")

        # TODO: Labs and tutorials seats might not all be avaialable

        for course in courses:
            lines = course.text.split("\n")
            title = lines[0]
            catalog = lines[5]
            seats = lines[6].split(" ")[-1] == "Available"
            prof = lines[-1]
            if title.startswith(course_name):
                info = {
                    "title": title,
                    "catalog": catalog,
                    "seats": seats,
                    "prof": prof
                }

        break
    except Exception as e:
        sleep(2)
        print("Waiting for page to load...")

print(info)