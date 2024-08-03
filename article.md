### Blog Series: Analyzing the Nigerian Job Market with Python

#### **Introduction**

Understanding the job market landscape is crucial for various stakeholders including businesses, job seekers, and students. By analyzing job listings, we can uncover valuable insights such as the top-paying jobs, prominent industries, key locations with job opportunities, and more. This blog series will guide you through the process of analyzing the Nigerian job market by scraping data from Jobberman, one of the largest job boards in the country.

**About the Data Source**

Jobberman is a comprehensive job board that lists numerous job opportunities across various industries in Nigeria. It provides detailed job descriptions, requirements, and other relevant information, making it an excellent source for our analysis.

#### **The Plan**

1. **Scrape job listings from Jobberman.**
2. **Build a RESTful API to serve the collected data.**
3. **Automate the entire process using Prefect.**
4. **Analyze the data with Pandas and perform Exploratory Data Analysis (EDA).**
5. **Deploy an interactive dashboard to present our findings.**

---

### **Part 1: Scraping Jobberman for Job Data**

In this first part, we'll dive into web scraping using Python to collect job data from Jobberman.

#### **Requirements**

To follow along, you'll need the following Python libraries:
- `requests`
- `pandas`
- `beautifulsoup4`

You can install these using pip:

```bash
pip install requests pandas beautifulsoup4
```

#### **Code Overview**

We'll break down the scraping process into smaller parts for better understanding. The complete code can be found at the end of this post.

**1. Importing Libraries**

First, we need to import the necessary libraries:

```python
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
```

**2. Setting Up Constants**

Next, we'll set up some constants for our scraping process:

```python
pages = 177
base_url = "https://www.jobberman.com"
```

**3. Function to Get Job Data**

We'll create a function to get detailed job data from a job's URL:

```python
def get_job_data(url: str) -> dict:
    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    
    data = dict(zip(["Location", "Job type", "Industry"], [i.text.strip() for i in soup.find_all("a", class_="text-sm font-normal px-3 rounded bg-brand-secondary-50 mr-2 mb-3 inline-block")]))
    data['Salary'] = soup.find('span', class_="text-sm font-normal px-3 rounded bg-brand-secondary-50 mr-2 mb-3 inline-block").text.strip()
    data['details'] = [i.text.strip() for i in soup.find('ul', class_="pl-5 text-sm list-disc text-gray-500").find_all('li')]
    data["info"] = [i.text.strip() for i in soup.find_all('ul', class_="list-disc list-inside")]
    
    return data
```

**4. Function to Get Job Listings from Landing Page**

We'll create another function to extract job information from the main job listings page:

```python
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
```

**5. Scraping Loop**

Now, we'll loop through all pages to collect job data:

```python
jobs = []

for page in range(1, pages + 1):
    print(f"Scraping page {page}")
    response = requests.get(f"{base_url}/jobs?page={page}")
    soup = bs(response.text, 'html.parser')
    
    jobs_per_page = soup.find_all(
        "div",
        class_="mx-5 md:mx-0 flex flex-wrap col-span-1 mb-5 bg-white rounded-lg border border-gray-300 hover:border-gray-400 focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-gray-500"
    )
    
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
        
        inner_data = get_job_data(job_url)
        data.update(inner_data)
        
        jobs.append(data)
```

**6. Saving Data to CSV**

Finally, we'll convert the job data to a DataFrame and save it as a CSV file:

```python
df = pd.DataFrame(jobs)
df.to_csv("Jobs NG.csv", index=False)
```

**Running the Code**

1. **Ensure you have Python installed on your machine.**
2. **Install the required libraries using the pip commands provided above.**
3. **Run the script using a Python IDE or terminal.**

**Complete Code**

The complete code can be found [here](#).

In the next part of this series, we will build a RESTful API to serve the collected job data. Stay tuned!