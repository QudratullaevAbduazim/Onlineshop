from django.urls import path
from .views import DeleteCommentView, AddCommentView

urlpatterns = [
    path('create/<int:product_id>/', AddCommentView.as_view(), name='create_comment'),
    path('delete/<int:comment_id>/', DeleteCommentView.as_view(), name='delete_comment'),
]
