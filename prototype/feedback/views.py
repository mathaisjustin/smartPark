from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import FeedbackForm

# Create your views here.


def upload_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/home")
    else:
        form = FeedbackForm
        # return HttpResponseRedirect("/feedback")
    return render(request, 'files/feedback.html', {'form': form})


def home_redirect(request):
    return HttpResponseRedirect("/home")
