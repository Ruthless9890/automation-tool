## first Bay area region -- lab view open positions, iwth company name and hiring manager name, then US

import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Your LinkedIn credentials
linkedin_username = "ragavan.ims@gmail.com"
linkedin_password = "Speed=MSDhoni07"

# Path to your ChromeDriver executable
driver = webdriver.Chrome()

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

    # Open the LinkedIn jobs page
    driver.get("https://www.linkedin.com/jobs/search/?keywords=Labview&location=San%20Francisco%20Bay%20Area&geoId=90000084&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true")
    print("Opened LinkedIn jobs page")
    time.sleep(20)

    # Scroll to the bottom of the page to load more jobs
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("Scrolled to bottom of the page")
        time.sleep(20)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    print("Completed scrolling")

    # Find job postings
    wait = WebDriverWait(driver, 60)
    jobs_list = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-search__results-list")))
    jobs = jobs_list.find_elements(By.TAG_NAME, "li")
    print(f"Found {len(jobs)} job postings")

    # Define the file path for the CSV in the Downloads directory
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    file_path = os.path.join(downloads_path, "linkedin_jobs.csv")

    # Ensure the Downloads directory exists
    if not os.path.exists(downloads_path):
        os.makedirs(downloads_path)

    print("Reached the file creation section")

    # Open a CSV file to write job details
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        print("CSV file opened")
        writer = csv.writer(file)
        writer.writerow(['Job Title', 'Company', 'Location', 'Job Link', 'Company Link', 'Hiring Manager'])
        print("CSV headers written")

        # Loop through each job posting and extract details
        for index, job in enumerate(jobs):
            try:
                job_link_element = job.find_element(By.CLASS_NAME, "base-card__full-link")
                job_link = job_link_element.get_attribute("href")

                title_element = job.find_element(By.CLASS_NAME, "base-search-card__title")
                title = title_element.text

                company_element = job.find_element(By.CLASS_NAME, "base-search-card__subtitle")
                company = company_element.text

                company_link_element = company_element.find_element(By.TAG_NAME, "a")
                company_link = company_link_element.get_attribute("href")

                location_element = job.find_element(By.CLASS_NAME, "job-search-card__location")
                location = location_element.text

                if job_link:
                    # Navigate to the job link to get the hiring manager's name
                    driver.get(job_link)
                    print(f"Navigated to job link for job {index + 1}")
                    time.sleep(20)  # Increase sleep duration to ensure the page loads

                    hiring_manager_element = driver.find_element(By.XPATH, "//span[@class='jobs-poster__name t-14 t-black t-bold']")
                    hiring_manager = hiring_manager_element.text if hiring_manager_element else "Not available"
                    print(f"Extracted hiring manager for job {index + 1}: {hiring_manager}")

                    # Write the details to the CSV file
                    writer.writerow([title, company, location, job_link, company_link, hiring_manager])
                    print(f"Written job {index + 1} to CSV")

                    # Navigate back to the job list page
                    driver.back()
                    time.sleep(10)
                else:
                    print(f"Job link not found for job: {title}")
            except Exception as e:
                print(f"An error occurred for job {index + 1}: {e}")

    print("CSV file creation completed")

finally:
    # Close the WebDriver
    driver.quit()
    print("Closed the WebDriver")