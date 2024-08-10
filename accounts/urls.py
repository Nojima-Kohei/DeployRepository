from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # マイページ関連のURLパターン
    path('mypage/', views.mypage, name='mypage'),
    path('save_annotations/', views.save_annotations, name='save_annotations'),
    path('view_annotations/<int:song_id>/', views.view_annotations, name='view_annotations'),
    path('delete_song/<int:song_id>/', views.delete_song, name='delete_song'),
]