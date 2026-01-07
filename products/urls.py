from django.urls import path
from .views import (
    ProductListView, ProductDetailView, 
    ProductCreateView, ProductUpdateView, ProductDeleteView, index, about, contact
)

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('product-list/', ProductListView.as_view(), name='product_list'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),

    # Admin sahifalar
    path('add/', ProductCreateView.as_view(), name='product_add'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
]
