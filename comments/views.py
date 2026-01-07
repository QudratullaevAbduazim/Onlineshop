from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import Comment
from products.models import Product


class AddCommentView(LoginRequiredMixin, View):
    login_url = 'login'  # agar login bo‘lmasa

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        text = request.POST.get('text')

        if not text:
            messages.error(request, "Comment bo‘sh bo‘lishi mumkin emas")
            return redirect('product_detail', product_id=product.id)

        Comment.objects.create(
            product=product,
            user=request.user,
            text=text
        )

        messages.success(request, "Comment muvaffaqiyatli qo‘shildi")
        return redirect('product_detail', product_id=product.id)

class DeleteCommentView(LoginRequiredMixin, View):

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)

        if comment.user != request.user and not request.user.is_staff:
            messages.error(request, "Siz bu commentni o‘chira olmaysiz")
            return redirect('product_detail', product_id=comment.product.id)

        comment.delete()
        messages.success(request, "Comment o‘chirildi")

        return redirect('product_detail', product_id=comment.product.id)