from django.urls import path

from .views import Home, PostDetail, CreatePost, EditPost, DeletePost, CreateCategory, CategoryView


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('post/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('add_post/', CreatePost.as_view(), name='add_post'),
    path('edit_post/<int:pk>', EditPost.as_view(), name='edit_post'),
    path('delete_post/<int:pk>', DeletePost.as_view(), name='delete_post'),
    path('add_category/', CreateCategory.as_view(), name='add_category'),
    path('category/<int:pk>/', CategoryView, name='category' )
]
