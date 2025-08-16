import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random


def scrape_books_complete():
    """Scrapes book data with correct stock flag."""
    all_books = []
    base_url = "https://books.toscrape.com/catalogue/page-{}.html"

    for page_num in range(1, 6):  # scrape first 5 pages (~100 books)
        print(f"Scraping page {page_num}...")
        response = requests.get(base_url.format(page_num))
        soup = BeautifulSoup(response.content, 'html.parser')
        books = soup.select('article.product_pod')
        for book in books:
            # Title
            title = book.h3.a['title'].strip()

            # Price
            price_text = book.select_one('p.price_color').text.strip()
            price = float(price_text.replace('£', ''))

            # Rating
            rating_class = book.select_one('p.star-rating')['class'][1]
            rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
            rating = rating_map.get(rating_class, 0)

            # Availability & Stock Flag
            avail_text = book.select_one('p.instock.availability').text.strip()
            if "In stock" in avail_text:
                stock_count = 1
                in_stock = True
            else:
                stock_count = 0
                in_stock = False

            # Derived categories
            price_category = "Budget" if price < 20 else "Mid-Range" if price < 40 else "Premium"
            rating_category = "Poor" if rating <= 2 else "Average" if rating == 3 else "Good"
            category = random.choice([
                'Fiction', 'Mystery', 'Romance', 'Science Fiction', 'Fantasy',
                'Non-fiction', 'Biography', 'History', 'Travel', 'Cooking'
            ])

            all_books.append({
                'title': title,
                'price': price,
                'rating': rating,
                'availability': avail_text,
                'stock_count': stock_count,
                'in_stock': in_stock,
                'price_category': price_category,
                'rating_category': rating_category,
                'category': category
            })

        time.sleep(1)

    df = pd.DataFrame(all_books)
    df.to_csv('ecommerce_books_data.csv', index=False)
    print(f"Saved {len(df)} records to ecommerce_books_data.csv")


if __name__ == "__main__":
    scrape_books_complete()
