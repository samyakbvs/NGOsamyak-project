from django.shortcuts import render , redirect
from Homepage.forms import SignUpForm , LoginForm
from Homepage.models import Register
# from Account.views import Info
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
##
# Create your views here.

# def contact(request):
#     return render(request, 'Homepage/index.html')

def OTP(dob,email):
    import smtplib
    import calendar
    import time
    from random import randint
    dob1 = dob
    timeapplicant = time.ctime(calendar.timegm(time.gmtime()))[11:19]
    timemain = timeapplicant.split(":")
    primelist = [2,3,5,7]
    id = ""
    id += str(primelist[randint(0,3)])
    id += timemain[1] + timemain[2]
    dobsum = int(dob1[2])+int(dob1[1])
    id += str(dobsum) if dobsum > 10 else "0" + str(dobsum)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('samyakjainbvs@gmail.com', 'ShivaniSamyak02')
    # message = "Your OTP is " + id
    message = "Greetings from NGO samyak," + "\nYour OTP is " + id + "\nPlease do not log in to your account without OTP verification also do not enter incorrect OTP " + "\ndoing either of the above will result in immediate deletion of your account." + "\nThis is done for security reasons, we regret any inconvinience caused."
    server.sendmail('samyakjainbvs@gmail.com',email, message)
    print(message)

    return id




def login(request):
    # print("succes")
    # if request.method=='POST':
    #     data = LoginForm(data = request.POST)
    #     if data.is_valid():
    #         try:
    #             Temp_username = data.cleaned_data['Username']
    #             Temp_Password = data.cleaned_data['Password']
    #             checker = Register.objects.filter(Username=Temp_username)[0]
    #             if Temp_Password == checker.Password:
    #                 return Info(request,checker)
    #             else:
    #                 return render(request,'Homepage/login.html')
    #         except:
    #             return render(request,'Homepage/login.html')
    #     else:
    #         return render(request,'Homepage/login.html')
    # else:
    #     dict = {'LoginForm':LoginForm}
    #     return render(request,'Homepage/login.html',context=dict)
    if request.method == 'POST':
        print(request.POST['Username'])
        user = auth.authenticate(username=request.POST['Username'],password=request.POST['Password'])
        if user is not None:
            if user.register.IsVerified == True:
                auth.login(request, user)
                return redirect('Info')
            else:
                user.register.delete()
                user.delete()
                return redirect('Homepage')
        else:
            return render(request, 'Homepage/Auth.html',{'error':'Username or Password is incorrect.'})
    else:
        return render(request, 'Homepage/Auth.html')


def signup(request):
    # tried_registered = False
    # if request.method == 'POST':
    #     tried_registered = True
    #     data = SignUpForm(data = request.POST)
    #     checker = request.POST.copy()
    #     if data.is_valid():
    #         if checker.get('Password') == checker.get('VerifyPassword'):
    #             final = data.save(commit=False)
    #             final.save()
    #             dict = {'LoginForm':LoginForm}
    #             return render(request, 'Homepage/login.html', context=dict)
    #         else:
    #             dict = {'error':'Passwords do not match','tried_registered':tried_registered}
    #             return render(request, 'Homepage/signup.html', context=dict)
    #     else:
    #         dict = {'error':'Something went wrong','tried_registered':tried_registered}
    #         return render(request, 'Homepage/signup.html', context=dict)
    # else:
    #     dict = {'SignUpForm':SignUpForm}
    #     return render(request, 'Homepage/signup.html',context=dict)

    if request.method == 'POST':
        # User has info and wants an account now!
        if request.POST['Password'] == request.POST['VerifyPassword']:
            try:
                validate_email(request.POST['Email'])
            except ValidationError as e:
                return render(request, 'Homepage/signup.html', {'error':"Email does not exist"})
            # print(str(request.POST['Phone'] % 1000000000))
            # print(type(request.POST['Phone']))
            try:
                phoneNumber = int(request.POST['Phone'])
                if len(str(phoneNumber )) == 10:
                    pass
                else:
                    return render(request, 'Homepage/signup.html', {'error':"Phone number must be a 10 digit integer"})
            except:
                return render(request, 'Homepage/signup.html', {'error':"Phone number must be a 10 digit integer"})
            try:
                enteredEmail = Register.objects.get(Email = request.POST['Email'])
                return render(request, 'Homepage/signup.html', {'error':'This account already exists'})
            except:
                pass
            try:
                user = User.objects.get(username=request.POST['Username'])
                return render(request, 'Homepage/signup.html', {'error':'Username has already been taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['Username'], password=request.POST['Password'])
                global logincode
                logincode = OTP(request.POST['Phone'],request.POST['Email'])
                addInfo = Register(user=user,FullName=request.POST['FullName'],Email=request.POST['Email'],Address=request.POST['Address'],Phone=int(request.POST['Phone']),OTP=logincode)
                addInfo.save()

                return render(request,'Homepage/confirmOTP.html')
        else:
            return render(request, 'Homepage/Signup.html', {'error':'Passwords must match'})
    else:
        # User wants to enter info
        return render(request, 'Homepage/Signup.html')

def verifyOTP(request):
    global logincode
    if request.POST['OTP'] == logincode:
        CurrentRegister = Register.objects.get(OTP=logincode)
        user = User.objects.get(register=CurrentRegister)
        user.register.IsVerified = True
        print(user.register.IsVerified)
        user.register.save()
        auth.login(request, user)
        return redirect('Info')
    else:
        CurrentRegister = Register.objects.get(OTP=logincode)
        user = User.objects.get(register=CurrentRegister)
        CurrentRegister.delete()
        user.delete()
        return redirect('Homepage')

def error(request):
    return render(request,'Homepage/404.html')

def Home(request):
    return render(request, 'Homepage/Home.html')

def About(request):
    return render(request, 'Homepage/About.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect('authHome')
