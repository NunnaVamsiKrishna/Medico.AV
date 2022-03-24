from tkinter import N
from unicodedata import name
from django.contrib import admin
from django.urls import path
from .views import dp,result
from diseasepredictor import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('predict/',dp,name='predictor'),
    path('predict/result/',result,name='result'),
]