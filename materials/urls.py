from django.urls import path
from materials import views

app_name = 'materials'

urlpatterns = [
    path('', views.MaterialListView.as_view(), name='material_list'),
    path('create/', views.MaterialCreateView.as_view(), name='material_create'),
    path(
        '<int:pk>/',
        views.MaterialDetailView.as_view(),
        name='material_detail'
    ),
    path(
        '<int:pk>/update',
        views.MaterialUpdateView.as_view(),
        name='material_update'
    ),
    path(
        '<int:pk>/delete',
        views.MaterialDeleteView.as_view(),
        name='material_delete'
    ),
]
