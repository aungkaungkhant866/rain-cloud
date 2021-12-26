from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .forms import SignUp
from django.contrib.auth.decorators import login_required
import requests
import pyrebase

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')

    else:
        return render(request, "account.html")

def account(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')

    else:
        return render(request, "account.html")

def signin(request):
    if request.user.is_authenticated:
        return render(request, "home.html")

    else:

        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return render(request, "home.html", {"success": "Sign In Successfully."})

            else:
                return render(request, "signin.html", {"error": "Invaild Username or password."})

        return render(request, "signin.html")

def signup(request):
    if request.user.is_authenticated:
        return render(request, "home.html")

    else:
        url = "https://rain-cloud-2021-default-rtdb.firebaseio.com/Users.json"
        email_url = "https://rain-cloud-2021-default-rtdb.firebaseio.com/Emails.json"

        if request.method == "POST":
            form = SignUp(request.POST)

            if form.is_valid():
                username = request.POST['username']
                username = username.replace(",","")
                email = request.POST['email']
                password1 = request.POST['password1']

                form.save()
                data = {username: {"Username": username, "Email": email, "Password": password1}}
                email_data = {username: email}
                requests.patch(url=url, json=data)
                requests.patch(url=email_url, json=email_data)
                user = authenticate(username=request.POST['username'], password=request.POST['password1'])

                if user is not None:
                    login(request, user)
                    return render(request, "home.html", {"success": "Sign Up Successfully."})

        else:
            form = SignUp()

        return render(request, "signup.html", {"signup": form})

@login_required
def signout(request):
    logout(request)
    return render(request, "account.html", {"alert": "Signed Out Successfully."})

def courses(request):
    if request.user.is_authenticated:
        Courses = "https://rain-cloud-2021-default-rtdb.firebaseio.com/Courses/.json"
        api = "hRswKpUPEonCv0ubir2Va1vllI1TORh7leBWPuZT"
        all_data = requests.get(Courses + '?auth=' + api)
        data = all_data.json()

        if data is None:
            return render(request, 'courses.html', {"warning": "No courses created yet."})

        else:
            data_value = list(data.values())
            return render(request, 'courses.html', {"data": data_value})

    else:
        return render(request, "account.html")

def explore(request):
    if request.user.is_authenticated:
        Courses = "https://rain-cloud-2021-default-rtdb.firebaseio.com/Courses/.json"
        api = "hRswKpUPEonCv0ubir2Va1vllI1TORh7leBWPuZT"
        all_data = requests.get(Courses + '?auth=' + api)
        data = all_data.json()

        if data is None:
            return render(request, 'explore.html', {"warning": "No courses created yet."})

        else:
            data_value = list(data.values())
            return render(request, 'explore.html', {"data": data_value})

    else:
        return render(request, "account.html")

def create(request):
    name = request.POST['name']
    name = name.replace(".", "")
    name = name.replace(" ", "-")
    description = request.POST['description']

    Courses_Data = "https://rain-cloud-2021-default-rtdb.firebaseio.com/Courses/.json"
    Courses = "https://rain-cloud-2021-default-rtdb.firebaseio.com/Courses/{}/.json".format(name)
    api = "hRswKpUPEonCv0ubir2Va1vllI1TORh7leBWPuZT"
    all_data = requests.get(Courses + '?auth=' + api)
    data = all_data.json()

    if data is None:
        data = {name: {"Name": name, "Description": description, "Username": request.user.username, "videos": ["none"]}}
        requests.patch(url=Courses_Data, json=data)
        return redirect("Courses")

    else:
        return render(request, "courses.html", {"error": "This course exists. Please choose another name."})

def delete_course(request):
    title = request.POST['title']

    Courses_Data = "https://rain-cloud-2021-default-rtdb.firebaseio.com/Courses/{}.json".format(title)
    api = "hRswKpUPEonCv0ubir2Va1vllI1TORh7leBWPuZT"
    all_data = requests.get(Courses_Data + '?auth=' + api)
    data = all_data.json()
    data_list = list(data.values())

    if data_list[2] == request.user.username:
        requests.delete(url=Courses_Data)
        return render(request, "home.html", {"success": "Deleted Successfully."})

    elif request.user.username == "codejapoe":
        requests.delete(url=Courses_Data)
        return render(request, "home.html", {"success": "Deleted Successfully."})

    return render(request, 'settings.html')

def video(request):
    if request.user.is_authenticated:
        Courses = "https://rain-cloud-2021-default-rtdb.firebaseio.com/Courses/.json"
        api = "hRswKpUPEonCv0ubir2Va1vllI1TORh7leBWPuZT"
        all_data = requests.get(Courses + '?auth=' + api)
        data = all_data.json()

        if data is None:
            return render(request, 'video.html', {"warning": "No courses created yet."})

        else:
            data_value = list(data.values())
            return render(request, 'video.html', {"data": data_value})

    else:
        return render(request, "account.html")

def upload(request):

    if request.method == "POST":
        course_name = request.POST['courses']
        title = request.POST['title']
        description = request.POST['description']
        file = request.FILES['video']

        config = {
            "apiKey": "AIzaSyDUQgbuO1auLYShpl10qcC7W16iiTEiYA0",
            "authDomain": "rain-cloud-2021.firebaseapp.com",
            "databaseURL": "https://rain-cloud-2021-default-rtdb.firebaseio.com",
            "projectId": "rain-cloud-2021",
            "storageBucket": "rain-cloud-2021.appspot.com",
            "messagingSenderId": "240468281374",
            "appId": "1:240468281374:web:1f5be760a1f7a08eae060f"
        }
        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()
        path = "Courses/{0}/{1}".format(course_name, file.name)
        storage.child(path).put(file)
        url = storage.child(path).get_url(None)

        Courses = "https://rain-cloud-2021-default-rtdb.firebaseio.com/Courses/{}/.json".format(course_name)
        api = "hRswKpUPEonCv0ubir2Va1vllI1TORh7leBWPuZT"
        all_data = requests.get(Courses + '?auth=' + api)
        json_data = all_data.json()
        data = list(json_data.values())
        videos = data[3]

        description = description.replace("", "No Description")
        description = "Description: " + description

        if videos[0] == "none":
            videos[0] = title
            videos.append(description)
            videos.append(url)
            json = {"Name": data[1], "Description": data[0], "Username": data[2], "videos": videos}
            requests.patch(url=Courses, json=json)
            return render(request, "home.html", {"success": "Uploaded Successfully."})

        else:
            videos.append(title)
            videos.append(description)
            videos.append(url)
            json = {"Name": data[1], "Description": data[0], "Username": data[2], "videos": videos}
            requests.patch(url=Courses, json=json)
            return render(request, "home.html", {"success": "Uploaded Successfully."})

    return render(request, "video.html")

def settings(request):
    Courses_Data = "https://rain-cloud-2021-default-rtdb.firebaseio.com/Courses/.json"
    api = "hRswKpUPEonCv0ubir2Va1vllI1TORh7leBWPuZT"
    all_data = requests.get(Courses_Data + '?auth=' + api)
    data = all_data.json()

    if data == None:
        return render(request, "settings.html")
        
    else:
        data_list = list(data.values())
        return render(request, "settings.html", {"data": data_list})