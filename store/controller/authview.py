from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from store.forms import CustomerUserForm


def register(request):

    form = CustomerUserForm()
    if request.method == 'POST':
        form = CustomerUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Register SuccessFully! Login To Continue')
            return redirect('/register_send_otp')
    context = {'form':form}
    return render(request, 'register.html', context)


def loginpage(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You Are Already Logged In')
        return redirect('/')
    else:

        if request.method == 'POST':
            name = request.POST.get('username')
            passwd= request.POST.get('password')

            user = authenticate(request, username =name, password = passwd)

            if user is not None:
                login(request,user)
                messages.success(request, 'Logged In Successfully!!!')
                return redirect('/')

            else:
               messages.error(request, 'Invailed Username Or Password')
               return redirect('/login')
        return render(request, 'login.html')


def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Logout Successfully')

    return redirect('/')



