"""crud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from blog.views import Create, Find, FindOne
from user.views import SingUp, Login, Edit, FindMember

urlpatterns = [
    path('admin/', admin.site.urls),

    path('blogs/', Find.as_view(), name='blogs'),
    path('blog-create/', Create.as_view()),
    path('blogs/<int:blog_id>/', FindOne.as_view()),

    path('singup/', SingUp.as_view(), name='singup'),
    path('login/', Login.as_view(), name='login'),
    path('users/<int:uid>/', Edit.as_view(), name='edit'),

    path('members/', FindMember.as_view()),
]
