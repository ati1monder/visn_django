from sales_management.models import Order, TakenOrder, OrderFiles
from .forms import NewOrderForm
from .abstract import OrderHandle

from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.conf import settings
from django.http.request import HttpRequest

def test_manager(request: HttpRequest) -> True | False:
    return request.user.groups.filter(name='Менеджер').exists()

class OrderList(View, UserPassesTestMixin):
    def test_func(self):
        return test_manager(self.request)
    
    def get(self, request):
        orders = Order.objects.exclude(id__in=TakenOrder.objects.values_list('order_id', flat=True))
        wip_orders = get_list_or_404(TakenOrder)
        manager_orders = get_list_or_404(TakenOrder, manager=request.user)

        context = {
            'orders': orders,
            'wip_orders': wip_orders,
            'manager_orders': manager_orders
        }
        return render(request, 'managerpanel/order_list.html', context)
    
class OrderDetails(View, UserPassesTestMixin):
    def test_func(self):
        return test_manager(self.request)
    
    def get(self, request, id):
        order = get_object_or_404(Order, pk=id)
        files = get_list_or_404(OrderFiles, order_model=order)
        context = {
            'order': order,
            'files': files,
            'file_root': settings.MEDIA_URL
        }
        return render(request, 'managerpanel/order_details.html', context)
    
class OrderHandling(View, UserPassesTestMixin):
    def test_func(self):
        return test_manager(self.request)
    
    def get(self, request, id):
        order = Order.objects.get(pk=id)
        form = NewOrderForm(user=request.user, order=order)
        context = {
            'form': form,
            'order': order
        }
        return render(request, 'managerpanel/handle_order.html', context)
    
    def post(self, request, id):
        order = Order.objects.get(pk=id)
        form = NewOrderForm(request.POST, user=request.user, order=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
        return render(request, 'managerpanel/handle_order.html', {'form': form})
    
class TakenOrderHandling(View, UserPassesTestMixin):
    def test_func(self):
        return test_manager(self.request)
    
    def get(self, request, id):
        pass