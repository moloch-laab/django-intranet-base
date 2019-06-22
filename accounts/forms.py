from django import forms
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from core.utils import validarRut


User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('rut', 'full_name', 'email',) #'full_name',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label= ("Password"),
        help_text= ("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = User
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        super(UserAdminChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



# class GuestForm(forms.Form):
#     email    = forms.EmailField()


class LoginForm(forms.Form):
    rut = forms.CharField(max_length = 20, label='rut', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput)
    password.widget.attrs.update({'class': 'form-control'})
    
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        request = self.request
        data = self.cleaned_data
        rut  = data.get("rut")
        password  = data.get("password")
        qs = User.objects.filter(rut=rut)
        if qs.exists():
            # user email is registered, check active/
            not_active = qs.filter(active=False)
            if not_active.exists():
                ## not active, check email activation
                link = reverse("account:resend-activation")
                reconfirm_msg = """Go to <a href='{resend_link}'>
                resend confirmation email</a>.
                """.format(resend_link = link)
                confirm_email = EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()
                if is_confirmable:
                    msg1 = "Please check your email to confirm your account or " + reconfirm_msg.lower()
                    raise forms.ValidationError(mark_safe(msg1))
                email_confirm_exists = EmailActivation.objects.email_exists(email).exists()
                if email_confirm_exists:
                    msg2 = "Email not confirmed. " + reconfirm_msg
                    raise forms.ValidationError(mark_safe(msg2))
                if not is_confirmable and not email_confirm_exists:
                    raise forms.ValidationError("This user is inactive.")
        user = authenticate(request, username=rut, password=password)
        if user is None:
            raise forms.ValidationError("Invalid credentials")
        login(request, user)
        self.user = user
        return data
        




class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    rut = forms.CharField(max_length = 20, label='Rut', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '11111111-1'}))
    full_name = forms.CharField(max_length = 255, label='Nombre Completo', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Juan Perez'}))
    email = forms.EmailField(max_length = 255, label='Email', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'jperez@email.com'}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmación de contraseña', widget=forms.PasswordInput)
    password1.widget.attrs.update({'class': 'form-control', 'placeholder': 'Debe tener o 8 más caracteres alfanuméricos'})
    password2.widget.attrs.update({'class': 'form-control', 'placeholder': 'Favor repita su contraseña'})
    check = forms.BooleanField(label='Aceptar')

    class Meta:
        model = User
        fields = ('rut', 'full_name', 'email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("las contraseñas no coinciden.")
        # Check if password is over 8 characters
        if len(password2) < 8:
            raise forms.ValidationError("La contraseña debe tener 8 o más caracteres.")
        # Check if password contains chars and numbers
        if password2.isalpha() or password2.isdigit():
            raise forms.ValidationError("La contraseña debe ser contener letras y números.")
        # Check if password constains only spaces
        # if isspace():
        #      raise forms.ValidationError("Ingrese una contraseña válida.")
        return password2

    def clean_rut(self):
        rut = self.cleaned_data.get("rut")
        if validarRut(rut):
            return rut
        else:
            raise forms.ValidationError("Rut no válido")
    
    def clean_check(self):
        check = self.changed_data.get("check")
        if check == False:
             raise forms.ValidationError("Debe aceptar los terminos y condiciones")
        return check

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # user.active = False # send confirmation email
        if commit:
            user.save()
        return user