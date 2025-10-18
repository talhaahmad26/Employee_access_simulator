from django.urls import path
from . import views
urlpatterns = [
    path('api/check_bulk/', views.check_bulk, name='check_bulk'),
]