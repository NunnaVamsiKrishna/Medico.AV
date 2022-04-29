from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from medico.models import Profile


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
      print('Invalid credentials')
      return redirect('loginpage')


  else:
    return render(request, 'login.html')
@login_required()
def profile(request, user_id):
  print(user_id)
  return render(request,"profile.html")


@login_required()
def editprofile(request):
      if request.method == 'POST':
        user_id=request.POST['user_id']
        age = request.POST['age']
        height = request.POST['height']
        weight = request.POST['weight']
        city = request.POST['city']
        address = request.POST['address']
        mobile = request.POST['mobile']
        if User.objects.get(username=user_id):
          ins=Profile(user_id=user_id,age=age,height=height,weight=weight,city=city,address=address,mobile=mobile)
          ins.save()
      return render(request,"editprofile.html")
    

def logout(request):
	auth.logout(request)
	return redirect('/')

def search(request):
    return render(request,"hospital.html")
