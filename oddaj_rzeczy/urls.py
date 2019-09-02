"""oddaj_rzeczy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from core.views import LandingPage, SignUpView, AdminListView, LoginView, SetAdminPermission, DeleteUserView, \
    ModifyUserView, CharityListView, AddAdminView, CharityUpdateView, CharityAddView, CharityDeleteView, \
    UserProfileView, UserProfileModifyView, ChangePasswordView, FormStepOne, load_charity, SaveDonateView, \
    DonateListView, CollectDonateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPage.as_view(), name='landing_page'),
    re_path('^accounts/', include('django.contrib.auth.urls')),
    re_path('^accounts/', include('django_registration.backends.activation.urls')),
    path('signup', SignUpView.as_view(), name='signup'),
    path('admin-list', AdminListView.as_view(), name='admin_list'),
    path('login', LoginView.as_view(), name='login2'),
    path('set-admin-permission', SetAdminPermission.as_view(), name='set_admin_permission'),
    path('add-admin', AddAdminView.as_view(), name='add_admin'),
    re_path('delete-user/(?P<pk>(\d)+)', DeleteUserView.as_view(), name='delete_user'),
    re_path('modify-user/(?P<pk>(\d)+)', ModifyUserView.as_view(), name='modify_user'),
    path('charity-list', CharityListView.as_view(), name='charity_list'),
    path('charity-add', CharityAddView.as_view(), name='add_charity'),
    re_path('charity-list/modify/(?P<pk>(\d)+)', CharityUpdateView.as_view(), name='update_charity'),
    re_path('charity-list/delete/(?P<pk>(\d)+)', CharityDeleteView.as_view(), name='delete_charity'),
    re_path('user/profile/(?P<pk>(\d)+)', UserProfileView.as_view(), name='profile'),
    re_path('user/profile-modify/(?P<pk>(\d)+)', UserProfileModifyView.as_view(), name='profile-modify'),
    re_path('user/change-password', ChangePasswordView.as_view(), name='change_password'),
    path('donate', FormStepOne.as_view(), name='form1'),
    path('ajax-load-charity', load_charity, name='ajax'),
    path('save-donate', SaveDonateView.as_view(), name="donate"),
    re_path('donate-list/(?P<pk>(\d)+)', DonateListView.as_view(), name='donate_list'),
    re_path('donate-collect/(?P<pk>(\d)+)', CollectDonateView.as_view(), name='collect_donate'),

]
