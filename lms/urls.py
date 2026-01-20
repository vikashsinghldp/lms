"""
URL configuration for lms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from .import views
from django.conf.urls.static import static
from . import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('base',views.BASE,name='base'),
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('courses', views.courses, name='courses'),
    path('course1', views.course1, name='course1'),
    path('ajax/login/', views.ajax_login, name='ajax_login'),
    path('ajax/signup/', views.ajax_signup, name='ajax_signup'),
    path('ajax/forgot-password/', views.ajax_forgot_password, name='ajax_forgot_password'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path("create-order/", views.create_order, name="create_order"),
    path("payment-success/", views.payment_success, name='payment_success'),
    path("course/<int:course_id>/lessons/", views.course_lessons, name="course_lessons"),
    path("course/<int:course_id>/doubts/", views.course_doubts, name="course_doubts"),
    path("course/<int:course_id>/ask-doubt/", views.ask_doubt, name="ask_doubt"),
    path("profile/settings/", views.profile_settings, name="profile_settings"),
    path("profile/", views.view_profile, name="view_profile"),
    path("course/<int:course_id>/resources/",views.course_resources,name="course_resources"),


]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
