from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import logout

class ManagerIndexView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='Менеджер').exists()

    def get(self, request, *args, **kwargs):
        if 'quit' in request.GET:
            logout(request)
            return redirect('/configuration/login')
        
        return render(request, 'managerpanel/index.html')