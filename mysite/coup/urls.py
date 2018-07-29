from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += [
    path('start', views.startGame, name='startGame'),
    ]
urlpatterns += [
    path('showTable', views.showTable, name='showTable'),
    ]

urlpatterns += [
    path('showDeck', views.showDeck, name='showDeck'),
    ]

urlpatterns += [
    path('initialDeal', views.initialDeal, name='initialDeal'),
    ]

urlpatterns += [
    path('shuffle', views.shuffle, name='shuffle'),
    ]

urlpatterns += [
    path('actions', views.actions, name='actions'),
    ]
