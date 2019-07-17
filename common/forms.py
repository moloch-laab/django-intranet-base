from django import forms
from django.contrib.auth import authenticate, login, get_user_model, password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField, SetPasswordForm
from django.utils.translation import gettext, gettext_lazy as _

from core.utils import valida_rut, valida_rut_gremio

User = get_user_model()

class RegisterForm(forms.ModelForm):
    """Formulario para registrar nuevos usuarios. Incluye todos 
    los campos requeridos, además de un campo de confirmación 
    de contraseña."""

    error_messages = {
        'password_mismatch': "Las contraseñas no coinciden.",
        'invalid_rut': "El rut ingresado no es válido.",
        'not_gremio_rut': "El rut ingresado no se encuentra en nuestra base de datos.",
    }

    first_name  = forms.CharField(max_length=255, label="Nombres", 
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name   = forms.CharField(max_length=255, label="Apellidos", 
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    rut         = forms.CharField(max_length=20, label="Rut", 
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    email       = forms.EmailField(max_length=255, label="Email", 
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    # profile_pic = forms.ImageField(max_length=1000, label="Foto de perfil", 
    #                                widget=forms.FileInput(attrs={'class': 'custom-file-input'}))
    password1 = forms.CharField(label="Contraseña",
                                widget=forms.PasswordInput({'class': 'form-control'}))
    password2 = forms.CharField(label="Confirmar contraseña", 
                                widget=forms.PasswordInput({'class': 'form-control', 
                                                            'placeholder': 'Favor repita su contraseña'}))
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'rut', 'email')

    def clean_password2(self):
        """Verifica si las contraseñas coinciden y si 
        cumple con los parámetros de validación."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
           raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        password_validation.validate_password(password2)
        return password2
    
    def clean_rut(self):
        """Verifica si el rut es válido"""
        rut = self.cleaned_data.get("rut")
        if not valida_rut(rut):
            raise forms.ValidationError(
                self.error_messages['invalid_rut'],
                code='invalid_rut',
            )
        if not valida_rut_gremio(rut):
            raise forms.ValidationError(
                self.error_messages['not_gremio_rut'],
                code='not_gremio_rut',
            )
        return rut
    
    def save(self, commit=True):
        """Guarda la contraseña en formato hash."""
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        # user.active = False # El usuario debe ser validado por el administrador.
        if commit:
            user.save()
        return user

class LoginForm(forms.ModelForm):
    """Formulario para ingresar a los módulos del sistema,
    requiere email y contraseña."""

    error_messages = {
        'invalid_credentials': 'Nombre de usuario y/o contraseña inválido.',
        'user_inactive': 'Usuario inactivo, favor comuniquese con el administrador del sistema.',
    }

    rut = forms.CharField(max_length=20, label="Rut", 
                             widget=forms.TextInput(attrs={'class': 'form-control', 
                                                            'placeholder': 'Rut'}))
    password = forms.CharField(label="Contraseña", 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 
                                                            'placeholder': 'Contraseña'}))

    class Meta:
        model = User
        fields = ['rut', 'password']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        """Verifica si la contraseña cumple con los estandares de validación"""
        password = self.cleaned_data.get('password')
        if password:
            password_validation.validate_password(password)
        return password

    def clean(self):
        rut = self.cleaned_data.get("rut")
        password = self.cleaned_data.get("password")

        if rut and password:
            self.user = authenticate(username=rut, password=password)
            if self.user:
                if not self.user.is_active:
                    raise forms.ValidationError(
                        self.error_messages['user_inactive'],
                        code='user_inactive',
                    )
            else:
                raise forms.ValidationError(
                    self.error_messages['invalid_credentials'],
                    code='invalid_credentials',
                )
        return self.cleaned_data

class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = {
        **SetPasswordForm.error_messages,
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
    }
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'autofocus': True}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

class UserAdminChangeForm(forms.ModelForm):
    """Formulario para actualizar nuevos usuarios. Incluye todos
    los campos requeridos, pero reemplaza el campo de contraseña
    por un campo de contraseña en formato hash.
    """
    password = ReadOnlyPasswordHashField(label= ("Password"),
        help_text= ("<a href=\"../password/\">Cambiar contraseña</a>."))

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

class UserAdminCreationForm(forms.ModelForm):
    """Formulario para crear nuevos usuarios. Incluye todos 
    los campos requeridos, además de un campo de confirmación 
    de contraseña."""

    error_messages = {
            'password_mismatch': "Las contraseñas no coinciden.",
            'invalid_rut': "El rut ingresado no es válido.",
            'not_gremio_rut': "El rut ingresado no se encuentra en nuestra base de datos.",
        }

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'rut', 'email')
    
    def clean_password2(self):
        """Verifica si las contraseñas coinciden y si 
        cumple con los parámetros de validación."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
           raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        password_validation.validate_password(password2)
        return password2
    
    def clean_rut(self):
        """Verifica si el rut es válido"""
        rut = self.cleaned_data.get("rut")
        if not valida_rut(rut):
            raise forms.ValidationError(
                self.error_messages['invalid_rut'],
                code='invalid_rut',
            )
        if not valida_rut_gremio(rut):
            raise forms.ValidationError(
                self.error_messages['not_gremio_rut'],
                code='not_gremio_rut',
            )
        return rut
    
    def save(self, commit=True):
        """Guarda la contraseña en formato hash."""
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        user.active = False # El usuario debe ser validado por el administrador.
        if commit:
            user.save()
        return user