# main script

from linkedin_scraper import LinkedInScraper
from config import LINKEDIN_USERNAME, LINKEDIN_PASSWORD, STATES
from utils import save_to_csv

def main():
    scraper = LinkedInScraper(username=LINKEDIN_USERNAME, password=LINKEDIN_PASSWORD)
    scraper.login()
    
    all_jobs = []
    for state in STATES:
        jobs = scraper.search_jobs('LabVIEW', state)
        print(f"Jobs found in {state}: {len(jobs)}")
        for job in jobs:
            print(job)  # display each job's details
        all_jobs.extend(jobs)
    
    # filter out unwanted industries
    filtered_jobs = [job for job in all_jobs if not any(industry in job['Company'] for industry in ['Aerospace', 'Defense', 'Semiconductor'])]
    
    save_to_csv(filtered_jobs, 'labview_jobs.csv')
    print("Job data saved to labview_jobs.csv")

if __name__ == "__main__":
    main()
