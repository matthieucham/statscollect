from django.contrib import admin
from statscollect_scrap import models

# Register your models here.
admin.site.register(models.FootballScrapper)
admin.site.register(models.ScrappedFootballStep)