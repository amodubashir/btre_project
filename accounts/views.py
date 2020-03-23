from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact

# Create your views here.


def register(request):
    if request.method == 'POST':
        # REGISTER USER
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password2 = request.POST['password2']
        password = request.POST['password']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'The user name is taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'The email is taken')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, password=password,
                                                    first_name=first_name, last_name=last_name, email=email)
                    # logged in user after registration
                    #    auth.login(request, user)
                    #    messages.success('request, You are now logged in ')
                    #    return redirect('index')
                user.save()
                messages.success(
                    request, 'You are now registered and can log in ')

                return redirect('islogin')
        else:
            messages.error(request, 'password do not match')
            return redirect('register')

    else:
        return render(request, 'accounts/register.html')


# def login(request):

#     if request.method == 'POST':

#         # lOGIN USER
#         return
#     else:
#         return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, "You now are now logged out")

    return redirect('index')


def dashboard(request):
    user_contact = Contact.objects.order_by(
        'contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contact
    }

    return render(request, 'accounts/dashboard.html', context)


def islogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'invalid credentials')
            return redirect('islogin')
    else:
        return render(request, 'accounts/islogin.html')
