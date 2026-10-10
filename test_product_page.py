
import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

response = requests.get(url, timeout=15)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Store all scraped information in one dictionary
product = {}

# 1. Product title
title_element = soup.select_one("div.product_main h1")
product["title"] = title_element.get_text(strip=True) if title_element else ""

# 2. Price
price_element = soup.select_one("p.price_color")
product["price"] = price_element.get_text(strip=True) if price_element else ""

# 3. Rating
rating_element = soup.select_one("p.star-rating")
product["rating"] = ""

if rating_element:
    rating_classes = rating_element.get("class", [])
    product["rating"] = next(
        (rating for rating in rating_classes
         if rating in ["One", "Two", "Three", "Four", "Five"]),
        ""
    )

# 4. Product description
description_heading = soup.find("div", id="product_description")
product["description"] = ""

if description_heading:
    description_element = description_heading.find_next_sibling("p")

    if description_element:
        product["description"] = description_element.get_text(" ", strip=True)

# 5. Product information table
product_details = {}

for row in soup.select("table tr"):
    label = row.find("th")
    value = row.find("td")

    if label and value:
        key = label.get_text(strip=True)
        detail = value.get_text(" ", strip=True)
        product_details[key] = detail

# Add the table information to the product dictionary
product["upc"] = product_details.get("UPC", "")
product["product_type"] = product_details.get("Product Type", "")
product["price_excl_tax"] = product_details.get("Price (excl. tax)", "")
product["price_incl_tax"] = product_details.get("Price (incl. tax)", "")
product["tax"] = product_details.get("Tax", "")
product["availability"] = product_details.get("Availability", "")
product["number_of_reviews"] = product_details.get("Number of reviews", "")

# 6. Product URL
product["url"] = url

# Display the results
print("\n--- COMPLETE PRODUCT DATA ---")

for key, value in product.items():
    print(f"{key}: {value}")