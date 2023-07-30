from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from ChatApp.models import Group, Chat
# Create your views here.


def home(request):
    ## Registration:-
    if request.method == "POST" and "registrations" in request.POST:
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')

        print("-------------------")
        print(f_name, l_name, email, username, password, c_password)
        print("-------------------")

        if password != c_password:
            messages.error(request, "Passwords do not match.")
            return redirect('home')
        
        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('home')
        

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('home')
        

        # Create the user
        user = User.objects.create_user(username=username, email=email, first_name=f_name, last_name=l_name)
        user.set_password(password)
        user.save()
        messages.success(request, "Registration successful. You can now log in.")
        return render(request, 'home.html')
    

    ## Login:-
    if request.method == "POST" and "login" in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)        
        if user:
            login(request, user)
            print("-------------------")
            print(login(request, user))
            print("-------------------")
            data = {
                'user': user,
            }
            return render(request, 'home.html', data) 
        
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'home.html')

    return render(request, 'home.html')



def logout_view(request):
    logout(request)
    return redirect('home')






def Chatting(request, group_name):
    print("----------------------")
    print("Group Name = ", group_name)
    print("----------------------")


    chats = []
    if Group.objects.filter(name = group_name).first():
        group = Group.objects.filter(name = group_name).first()
        chats = Chat.objects.filter(group = group)

    else:
        Group.objects.create(name = group_name)

    data = {
        'group_name': group_name,
        'chats': chats,
    }
    return render(request, 'chat.html', data)
