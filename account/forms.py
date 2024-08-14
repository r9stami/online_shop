from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User, Address, Contact


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["phone","email"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["phone","email", "password", "first_name"
            ,"last_name", "is_active", "is_admin"]


class AddressForm(forms.ModelForm):
    user = forms.CharField(required=False)

    class Meta:
        model = Address
        fields = ('first_name', 'last_name', 'address','email','phone','postal_code')
        widgets={
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels={
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'address': 'Address',
            'email': 'Email',
            'phone': 'Phone',
            'postal_code': 'Postal Code',

        }


class LoginForm(forms.Form):
    phone = forms.CharField(label='phone number',widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) != 11:
            raise ValidationError("Phone number must be 11 digits")
        if phone[:2] != '09':
            raise ValidationError("Phone number must be 09 digits")

        return phone


class SignUpForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=30, required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', max_length=30, required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(label='phone number',widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='email',widget=forms.EmailInput(attrs={'class': 'form-control'}))
    pwd = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    pwd2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # def clean(self):
    #     if self.pwd != self.pwd2:
    #         raise ValidationError("Passwords don't match")

    def clean_password(self):
        if len(self.cleaned_data['pwd']) < 8:
            raise ValidationError("Password must be at least 8 characters")
        return self.cleaned_data['psw']

    def clean_password2(self):
        if len(self.cleaned_data['psw2']) < 8:
            raise ValidationError("Password must be at least 8 characters")
        return self.cleaned_data['psw2']


class VerifyPhoneForm(forms.Form):
    code = forms.CharField(label="code",widget=forms.TextInput(attrs={'class': 'form-control'}),required=True)

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if len(code) != 4:
            raise ValidationError("Code must be 4 digits")

        return code


class UserProfileForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email','phone','email','biography')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'biography': forms.Textarea(attrs={'class': 'form-control'}),



        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'phone': 'Phone',
            'biography': 'Biography',
            'image': 'Image',


        }

        def clean_email(self):
            if '@gmail.com' not in self.clean_email():
                raise ValidationError("Email must contain @gmail.com")
            return self.clean_email()

        def clean_phone(self):
            phone = self.clean_phone()
            if len(phone) != 11:
                raise ValidationError("Phone number must be 11 digits")
            if phone[:2] != '09':
                raise ValidationError("Phone number must be 09 digits")

            return phone

        def clean_password(self):
            password = self.clean_password()
            if len(password) > 18:
                raise ValidationError("Password must be less than 18 characters")
            if len(password) < 8:
                raise ValidationError("Password must be less than 8 characters")

            return password

        def clean_first_name(self):
            first_name = self.clean_first_name()
            if first_name.is_alpha():
                return first_name
            else:
                raise ValidationError("First name must be alpha")

        def clean_last_name(self):
            last_name = self.clean_last_name()
            if last_name.is_alpha():
                return last_name
            else:
                raise ValidationError("Last name must be alpha")


# contact us form
class ContactUsForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('username', 'email', 'phone', 'text')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','placeholder':'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder':'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control','placeholder':'Phone'}),
            'text': forms.Textarea(attrs={'class': 'form-control','placeholder':'Text'}),
        }
        labels = {
            'username': 'Username',
            'email': 'Email',
            'phone': 'Phone',
            'text': 'Text',
        }