from django.shortcuts import render, redirect
import pyrebase
from django.contrib import auth
import razorpay
from django.conf import settings
from pymongo import MongoClient
import firebase_admin
from firebase_admin import auth
from django.core.mail import send_mail
from firebase_admin import credentials

cred = credentials.Certificate('./smartpark/firebase-admin-sdk.json')
firebase_admin.initialize_app(cred)



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
        return redirect("/payments/")
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


def postsignup(request):
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    print(email, passw)
    try:
        user = authe.create_user_with_email_and_password(email, passw)
        uid = user['localId']
        print(uid)
        data = {"status": "1"}
        database.child("users").child(uid).child("status").set(data)
    except:
        message = "signup unsucessfull"
        return render(request, "signUp.html", {"msg": message})
    return render(request, "signIn.html")


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
        vno = database.child("users").child(a).child(
            'userdetails').child(i).child('vehicle no').get().val()
    return render(request, "profile.html", {"fname": fname, "lname": lname, "uname": uname, "pno": pno, "add": add, "city": city, "state": state, "zip": zip, "e": e, "vno": vno})

def changepass(request):
    return render(request, "changepass.html")

def postprofile(request):
    try:
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
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
    vno = request.POST.get('vno')

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
        "zip": zip,
        "vehicle no": vno
    }

    database.child('users').child(a).child(
        'userdetails').child(millis).set(data, idtoken)

    return render(request, "welcome.html")

def subscription(request):
    return render(request, "subscription.html")

def postsubscription(request):
    name = request.POST.get('name')

def successpayment(request):
    return render(request, "successpayment.html")

def terms(request):
    return render(request, "terms.html")

def forgotpass(request):
    return render(request, 'forgotpass.html')

def postforgotpass(request):
    email = request.POST.get('email')
    try:
        link = auth.generate_password_reset_link(email)
        send_mail('Password Reset Link', link, 'mathaisjustin@gmil.com.com', [email], fail_silently=False)
        return render(request, 'password_reset_sent.html')
    except ValueError as e:
        error_message = str(e)
    return render(request, 'forgotpass.html', {'error_message': error_message})
    return render(request, 'forgotpass.html')

def park(request):
    client = MongoClient('mongodb+srv://smartpark:smartpark123@park-cluster.vmefitc.mongodb.net/test', connectTimeoutMS=30000)
    db = client['smartpark-db']
    collection = db['realtime']
    data = list(collection.find())
    return render(request, "park.html", {'data': data})

def settings(request):
    return render(request, "settings.html")