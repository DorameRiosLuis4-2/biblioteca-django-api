"""
URL Configuration for biblioteca_project
"""
from django.contrib import admin
from django.urls import path, include
from libros import web_views
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # Interfaz de Administración
    path('admin/', admin.site.urls),

    # Rutas de Frontend (Vistas de Navegador)
    path('', web_views.home, name='home'),
    path('oauth/login/', web_views.oauth_login, name='oauth_login'),
    path('login/jwt/', web_views.jwt_login_page, name='jwt_login_page'),

    # ============================================================
    # API REST
    # ============================================================
    path('api/', include('libros.api_urls')),

    # ============================================================
    # AUTENTICACIÓN Y OAUTH2
    # ============================================================
    
    # 1. Django Allauth (Login social con Google para usuarios)
    path('accounts/', include('allauth.urls')),

    path('chat/', web_views.chat_view, name='chat'),


    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    # 2. Django OAuth Toolkit (Para que tu API actúe como proveedor OAuth2)
    # Proporciona endpoints como /o/authorize/, /o/token/, etc.
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]