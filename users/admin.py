from django.contrib import admin
from .models import Profile, CartItem, Cart

# Savatcha ichidagi mahsulotlarni savatchaning o'zida ko'rsatish uchun (Inline)
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1 # Bo'sh qatorlar soni

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_total') # Savatcha egasi va umumiy summani ko'rsatadi
    inlines = [CartItemInline] # Savatcha ichida mahsulotlarni ko'rsatadi

    def get_total(self, obj):
        return f"{obj.get_total_price()} so'm"
    get_total.short_description = "Jami summa"

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'phone_number')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'total_price')
    list_filter = ('cart',)