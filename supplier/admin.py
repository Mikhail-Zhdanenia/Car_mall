from django.contrib import admin
from supplier.models import (
    Supplier, SupplierGarage, SupplierPromo, SupplierStatistic
)


# Tuple of current application models
models = (SupplierPromo, SupplierStatistic)

# Registration of models
for m in models:
    admin.site.register(m)


@admin.register(Supplier)
class SupplierGarageAdmin(admin.ModelAdmin):

    list_display = ('user', 'name', 'year_of_foundation', 'car_count')


@admin.register(SupplierGarage)
class SupplierGAdmin(admin.ModelAdmin):

    list_display = ('car', 'supplier', 'price')