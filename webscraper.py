import requests
from bs4 import BeautifulSoup
from markupsafe import escape #fixes jinja2 escape error

city = input("Enter the city: ")
state = input("Enter the state: ")

# Format the user input into proper URL parameters
city_param = f"City={city}"
state_param = f"State={state}"

# Construct the URL with the updated parameters
url = f"https://www.prodrivers.com/jobs/?{city_param}&{state_param}"

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
