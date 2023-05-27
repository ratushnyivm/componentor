from componentor import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Home
    path('', views.HomePageView.as_view(), name='home'),

    # Apps
    path('materials/', include('materials.urls', namespace='materials')),
    path('parts/', include('parts.urls', namespace='parts')),
    path('assemblies/', include('assemblies.urls', namespace='assemblies')),
]
