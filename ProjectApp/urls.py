from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name="home"),
    path('UserGuide/', views.userguide, name='userguide'),
    path('ProgrammerGuide/', views.programmerguide, name='programmerguide'),
    path('Import/', views.importCSVXES, name="import"),
    path('Import/AttrType/', views.attrType, name='attrType'),
    path('Import/SaveAttrNames/', views.saveAttrNames, name='saveAttrNames'),
    path('Attributes/', views.attributes, name="attributes"),
    path('Attributes/ListAttributes/', views.updateeventlog, name='updateeventlog'),
    path('Filters/', views.filters, name="filters"),
    path('Filters/ListFilters/', views.filtereventlog, name='filtereventlog'),
    path('UseCase/', views.useCase, name="useCase"),
    path('UseCase/DecisionTree/', views.decisionTree, name='decisionTree'),
    path('UseCase/DecisionTree/Clustering/', views.clustering, name='clustering'),
    path('UseCase/DecisionTree/Clustering/ProcessModel/', views.processModel, name='processModel'),
]
