import json
from django.db import models
from django.db.models.signals import post_save, pre_save

from django_celery_beat.models import (
    CrontabSchedule, # IntervalSchedule
    PeriodicTask,
    PeriodicTasks,
)

from .tasks import perform_scrape, company_granular_price_scrape_task

STOCK_MARKET_LOOKUP_SOURCES = (
    ('business_insider', 'Business Insider Markets'),
    ('google_finance', 'Google Finance'),
    ('echo', 'Http Bin Echo'),    
)

class Company(models.Model):
    periodic_task = models.ForeignKey(PeriodicTask, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=220)
    ticker = models.CharField(max_length=20)
    description = models.TextField(blank=True,null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    scraping_scheduler_enabled = models.BooleanField(default=False)
    has_granular_scraping = models.BooleanField(default=False)
    one_off_scrape = models.BooleanField(default=False)
    # default_service
    # events per minute

    def scrape(self, service='business_insider'):
        return company_granular_price_scrape_task.delay(self.id, service='business_insider')

    def enable_periodic_task(self, save=True):
        instance_id = self.id
        ticker = self.ticker
        task_name = f'company-{ticker}-{instance_id}'.lower()
        if not self.periodic_task:
            schedule = CrontabSchedule.objects.get(id=3)
            obj, _ = PeriodicTask.objects.get_or_create(
                crontab=schedule,
                kwargs=json.dumps({
                    'instance_id': instance_id,
                    'service': 'business_insider'
                }),
                name=task_name,
                task='stocks.tasks.company_granular_price_scrape_task'
            )
            obj.enabled=True
            obj.save()
            PeriodicTasks.update_changed()
            self.periodic_task = obj
            if save:
                self.save()
        return self.periodic_task


    def disable_periodic_task(self, save=True):
        if self.periodic_task:
            obj = self.periodic_task
            obj.delete()
            PeriodicTasks.update_changed()
            self.periodic_task = None
            if save:
                self.save()
        return self.periodic_task
    
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
        if instance.scraping_scheduler_enabled and not instance.periodic_task:
            '''
            No periodic task and we just enabled it.
            '''
            instance.enable_periodic_task(save=False)
        if instance.scraping_scheduler_enabled == False and instance.periodic_task:
            '''
            Remove periodic task and we just enabled it.
            '''
            instance.disable_periodic_task(save=False)

pre_save.connect(company_pre_save, sender=Company)


def company_post_save(sender, instance, created, *args, **kwargs):
    if created:
        if instance.scraping_scheduler_enabled and not instance.periodic_task:
            '''
            No periodic task and we just enabled it.
            '''
            instance.enable_periodic_task(save=True)

post_save.connect(company_post_save, sender=Company)


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
