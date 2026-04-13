from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .api_views import importar_desde_google_books # Asegúrate de importarla
from . import api_views
from . import oauth_views  # ← AGREGAR

router = DefaultRouter()
router.register(r'libros', api_views.LibroViewSet, basename='libro')
router.register(r'autores', api_views.AutorViewSet, basename='autor')
router.register(r'categorias', api_views.CategoriaViewSet, basename='categoria')
router.register(r'prestamos', api_views.PrestamoViewSet, basename='prestamo')

urlpatterns = [
    # ─────────────────────────────────
    # 🔐 AUTENTICACIÓN JWT
    # ─────────────────────────────────
    path('auth/jwt/login/', TokenObtainPairView.as_view(), name='jwt_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # ─────────────────────────────────
    # 🔑 AUTENTICACIÓN OAUTH 2.0 (GOOGLE)
    # ─────────────────────────────────
    path('auth/google/redirect/', oauth_views.google_oauth_redirect, name='google_redirect'),
    path('auth/google/callback/', oauth_views.google_oauth_callback, name='google_callback'),
    
    # ─────────────────────────────────
    # 📚 ENDPOINTS CRUD
    # ─────────────────────────────────
    path('', include(router.urls)),
    path('libros/importar/', importar_desde_google_books, name='importar-google-books'),
]