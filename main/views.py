from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction

from .models import Wallet, Transaction
from users.models import Cart  


class WalletDetailView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        transactions = wallet.transactions.all().order_by('-created_at')
        return render(request, 'wallet/detail.html', {
            'wallet': wallet,
            'transactions': transactions
        })


class WalletTopUpView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request):
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        amount = request.POST.get('amount')

        try:
            amount = float(amount)
            if amount <= 0:
                messages.error(request, "Miqdor 0 dan katta bo‘lishi kerak")
                return redirect('wallet_detail')
        except:
            messages.error(request, "Miqdor xato kiritildi")
            return redirect('wallet_detail')

        Transaction.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type='topup',
            is_approved=False 
        )

        messages.success(request, f"{amount} so‘m top-up yaratildi. Admin tasdiqlaydi")
        return redirect('wallet_detail')


class WalletCheckoutView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            if cart.items.count() == 0:
                messages.error(request, "Savatchangiz bo'sh")
                return redirect('cart')
        except Cart.DoesNotExist:
            return redirect('cart')
        return render(request, 'wallet/checkout_address.html', {'cart': cart})

    def post(self, request):
        # 1. HTML formadan 'address' nomli ma'lumotni olamiz
        address = request.POST.get('address')
        print(address)
        wallet, _ = Wallet.objects.get_or_create(user=request.user)

        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return redirect('cart')

        total_price = cart.get_total_price()

        # 2. Tekshiruvlar
        if wallet.balance < total_price:
            messages.error(request, f"Mablag' yetarli emas! Sizga yana {total_price - wallet.balance} so'm kerak.")
            return redirect('wallet_detail')

        if not address:
            messages.error(request, "Manzilni kiritish shart!")
            return redirect('wallet_checkout')

        # 3. Tranzaksiyani yaratish va manzilni saqlash
        try:
            with transaction.atomic():
                new_transaction = Transaction.objects.create(
                    wallet=wallet,
                    amount=total_price,  # Summani saqlash
                    transaction_type='purchase',
                    address=address,  # MANZIL SHU YERDA SAQLANADI
                    is_approved=False
                )

                # Mahsulotlar ro'yxatini JSON qilib saqlash
                if hasattr(new_transaction, 'set_items'):
                    new_transaction.set_items(cart.items.all())

                new_transaction.save()

                # Savatchani tozalash
                cart.items.all().delete()

            messages.success(request, "Buyurtma qabul qilindi. Admin tasdiqlagach, pul yechiladi.")
            return redirect('wallet_detail')

        except Exception as e:
            messages.error(request, f"Xatolik yuz berdi: {str(e)}")
            return redirect('cart')

from django.shortcuts import get_object_or_404


class TransactionCancelView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Faqat shu foydalanuvchiga tegishli va hali tasdiqlanmagan tranzaksiyani topamiz
        transaction = get_object_or_404(Transaction, pk=pk, wallet__user=request.user, is_approved=False)

        # Tranzaksiyani o'chiramiz
        transaction.delete()

        messages.success(request, "Buyurtma muvaffaqiyatli bekor qilindi.")
        return redirect('wallet_detail')