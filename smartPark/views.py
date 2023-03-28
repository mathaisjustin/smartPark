from django.shortcuts import render
import pyrebase
from django.contrib import auth

config = {
    'apiKey': "AIzaSyBl-5DPtTBMXwC6eOxDP1K19wLSANBhkeg",
    'authDomain': "smartpark-380e6.firebaseapp.com",
    'projectId': "smartpark-380e6",
    'storageBucket': "smartpark-380e6.appspot.com",
    'messagingSenderId': "986213369518",
    'appId': "1:986213369518:web:6170bf0b8ad076e482cf3f",
    'measurementId': "G-LY5T3CR6CN",
    'databaseURL': "https://smartpark-380e6-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
database = firebase.database()


def signIn(request):
    return render(request, "signIn.html")


def postsign(request):
    global email
    email = request.POST.get('email')
    passw = request.POST.get('password')
    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        message = "Invalid Credentials"
        return render(request, "signIn.html", {"msg": message})
    print(user['idToken'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    # return render(request, "welcome.html")
    return render(request, "profile.html", {"e": email})


def logout(request):
    auth.logout(request)
    return render(request, "signIn.html")


def signUp(request):
    return render(request, "signUp.html")


def notify(request):
    return render(request, "notification.html")


def home(request):
    return render(request, "welcome.html")


def feedback(request):
    return render(request, "feedback.html")


def profile(request):
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['email']

    return render(request, "profile.html", {"e": a})


def postsignup(request):
    name = request.POST.get('name')
    # username = request.POST.get('username')
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = authe.create_user_with_email_and_password(email, passw)
        uid = user['localId']
        data = {"name": name, "status": "1"}
        database.child("users").child(uid).child("details").set(data)
    except:
        return render(request, "signUp.html")
    return render(request, "signIn.html")


def postprofile(request):
    import time
    from datetime import datetime, timezone
    import pytz

    tz = pytz.timezone('Asia/Kolkata')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    # print("mili"+str(millis))

    state = request.POST.get('state')
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    bio = request.POST.get('bio')
    print(str(state), str(fname), str(lname), str(bio))

    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    user = a['localId']
    print("users "+str(user))
    # print("info "+str(a))
    data = {
        "state": state,
        "fname": fname,
        "lname": lname,
        "bio": bio
    }
    print("data = "+str(data))
    # database.child("users").child(user).child("report").child("milis").set(data)
    database.child("users").update(data, user['localId']['report'])
    return render(request, "welcome.html")
