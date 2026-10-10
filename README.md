# Python Web Scraping and Excel Export

A Python web scraping project that collects book information from [Books to Scrape](https://books.toscrape.com/) and exports the results to CSV and Excel files.

## Features

* Scrapes book titles, prices, ratings, availability, and product URLs.
* Extracts detailed product information, including UPC, product type, tax, descriptions, and review counts.
* Collects data across multiple catalogue pages.
* Exports scraped information to CSV files.
* Generates formatted Excel workbooks with clickable URLs, filters, and frozen headers.
* Handles HTTP errors and request timeouts.

## Technologies Used

* Python 3
* Requests
* BeautifulSoup
* OpenPyXL
* CSV

## Project Files

| File                        | Purpose                                             |
| --------------------------- | --------------------------------------------------- |
| `main.py`                   | Scrapes basic book information                      |
| `scrape_product_details.py` | Extracts detailed information from product pages    |
| `export_excel.py`           | Exports basic data to Excel                         |
| `export_detailed_excel.py`  | Exports detailed data to a formatted Excel workbook |
| `requirements.txt`          | Lists Python dependencies                           |

## Installation

Clone the repository:

```bash
git clone https://github.com/kaveenhansajith22/Web-scraping-project-1.git
cd Web-scraping-project-1
```

Create and activate a virtual environment on macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
python3 -m pip install -r requirements.txt
```

## Usage

Scrape the catalogue:

```bash
python3 main.py
```

Extract detailed product information:

```bash
python3 scrape_product_details.py
```

Export the detailed data to Excel:

```bash
python3 export_detailed_excel.py
```

The scripts generate CSV and Excel files in the project directory.

## Data Quality

The detailed scraping run collected 1,000 book records. The initial quality check found no missing UPCs or duplicate product URLs and two missing descriptions.

## Learning Project

This project was built for practice and portfolio development. The target website is a practice website designed for web scraping.

Please use scraping techniques responsibly, respect website terms and access restrictions, and avoid excessive requests.

## Author

**Kaveen Hansajith Karunarathna**

GitHub: [@kaveenhansajith22](https://github.com/kaveenhansajith22)
