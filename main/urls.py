from django.urls import path
from .views import WalletDetailView, WalletTopUpView, WalletCheckoutView, TransactionCancelView

urlpatterns = [
    path('wallet/', WalletDetailView.as_view(), name='wallet_detail'),
    
    path('wallet/top-up/', WalletTopUpView.as_view(), name='wallet_topup'),
    
    path('wallet/checkout/', WalletCheckoutView.as_view(), name='wallet_checkout'),
    path('transaction/<int:pk>/cancel/', TransactionCancelView.as_view(), name='transaction_cancel'),
]