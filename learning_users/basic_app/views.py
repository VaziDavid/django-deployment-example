from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

#for login
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
#from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request,'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse('you are logged in, nice !')

@login_required #this decorator requires the user is loged in
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save() #saving to database
            user.set_password(user.password) # hashing the password
            user.save() #saving it the # DEBUG:

            profile = profile_form.save(commit=False)
            profile.user = user #that set up the one to one relationship

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else :
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basic_app/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})


def user_login(request):
# looks pretty similar to the registration with a lot of LANGUAGE_CODE

        if request.method == "POST" : # user has filled in login info
            username = request.POST.get('username') # .get comes from the login.html name='username'
            password = request.POST.get('password')
#we're going to use django built in authentication function and this makes your life really easy.

            user = authenticate(username=username,password=password)

            if user:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('index'))

                else:
                    return HttpResponse('Account not Active')
            else:
                print('someone tried to login and failed')
                print('Username : {} and password : {}'.format(username,password)) # what they tried to login with
                return HttpResponse('Invalid login details supplied!')

        else :
            return render(request,'basic_app/login.html',{})
