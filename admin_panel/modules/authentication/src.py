from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

class Login(View):
    error_message = ''
    template = 'adminpanel/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('admin_index')
        return render(request, self.template, {'error_message': self.error_message})
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'admin_index'
            return redirect(next_url)
        else:
            self.error_message = 'Invalid Credentials!'
            return render(request, self.template, {'error_message': self.error_message})