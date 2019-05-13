from django import forms
from authapp.models import ShopUser
from authapp.forms import ShopUserEditForm
from mainapp.models import Category, Product
from django.shortcuts import get_object_or_404


class ShopUserAdminEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'


class CategoryEditForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        exclude = ('nesting_level',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def save(self, commit=True):
        if self.instance.parent:
            if self.instance.parent == self.instance:
                self.instance.parent = None
                self.instance.nesting_level = 0
            else:
                parent_nesting_level = get_object_or_404(Category, name=self.instance.parent).nesting_level
                self.instance.nesting_level = parent_nesting_level + 1

        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate." % (
                    self.instance._meta.object_name,
                    'created' if self.instance._state.adding else 'changed',
                )
            )
        if commit:
            # If committing, save the instance and the m2m data immediately.
            self.instance.save()
            self._save_m2m()
        else:
            # If not committing, add a method to the form to allow deferred
            # saving of m2m data.
            save_m2m = self._save_m2m
        return self.instance


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
