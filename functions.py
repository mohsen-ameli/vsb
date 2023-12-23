from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from dotenv import load_dotenv
import os
import discord
import random
import asyncio

###
# the main parameters
###
url = "https://schedulebuilder.yorku.ca/vsb/criteria.jsp?access=0&lang=en&tip=0&page=results&scratch=0&term=2023102119"
course_name = "LE-EECS-2101-3.00-EN"
course_term = "Term W"
course_section = "Section N"

###
# Environment variables
###
load_dotenv()
username = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")
discord_token = os.getenv("DISCORD_TOKEN")
discord_user = os.getenv("DISCORD_TARGET_USER")

###
# Will give you the seats and prof info using the visual schedule builder from york
###
def get_info_vsb(driver: webdriver.Chrome) -> dict:
    info = {}

    try:
        driver.get(url)
        sleep(1)
        login(driver)
        driver.refresh()
        sleep(1)

        # Search for the course
        driver.find_element(By.ID, "code_number").send_keys(course_name + Keys.ENTER)
        sleep(1)

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
    except Exception as e:
        sleep(5)
        print("Waiting for page to load...")

    return info

###
# Login to the york passport
###
def login(driver: webdriver.Chrome):
    driver.find_element(By.ID, "mli").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password + Keys.ENTER)

    # Wait for the duo mobile iframe to load
    sleep(3)

    # Wait for the duo mobile iframe to load
    WebDriverWait(driver, 5).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "duo_iframe"))
    )

    # Click on send me a push
    driver.find_element(By.NAME, "dampen_choice").click()
    driver.find_element(By.CSS_SELECTOR, "#auth_methods > fieldset > div.row-label.push-label > button").click()
    driver.find_elements(By.TAG_NAME, "button")[0].click()

    ####################
    # Wait for the page to load
    ####################
    sleep(20)

###
# fetches info from VSB by refreshing the page
###
def fetch_info(driver: webdriver.Chrome) -> dict:
    driver.refresh()
    sleep(1)
    
    info = {}

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
    
    return info

###
# Runs the discord bot
###
def run_discord_bot(driver: webdriver.Chrome):
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')


    @client.event
    async def on_message(message: discord.Message):
        if message.author == client.user:
            return
        if str(message.author) == discord_user and str(message.content) == "start":
            await message.channel.send("Ok starting bot daddy...")
            # Every 5-10 minutes check if there are seats available, and if yes, send a message to the me
            while True:
                info = fetch_info(driver)
                print(info)
                if info["seats"] == True:
                    await message.author.send(f"Seats are available for {info['title']} with {info['prof']}")
                await asyncio.sleep(random.randint(5, 10) * 60)
        else:
            return

    client.run(discord_token)



###
# @DEPRECATED
# Function that will give you the info from the york's courses website
# This website has a ~2 minute cookie time, so you have to login every 2 minutes
###
def get_info_course_web(driver: webdriver.Chrome) -> dict:
    url = "https://w2prod.sis.yorku.ca/Apps/WebObjects/cdm"
    course_name = "Fundamentals of Data Structures"
    course_catalog = "G26C01"

    try:
        # Going to the course title search
        driver.get(url)
        driver.find_element(By.XPATH, "/html/body/p/table/tbody/tr[2]/td[1]/table/tbody/tr[5]/td/a/img").click()

        # Clear the search bar
        driver.find_element(By.ID, "courseTitleInput").clear()
        
        # Search for the course
        driver.find_element(By.ID, "courseTitleInput").send_keys(course_name + Keys.ENTER)

        # Get the course url
        course_url = driver.find_element(By.CSS_SELECTOR, "body > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > table:nth-child(3) > tbody > tr:nth-child(2) > td:nth-child(3) > a").get_attribute("href")
        driver.get(course_url)

        row = driver.find_element(By.CSS_SELECTOR, "body > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > table:nth-child(9) > tbody").find_elements(By.TAG_NAME, "tr")[0]
        login_url = row.find_elements(By.TAG_NAME, "td")[0].find_element(By.TAG_NAME, "table").find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")[1].find_elements(By.TAG_NAME, "td")[0].find_element(By.TAG_NAME, "a").get_attribute("href")

        driver.get(login_url)
        sleep(3)
        login(driver)

        # soup = BeautifulSoup(driver.page_source, "html.parser")

        # # All course tables
        # courses = soup.find_all("table")[7].find("tbody").findChildren("tr", recursive=False)

        # for i in range(len(courses)):
        #     course = courses[i].find("td").find("table").find("tbody").findChildren("tr", recursive=False)
        #     section = course[0] # the section and terms
        #     seats_and_prof = course[1].text # seats and prof
        #     details = course[2].find("tbody").findChildren("tr", recursive=False) # details of the course which is a table
        #     lecture = details[1].findChildren("td", recursive=False) # the first row of the details table is the lecture
        #     # the second row if it exists is the lab?
        #     # the third row if it exists is the tutorial?
        #     catalog = lecture[2].text
        #     prof = seats_and_prof.strip().split("\n")[-1].strip()

        #     # If we found the course
        #     if catalog == course_catalog:
        #         seats = seats_and_prof.find("Section/Course") == -1
        #         info = {
        #             "seats": seats,
        #             "prof": prof
        #         }
        #         break

        # Scraping for info
        for el in driver.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td/table[2]/tbody").find_elements(By.TAG_NAME, "tr"):
            if course_catalog in el.text:
                lines = el.text.split("\n")
                prof = lines[-2]
                if el.text.find("Section/Course") != -1 or el.text.find("Seats Available") != -1:
                    seats = lines[1].split(" ")[-1]
                else:
                    seats = "Available"
                info = {
                    "seats": seats,
                    "prof": prof
                }
                break

        return info

    except Exception as e:
        print(e)