from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth import views as auth_views

from .models import Profile, Cart, CartItem
from .forms import UserUpdateForm, ProfileUpdateForm
from products.models import Product


# --- PROFIL BILAN ISHLASH ---
class ProfileView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)

        profile, created = Profile.objects.get_or_create(user=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

        password_form = PasswordChangeForm(user=request.user)

        # 🔥 ADMIN / USER QO‘SHGAN MAHSULOTLAR
        products = Product.objects.filter(owner=request.user)

        return render(request, 'users/profile.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'password_form': password_form,
            'products': products,   # 👈 context
        })

    def post(self, request):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if 'update_profile' in request.POST:
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, "Profil muvaffaqiyatli yangilandi!")
                return redirect('profile')
            else:
                messages.error(request, "Xatolik! Ma’lumotlarni tekshiring.")

        elif 'update_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Parol muvaffaqiyatli o‘zgartirildi!")
                return redirect('profile')
            else:
                messages.error(request, "Parol xato yoki mos emas.")

        products = Product.objects.filter(owner=request.user)

        return render(request, 'users/profile.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'password_form': password_form,
            'products': products,
        })


# --- AVTORIZATSIYA ---
class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        form = UserCreationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Foydalanuvchi uchun avtomatik profil va savatcha yaratish
            Profile.objects.get_or_create(user=user)
            Cart.objects.get_or_create(user=user)

            messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz. Tizimga kiring.")
            return redirect('login')
        return render(request, 'users/register.html', {'form': form})


class LoginView(auth_views.LoginView):
    template_name = 'users/login.html'


class LogoutView(auth_views.LogoutView):
    next_page = 'index'


# --- SAVATCHA (CART) BILAN ISHLASH ---
class CartDetailView(LoginRequiredMixin, View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        return render(request, 'users/cart.html', {'cart': cart})


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
            messages.info(request, f"{product.name} miqdori oshirildi.")
        else:
            messages.success(request, f"{product.name} savatchaga qo'shildi.")

        return redirect('cart')


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        product_name = cart_item.product.name
        cart_item.delete()
        messages.warning(request, f"{product_name} savatchadan olib tashlandi.")
        return redirect('cart')


class UpdateCartQuantityView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        action = request.POST.get('action')

        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                cart_item.delete()
                return redirect('cart')

        cart_item.save()
        return redirect('cart')