import requests
from bs4 import BeautifulSoup

# Define the URL of the website to scrape
url = "https://cpclogistics.com/jobs/us/?search_location=denver"

# Define a User-Agent header to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Send a GET request to the URL with headers
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract job listings
    job_listings = soup.select('li.job_listing')

    # Initialize a list to store job info objects
    job_info_list = []

    for job_listing in job_listings:
        # Extract job title
        title = job_listing.find('h3').text.strip()

        # Extract job location
        location = job_listing.find('span', class_='location').text.strip()

        # Extract city and state from location (assuming the format is "City, State")
        city, state = location.split(', ')

        # Extract base pay (if available)
        base_pay_element = job_listing.find('span', class_='salary-content')
        base_pay = base_pay_element.text.strip() if base_pay_element else None

        # Extract job duties
        duties_elements = job_listing.find_all('li', class_='job-duty')
        duties_list = [duty.text.strip() for duty in duties_elements]

        # Extract job link
        job_link = job_listing.find('a', href=True)['href']

        # Create a job_info dictionary for this listing
        job_info = {
            'Title': title,
            'Location': location,
            'City': city,
            'State': state,
            'Base Pay': base_pay,
            'Duties': duties_list,
            'Job Link': job_link
        }

        # Add this job_info dictionary to the list
        job_info_list.append(job_info)

    # Print the scraped job info
    for job_info in job_info_list:
        print("Job Information:")
        print(job_info)
        print("---")

else:
    print("Failed to fetch data. Status code:", response.status_code)
