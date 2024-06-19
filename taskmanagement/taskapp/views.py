from django.shortcuts import render,redirect
import pymongo
from django.conf import settings
from datetime import datetime
client = pymongo.MongoClient(settings.MONGODB_URI)
db = client[settings.MONGODB_NAME]
usercollection = db['users']
alltaskscollection = db['alltasks']

def index(request):
    email = request.COOKIES.get('email')
    if email is not None:
        user = usercollection.find_one({"mail":email})
        alltasks = list(alltaskscollection.find({"email":email}))
        taskname =[]
        task_description =[]
        due_time =[]
        date = datetime.now()
        date = date.strftime("%Y-%m-%d")
        for item in alltasks:
            print(item["due_date"],date)
            if item["due_date"] == date:
                taskname.append(item["taskname"])
                task_description.append(item["task_description"])
                due_time.append(item["due_time"])
        alltasks = zip(taskname,task_description,due_time)        

        context={
            "name":user["name"],
            "alltasks":alltasks
        }
        return render(request,"index.html",context)
    return redirect('/login/')

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
        email = request.COOKIES.get("email")
        taskname = request.POST["task_name"]
        task_description = request.POST["task_description"]
        due_date = request.POST["due_date"]
        due_time = request.POST["due_time"]

        if 'alltasks' not in db.list_collection_names():
            db.create_collection('alltasks')
        alltaskscollection = db['alltasks']

        data={
            "email":email,
            "taskname":taskname,
            "task_description":task_description,
            "due_date":due_date,
            "due_time":due_time
        }
        alltaskscollection.insert_one(data)

    return render(request,"createtask.html")

def tasks(request):
    alltasks = list(alltaskscollection.find())
    taskname =[]
    task_description =[]
    due_date = []
    due_time =[]
    date = datetime.now()
    date = date.strftime("%Y-%m-%d")
    for item in alltasks:
        taskname.append(item["taskname"])
        task_description.append(item["task_description"])
        due_date.append(item["due_date"])
        due_time.append(item["due_time"])
    alltasks = zip(taskname,task_description,due_date,due_time) 
    context = {
        "alltasks":alltasks
    }
    return render(request,"task.html",context)     