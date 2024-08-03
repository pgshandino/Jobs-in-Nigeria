### README

# Analyzing the Nigerian Job Market with Python

This project aims to analyze the Nigerian job market by scraping job data from Jobberman, building an API to serve the collected data, and automating the process using Prefect. The data will be analyzed using Pandas for insights, and the findings will be presented through an interactive dashboard.

## Table of Contents

- [Introduction](#introduction)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Requirements](#requirements)
  - [Installation](#installation)
- [Part 1: Web Scraping](#part-1-web-scraping)
  - [Scraping Jobberman](#scraping-jobberman)
  - [How to Run](#how-to-run)
- [Part 2: Building the API](#part-2-building-the-api)
- [Part 3: Automating with Prefect](#part-3-automating-with-prefect)
- [Part 4: Data Analysis and EDA](#part-4-data-analysis-and-eda)
- [Part 5: Deploying the Dashboard](#part-5-deploying-the-dashboard)
- [License](#license)

## Introduction

Understanding the job market landscape is crucial for various stakeholders including businesses, job seekers, and students. By analyzing job listings, we can uncover valuable insights such as the top-paying jobs, prominent industries, key locations with job opportunities, and more. This project will guide you through the process of analyzing the Nigerian job market by scraping data from Jobberman, one of the largest job boards in the country.

## Project Structure

1. **Part 1: Web Scraping** - Scraping job data from Jobberman.
2. **Part 2: Building the API** - Creating a RESTful API to serve the collected data.
3. **Part 3: Automating with Prefect** - Automating the scraping and data serving process.
4. **Part 4: Data Analysis and EDA** - Analyzing the data using Pandas and performing Exploratory Data Analysis (EDA).
5. **Part 5: Deploying the Dashboard** - Deploying an interactive dashboard to present the findings.

## Getting Started

### Requirements

- Python 3.7+
- `requests`
- `pandas`
- `beautifulsoup4`
- `Flask` (for the API)
- `Prefect` (for automation)
- `Dash` (for the dashboard)

### Installation

Clone the repository:

```bash
git clone https://github.com/pgshandino/Jobs-in-Nigeria.git
cd Jobs-in-Nigeria
```

Install the required libraries:

```bash
pip install requests pandas beautifulsoup4 Flask Prefect
```

## Part 1: Web Scraping

### Scraping Jobberman

In the first part of this project, we scrape job data from Jobberman. The script collects job details such as location, job type, industry, salary, and other relevant information.

### How to Run

1. Ensure you have Python installed on your machine.
2. Install the required libraries using the pip commands provided above.
3. Run the script using a Python IDE or terminal:

```bash
python scraper.py
```

The script will save the scraped data to a CSV file named `Jobs_NG.csv`.

## Part 2: Building the API

In the second part, we build a RESTful API using Flask to serve the collected job data. This API will allow users to access the job data programmatically.

## Part 3: Automating with Prefect

The third part involves automating the scraping and API serving process using Prefect. This will ensure that the job data is regularly updated without manual intervention.

## Part 4: Data Analysis and EDA

In the fourth part, we use Pandas to analyze the collected job data. We will perform Exploratory Data Analysis (EDA) to uncover insights such as the top-paying jobs, prominent industries, key locations with job opportunities, and more.

## Part 5: Deploying the Dashboard

Finally, we will deploy an interactive dashboard using Dash to present our findings. The dashboard will provide a user-friendly interface to explore the insights derived from the job data.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.