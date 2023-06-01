from django.urls import path
from parts import views

app_name = 'parts'

urlpatterns = [
    path('', views.PartListView.as_view(), name='part_list'),
    path('create/', views.PartCreateView.as_view(), name='part_create'),
    path('<int:pk>/', views.PartDetailView.as_view(), name='part_detail'),
    path(
        '<int:pk>/update', views.PartUpdateView.as_view(), name='part_update'
    ),
    path(
        '<int:pk>/delete', views.PartDeleteView.as_view(), name='part_delete'
    ),
]
