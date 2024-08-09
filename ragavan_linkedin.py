import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Your LinkedIn credentials
linkedin_username = "ENTER YOUR USERNAME"
linkedin_password = "ENTER YOUR PASSWORD"

# Path to your ChromeDriver executable
driver = webdriver.Chrome()

file = [['Job Title', 'Company', 'Location', 'Job Link']]

# Define the file path for the CSV in the Downloads directory
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
file_path = os.path.join(downloads_path, "linkedin_jobs.csv")

# Ensure the Downloads directory exists
if not os.path.exists(downloads_path):
    os.makedirs(downloads_path)

try:
    # Open the LinkedIn login page
    driver.get("https://www.linkedin.com/login")
    print("Opened LinkedIn login page")
    time.sleep(10)

    # Enter username
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys(linkedin_username)
    print("Entered username")

    # Enter password
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(linkedin_password)
    print("Entered password")

    # Click the login button
    login_button = driver.find_element(By.XPATH, "//button[@aria-label='Sign in' and @type='submit']")
    login_button.click()
    print("Clicked login button")
    time.sleep(20)
except:
    print("Problem logging in")
    exit()
def jobs(url):
    try:
        # Open the LinkedIn jobs page for Labview positions in the San Francisco Bay Area
        driver.get(url)
        print("Opened LinkedIn jobs page for Labview positions in the San Francisco Bay Area")
        time.sleep(10)

        print("Reached the file creation section")

        # Find the <ul> element by class name or any other suitable selector
        ul_element = driver.find_element(By.CLASS_NAME, 'scaffold-layout__list-container')

        # Extract the HTML of the <ul> element
        html = ul_element.get_attribute('outerHTML')

        # Create a BeautifulSoup object
        soup = BeautifulSoup(html, 'html.parser')

        # Find the container that holds all the job listings
        job_listings = soup.find_all('li', class_='jobs-search-results__list-item')
        # Scrolling
        print("Scrolling")
        try:
            driver.execute_script("objDiv = document.getElementsByClassName(\"jobs-search-results-list\")[0]; while (objDiv.scrollTop < objDiv.scrollHeight) { objDiv.scrollTop += objDiv.scrollHeight/30; await new Promise(r => setTimeout(r, 1000)); }")
        except:
            pass # Avoid selenium script timeout
        time.sleep(5)
            # Find the <ul> element by class name or any other suitable selector
        ul_element = driver.find_element(By.CLASS_NAME, 'scaffold-layout__list-container')

        # Extract the HTML of the <ul> element
        html = ul_element.get_attribute('outerHTML')

        # Create a BeautifulSoup object
        soup = BeautifulSoup(html, 'html.parser')

        # Find the container that holds all the job listings
        job_listings = soup.find_all('li', class_='jobs-search-results__list-item')

        for job in job_listings:
            # Extract the job link
            job_link_tag = job.find('a', class_='job-card-container__link')
            job_link = job_link_tag['href'] if job_link_tag else None
            new_job_link = "https://linkedin.com" + job_link.split("?")[0] if job_link_tag else None
            # Extract the job title
            job_title = job_link_tag.get_text(strip=True) if job_link_tag else None
            
            # Extract the company name
            company_name_tag = job.find('span', class_='job-card-container__primary-description')
            company_name = company_name_tag.get_text(strip=True) if company_name_tag else None
            
            # Extract the company location
            company_location_tag = job.find('li', class_='job-card-container__metadata-item')
            company_location = company_location_tag.get_text(strip=True) if company_location_tag else None
            
            # Print the extracted details
            file.append([job_title, company_name, company_location, new_job_link])
    except:
        print("Error, moving on")

links = ["https://www.linkedin.com/jobs/search/?currentJobId=3978165932&geoId=90000084&keywords=Labview&location=San%20Francisco%20Bay%20Area&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true", "https://www.linkedin.com/jobs/search/?currentJobId=3864166405&geoId=90000084&keywords=Labview&location=San%20Francisco%20Bay%20Area&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&start=25", "https://www.linkedin.com/jobs/search/?currentJobId=3864166405&geoId=90000084&keywords=Labview&location=San%20Francisco%20Bay%20Area&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&start=50", "https://www.linkedin.com/jobs/search/?currentJobId=3864166405&geoId=90000084&keywords=Labview&location=San%20Francisco%20Bay%20Area&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&start=75"]

for link in links:
    jobs(link)

try:
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(file)
        print("CSV file creation completed")

finally:
    # Close the WebDriver
    driver.quit()
    print("Closed the WebDriver")
