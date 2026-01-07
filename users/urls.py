from django.urls import path
from .views import ProfileView, RegisterView, LoginView, LogoutView, CartDetailView, AddToCartView, RemoveFromCartView, \
    UpdateCartQuantityView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('cart/', CartDetailView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('cart/update/<int:item_id>/', UpdateCartQuantityView.as_view(), name='update_cart'),
]
