
from django.contrib import admin
from django.urls import path
from wifi_qr import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
]
