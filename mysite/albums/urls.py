from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, PhotoAlbumView,
    PhotoUploadView, PhotoDeleteView, FolderCreateView,
    FolderRenameView, FolderDeleteView, FolderDetailView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', PhotoAlbumView.as_view(), name='photo_album'),
    path('folder/<int:folder_id>/', FolderDetailView.as_view(), name='folder_detail'),
    path('upload/', PhotoUploadView.as_view(), name='photo_upload'),
    path('upload/<int:folder_id>/', PhotoUploadView.as_view(), name='photo_upload_in_folder'),
    path('delete/photo/<int:pk>/', PhotoDeleteView.as_view(), name='photo_delete'),
    path('folder/create/', FolderCreateView.as_view(), name='folder_create'),
    path('folder/create/<int:parent_folder_id>/', FolderCreateView.as_view(), name='folder_create_in_folder'),
    path('folder/rename/<int:pk>/', FolderRenameView.as_view(), name='folder_rename'),
    path('folder/delete/<int:pk>/', FolderDeleteView.as_view(), name='folder_delete'),
]
