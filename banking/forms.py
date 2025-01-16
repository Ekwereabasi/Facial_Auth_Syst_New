from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Account, Transaction

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15,required=False )
    profile_picture = forms.ImageField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'profile_picture', 'password1', 'password2']

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        fields = ['username', 'password', 'profile_picture']


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['balance', 'account_type']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'description', ]  # Add relevant fields


# class FacialRecognitionForm(forms.Form):
#     image = forms.ImageField()

#     def clean_image(self):
#         image = self.cleaned_data.get('image')
#         if not image:
#             raise forms.ValidationError("Please upload an image.")
#         if image.content_type not in ['image/jpeg', 'image/png']:
#             raise forms.ValidationError("Only JPEG and PNG images are supported.")
#         return image

# class FacialRecognitionForm(forms.Form):
#     image = forms.ImageField()

#     def clean_image(self):
#         image = self.cleaned_data.get('image')
#         if not image:
#             raise forms.ValidationError("Please upload an image.")
#         return image


class FacialRecognitionForm(forms.Form):
    image = forms.ImageField()

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError("Please upload an image.")
        
        # Validate content type
        if image.content_type not in ['image/jpeg', 'image/png']:
            raise forms.ValidationError("Only JPEG and PNG images are supported.")
        
        # Validate file size (optional: limit to 5MB for example)
        max_size = 5 * 1024 * 1024  # 5 MB
        if image.size > max_size:
            raise forms.ValidationError("Image file size should not exceed 5 MB.")
        
        return image


class CustomUserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'profile_picture']