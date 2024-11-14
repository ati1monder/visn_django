from sales_management.models import TakenOrder

from django import forms

class NewOrderForm(forms.ModelForm):
    class Meta:
        model = TakenOrder
        fields = ['status', 'response']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        order = kwargs.pop('order')
        super().__init__(*args, **kwargs)
        
        self.instance.manager = user
        self.instance.order = order