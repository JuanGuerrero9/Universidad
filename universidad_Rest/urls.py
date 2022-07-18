"""universidad_Rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.views.static import serve
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth.decorators import login_required


from rest_framework.authtoken import views

from apps.usuario.views import Index, Login, logoutUsuario
from apps.usuario.api.api import Login_rest, Logout_rest


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuario/', include(('apps.usuario.urls', 'usuario'))),
    path('institucional/', include(('apps.institucional.urls', 'institucional'))),
    path('rest/usuario/', include(('apps.usuario.api.routers', 'routers_usuario'))),
    path('rest/institucional/', include(('apps.institucional.api.routers', 'routers_institucional'))),
    path('', Index.as_view(), name='index'),
    path('accounts/login/', Login.as_view(), name='login'),
    path('logout/',login_required(logoutUsuario),name = 'logout'),
    path('login_rest/', Login_rest.as_view(), name='login_rest'),
    path('logout_rest/',login_required(Login_rest),name = 'logout_rest'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
    
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    })
]