from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name="home"),
    path('UserGuide/', views.userguide, name='userguide'),
    path('Import/', views.importCSVXES, name="import"),
    path('Import/upload/', views.file_upload_view,name='upload-view'),
    path('Import/AttrType/', views.attrType, name='attrType'),
    path('Import/AttrType/SaveAttrNames/', views.saveAttrNames, name='saveAttrNames'),
    path('Attributes/', views.attributes, name="attributes"),
    path('Attributes/ListAttributes/', views.updateeventlog, name='updateeventlog'),
    path('Attributes/download/', views.download,name='download'),
    path('Filters/', views.filters, name="filters"),
    path('Filters/ListFilters/', views.filtereventlog, name='filtereventlog'),
    path('Filters/download/', views.downloadFilters,name='downloadFilters'),
    path('UseCase/', views.useCase, name="useCase"),
    path('UseCase/DecisionTree/', views.decisionTree, name='decisionTree'),
    path('UseCase/DecisionTree/Clustering/', views.clustering, name='clustering'),
    path('UseCase/DecisionTree/Clustering/ProcessModel/', views.processModel, name='processModel'),
]
