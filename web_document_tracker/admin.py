from django.contrib import admin
from web_document_tracker.models import *
from django.http import HttpResponse
from django.shortcuts import render

admin.site.register(Profile)
admin.site.register(Agent)
admin.site.register(AgentData)
admin.site.register(ContractType)
admin.site.register(Document)
admin.site.register(DocumentType)
admin.site.register(CompanyType)
admin.site.register(ExtraData)
admin.site.register(TradingPlatform)

admin.site.site_header = "Моя пользовательская админка"
admin.site.site_title = "Моя админка"

@admin.register(Contract)
class ExtraDataAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    search_fields = ['extra_data_model__registration_number']
    list_filter  = ['type__name', 'trading_platform__name']
