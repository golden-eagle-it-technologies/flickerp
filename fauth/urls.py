# Authentication
from django.urls import path
from fauth import views
from django.contrib.auth.views import (PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
                                       PasswordResetCompleteView)

urlpatterns = [
    path('accounts/login/', views.login_page, name="loginAccounts"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('reset_password/', PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name="password_reset"),
    path('reset_password/done/', PasswordResetDoneView.as_view(template_name="ems_auth/password_reset_done.html"),
         name="password_reset_done"),
    path('reset_password/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name="ems_auth/password_reset_confirm.html"),
         name="password_reset_confirm"),
    path('reset_password/complete/',
         PasswordResetCompleteView.as_view(template_name="ems_auth/password_reset_complete.html"),
         name="password_reset_complete"),
    path('super_admin_required/', views.super_admin_required_page, name="super_admin_required_page"),
    path('hr_required/', views.hr_required_page, name="hr_required_page"),
    path('hod_required/', views.hod_required_page, name="hod_required_page"),

]


urlpatterns += [
    path('manage_users_page/', views.manage_users_page, name="manage_users_page"),
    path('edit_user_page/<int:id>/', views.edit_user_page, name="edit_user_page"),
    path('view_users_page/', views.view_users_page, name="view_users_page"),
]