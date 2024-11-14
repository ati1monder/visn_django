from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.shortcuts import render
from admin_panel.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class Users(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request):
        users = User.objects.all().order_by('pk')
        paginator = Paginator(users, 10)

        page_number = request.GET.get('page')
        try:
            users = paginator.page(page_number)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        
        context = {'users': users}
        return render(request, 'adminpanel/users.html', context)
    
    def post(self, request):
        filtered_users = []

        context = {'users': filtered_users}
        return render(request, 'adminpanel/users.html', context)

class User_Details(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff
    
    def get(self, request, id):
        user = User.objects.get(pk=id)
        # for the future
        # user.groups.filter(name='Менеджер').exists())
        
        context = {'user': user}
        return render(request, 'adminpanel/user_details.html', context)