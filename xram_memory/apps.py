from django.contrib.admin.apps import AdminConfig


class DefaultAdminConfig(AdminConfig):
    default_site = 'xram_memory.admin.DefaultAdminSite'
