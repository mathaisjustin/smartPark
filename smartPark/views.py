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

    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    timestaps = database.child("users").child(
        a).child('userdetails').shallow().get().val()
    if timestaps is None:
        return render(request, "userdetails.html")
    else:
        return render(request, "welcome.html")


def logout(request):
    try:
        del request.session['uid']
    except KeyError:
        pass
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
    import datetime
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    IDtoken = request.session['uid']
    e = authe.get_account_info(IDtoken)
    e = e['users']
    e = e[0]
    e = e['email']

    timestaps = database.child("users").child(
        a).child('userdetails').shallow().get().val()

    lis_time = []
    for i in timestaps:
        lis_time.append(i)

    lis_time.sort(reverse=True)
    # print(lis_time)

    for i in lis_time:
        fname = database.child("users").child(a).child(
            'userdetails').child(i).child('fname').get().val()
        lname = database.child("users").child(a).child(
            'userdetails').child(i).child('lname').get().val()
        uname = database.child("users").child(a).child(
            'userdetails').child(i).child('uname').get().val()
        pno = database.child("users").child(a).child(
            'userdetails').child(i).child('pno').get().val()
        add = database.child("users").child(a).child(
            'userdetails').child(i).child('add').get().val()
        city = database.child("users").child(a).child(
            'userdetails').child(i).child('city').get().val()
        state = database.child("users").child(a).child(
            'userdetails').child(i).child('state').get().val()
        zip = database.child("users").child(a).child(
            'userdetails').child(i).child('zip').get().val()

    # print(fname, lname, uname, pno, add, city, state, zip, e)

    # print(info)

    # fname = database.child("users").child(a).child('userdetails').get().val()
    # print({"fname": fname})
    return render(request, "profile.html", {"fname": fname, "lname": lname, "uname": uname, "pno": pno, "add": add, "city": city, "state": state, "zip": zip, "e": e})


def postsignup(request):
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = authe.create_user_with_email_and_password(email, passw)
        uid = user['localId']
        data = {"status": "1"}
        database.child("users").child(uid).child("status").set(data)
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
    # print(str(state), str(fname), str(lname), str(bio))

    # work = request.POST.get('work')
    # progress = request.POST.get('progress')
    try:
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
        print(str(a))
        # print("users "+str(user))
        print("info "+str(a))
        data = {
            "state": state,
            "fname": fname,
            "lname": lname,
            "bio": bio
        }

        # data = {
        #     "work": work,
        #     "progress": progress
        # }

        database.child('users').child(a).child(
            'profile').child(millis).set(data, idtoken)

        # print("data = "+str(data))
        # database.child('users').child(a).child('report').child('milis').set(data)
        # database.child('users').child(a).child('report').child('milis').set(data)
        # database.child("users").update(data, user['localId']['report'])
        return render(request, "welcome.html")
    except KeyError:
        message = "Oops! User Logged Out. Please Sign In Again."
        return render(request, "signIn.html", {"msg": message})


def userdetails(request):
    return render(request, "userdetails.html")


def postuserdetails(request):
    import time
    from datetime import datetime, timezone
    import pytz

    tz = pytz.timezone('Asia/Kolkata')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))

    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    uname = request.POST.get('uname')
    pno = request.POST.get('phone')
    add = request.POST.get('address')
    city = request.POST.get('city')
    state = request.POST.get('state')
    zip = request.POST.get('zip')

    # print(str(fname), str(lname), str(uname), str(pno),str(add), str(city), str(state), str(zip))

    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    data = {
        "fname": fname,
        "lname": lname,
        "uname": uname,
        "pno": pno,
        "add": add,
        "city": city,
        "state": state,
        "zip": zip
    }

    database.child('users').child(a).child(
        'userdetails').child(millis).set(data, idtoken)

    return render(request, "welcome.html")
