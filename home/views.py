from django.shortcuts import render, HttpResponse, redirect
from notes.models import Note
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def home(request):
    return render(request, 'index.html')

def search(request):
    query = request.GET['query']

    if len(query)>100 or len(query)==0:
        results = Note.objects.none()

    else:
        searchByHeading = Note.objects.filter(author=request.user, noteHeading__icontains = query)
        searchByContent = Note.objects.filter(author=request.user, noteContent__icontains = query)
        searchByUploadedDateAndTime = Note.objects.filter(author=request.user, timeStamp__icontains = query)
        searchByDeadlineDate = Note.objects.filter(author=request.user, deadlineDate__icontains = query)
        searchByDeadlineTime = Note.objects.filter(author=request.user, deadlineTime__icontains = query)
        searchByTag = Note.objects.filter(author=request.user, tag__icontains = query)

        results = searchByHeading.union(searchByContent, searchByUploadedDateAndTime, searchByDeadlineDate, searchByDeadlineTime, searchByTag)

    context = {'results': results, 'query':query}
    return render(request, 'search.html', context)

def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Checks for errorneous input
        userExists = User.objects.filter(username=username).exists()
        if userExists:
            messages.error(request, "This username is not available")
            return redirect('/')

        if len(username)<2 or len(username)>10:
            messages.error(request, "Username must be between 2 to 10 characters long")
            return redirect('/')

        if not username.isalnum():
            messages.error(request, "Username should contain alphabets and numbers only")
            return redirect('/')

        if not fname.isalpha() or not lname.isalpha():
            messages.error(request, "First name and last name should contain alphabets only")
            return redirect('/')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('/')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your MyNotes account has been created successfully")

        return redirect('/')

    else:
        return HttpResponse("404 - Not Found")

def handleLogin(request):
    if request.method == 'POST':
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
        
        else:
            messages.error(request, "Invalid credentials. Please try again!")

        return redirect('/')

    else:
        return HttpResponse("404 - Not Found")

def handleLogout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Successfully logged out")
        return redirect('/')

    else:
        return HttpResponse("404 - Not Found")
