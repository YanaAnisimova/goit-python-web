from django import forms


class RegistrationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Name', 'style': 'width: 200px;', 'class': 'form-control'}),
        max_length=50
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'E-mail', 'style': 'width: 200px;', 'class': 'form-control'}),
        max_length=50
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'style': 'width: 200px;', 'class': 'form-control'}),
        max_length=50
    )


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'E-mail', 'style': 'width: 200px;', 'class': 'form-control'}),
        max_length=50,
        error_messages={'required': '* E-mail or password is incorrect'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'style': 'width: 200px;', 'class': 'form-control'}),
        max_length=50,
        # error_messages={'required': '* E-mail or password is incorrect'}
    )
