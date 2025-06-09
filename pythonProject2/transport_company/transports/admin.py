from django.contrib import admin
from .models import Driver, Trailer, Order


class DriverAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'passport_number', 'experience', 'driver_class', 'partner')
    list_filter = ('driver_class',)
    search_fields = ('full_name', 'passport_number')


class TrailerAdmin(admin.ModelAdmin):
    list_display = ('brand', 'license_plate', 'load_capacity', 'driver')
    list_filter = ('brand', 'company')
    search_fields = ('brand', 'license_plate')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'departure_point', 'destination_point', 'distance', 'weight', 'trailer', 'driver')
    list_filter = ('departure_point', 'destination_point', 'completed')
    search_fields = ('name', 'departure_point', 'destination_point')
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('name', 'weight', 'items_count')
        }),
        ('Маршрут', {
            'fields': ('departure_point', 'destination_point', 'distance')
        }),
        ('Исполнители', {
            'fields': ('trailer', 'driver')
        }),
        ('Статус', {
            'fields': ('completed', 'created_at')
        }),
    )


admin.site.register(Driver, DriverAdmin)
admin.site.register(Trailer, TrailerAdmin)
admin.site.register(Order, OrderAdmin)