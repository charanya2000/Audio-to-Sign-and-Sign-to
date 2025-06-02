from django.shortcuts import render

from .facialexpression import facialexpression_model
from .forms import RegistrationForm, LoginForm
from .signtoaudio import start_sign_to_audio
from .models import RegistrationModel

def registration(request):

    status = False

    if request.method == "POST":
        # Get the posted form
        registrationForm = RegistrationForm(request.POST)

        if registrationForm.is_valid():

            regModel = RegistrationModel()
            regModel.name = registrationForm.cleaned_data["name"]
            regModel.email = registrationForm.cleaned_data["email"]
            regModel.mobile = registrationForm.cleaned_data["mobile"]
            regModel.username = registrationForm.cleaned_data["username"]
            regModel.password = registrationForm.cleaned_data["password"]

            user = RegistrationModel.objects.filter(username=regModel.username).first()

            if user is not None:
                status = False
            else:
                try:
                    regModel.save()
                    status = True
                except:
                    status = False
    if status:
        return render(request, 'login.html', locals())
    else:
        response = render(request, 'registration.html', {"message": "User All Ready Exist"})

    return response

def login(request):

    if request.method == "GET":

        loginForm = LoginForm(request.GET)

        if loginForm.is_valid():

            uname = loginForm.cleaned_data["username"]
            upass = loginForm.cleaned_data["password"]

            user = RegistrationModel.objects.filter(username=uname, password=upass).first()

            if user is not None:
                request.session['username'] = uname
                request.session['role'] = "user"
                return render(request, "home.html")
            else:
                response = render(request, 'index.html', {"message": "Invalid Credentials"})
        else:
            response = render(request, 'index.html', {"message": "Invalid Request"})

    return response

def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return render(request, 'index.html', {})


#=====================================================================================================
def detect_sing_to_audio(request):
    start_sign_to_audio()
    return render(request, 'home.html')

def facial_expression(request):
    facialexpression_model()
    return render(request, 'home.html')