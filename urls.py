"""
URL configuration for SignLanguageWeb project.

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
from django.urls import path
from django.views.generic import TemplateView

from signlanguage.audiotosign import audiotosign_model
from signlanguage.views import login, registration, logout, detect_sing_to_audio,facial_expression

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('index/', TemplateView.as_view(template_name='index.html'), name='index'),

    path('login/',TemplateView.as_view(template_name = 'login.html'),name='login'),
    path('loginaction/',login,name='loginaction'),

    path('registration/',TemplateView.as_view(template_name = 'registration.html'),name='registration'),
    path('regaction/',registration,name='regaction'),

    path('logout/',logout,name='logout'),

    #-----------------------------------------------------------------------

    path('signtoaudio/',TemplateView.as_view(template_name = 'signtoaudio.html'), name=""),
    path('detectsigntoaudio/', detect_sing_to_audio, name="signtoaudio"),

    #-----------------------------------------------------------------------
    path('audiotosign/',audiotosign_model,name='animation'),

    #-----------------------------------------------------------------------
    path('facialexpression/',facial_expression,name='animation'),
]
