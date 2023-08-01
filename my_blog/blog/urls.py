from django.urls import path

from .views import Home, PostDetail, CreatePost, EditPost, DeletePost, CreateCategory, CategoryView, CreateComment, EditComment, DeleteComment, EditProfile, ImportPost, CreateProfile


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('post/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('add_post/', CreatePost.as_view(), name='add_post'),
    path('edit_post/<int:pk>', EditPost.as_view(), name='edit_post'),
    path('delete_post/<int:pk>', DeletePost.as_view(), name='delete_post'),
    path('add_category/', CreateCategory.as_view(), name='add_category'),
    path('category/<int:pk>/', CategoryView, name='category' ),
    path('post/<int:pk>/add_comment/', CreateComment.as_view(), name='add_comment'),
    path('edit_comment/<int:pk>/', EditComment.as_view(), name='edit_comment'),
    path('delete_comment/<int:pk>/', DeleteComment.as_view(), name='delete_comment'),
    path('user/edit_profile/<int:pk>', EditProfile.as_view(), name='edit_profile'),
    path('user/create_profile', CreateProfile.as_view(), name='create_profile'),
    path('import_post/', ImportPost.as_view(), name='import_post')
]
