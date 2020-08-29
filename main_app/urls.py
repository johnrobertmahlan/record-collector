from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # path('records/', views.records_index, name='index'),
    path('records/', views.RecordList.as_view(), name='index'),
    path('records/create', views.RecordCreate.as_view(), name='records_create'),
    # path('records/<int:record_id>/', views.records_detail, name='detail'),
    path('records/<int:pk>/', views.RecordDetail.as_view(), name='detail'),
]