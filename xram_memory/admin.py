from django.contrib import admin


class DefaultAdminSite(admin.AdminSite):
    site_header = "Área administrativa"
    site_title = "Xram-Memory"
    index_title = "Área administrativa"
