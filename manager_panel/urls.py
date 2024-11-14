from django.urls import path
from .modules import *

urlpatterns = [
    path('', ManagerIndexView.as_view(), name='manager_index'),
    path('orders/', OrderList.as_view(), name='order_list'),
    path('orders/<int:id>', OrderDetails.as_view(), name='order_details'),
    path('orders/<int:id>/create', OrderHandling.as_view(), name='order_handling')
]