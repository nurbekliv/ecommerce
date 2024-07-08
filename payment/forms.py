from django import forms
from .models import ShippingAddress


class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label='',
                                         widget=forms.TextInput(
                                             attrs={'class': 'form-control', 'placeholder': 'full name'}),
                                         required=True)
    shipping_email = forms.CharField(label='',
                                     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email'}),
                                     required=True)
    shipping_address1 = forms.CharField(label='',
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', 'placeholder': 'address1'}),
                                        required=True)
    shipping_address2 = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'address2'}),
                                        required=False)
    shipping_city = forms.CharField(label='',
                                    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'city'}),
                                    required=True)
    shipping_state = forms.CharField(label='',
                                     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'state'}),
                                     required=True)
    shipping_zipcode = forms.CharField(label='',
                                       widget=forms.TextInput(
                                           attrs={'class': 'form-control', 'placeholder': 'zipcode'}),
                                       required=True)
    shipping_country = forms.CharField(label='',
                                       widget=forms.TextInput(
                                           attrs={'class': 'form-control', 'placeholder': 'country'}),
                                       required=True)

    class Meta:
        model = ShippingAddress
        fields = '__all__'
        exclude = ['user']


class PaymentForm(forms.Form):
    card_name = forms.CharField(label='',
                                         widget=forms.TextInput(
                                             attrs={'class': 'form-control', 'placeholder': 'name on card'}),
                                         required=True)
    card_number = forms.CharField(label='',
                                     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'card number'}),
                                     required=True)
    card_exp_date = forms.CharField(label='',
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', 'placeholder': 'expiration date'}),
                                        required=True)
    card_cvv_number = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'cvv code'}),
                                        required=False)
    card_address1 = forms.CharField(label='',
                                    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'billing address1'}),
                                    required=True)
    card_address2 = forms.CharField(label='',
                                     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'billing address2'}),
                                     required=True)
    card_city = forms.CharField(label='',
                                       widget=forms.TextInput(
                                           attrs={'class': 'form-control', 'placeholder': 'billing city'}),
                                       required=True)
    card_state = forms.CharField(label='',
                                       widget=forms.TextInput(
                                           attrs={'class': 'form-control', 'placeholder': 'billing state'}),
                                       required=True)
    card_zipcode = forms.CharField(label='',
                                       widget=forms.TextInput(
                                           attrs={'class': 'form-control', 'placeholder': 'billing zipcode'}),
                                       required=True)
    card_country = forms.CharField(label='',
                                       widget=forms.TextInput(
                                           attrs={'class': 'form-control', 'placeholder': 'billing country'}),
                                       required=True)
