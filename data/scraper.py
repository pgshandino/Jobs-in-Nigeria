import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

# Number of pages to scrape
pages = 177
base_url = "https://www.jobberman.com"

# Function to get detailed job data from a job's URL
def get_job_data(url: str) -> dict:
    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    
    # Extracting job details such as location, job type, and industry
    data = dict(zip(["Location", "Job type", "Industry"], [i.text.strip() for i in soup.find_all("a", class_="text-sm font-normal px-3 rounded bg-brand-secondary-50 mr-2 mb-3 inline-block")]))
    
    # Extracting salary information
    data['Salary'] = soup.find('span', class_="text-sm font-normal px-3 rounded bg-brand-secondary-50 mr-2 mb-3 inline-block").text.strip()
    
    # Extracting additional job details
    data['details'] = [i.text.strip() for i in soup.find('ul', class_="pl-5 text-sm list-disc text-gray-500").find_all('li')]
    
    # Extracting other relevant information
    data["info"] = [i.text.strip() for i in soup.find_all('ul', class_="list-disc list-inside")]
    
    return data

# Function to extract job information from the landing page
def get_jobs_landing():
    data = dict(
        name = job.find('a').text.strip(),
        job_url = job.find('a')['href'],
        hiring_firm = job.find("p", class_="text-sm text-link-500").text.strip(),
        hiring_firm_url = job.find("p", class_="text-sm text-link-500").find('a')['href'],
        job_function = job.find("p", class_="text-sm text-gray-500 text-loading-animate inline-block").text.strip(),
        title = job.find("p", class_="text-lg font-medium break-words text-link-500").text.strip(),
        date_posted = job.find("p", class_="ml-auto text-sm font-normal text-gray-700 text-loading-animate").text.strip()
    )
    
    return data

# List to store job data
jobs = []

# Loop through all pages to collect job data
for page in range(1, pages + 1):
    print(f"Scraping page {page}")
    response = requests.get(f"{base_url}/jobs?page={page}")
    soup = bs(response.text, 'html.parser')
    
    # Find all job listings on the page
    jobs_per_page = soup.find_all(
        "div",
        class_="mx-5 md:mx-0 flex flex-wrap col-span-1 mb-5 bg-white rounded-lg border border-gray-300 hover:border-gray-400 focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-gray-500"
    )
    
    # Extract data for each job listing
    for job in jobs_per_page:
        job_url = job.find('a')['href']
        
        try:
            data = dict(
                name = job.find('a').text.strip(),
                job_url = job.find('a')['href'],
                hiring_firm = job.find("p", class_="text-sm text-link-500").text.strip(),
                hiring_firm_url = base_url + job.find("p", class_="text-sm text-link-500").find('a')['href'],
                job_function = job.find("p", class_="text-sm text-gray-500 text-loading-animate inline-block").text.strip(),
                title = job.find("p", class_="text-lg font-medium break-words text-link-500").text.strip(),
                date_posted = job.find("p", class_="ml-auto text-sm font-normal text-gray-700 text-loading-animate").text.strip()
            )
        except TypeError:
            data = dict(
                name = job.find('a').text.strip(),
                job_url = job.find('a')['href'],
                hiring_firm = job.find("p", class_="text-sm text-link-500").text.strip(),
                hiring_firm_url = None,
                job_function = job.find("p", class_="text-sm text-gray-500 text-loading-animate inline-block").text.strip(),
                title = job.find("p", class_="text-lg font-medium break-words text-link-500").text.strip(),
                date_posted = job.find("p", class_="ml-auto text-sm font-normal text-gray-700 text-loading-animate").text.strip()
            )
        
        # Get additional data from the job's detailed page
        inner_data = get_job_data(job_url)
        data.update(inner_data)
        
        jobs.append(data)

# Convert the job data to a DataFrame and save as CSV
df = pd.DataFrame(jobs)
df.to_csv("Jobs NG.csv", index=False)
