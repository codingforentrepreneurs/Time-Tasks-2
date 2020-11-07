import time
from celery import shared_task

from .models import PriceLookupEvent
from .scraper import StockTickerScraper

@shared_task
def hello_world(num=10):
    time.sleep(num)
    print(f"Hello world {num}")


@shared_task
def perform_scrape(ticker='AAPL', service='echo'):
    client = StockTickerScraper(service=service)
    name, price = client.scrape(ticker=ticker)
    # custom_django_signal - > send when this event happens
    print('task', name, price)
    PriceLookupEvent.objects.create_event(ticker, price, name=name, source=service)