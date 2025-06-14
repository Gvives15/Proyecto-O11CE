"""
URL configuration for miproyecto_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
#from django.contrib import admin
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/clientes/", include("apps.clientes.urls")),
    path('api/v1/user/', include('apps.user.urls')),
    path("api/v1/empresa/", include("apps.empresa.urls")),
    path("api/v1/core/auditoria/", include("apps.core.urls")),
    path('api/v1/stock/', include('apps.stock.urls')),
    path('api/v1/proveedores/', include('apps.proveedores.urls')),
    path('api/v1/ventas/', include('apps.ventas.urls')),
    path('api/v1/caja/', include('apps.caja.urls')),
]