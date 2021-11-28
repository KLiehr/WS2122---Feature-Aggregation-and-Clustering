from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name="home"),
    path('UserGuide/', views.userguide, name='userguide'),
    path('Import/', views.importCSVXES, name="import"),
    path('Import/upload/', views.file_upload_view,name='upload-view'),
    path('Import/AttrType/', views.attrType, name='attrType'),
    path('Attributes/', views.attributes, name="attributes"),
    path('Attributes/ListAttributes/', views.updateeventlog, name='updateeventlog'),
    path('Attributes/download/', views.download,name='download'),
    path('Filters/', views.filters, name="filters"),
    path('Filters/ListFilters/', views.filtereventlog, name='filtereventlog'),
    path('Filters/download/', views.downloadFilters,name='downloadFilters'),
<<<<<<< HEAD
=======
    path('UseCase/', views.useCase, name="useCase"),
    path('UseCase/DecisionTree/', views.decisionTree, name='decisionTree'),
    
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> parent of 8d83130 (revert 2)
=======
>>>>>>> parent of 8d83130 (revert 2)
=======
>>>>>>> parent of 8d83130 (revert 2)
]
