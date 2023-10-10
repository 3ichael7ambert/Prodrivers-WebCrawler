import requests
from bs4 import BeautifulSoup

# Construct the URL with the city parameter
url = f"https://cpclogistics.com/jobs/us/?search_location=denver"
print(url)
# Define a User-Agent header to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Send a GET request to the URL with headers
response = requests.get(url, headers=headers)


soup = BeautifulSoup(response.content, "html.parser")

    # Extract job URLs
job_urls = [a['href'] for a in soup.select('a[href*="https://cpclogistics.com/job/"]')]
print("Test::",job_urls)
    # Print the scraped job URLs
for job_url in job_urls:
        print("Job URL:", job_url)
        print("---")