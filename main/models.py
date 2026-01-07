from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import json

# 1. Hamyon modeli
class Wallet(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='wallet'
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} | Balans: {self.balance} so'm"

    def deposit(self, amount):
        """Hamyonga pul qo'shish"""
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        """Hamyondan pul yechish"""
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('topup', 'Hisobni to\'ldirish'),
        ('purchase', 'Xarid'),
        ('refund', 'Pulni qaytarish'),
    )
    address = models.TextField(blank=True, null=True, max_length=255)
    items_json = models.TextField(blank=True, null=True, max_length=255)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # 1. Agar bu tahrirlanayotgan (eskidan bor) tranzaksiya bo'lsa
        if self.pk:
            # Bazadagi eski holatini tekshiramiz
            old_obj = Transaction.objects.get(pk=self.pk)

            # Agar oldin tasdiqlanmagan bo'lsa va HOZIR admin ✅ qilib saqlayotgan bo'lsa
            if not old_obj.is_approved and self.is_approved:
                wallet = self.wallet
                if self.transaction_type == 'topup':
                    wallet.balance += self.amount
                elif self.transaction_type == 'purchase':
                    wallet.balance -= self.amount
                elif self.transaction_type == 'refund':
                    wallet.balance += self.amount

                # Walletni albatta saqlash kerak!
                wallet.save()

        # 2. Asosiy tranzaksiyani saqlash
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.wallet.user.username} | {self.amount}"