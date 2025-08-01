from django import forms
from .models import Customer
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm


class PasswordChangeForm(DjangoPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-700 bg-gray-800 text-white rounded-lg',
                'placeholder': field.label
            })


class ProfileForm(forms.Form):
    first_name = forms.CharField(
        label="First Name",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-700 bg-gray-800 text-white rounded-lg',
            'placeholder': 'First Name'
        })
    )

    last_name = forms.CharField(
        label="Last Name",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-700 bg-gray-800 text-white rounded-lg',
            'placeholder': 'Last Name'
        })
    )

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-700 bg-gray-800 text-white rounded-lg',
            'placeholder': 'Email Address'
        })
    )

    phone = forms.CharField(
        label="Phone",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-700 bg-gray-800 text-white rounded-lg',
            'placeholder': 'Phone Number'
        })
    )

    address = forms.CharField(
        label="Address",
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 border border-gray-700 bg-gray-800 text-white rounded-lg',
            'rows': 3,
            'placeholder': 'Physical Address'
        })
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].initial = self.user.first_name
        self.fields['last_name'].initial = self.user.last_name
        self.fields['email'].initial = self.user.email
        self.fields['phone'].initial = self.user.customer.phone
        self.fields['address'].initial = self.user.customer.address

    def save(self):
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        self.user.email = self.cleaned_data['email']
        self.user.save()

        customer = self.user.customer
        customer.phone = self.cleaned_data['phone']
        customer.address = self.cleaned_data['address']
        customer.save()