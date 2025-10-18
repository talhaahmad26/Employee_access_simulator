"""
URL configuration for newproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.views.generic.base import TemplateView
from django.urls import path,include
# from learning import views
# from rest_framework.routers import DefaultRouter
# model viewset
# router = DefaultRouter()
# router.register('stapi',views.classmo,basename='student')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',TemplateView.as_view(template_name='learning/index.html'), name='home'),
    path('', include('learning.urls'),)

    # serializers url
    # path('info/<int:pk>', views.detail),
    # path('in/', views.show),
    # mixins 
    # path('list/', views.StudentList.as_view()),
    # path('cr/', views.classcreate.as_view()),
    # path('r/<int:pk>', views.classretrieve.as_view()),
    # path('up/<int:pk>', views.classupdate.as_view()),
    # path('dl/<int:pk>', views.classdel.as_view()),
    # generic listcreate
    # path('lc/', views.classlc.as_view()),
    # path('rud/<int:pk>', views.classrud.as_view()),
# model viewset
    # path('', include(router.urls)),
# session authenciation

    # path('auth/', include('rest_framework.urls')),


]
