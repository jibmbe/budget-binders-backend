from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet
from . import views
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/register/', views.register_view),
    path('api/login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
