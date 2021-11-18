from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name="home"),
    path('Import/', views.importCSVXES, name="import"),
    path('Attributes/', views.attributes, name="attributes"),
    path('Import/upload/', views.file_upload_view,name='upload-view'),
    path('UserGuide/', views.userguide, name='userguide'),
    path('Attributes/ListAttributes/', views.updateeventlog, name='updateeventlog'),
    path('Attributes/download/', views.download,name='download'),
]
