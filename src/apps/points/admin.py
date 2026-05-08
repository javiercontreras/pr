from django.contrib import admin
from .models import WasteCategory, WasteSubcategory, RecyclingPoint, Container

admin.site.register(WasteCategory)
admin.site.register(WasteSubcategory)
admin.site.register(RecyclingPoint)
admin.site.register(Container)