from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth

def index(request):
    return render(request,"index.html")
def dash(request):
    return render(request,"dash.html")
def signup(request):
  if request.method == 'POST':
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    email = request.POST['email']

    if password1 == password2:
      if User.objects.filter(username=username).exists() and User.objects.filter(email=email).exists():
        #messages.info(request,'Username or email already taken')
        print('Username or email already taken')
        return redirect('signuppage')

      else:
        user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
        user.save()
        return redirect('loginpage')
  else:
    return render(request, 'signup.html')


def login(request):
  if request.method == "POST":
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username,password=password)

    if user is not None:
      auth.login(request, user)
      return redirect('dashpage')

    else:
      #messages.info(request, 'Invalid credentials')
      print('Invalid credentials')
      return redirect('loginpage')


  else:
    return render(request, 'login.html')
