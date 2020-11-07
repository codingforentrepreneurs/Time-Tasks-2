from django.db import models
from django.db.models.signals import post_save, pre_save

from .tasks import perform_scrape, company_granular_price_scrape_task

STOCK_MARKET_LOOKUP_SOURCES = (
    ('business_insider', 'Business Insider Markets'),
    ('google_finance', 'Google Finance'),
    ('echo', 'Http Bin Echo'),    
)

class Company(models.Model):
    name = models.CharField(max_length=220)
    ticker = models.CharField(max_length=20)
    description = models.TextField(blank=True,null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    has_granular_scraping = models.BooleanField(default=False)
    one_off_scrape = models.BooleanField(default=False)
    # default_service
    # events per minute

    def scrape(self, service='business_insider'):
        return company_granular_price_scrape_task.delay(self.id, service='business_insider')
    
    def __str__(self):
        return f"{self.name} ({self.ticker})"
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


def company_pre_save(sender, instance, *args, **kwargs):
    if instance.id:
        if instance.one_off_scrape:
            instance.one_off_scrape = False
            instance.scrape()

pre_save.connect(company_pre_save, sender=Company)


class PriceLookupEventManager(models.Manager):
    def create_event(self, ticker, price, name='', source='echo'):
        try:
            company_obj = Company.objects.get(ticker__iexact=ticker)
        except Company.DoesNotExist:
            # log issue
            company_obj = None
        except:
            company_obj = None
        obj = self.model(ticker=ticker, price=price, name=name, source=source)
        obj.company = company_obj
        obj.save()
        return obj

class PriceLookupEvent(models.Model):
    company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)
    ticker = models.CharField(max_length=20)
    name = models.CharField(max_length=220, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=50, choices=STOCK_MARKET_LOOKUP_SOURCES, default='echo')
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = PriceLookupEventManager()




# def price_event_post_save(sender, instance, created, *args, **kwargs):
#     if created:
#         if not instance.company:
#             try:
#                 company_obj = Company.objects.get(ticker__iexact=instance.ticker)
#             except Company.DoesNotExist:
#                 # log issue
#                 company_obj = None
#             except:
#                 company_obj = None
#             instance.company = company_obj
#             instance.save()
#     return

# post_save.connect(price_event_post_save, sender=PriceLookupEvent)
