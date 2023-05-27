from django.urls import path

from . import views

app_name = 'assemblies'

urlpatterns = [
    path('', views.AssemblyListView.as_view(), name='assembly_list'),
    path('create/', views.AssemblyCreateView.as_view(), name='assembly_create'),
    path(
        '<int:pk>/', views.AssemblyDetailView.as_view(), name='assembly_detail'
    ),
    path(
        '<int:pk>/update',
        views.AssemblyUpdateView.as_view(),
        name='assembly_update'
    ),
    path(
        '<int:pk>/delete',
        views.AssemblyDeleteView.as_view(),
        name='assembly_delete'
    ),
]
