from django import forms

from authapp.forms import ShopUserEditForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from ordersapp.models import Order


class ShopUserAdminEditForm(ShopUserEditForm):

    class Meta:
        model = ShopUser
        fields = '__all__'


class ProductCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Product
        fields = '__all__'


class OrderUpdateStatusForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Order
        fields = ('status',)
