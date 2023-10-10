import requests
from bs4 import BeautifulSoup

# Define the URL to scrape
url = "https://trilliumstaffing.com/jobs/search/?keywords=cdl&location={city}"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

# Initialize a list to store job information dictionaries
job_info_list = []

# Find all job teaser items
job_teaser_items = soup.find_all('a', class_='job_teaser_item')

# Loop through each job teaser item and extract information
for job_teaser in job_teaser_items:
    # Extract title
    title = job_teaser.find('h2').text.strip()

    # Extract location, city, and state
    location_and_timestamp = job_teaser.find('p', class_='location_and_timestamp').text.strip()
    location_parts = location_and_timestamp.split(' - ')
    location = location_parts[0]
    city, state = location.split(', ')
    
    # Extract job description
    description = job_teaser.find('p', class_='short_job_description').text.strip()

    # Create a job information dictionary
    job_info = {
        'Title': title,
        'Location': location,
        'City': city,
        'State': state,
        'Description': description
    }

    # Append the job information dictionary to the list
    job_info_list.append(job_info)

# Print the list of job information
for job_info in job_info_list:
    print(job_info)
