from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password, UserAttributeSimilarityValidator
from django.core.exceptions import ValidationError

# ログインフォーム（2024/09/03）
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="メールアドレス",
        widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "メールアドレス"

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                "このアカウントは無効です。",
                code='inactive',
            )
        if not user.check_password(self.cleaned_data['password']):
            raise forms.ValidationError(
                "メールアドレスまたはパスワードが間違っています。どちらの入力フォームも大文字と小文字は区別されます。",
                code='invalid_login',
            )

    def get_invalid_login_error(self):
        return forms.ValidationError(
            "メールアドレスまたはパスワードが間違っています。どちらの入力フォームも大文字と小文字は区別されます。",
            code='invalid_login',
        )

# ユーザー登録フォーム(2024/09/03)
User = get_user_model()  # カスタムユーザーモデルを取得

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'ユーザー名',
            'email': 'メールアドレス',
            'password1': 'パスワード',
            'password2': 'パスワード（確認用）',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].error_messages.update({
            'required': "ユーザー名は必須です。",
            'invalid': "無効なユーザー名です。",
            'unique': "このユーザー名はすでに使用されています。",
        })
        self.fields['email'].error_messages.update({
            'required': "メールアドレスは必須です。",
            'invalid': "無効なメールアドレスです。正しい形式で入力してください。",
            'unique': "このメールアドレスはすでに使用されています。",
        })
        self.fields['password1'].error_messages.update({
            'required': "パスワードは必須です。",
        })
        self.fields['password2'].error_messages.update({
            'required': "確認用パスワードは必須です。",
            'password_mismatch': "パスワードが一致しません。",
        })

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        # パスワードの類似性チェック
        if username and username.lower() in password1.lower():
            raise ValidationError(f"このパスワードは{self.fields['username'].label}と似すぎています。")
        if email and email.lower().split('@')[0] in password1.lower():
            raise ValidationError(f"このパスワードは{self.fields['email'].label}と似すぎています。")

        # Djangoのデフォルトバリデーションを適用
        try:
            validate_password(password1, self.instance)
        except ValidationError as e:
            raise ValidationError(e.messages)
        
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "パスワードが一致しません。")
        
        return cleaned_data

class CustomSignupForm(CustomUserCreationForm):
    class Meta(CustomUserCreationForm.Meta):
        fields = CustomUserCreationForm.Meta.fields
        widgets = CustomUserCreationForm.Meta.widgets
        labels = CustomUserCreationForm.Meta.labels

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


# ログインフォーム
class LoginForm(forms.Form):
    email = forms.EmailField(
        label="メールアドレス",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

# Email認証フォーム
class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(
        label="メールアドレス",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

# # サインアップフォーム (2024/09/03)
# class CustomSignupForm(CustomUserCreationForm):
#     class Meta(CustomUserCreationForm.Meta):
#         fields = CustomUserCreationForm.Meta.fields
#         widgets = CustomUserCreationForm.Meta.widgets
#         labels = CustomUserCreationForm.Meta.labels

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         if commit:
#             user.save()
#         return user


# ユーザー名編集用のフォーム
class EditUsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        labels = {
            'username': 'ユーザー名'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'})
        }
