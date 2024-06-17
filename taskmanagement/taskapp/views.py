from django.shortcuts import render,redirect

def index(request):
    email = request.COOKIES.get('email')
    if email is not None:
        return render(request,"index.html")
    return redirect('/registration/')
def registration(request):
    return render(request,"registration.html")
def login(request):
    return render(request,"login.html")