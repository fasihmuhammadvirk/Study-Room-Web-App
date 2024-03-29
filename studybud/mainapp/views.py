from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User, OTP
from .forms import RoomForm, UserForm, MyUserCreationForm
import pandas as pd
import joblib
from django.core.mail import send_mail
from django.conf import settings
import random
# Create your views here.


def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            mymessage = ["User doesnot exit"]
            context = {'page': page, 'messages': mymessage}
            return render(request, 'mainapp/login_register.html', context)

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect Email or Password')

    context = {'page': page}
    return render(request, 'mainapp/login_register.html', context)


def forget_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Return an error message to the user
            return render(request, 'mainapp/forget_password.html', {'messages': ['Email not found']})

        # Generate and save the OTP
        otp = OTP.objects.create(email=email, otp=str(
            random.randint(100000, 999999)))

        host_mail = settings.EMAIL_HOST_USER
        # Send the OTP via email
        send_mail(
            'Your OTP',  # title
            f'Your OTP is {otp.otp}',  # message
            host_mail,  # host email
            [email],  # reciver email address
            fail_silently=False,
        )

        return redirect('otp_input',email=email)

    return render(request, 'mainapp/forget_password.html')


def otp_input(request, email):
    if request.method == 'POST':
        otp = request.POST['otp']
        # email = request.POST['email']
        try:
            otp_obj = OTP.objects.filter(
                email=email).order_by('-created_at').first()
        except OTP.DoesNotExist:
            return render(request, 'mainapp/otp_input.html', {'messages': ['Invalid email']})

        if otp_obj.otp == otp and not otp_obj.is_expired():
            return redirect('change_password', email=email)
        else:
            return render(request, 'mainapp/otp_input.html', {'messages': ['Invalid or expired OTP']})
    return render(request, 'mainapp/otp_input.html')


def change_password(request, email):
    if request.method == 'POST':
        new_password = request.POST['new_password']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'mainapp/change_password.html', {'messages': ['User not found']})

        user.set_password(new_password)
        user.save()
        return redirect('login')
    return render(request, 'mainapp/change_password.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    context = {'form': form}
    return render(request, 'mainapp/login_register.html', context)


@login_required(login_url='login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q))

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms,
               'topics': topics,
               'room_count': room_count,
               'room_messages': room_messages,
               }
    return render(request, 'mainapp/home.html', context)


@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        # Access file from request.FILES
        bodyimage = request.FILES.get('bodyimage')
        if bodyimage:
            message = Message.objects.create(
                user=request.user,
                room=room,
            )
            message.bodyimage.save(bodyimage.name, bodyimage)
        else:
            message = Message.objects.create(
                user=request.user,
                room=room,
                body=request.POST.get('body'),
            )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room,
               'room_messages': room_messages,
               'participants': participants}
    return render(request, 'mainapp/room.html', context)


@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'mainapp/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':

        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'))
        return redirect('home')
    context = {'form': form, "topics": topics}
    return render(request, 'mainapp/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':

        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'mainapp/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'mainapp/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        # return redirect(request.META.get('HTTP_REFERER', '/'))
        return redirect('home')
    return render(request, 'mainapp/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    context = {'form': form}
    return render(request, 'mainapp/update-user.html', context)


@login_required(login_url='login')
def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'mainapp/topics.html', {'topics': topics})


@login_required(login_url='login')
def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'mainapp/activity.html', {'room_messages': room_messages})


@login_required(login_url='login')
def predict_sgpa_cgpa(request):
    if request.method == 'POST':
        # Extract form data from POST request
        input_data = {
            'SGPA1': float(request.POST.get('SGPA1')),
            'SGPA2': float(request.POST.get('SGPA2')),
            'SGPA3': float(request.POST.get('SGPA3')),
            'SGPA4': float(request.POST.get('SGPA4')),
            'Inter Percentage': float(request.POST.get('InterPercentage')),
            'Time Consumed on Commuting': int(request.POST.get('TimeConsumedOnCommuting')),
            'Exam Stress Impact on Performance': int(request.POST.get('ExamStressImpactOnPerformance')),
            'Interest': int(request.POST.get('Interest'))
        }

        # Convert the input values to a DataFrame
        input_df = pd.DataFrame([input_data])

        # Load the trained models
        loaded_sgpa_model = joblib.load(
            '/Users/fasihmuhammad/Desktop/Github/Study-Room-Web-App/model/sgpa_model.pkl')
        loaded_cgpa_model = joblib.load(
            '/Users/fasihmuhammad/Desktop/Github/Study-Room-Web-App/model/cgpa_model.pkl')

        # Make predictions for both SGPA and CGPA
        sgpa_prediction = loaded_sgpa_model.predict(input_df)
        cgpa_prediction = loaded_cgpa_model.predict(input_df)

        # Prepare the context for rendering the template
        context = {
            'SGPA': sgpa_prediction[0],
            'CGPA': cgpa_prediction[0]
        }

        # Render the template with the prediction results
        return render(request, 'mainapp/prediction_form.html', context)
    else:
        return render(request, 'mainapp/prediction_form.html')
