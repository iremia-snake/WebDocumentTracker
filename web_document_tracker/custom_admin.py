from django.contrib import admin

class CustomAdminSite(admin.AdminSite):
    # Дополнительные настройки могут быть добавлены здесь
    site_header = "Моя пользовательская админка"
    site_title = "Моя админка"
    # date_hierarchy = "pub_date"

custom_admin_site = CustomAdminSite()