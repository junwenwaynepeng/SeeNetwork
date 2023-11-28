"""
URL configuration for SeeNetwork project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from accounts import views as accounts_views
from network import views
from django.contrib.auth import views as auth_views
import notifications.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', accounts_views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('search/', views.search_users, name='search_users'),
    path('send_friend_request/<int:user_id>', views.send_friend_request, name='send_friend_request'),
    path('unsend_friend_request/<int:user_id>', views.unsend_friend_request, name='unsend_friend_request'),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('confirm_request/<int:notification_id>', views.confirm_request, name='confirm_request'),
    path('profile/<slug:user_slug>/', accounts_views.profile_view, name='profile_view'),
    path('save_profile', accounts_views.save_profile, name='save_profile'),
    path('settings', accounts_views.settings, name='settings'),
    path('save_other_profile/<slug:modal>', accounts_views.save_other_profile, name='save_other_profile'),
    path('save_cv_card_order', accounts_views.save_cv_card_order, name='save_cv_card_order'),
    path('delete_profile_item', accounts_views.delete_profile_item, name='delete_profile_item'),
    path('ignore_request/<int:notification_id>', views.ignore_request, name='ignore_request'),
    path('mark_all_as_read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('notifications/', views.notifications, name='notifications'),
    path('network/', views.network, name='network'),
    path('graph/<slug:option>', views.graph, name='graph'),
    path('martor/', include('martor.urls')),
    path('settings/', accounts_views.settings, name='settings'),
    path('save_setting/<slug:modal>', accounts_views.save_setting, name='save_setting'),
    path("__reload__/", include("django_browser_reload.urls")),
]