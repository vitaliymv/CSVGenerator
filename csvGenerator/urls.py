"""csvGenerator URL Configuration

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
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from core import views
from csvGenerator import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name="login.html")),
    path('logout/', LogoutView.as_view()),
    path('', views.SchemasView.as_view()),
    path('schemas/', views.SchemasView.as_view()),
    path('new-schema/', views.CreateSchemaView.as_view()),
    path('edit/<int:pk>', views.UpdateSchemaView.as_view()),
    path('delete/<int:pk>', views.DeleteSchemaView.as_view()),
    path('generate-data/<int:pk>/', views.DataSetView.as_view()),
    path('generate-data/<int:pk>/download/<int:pk_ds>/', views.DownloadCsvView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)