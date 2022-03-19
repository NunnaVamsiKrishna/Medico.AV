from tkinter import N
from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from .views import dp
from diseasepredictor import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('predict/',dp,name='predictor'),
]