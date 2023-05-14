from django.contrib import admin
from django.urls import path, include

from . import views
# from django.conf.urls import url

urlpatterns = [
    # connections to admin app
    path('admin/', admin.site.urls),
    # connections to payment app
    path('payments/', include('payment.urls')),
    # connections to feedback app
    path('feedback/', include('feedback.urls')),
    # connections to profile app
    # path('profile/', include('Profile.urls')),
    # path to signin page
    path('', views.signIn, name="index"),
    # path to logout
    path('logout/', views.logout, name="log"),
    # path to postsign
    path('postsign/', views.postsign),
    # path to notification page
    path('notification/', views.notify, name="notify"),
    # path to home page
    path('home/', views.home, name="home"),
    # path to userdetails page
    path('userdetails/', views.userdetails, name="userdetails"),
    # path to postuserdetails
    path('postuserdetails/', views.postuserdetails),
    # path to profile page
    path('profile/', views.profile, name="profile"),
    # path to postprofile
    path('postprofile/', views.postprofile, name="postprofile"),
    # path to changepass page
    path('changepass/', views.changepass, name="changepass"),
    # path to signup page
    path('signup/', views.signUp, name="signup"),
    # path to postsignup
    path('postsignup/', views.postsignup, name="postsignup"),
    # path to subscription page
    path('subscription/', views.subscription),
    # path to postsubscription
    path('postsubscription/', views.subscription, name="postsubscription"),
    # path to paymentsuccess page
    path('paymentsuccess/', views.successpayment),
    # path to terms page
    path('terms/', views.terms, name="terms"),
    # path to park page
    path('park/', views.park, name="park"),
    # path to forgotpass page
    path('forgotpass/', views.forgotpass, name="forgotpass"),
    # path to postforgotpass
    path('postforgotpass/', views.postforgotpass, name="postforgotpass"),
    # path to settings page
    path('settings/', views.settings, name="settings"),
    # path to postprofilepic
    path('postprofilepic/', views.postprofilepic, name="postprofilepic"),
    # path to about us page
    path('aboutus/', views.aboutus, name="aboutus"),
    # path to mechanics page
    path('mechanic/', views.mechanic, name="mechanic"),
    # path to rcc page
    path('rcc/', views.rcc, name="rcc"),
    # path to discover page
    path('discover/', views.discover, name="discover"),
    # path to tips page
    path('tips/', views.tips, name="tips"),
    # path to fuel page
    path('fuel/', views.fuel, name="fuel"),
]
