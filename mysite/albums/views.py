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

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DeleteView
from .models import Photo
from django.urls import reverse_lazy

@method_decorator(login_required, name='dispatch')
class PhotoAlbumView(ListView):
    model = Photo
    template_name = 'albums/photo_album.html'
    context_object_name = 'photos'

    def get_queryset(self):
        return Photo.objects.filter(user=self.request.user)

from django.core.exceptions import ValidationError

@method_decorator(login_required, name='dispatch')
class PhotoUploadView(CreateView):
    model = Photo
    fields = ['image', 'title', 'description']
    template_name = 'albums/photo_upload.html'
    success_url = reverse_lazy('photo_album')

    def form_valid(self, form):
        if Photo.objects.filter(user=self.request.user).count() >= 30:
            form.add_error(None, "You can't upload more than 30 photos.")
            return self.form_invalid(form)
        form.instance.user = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class PhotoDeleteView(DeleteView):
    model = Photo
    template_name = 'albums/photo_confirm_delete.html'
    success_url = reverse_lazy('photo_album')

    def get_queryset(self):
        return Photo.objects.filter(user=self.request.user)