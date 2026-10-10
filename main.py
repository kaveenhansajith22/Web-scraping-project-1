
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from decimal import Decimal, InvalidOperation

BASE_URL = "https://books.toscrape.com/"
START_URL = urljoin(BASE_URL, "catalogue/page-1.html")

books = []
current_url = START_URL

# Step 1: Scrape the books
while current_url:
    print(f"Scraping: {current_url}")

    response = requests.get(current_url, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for book in soup.select("article.product_pod"):
        title = book.h3.a["title"].strip()
        price = book.select_one(".price_color").get_text(strip=True)
        availability = book.select_one(
            ".availability"
        ).get_text(" ", strip=True)
        rating = book.select_one("p.star-rating")["class"][1]

        book_url = urljoin(current_url, book.h3.a["href"])

        books.append({
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
            "url": book_url
        })

    next_link = soup.select_one("li.next a")

    if next_link:
        current_url = urljoin(current_url, next_link["href"])
    else:
        current_url = None

# Step 2: Validate the scraped data
print("\n--- DATA VALIDATION REPORT ---")

valid_ratings = {"One", "Two", "Three", "Four", "Five"}
invalid_records = []

for book in books:
    problems = []

    # Check that the price is a valid number
    try:
        price_number = Decimal(
            book["price"].replace("£", "").strip()
        )

        if price_number < 0:
            problems.append("Negative price")

    except InvalidOperation:
        problems.append("Invalid price")

    # Check that the rating is valid
    if book["rating"] not in valid_ratings:
        problems.append("Invalid rating")

    # Check required fields
    for field in ["title", "price", "rating", "availability", "url"]:
        if not book[field]:
            problems.append(f"Missing {field}")

    if problems:
        invalid_records.append({
            "title": book["title"],
            "problems": problems
        })

# Step 3: Print the results
print(f"Total records: {len(books)}")
print(f"Invalid records: {len(invalid_records)}")
print(f"Valid records: {len(books) - len(invalid_records)}")

if invalid_records:
    print("\nRecords needing attention:")

    for record in invalid_records[:10]:
        print(record["title"], "-", ", ".join(record["problems"]))
else:
    print("All records passed these validation checks!")

# Step 4: Export the data to CSV
with open(
    "books.csv", "w", newline="", encoding="utf-8-sig"
) as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "title", "price", "rating", "availability", "url"
        ]
    )

    writer.writeheader()
    writer.writerows(books)

print("\nData saved to books.csv")