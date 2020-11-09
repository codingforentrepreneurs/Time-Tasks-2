from django.contrib import admin

from .models import Company, PriceLookupEvent

admin.site.register(PriceLookupEvent)

class PriceLookupEventAdmin(admin.TabularInline):
    model = PriceLookupEvent
    extra = 0

class CompanyAdmin(admin.ModelAdmin):
    # inlines = [PriceLookupEventAdmin]
    readonly_fields = ['periodic_task']
    class Meta:
        model = Company

admin.site.register(Company, CompanyAdmin)