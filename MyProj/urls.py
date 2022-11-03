"""MyProj URL Configuration

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
from book import views as book_views
from django.contrib.auth import views as auth_views
from myapp import views as myapp_views

urlpatterns = [
    path(
        "admin/login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    path("admin/", admin.site.urls),
    path("", myapp_views.bookview),
    path("cadastrarVoo/", myapp_views.cadastrarVoo),
    path("consultarVoo/", myapp_views.consultarVoo),
    path("deletarVoo/", myapp_views.deletarVoo),
    path("editarVoo/", myapp_views.editarVoo),
    path("relatorioVoos/", myapp_views.relatorioVoos),
    path("areaDoOperador/", myapp_views.areaDoOperador),
    path("areaDoFuncionario/", myapp_views.areaDoFuncionario),
    path("areaDoGerente/", myapp_views.areaDoGerente),
]
