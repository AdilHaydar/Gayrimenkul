from django import forms
from .models import User, UserUpdateModel
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm
     
class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','email','cep_telefonu')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email','full_name','is_telefonu','cep_telefonu',"registration_code",'password', 'active', 'admin')

    def clean_password(self):
        return self.initial["password"]


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label = "Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password Confirmation", widget = forms.PasswordInput)
    class Meta:
        model = User
        fields = ["username"]
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password do not match")
        return password2
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.clean_data["password1"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(label = 'Username')
    password = forms.CharField(widget=forms.PasswordInput) 

class RegisterForm(forms.Form):
    class Meta:
        model = User
        fields = ['username','email','cep_telefonu','is_telefonu','full_name','password','confirm','registration_code']
    def __init__(self,*args,**kwargs):
        super(RegisterForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs={'class':'form-control'}

    username = forms.CharField(label = 'Username')
    email = forms.EmailField()
    full_name = forms.CharField(label = 'Ad Soyad')
    cep_telefonu = forms.CharField(label= 'Cep Telefonu')
    is_telefonu = forms.CharField(label = 'İş Telefonu', required=False)
    password = forms.CharField(widget = forms.PasswordInput)
    confirm = forms.CharField(label='Confirm Password',widget = forms.PasswordInput)
    registration_code = forms.CharField(required = True, label = "Kayıt Onay Kodu")
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")
        email = self.cleaned_data.get("email")
        full_name = self.cleaned_data.get("full_name")
        registration_code = self.cleaned_data.get("registration_code")
        cep_telefonu = self.cleaned_data.get("cep_telefonu")
        is_telefonu = self.cleaned_data.get("is_telefonu")
        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords Does Not Match")
        if email == False:
            raise forms.ValidationError("A Valid Email Address")
        values = {
            "username" : username,
            "password" : password,
            "email" : email,
            "full_name" : full_name,
            "registration_code":registration_code,
            "cep_telefonu":cep_telefonu,
            "is_telefonu":is_telefonu
        }
        return values



class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    confirm = forms.CharField(label='Confirm Password',widget = forms.PasswordInput)
    class Meta:
        model = UserUpdateModel
        fields = {'email',
            'full_name',
            'cep_telefonu',
            'is_telefonu',}
    
 


