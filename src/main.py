from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from functions import *
import os

if __name__ == "__main__":
    loop = True

    while loop:
        course_name = input("Enter course name (e.g: LE-EECS-2101-3.00-EN): ").strip()
        course_term = input("Enter course term (e.g: W): ").strip().upper()
        course_section = input("Enter course section (e.g: N): ").strip().upper()

        if not course_name or not course_term or not course_section:
            print("Please enter all the fields")
        elif len(course_name.split("-")) != 5:
            print("Please enter a valid course name, with dashes in between (like LE-EECS-2101-3.00-EN)")
        elif len(course_term) != 1 or not course_term.isalpha():
            print("Please enter a single character for term")
        elif len(course_section) != 1 or not course_section.isalpha():
            print("Please enter a single character for section")
        else:
            loop = False
        print()

        course_term = "Term " + course_term
        course_section = "Section " + course_section

    try:
        service = Service(executable_path=os.getenv("CHROME_DRIVER_PATH"))
        options = Options()
        # options.add_argument('--no-sandbox')
        # options.add_argument('--headless')
        # options.add_argument('--disable-dev-shm-usage')
        options.add_argument("start-maximized")
        driver = webdriver.Chrome(service=service, options=options)

        # Login and find/select the course on VSB
        login_and_select_course(course_name, course_term, course_section, driver)

        # Start the discord bot
        run_discord_bot(course_name, driver)
    except KeyboardInterrupt as e:
        print("exiting...")
    except Exception as e:
        print(e)