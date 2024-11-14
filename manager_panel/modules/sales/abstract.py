from abc import ABC, abstractmethod

from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http.request import HttpRequest
from django.http.response import HttpResponse

class OrderHandle:
    @abstractmethod
    def test_manager(request: HttpRequest) -> True | False:
        pass

    class BaseOrderView(ABC, View, UserPassesTestMixin):
        @abstractmethod
        def test_func(self) -> bool | None:
            pass

    @classmethod
    class OrderList(BaseOrderView):
        def get(self, request: HttpRequest) -> HttpResponse:
            pass
    
    @classmethod
    class NewOrderDetails(BaseOrderView):
        def get(self, request: HttpRequest, id: int) -> HttpResponse:
            pass

        def post(self, request: HttpRequest, id: int) -> HttpResponse:
            pass