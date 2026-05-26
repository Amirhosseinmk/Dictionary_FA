from django.contrib import admin
from django.urls import path
from dictionary.views import home, about_us

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about/', about_us, name='about_us'),
    
]