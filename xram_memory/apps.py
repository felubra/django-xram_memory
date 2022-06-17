from django.contrib.admin.apps import AdminConfig
from filer.apps import FilerConfig as OriginalFilerConfig


class DefaultAdminConfig(AdminConfig):
    default_site = "xram_memory.admin.DefaultAdminSite"


class FilerConfig(OriginalFilerConfig):
    verbose_name = "Pastas e arquivos"
