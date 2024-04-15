from django.contrib import admin
from web_document_tracker.models import *


# Register your models here.
admin.site.register(Profile)

admin.site.register(Agent)
admin.site.register(AgentData)

admin.site.register(Contract)
admin.site.register(ContractType)

admin.site.register(Document)
admin.site.register(DocumentType)

admin.site.register(CompanyType)
admin.site.register(ExtraData)

admin.site.register(TradingPlatform)

admin.site.site_header = "Моя пользовательская админка"
admin.site.site_title = "Моя админка"
