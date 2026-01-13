from django.contrib import admin
from .models import Wallet, Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['wallet', 'transaction_type', 'amount', 'is_approved', 'created_at']
    fields = ['wallet', 'transaction_type', 'amount', 'address', 'is_approved']

    def approve_transactions(self, request, queryset):
        unapproved = queryset.filter(is_approved=False)
        for transaction in unapproved:
            transaction.is_approved = True
            # Faqat save() ni chaqiramiz.
            # models.py dagi biz yozgan save() mantiqi qolganini o'zi bajaradi (pul qo'shadi).
            transaction.save()

        count = unapproved.count()
        self.message_user(request, f"{count} ta tranzaksiya muvaffaqiyatli tasdiqlandi.")

    approve_transactions.short_description = "Tanlangan tranzaksiyalarni tasdiqlash"


admin.site.register(Wallet)
