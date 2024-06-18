from django.shortcuts import render,redirect
import pymongo
from django.conf import settings

client = pymongo.MongoClient(settings.MONGODB_URI)
db = client[settings.MONGODB_NAME]
usercollection = db['users']

def index(request):
    email = request.COOKIES.get('email')
    if email is not None:
        return render(request,"index.html")
    return redirect('/registration/')

def registration(request):
    if request.method == 'POST':
        name = request.POST['username']
        mail = request.POST['email']
        password = request.POST['confirm_password']
        if 'users' not in db.list_collection_names():
            db.create_collection('users')

        usercollection = db['users']
        if usercollection.find_one({"mail": mail}):
            context={
                'message':'Email has already been taken'
            }
            return render(request,"registration.html",context)

        doctor_data = {
            "name": name,
            "mail": mail,
            "password": password
        }
        usercollection.insert_one(doctor_data)
        return redirect("/login/")
    return render(request,"registration.html")

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = usercollection.find_one({"mail": email, "password": password})
        if user:
            response = redirect("/")
            response.set_cookie('email', email)
            return response
        else:
            context = {
                'message': 'Invalid email or password.'
            }
            return render(request, 'login.html', context)
    return render(request,"login.html")

def logout(request):
    response = redirect('/login/')
    response.delete_cookie('email')
    return response

def createtask(request):
    if request.method == "POST":
        taskname = request.POST[""]
        taskname = request.POST[""]
        taskname = request.POST[""]
        taskname = request.POST[""]

    return render(request,"createtask.html")

