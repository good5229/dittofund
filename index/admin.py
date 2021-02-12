from django.contrib import admin

from .models import HedgeFund, Portfolio, Data

# Register your models here.

admin.site.register(HedgeFund)
admin.site.register(Portfolio)
admin.site.register(Data)
