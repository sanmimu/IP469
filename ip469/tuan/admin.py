# -*-coding:utf-8-*-

from django.contrib import admin
from models import Deal, Site, Category, City, SiteCity

class DealAdmin(admin.ModelAdmin):
    pass


admin.site.register(Deal, DealAdmin)
admin.site.register(Site)
admin.site.register(Category)
admin.site.register(City)
admin.site.register(SiteCity)

