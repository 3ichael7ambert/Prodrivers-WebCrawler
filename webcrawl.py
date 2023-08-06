import requests
from bs4 import BeautifulSoup
import json

def scrape_job_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        job_blocks = soup.select('div.job.accordion')

        job_data = []
        for block in job_blocks:
            title = block.select_one('h2.job-title a').text.strip()
            location = block.select_one('h3.job-location').text.strip()
            base_pay = block.select_one('div.base-pay p strong').next_sibling.strip()
            duties = block.select('div.accordion-content ul li')
            duties_list = [duty.text.strip() for duty in duties]

            job_info = {
                'Title': title,
                'Location': location,
                'Base Pay': base_pay,
                'Duties': duties_list
            }

            job_data.append(job_info)

        return job_data
    else:
        print("Failed to fetch data. Status code:", response.status_code)
        return None

if __name__ == "__main__":
    url = "https://www.prodrivers.com/jobs/?_city=denver&_state=co&_title=driver"
    job_data = scrape_job_data(url)

    if job_data:
        json_output = json.dumps(job_data, indent=2)
        print(json_output)
    else:
        print("Failed to fetch data.")
