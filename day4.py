import requests
from win10toast import ToastNotifier
import schedule
import time

# Function to fetch top news
def get_top_news(category="general", country_code="in"):
    base_url = 'https://saurav.tech/NewsAPI'
    url = f'{base_url}/top-headlines/category/{category}/{country_code}.json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        top_articles = data["articles"][:10]  # Fetching top 10 articles
        headlines = [article['title'] for article in top_articles]
        return headlines
    else:
        return ["Unable to fetch news at the moment."]

# Function to send desktop notifications
def send_desktop_notification(headlines):
    toaster = ToastNotifier()
    news_summary = "\n".join(headlines)
    toaster.show_toast(
        "Top News Headlines",
        news_summary,
        duration=30  # Increased notification duration in seconds
    )

# Function to be scheduled
def job():
    headlines = get_top_news(category="entertainment", country_code="in")
    send_desktop_notification(headlines)

# Schedule the job to run every hour
schedule.every().hour.do(job)

# Initial call to run the job immediately (optional)
job()

# Keep the script running to check for scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)
