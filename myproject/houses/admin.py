from django.contrib import admin
from .models import HouseList, SoldHouse, LoanAmount
# Register your models here.

class HouseListAdmin(admin.ModelAdmin):

    list_display = ["id", "location_city", "developer", "price"]

class SoldHouseAdmin(admin.ModelAdmin):

    list_display = ["id_of_house", "financing_option", "downpayment_amount", "broker_name", "commission_percent"]

class LoanAmountAdmin(admin.ModelAdmin):

    list_display = ["id_of_house", "original_amount", "current_amount"]






admin.site.register(HouseList, HouseListAdmin)
admin.site.register(SoldHouse, SoldHouseAdmin)
admin.site.register(LoanAmount, LoanAmountAdmin)
