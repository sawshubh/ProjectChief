from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


TENANT_APP_MAP = {
    'cinex360': 'cinex360',
    'portfolio': 'portfolio',
    'siddhitaarts': 'siddhitaarts',
    'public': None,
}


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_on = models.DateField(auto_now_add=True)
    auto_create_schema = True

    def get_tenant_apps(self):
        app = TENANT_APP_MAP.get(self.schema_name)
        return [app] if app else []

    def __str__(self):
        return self.name


class Domain(DomainMixin):
    pass
