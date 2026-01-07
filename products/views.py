from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy

from .models import Product, Category


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff  # staff = admin
    def handle_no_permission(self):
        from django.shortcuts import redirect
        from django.contrib import messages
        messages.error(self.request, "Sizda ruxsat yo‘q")
        return redirect('index')


class ProductListView(ListView):
    model = Product
    template_name = 'product-list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Product
    template_name = 'product_add.html'
    # 'image' maydonini bu yerga qo'shdik
    fields = ['name', 'description', 'image', 'price', 'category', 'quantity', 'is_active']

    # urls.py dagi nomga qarang, agar u yerda 'product_list' bo'lsa shunday qoldiring
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        # Eng muhim joyi: Mahsulot egasini avtomatik biriktiramiz
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Product
    template_name = 'product_update.html'
    fields = ['name','image', 'description', 'price', 'category', 'quantity', 'is_active']
    success_url = reverse_lazy('product_list')

class ProductDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Product
    template_name = 'products_delete.html'
    success_url = reverse_lazy('product_list')


def index(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')

    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    return render(request, 'index.html', {
        'products': products,
        'categories': categories,
        'current_category': category_id
    })


def about(request):
    return render (request, 'about.html')

def contact(request):
    return render (request, 'contact.html')

