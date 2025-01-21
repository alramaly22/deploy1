from django import forms
from .models import ShippingAddress


  
class PaymentForm(forms.Form):
	card_name =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'info-field', 'placeholder':'Name On Card'}), required=True)
	card_number =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'info-field', 'placeholder':'Card Number'}), required=True)
	card_exp_date =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'info-field', 'placeholder':'Expiration Date'}), required=True)
	card_cvv_number =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'info-field', 'placeholder':'CVV Code'}), required=True)
	card_address1 =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'info-field', 'placeholder':'Billing Address 1'}), required=True)
	card_address2 =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'info-field', 'placeholder':'Billing Address 2'}), required=False)
	card_city =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'info-field', 'placeholder':'Billing City'}), required=True)
	card_state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'info-field', 'placeholder':'Billing State'}), required=True)
	card_zipcode =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'info-field', 'placeholder':'Billing Zipcode'}), required=True)
	card_country =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'info-field', 'placeholder':'Billing Country'}), required=True)