from prefect import task, flow
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
import re


pages = 2
base_url = "https://www.jobberman.com"
current_date = datetime.strptime('2024-07-25', '%Y-%m-%d').date()

def convert_relative_dates(date_str, current_date):
    date_str = date_str.lower()
    if date_str == 'today':
        return current_date
    elif date_str == 'yesterday':
        return current_date - timedelta(days=1)
    elif 'day' in date_str:
        days = int(date_str.split()[0])
        return current_date - timedelta(days=days)
    elif 'week' in date_str:
        weeks = int(date_str.split()[0])
        return current_date - timedelta(weeks=weeks)
    elif 'month' in date_str:
        months = int(date_str.split()[0])
        return current_date - timedelta(days=30*months)
    else:
        return None

def extract_currency(salary_str):
    return salary_str.split('\n\n')[0]

def extract_min_salary(salary_str):
    if 'Confidential' in salary_str:
        return 'Confidential'
    elif 'Commission Only' in salary_str:
        return 'Commission Only'
    elif 'Less than' in salary_str:
        return re.findall(r'\d+', salary_str.replace(',', ''))[0]
    elif 'More than' in salary_str:
        return re.findall(r'\d+', salary_str.replace(',', ''))[0]
    else:
        return salary_str.split('\n\n')[1].split(' - ')[0].replace(',', '')

def extract_max_salary(salary_str):
    if 'Confidential' in salary_str:
        return 'Confidential'
    elif 'Commission Only' in salary_str:
        return 'Commission Only'
    elif 'Less than' in salary_str:
        return re.findall(r'\d+', salary_str.replace(',', ''))[0]
    elif 'More than' in salary_str:
        return re.findall(r'\d+', salary_str.replace(',', ''))[0]  # Adjust if necessary for more precise handling
    else:
        return salary_str.split('\n\n')[1].split(' - ')[-1].replace(',', '')


# Function to get detailed job data from a job's URL
@task
def get_job_data(url: str) -> dict:
    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    
    # Extracting job details such as location, job type, and industry
    data = dict(zip(["Location", "Job type", "Industry"], [i.text.strip() for i in soup.find_all("a", class_="text-sm font-normal px-3 rounded bg-brand-secondary-50 mr-2 mb-3 inline-block")]))
    
    # Extracting salary information
    data['Salary'] = soup.find('span', class_="text-sm font-normal px-3 rounded bg-brand-secondary-50 mr-2 mb-3 inline-block").text.strip()
    
    # Extracting additional job details
    data['details'] = ';'.join([i.text.strip() for i in soup.find('ul', class_="pl-5 text-sm list-disc text-gray-500").find_all('li')])
    
    # Extracting other relevant information
    data["info"] = [i.text.strip() for i in soup.find_all('ul', class_="list-disc list-inside")]
    
    return data

@task
def get_jobs(pages: int) -> list:
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
            inner_data = get_job_data.submit(job_url)
            data.update(inner_data.result())
            
            jobs.append(data)

    return jobs

@flow
def job_data_flow():
    data = get_jobs(pages=pages)
    return data

@task
def convert_data_to_df(data):
    df = pd.DataFrame(data)
    return df

@task
def clean_data(df):
    df['date_posted'] = df.date_posted.apply(lambda x: convert_relative_dates(x, current_date))
    df['currency'] = df['Salary'].apply(extract_currency)
    df['min_salary'] = df['Salary'].apply(extract_min_salary)
    df['max_salary'] = df['Salary'].apply(extract_max_salary)
    deets = ["Minimum Qualification", "Experience Level", "Experience Length"]

    df[deets] = df.details.str.split(";", expand=True)

    

    for deet in deets:
        df[deet] = df[deet].str.split(":", expand=True)[1].str.strip("\\n")

    return df

@task
def save_to_csv(df, filename):
    df.to_csv(filename, index=False)

@flow
def data_flow(data):
    df = convert_data_to_df(data)
    cleaned_df = clean_data(df)
    save_to_csv(cleaned_df, "job_data.csv")
    return "Data saved successfully!"

@flow
def pipe():
    data = job_data_flow()
    dflow =  data_flow(data)

    print(dflow)


if __name__ == "__main__":
    pipe.serve(
        name="Daily Jobberman Data Pipeline",
        cron="59 23 * * *",  # Schedule to run every day at 11:59 PM
        tags=["Jobberman", "job scraping", "data pipeline", "automation"],
        description="This pipeline automates the scraping, cleaning, and saving of job data from Jobberman on a daily basis.",
        version="jobberman-pipeline/v1.0",
    )
