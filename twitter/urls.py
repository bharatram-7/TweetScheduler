from django.contrib.auth import views as auth_views
from . import views
from django.urls import path, reverse_lazy, re_path
from .forms import UserLoginForm


urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/history', views.history, name='history'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name="registration/login.html",
                                                         authentication_form=UserLoginForm,
                                                         redirect_authenticated_user=True), name='login'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/forgot_password/', auth_views.PasswordResetView.as_view(
        template_name="registration/forgot_password.html", success_url=reverse_lazy('forgot_password_success'),
        email_template_name="registration/password_reset_template.html"),
        name='forgot_password'),
    path('accounts/forgot_password_success/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/forgot_password_success.html'), name='forgot_password_success'),
    path('accounts/password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirmation.html",
        success_url=reverse_lazy('password_reset_completed')), name='password_reset_confirm'),
    path('accounts/password_reset_completed/', auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_completion.html"), name='password_reset_completed'),
    path('posts/<int:post_id>/edit/', views.editpost, name="edit_post"),
    path('posts/<int:post_id>/delete/', views.deletepost, name="delete_post"),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('integrations/', views.integration, name="integrations"),
    path('twitter/', views.twitter, name='twitter'),
    path('api/v1/posts', views.PostList.as_view(), name='post_list_view'),
    path('api/v1/posts/<int:pk>', views.PostDetail.as_view(), name='post_detail_view'),
    path('api/v1/history', views.HistoryList.as_view(), name='history_list_view'),
]
