from django.contrib import admin
from .models import Merchant, Dish, UserPreference, Order, OrderItem, FootTraffic

@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'hall', 'location', 'status', 'created_at']
    list_filter = ['hall', 'status']
    search_fields = ['name', 'hall']

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'merchant', 'price', 'category', 'is_available']
    list_filter = ['category', 'taste', 'is_available']
    search_fields = ['name', 'merchant__name']

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'price_range_min', 'price_range_max', 'updated_at']
    search_fields = ['user__username']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'merchant', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'merchant__name']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'dish', 'quantity', 'unit_price']
    search_fields = ['order__id', 'dish__name']

@admin.register(FootTraffic)
class FootTrafficAdmin(admin.ModelAdmin):
    list_display = ['merchant', 'record_date', 'time_slot', 'traffic_count']
    list_filter = ['time_slot', 'record_date']