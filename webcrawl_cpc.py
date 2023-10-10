import requests
from bs4 import BeautifulSoup
import json

def get_job_urls(city):
    search_url = f"https://cpclogistics.com/jobs/us/?search_location={city}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        job_urls = [a['href'] for a in soup.select('a[href*="https://cpclogistics.com/job/"]')]
        return job_urls
    else:
        print(f"Failed to fetch job URLs. Status code:", response.status_code)
        return []

def scrape_job_data_cpc(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract jobName from the URL
        job_name = url.split("/")[-2]

        # Extract job description, pay, location, etc. from the job detail page
        job_description_elem = soup.find('div', class_='position')
        if job_description_elem:
            job_description = job_description_elem.find('h3').text.strip()
        else:
            job_description = None

        salary_elem = soup.find('span', class_='salary-content')
        if salary_elem:
            salary = salary_elem.text.strip()
        else:
            salary = None

        job_type_elem = soup.find('span', class_='job-type-content')
        if job_type_elem:
            job_type = job_type_elem.text.strip()
        else:
            job_type = None

        overtime_elem = soup.find('span', class_='overtime-content')
        if overtime_elem:
            overtime = overtime_elem.text.strip()
        else:
            overtime = None

        license_type_elem = soup.find('h4', class_='class-a-cdl-driver')
        if license_type_elem:
            license_type = license_type_elem.text.strip()
        else:
            license_type = None

        work_days_elem = soup.find('span', class_='workdays-content')
        if work_days_elem:
            work_days = work_days_elem.text.strip()
        else:
            work_days = None

        run_shift_elem = soup.find('span', class_='runshift-content')
        if run_shift_elem:
            run_shift = run_shift_elem.text.strip()
        else:
            run_shift = None

        travel_distance_elem = soup.find('span', class_='distance-content')
        if travel_distance_elem:
            travel_distance = travel_distance_elem.text.strip()
        else:
            travel_distance = None

        freight_interaction_elem = soup.find('span', class_='freight-interaction-content')
        if freight_interaction_elem:
            freight_interaction = freight_interaction_elem.text.strip()
        else:
            freight_interaction = None

        job_info = {
            'Job Name': job_name,
            'Job Description': job_description,
            'Salary': salary,
            'Job Type': job_type,
            'Overtime': overtime,
            'License Type': license_type,
            'Work Days': work_days,
            'Run Shift': run_shift,
            'Travel Distance': travel_distance,
            'Freight Interaction': freight_interaction
        }

        return job_info
    else:
        print(f"Failed to fetch data for URL {url}. Status code:", response.status_code)
        return None