# Create your views here.
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm

class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'albums/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('photo_album')
        return render(request, 'albums/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'albums/login.html', {'form': form})

    def post(self, request):
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('photo_album')
        return render(request, 'albums/login.html', {'form': form})

class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('login')

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Folder, Photo
from .forms import FolderForm, PhotoForm

class PhotoAlbumView(LoginRequiredMixin, View):
    def get(self, request):
        root_folders = Folder.objects.filter(user=request.user, parent_folder__isnull=True)
        root_photos = Photo.objects.filter(user=request.user, folder__isnull=True)  # Фотографии в корне
        return render(request, 'albums/photo_album.html', {'folders': root_folders, 'root_photos': root_photos})


class FolderDetailView(LoginRequiredMixin, View):
    def get(self, request, folder_id):
        folder = get_object_or_404(Folder, id=folder_id, user=request.user)
        subfolders = folder.subfolders.all()
        photos = folder.photos.all()
        return render(request, 'albums/folder_detail.html', {'folder': folder, 'subfolders': subfolders, 'photos': photos})

class FolderCreateView(LoginRequiredMixin, View):
    def get(self, request, parent_folder_id=None):
        form = FolderForm()
        return render(request, 'albums/folder_form.html', {'form': form, 'parent_folder_id': parent_folder_id})

    def post(self, request, parent_folder_id=None):
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user
            if parent_folder_id:
                folder.parent_folder = get_object_or_404(Folder, id=parent_folder_id, user=request.user)
            folder.save()
            return redirect('folder_detail', folder_id=parent_folder_id) if parent_folder_id else redirect('photo_album')
        return render(request, 'albums/folder_form.html', {'form': form})

class FolderRenameView(LoginRequiredMixin, View):
    def get(self, request, pk):
        folder = get_object_or_404(Folder, id=pk, user=request.user)
        form = FolderForm(instance=folder)
        return render(request, 'albums/folder_form.html', {'form': form, 'edit_mode': True})

    def post(self, request, pk):
        folder = get_object_or_404(Folder, id=pk, user=request.user)
        form = FolderForm(request.POST, instance=folder)
        if form.is_valid():
            form.save()
            return redirect('folder_detail', folder_id=folder.parent_folder.id) if folder.parent_folder else redirect('photo_album')
        return render(request, 'albums/folder_form.html', {'form': form, 'edit_mode': True})

class FolderDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        folder = get_object_or_404(Folder, id=pk, user=request.user)
        parent_folder_id = folder.parent_folder.id if folder.parent_folder else None
        folder.delete()
        return redirect('folder_detail', folder_id=parent_folder_id) if parent_folder_id else redirect('photo_album')

class PhotoUploadView(LoginRequiredMixin, View):
    def get(self, request, folder_id=None):
        form = PhotoForm()
        return render(request, 'albums/photo_upload.html', {'form': form, 'folder_id': folder_id})

    def post(self, request, folder_id=None):
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            if folder_id:
                photo.folder = get_object_or_404(Folder, id=folder_id, user=request.user)
            photo.save()
            return redirect('folder_detail', folder_id=folder_id) if folder_id else redirect('photo_album')
        return render(request, 'albums/photo_upload.html', {'form': form})
class PhotoDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        photo = get_object_or_404(Photo, id=pk, user=request.user)
        photo.delete()
        return redirect('photo_album')