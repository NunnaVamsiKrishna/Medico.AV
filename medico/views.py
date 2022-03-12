from django.shortcuts import render
def index(request):
    return render(request,"index.html")
def login(request):
    return render(request,"login.html")
def dash(request):
    return render(request,"dash.html")