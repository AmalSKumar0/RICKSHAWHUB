from django import forms

class DriverLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))

class DriverLocForm(forms.Form):
    location = forms.CharField(
        widget=forms.TextInput(attrs={
            'name': 'cloc',
            'id': 'autocomplete',
            'placeholder': 'Current location',
            'required': True
        })
    )

class DriverRegistrationForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'})
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'form-control'})
    )
    
    gender = forms.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    address = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control'})
    )
    
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'Phone number', 'class': 'form-control'})
    )
    
    licence = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Licence number', 'class': 'form-control'})
    )
    
    vehicle = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Vehicle number', 'class': 'form-control'})
    )
    
    image = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'})
    )
    
    # Clean method to validate passwords match
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")


