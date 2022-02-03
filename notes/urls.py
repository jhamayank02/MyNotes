from django.urls import path
from . import views

urlpatterns = [
    path('', views.notes, name='notes'),
    path('addNote/', views.addNotes, name='addNotes'),
    path('deleteNote/', views.deleteNote, name='deleteNote'),
    path('<str:slug>', views.readNote, name='readNote')
]