from django.urls import path
from .views import RegisterView, LoginView, LogoutView, PhotoAlbumView, PhotoUploadView, PhotoDeleteView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', PhotoAlbumView.as_view(), name='photo_album'),
    path('upload/', PhotoUploadView.as_view(), name='photo_upload'),
    path('delete/<int:pk>/', PhotoDeleteView.as_view(), name='photo_delete'),
]