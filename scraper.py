# interacting with linkedin

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class LinkedInScraper:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        self.driver = webdriver.Chrome(service=Service('C:/Program Files/chromedriver.exe'), options=options)
    
    def login(self):
        try:
            self.driver.get('https://www.linkedin.com/login')
            time.sleep(2)
            self.driver.find_element(By.ID, 'username').send_keys(self.username)
            self.driver.find_element(By.ID, 'password').send_keys(self.password)
            self.driver.find_element(By.XPATH, '//*[@type="submit"]').click()
            time.sleep(3)
        except Exception as e:
            print(f"Error during login: {e}")
    
    def search_jobs(self, keyword, state):
        self.driver.get('https://www.linkedin.com/jobs')
        time.sleep(2)

        try:
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@placeholder="Search jobs"]'))
            )
            search_input.send_keys(keyword)
            search_input.send_keys(Keys.RETURN)
            time.sleep(3)

            location_filter = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@placeholder="City, state, or zip code"]'))
            )
            location_filter.clear()
            location_filter.send_keys(state)
            location_filter.send_keys(Keys.RETURN)
            time.sleep(3)
        
        except Exception as e:
            print(f"Error during search: {e}")
            self.driver.quit()
            return []

        all_jobs = []
        page_number = 1
        
        while len(all_jobs) < 100:
            jobs = self._extract_jobs()
            all_jobs.extend(jobs)
            if len(all_jobs) >= 100:
                break
            page_number += 1
            try:
                next_page_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f'//button[@aria-label="Page {page_number}"]'))
                )
                next_page_button.click()
                time.sleep(3)
            except:
                break
        
        return all_jobs[:100]
    
    def _extract_jobs(self):
        job_titles = []
        company_names = []
        locations = []
        dates = []
        
        jobs = self.driver.find_elements(By.CLASS_NAME, 'result-card__contents')
        for job in jobs:
            try:
                job_titles.append(job.find_element(By.CLASS_NAME, 'job-result-card__title').text)
                company_names.append(job.find_element(By.CLASS_NAME, 'job-result-card__subtitle').text)
                locations.append(job.find_element(By.CLASS_NAME, 'job-result-card__location').text)
                dates.append(job.find_element(By.CLASS_NAME, 'job-result-card__listdate').text)
            except Exception as e:
                print(e)
        
        return [{'Job Title': jt, 'Company': cn, 'Location': loc, 'Date': dt} for jt, cn, loc, dt in zip(job_titles, company_names, locations, dates)]

    def close(self):
        self.driver.quit()
