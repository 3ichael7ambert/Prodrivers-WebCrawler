import requests
from bs4 import BeautifulSoup

url = "https://www.prodrivers.com/jobs/?City=Denver&State=Colorado"

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Extract the desired information from the parsed HTML
job_titles = [job.text for job in soup.find_all("h2", class_="jobTitle")]
job_locations = [location.text for location in soup.find_all("span", class_="jobLocation")]

# Print the scraped data
for title, location in zip(job_titles, job_locations):
    print("Job Title:", title)
    print("Job Location:", location)
    print("---")