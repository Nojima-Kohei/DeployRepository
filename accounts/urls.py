from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthenticationForm
from django.urls import path, include

app_name = 'accounts'  # 名前空間を設定

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        authentication_form=CustomAuthenticationForm  # カスタムフォームを指定
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('mypage/', views.MyPageView.as_view(), name='mypage'),

    # マイページ関連のURLパターン
    path('save_annotations/', views.save_annotations, name='save_annotations'),
    path('view_annotations/<int:lyric_id>/', views.view_annotations, name='view_annotations'),
    path('delete_song/<int:lyric_id>/', views.delete_song, name='delete_song'),
]