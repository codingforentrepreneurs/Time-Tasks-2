import time
from celery import shared_task
from django.apps import apps
# from .models import PriceLookupEvent
from .scraper import StockTickerScraper


@shared_task
def hello_world(num=10):
    time.sleep(num)
    print(f"Hello world {num}")


@shared_task
def perform_scrape(ticker='AAPL', service='echo'):
    client = StockTickerScraper(service=service)
    name, price = client.scrape(ticker=ticker)
    price = price.replace(",", "")
    # custom_django_signal - > send when this event happens
    print('task', name, price)
    PriceLookupEvent = apps.get_model("stocks", "PriceLookupEvent")
    PriceLookupEvent.objects.create_event(ticker, price, name=name, source=service)
    

@shared_task
def company_price_scrape_task(instance_id, service='echo'):
    """
    Perform company price scraping event.
    """
    Company = apps.get_model("stocks", "Company")
    obj = Company.objects.get(id=instance_id)
    ticker = obj.ticker
    perform_scrape(ticker=ticker, service=service)
