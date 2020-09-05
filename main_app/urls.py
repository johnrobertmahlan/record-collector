from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # path('records/', views.records_index, name='index'),
    path('records/', views.RecordList.as_view(), name='index'),
    path('records/create/', views.RecordCreate.as_view(), name='records_create'),
    path('records/<int:record_id>/', views.records_detail, name='records_detail'),
    path('records/<int:pk>/update/', views.RecordUpdate.as_view(), name='records_update'),
    path('records/<int:pk>/delete/', views.RecordDelete.as_view(), name='records_delete'),
    path('listenings/<int:record_id>/add_listening/', views.add_listening, name='add_listening'),
    path('musicians/', views.MusicianIndex.as_view(), name='musicians_index'),
    path('musicians/create/', views.MusicianCreate.as_view(), name='musicians_create'),
    path('musicians/<int:pk>/', views.MusicianDetail.as_view(), name='musicians_detail'),
    path('musicians/<int:pk>/update/', views.MusicianUpdate.as_view(), name='musicians_update'),
    path('musicians/<int:pk>/delete/', views.MusicianDelete.as_view(), name='musicians_delete'),
    path('records/<int:record_id>/assoc_musician/<int:musician_id>/', views.assoc_musician, name='assoc_musician'),
    path('records/<int:record_id>/unassoc_musician/<int:musician_id>/', views.unassoc_musician, name='unassoc_musician'),
    path('records/<int:record_id>/add_photo/', views.add_photo, name='add_photo')
]