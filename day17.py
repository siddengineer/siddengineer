import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table

# Function to scrape books from the website
def scrape_books(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    data = []
    
    # Finding book titles and prices
    for book in soup.find_all('article', class_='product_pod'):
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        data.append({'title': title, 'price': price})
    
    return data

# Main CLI program
def main():
    console = Console()
    
    # Test URL for scraping books
    url = "http://books.toscrape.com/"
    
    console.print(f"[bold green]Scraping {url}...[/bold green]", style="bold")
    data = scrape_books(url)

    if data:
        # Display results in a table format
        table = Table(title="Scraped Books")

        table.add_column("Title", style="cyan", no_wrap=True)
        table.add_column("Price", style="green")

        for item in data:
            table.add_row(item['title'], item['price'])

        console.print(table)
    else:
        console.print("[bold red]No data found or scraping failed.[/bold red]")

if __name__ == "__main__":
    main()
