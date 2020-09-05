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
    path('labels/', views.LabelIndex.as_view(), name='labels_index'),
    path('labels/create/', views.LabelCreate.as_view(), name='labels_create'),
    path('labels/<int:pk>/', views.LabelDetail.as_view(), name='labels_detail'),
    path('labels/<int:pk>/update/', views.LabelUpdate.as_view(), name='labels_update'),
    path('labels/<int:pk>/delete/', views.LabelDelete.as_view(), name='labels_delete')
]