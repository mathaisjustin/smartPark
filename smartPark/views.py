from django.shortcuts import render, redirect
import pyrebase
from django.contrib import auth
import razorpay
import requests
from django.http import JsonResponse
from django.conf import settings
from pymongo import MongoClient
from django.core.mail import send_mail
from django.contrib import messages
import firebase_admin
from firebase_admin import auth, credentials
from firebase_admin import storage, db
from payment.models import Subscriptions
from django.core.paginator import Paginator

cred = credentials.Certificate("./smartpark/firebase-admin-sdk.json")
firebase_admin.initialize_app(cred)

config = {
    'apiKey': "AIzaSyBl-5DPtTBMXwC6eOxDP1K19wLSANBhkeg",
    'authDomain': "smartpark-380e6.firebaseapp.com",
    'projectId': "smartpark-380e6",
    'storageBucket': "smartpark-380e6.appspot.com",
    'messagingSenderId': "986213369518",
    'appId': "1:986213369518:web:6170bf0b8ad076e482cf3f",
    'measurementId': "G-LY5T3CR6CN",
    'databaseURL': "https://smartpark-380e6-default-rtdb.firebaseio.com/",
    'serviceAccount': "./smartpark/firebase-admin-sdk.json"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()
storage = firebase.storage()


def signIn(request):
    return render(request, "signIn.html")


def postsign(request):
    email = request.POST.get('email')
    passw = request.POST.get('password')
    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        message = "Please Check Your Credentials!"
        return render(request, "signIn.html", {"msg": message})

    # Get the user's ID from Firebase
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    idtoken = request.session['uid']
    if idtoken:
        a = authe.get_account_info(idtoken)['users'][0]['localId']
    else:
        message = "Oops! User Logged Out. Please Sign In Again."
        return render(request, "signIn.html", {"msg": message})
    subscription = Subscriptions.objects.filter(uid=a, paid=True).first()
    if subscription is not None:
        print("User has made a payment")
        # Redirect the user to the userdetails page
        userdetails = database.child("users").child(
            a).child('userdetails').shallow().get().val()
        if userdetails is None:
            return redirect("/userdetails/")
        else:
            return render(request, "welcome.html")
    else:
        print("User has not made a payment")
        # Redirect the user to the payment page
        return redirect("/payments/")


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
    try:
        user = authe.create_user_with_email_and_password(email, passw)
        uid = user['localId']
        database.child("users").child(uid).child("status").set({"status": "1"})
        messages.success(request, "Signup successful!")
    except:
        message = "Signup unsuccessful"
        return render(request, "signUp.html", {"msg": message})
    return render(request, "signIn.html")


def profile(request):
    import datetime
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)['users'][0]['localId']

    IDtoken = request.session['uid']
    e = authe.get_account_info(IDtoken)['users'][0]['email']

    userdetails = database.child("users").child(
        a).child('userdetails').get().val()

    profile = database.child("users").child(
        a).child('profile').get().val()

    latest_timestamp = max(userdetails.keys())
    details = userdetails[latest_timestamp]

    timestamp = max(profile.keys())
    det = profile[timestamp]

    url = det.get('url', '')

    print(url)

    fname = details.get('fname', '')
    lname = details.get('lname', '')
    uname = details.get('uname', '')
    pno = details.get('pno', '')
    add = details.get('add', '')
    city = details.get('city', '')
    state = details.get('state', '')
    zip = details.get('zip', '')
    vno = details.get('vehicle no', '')

    return render(request, "profile.html", {"fname": fname, "lname": lname, "uname": uname, "pno": pno, "add": add, "city": city, "state": state, "zip": zip, "e": e, "vno": vno})


def changepass(request):
    return render(request, "changepass.html")


def postprofile(request):
    idtoken = request.session.get('uid')
    if idtoken:
        a = authe.get_account_info(idtoken)
        a = a['users'][0]['localId']
        return render(request, "welcome.html")
    else:
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
        send_mail(
            'Password Reset Link',
            link,
            'mathaisjustin@gmail.com',
            [email],
            fail_silently=False
        )
        return render(request, 'password_reset_sent.html')
    except ValueError as e:
        error_message = str(e)
        return render(request, 'forgotpass.html', {'error_message': error_message})


def park(request):
    client = MongoClient(
        'mongodb+srv://smartpark:smartpark123@park-cluster.vmefitc.mongodb.net/test', connectTimeoutMS=30000)
    db = client['smartpark-db']
    collection = db['realtime']
    data = list(collection.find())
    return render(request, "park.html", {'data': data})


def settings(request):
    return render(request, "settings.html")


def postprofilepic(request):
    import time
    from datetime import datetime, timezone
    import pytz

    tz = pytz.timezone('Asia/Kolkata')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))

    url = request.POST.get('url')

    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    data = {
        "url": url
    }

    database.child('users').child(a).child(
        'profile').child(millis).set(data, idtoken)

    return render(request, "welcome.html")


def aboutus(request):
    return render(request, "about.html")


def mechanic(request):
    return render(request, "mechanic.html")


def discover(request):
    return render(request, "discover.html")


def tips(request):
    return render(request, "tips.html")


def fuel(request):
    return render(request, "fuel.html")


def rcc(request):
    import datetime
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)['users'][0]['localId']

    userdetails = database.child("users").child(
        a).child('userdetails').get().val()

    latest_timestamp = max(userdetails.keys())
    details = userdetails[latest_timestamp]

    vno = details.get('vehicle no', '')

    url = 'https://vehicle-rc-verification-advanced.p.rapidapi.com/v3/tasks/sync/verify_with_source/ind_rc_plus'
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "769e7b2e62msh48afe16ada1117dp1c5b62jsnf69f27fcdf22",
        "X-RapidAPI-Host": "vehicle-rc-verification-advanced.p.rapidapi.com"
    }
    data = {
        'task_id': '74f4c926-250c-43ca-9c53-453e87ceacd1',
        'group_id': '8e16424a-58fc-4ba4-ab20-5bc8e7c3c41e',
        'data': {
            'rc_number': vno
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.text.split('\n')

    return JsonResponse({'result': result})
