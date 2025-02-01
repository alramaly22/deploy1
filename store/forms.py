from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,  UserChangeForm , SetPasswordForm
from django import forms
from .models import Profile


class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'info-field', 'placeholder':'Phone'}), required=False)
    address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'info-field', 'placeholder':'Address 1'}), required=False)
    address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'info-field', 'placeholder':'Address 2'}), required=False)
    city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'info-field', 'placeholder':'City'}), required=False)
    state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'info-field', 'placeholder':'State'}), required=False)
    zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'info-field', 'placeholder':'Zipcode'}), required=False)
    country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'info-field', 'placeholder':'Country'}), required=False)
    full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'info-field', 'placeholder':'Full Name'}), required=False)
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'info-field', 'placeholder':'Email'}), required=False)

    class Meta:
        model = Profile
        fields = ('full_name', 'phone', 'email', 'address1', 'address2', 'city', 'state', 'zipcode', 'country', )
class ChangePasswordForm(SetPasswordForm):
	class Meta:
		model = User
		fields = ['new_password1', 'new_password2']

	def __init__(self, *args, **kwargs):
		super(ChangePasswordForm, self).__init__(*args, **kwargs)

		self.fields['new_password1'].widget.attrs['class'] = 'info-field'
		self.fields['new_password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['new_password1'].label = ''
		self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li style="color:white;">Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['new_password2'].widget.attrs['class'] = 'info-field'
		self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['new_password2'].label = ''
		self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

class UpdateUserForm(UserChangeForm):
	# Hide Password stuff
	# password = None
	# Get other fields
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'info-field', 'placeholder':'Email Address'}), required=False)
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'info-field', 'placeholder':'First Name'}), required=False)
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'info-field', 'placeholder':'Last Name'}), required=False)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')

	def __init__(self, *args, **kwargs):
		super(UpdateUserForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'info-field'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'info-field', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'info-field', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'info-field', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'info-field'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = ''  # إزالة النص المساعد

        self.fields['password1'].widget.attrs['class'] = 'info-field'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<span class="form-text text-muted small">Minimum 6 characters.</span>'

        self.fields['password2'].widget.attrs['class'] = 'info-field'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = ''