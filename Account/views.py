from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import Site
from random import randint
from .models import CreateHistory
from .models import Collection,MonetaryCollection
from Homepage.models import Register
from django.contrib.auth.models import User
from django.contrib import auth
import xlrd
import xlwt
from xlutils.copy import copy
import openpyxl
from PIL import Image
from django.views.decorators.csrf import csrf_exempt
from .PayTm import Checksum
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
MERCHANT_KEY = 'RFXkcY7NUTsKgces'
MainUser = 'Alpha'
# kind_don_his = 0
# kind_don_col = 0
# mon_don_his = 0
# mon_don_col = 0
# Create your views here.
# MainIdKindHistory = 0
# MainIdKindCollection = 0
# MainIdMonHistory = 0
# MainIdMonCollection = 0

# global mon_don_his,mon_don_col,kind_don_col,kind_don_his


def Info(request):
    if request.method == 'POST':
        CurrentUser = User.objects.get(username=request.user.username)
        print(request.FILES)
        CurrentUser.register.UserImage = request.FILES["UploadedImage"]
        # im = Image.open("/Users/samyakjain/NGOsamyak-project/media/images/sambam.jpg")
        # im.thumbnail((220, 130), Image.ANTIALIAS)
        # CurrentUser.register.UserImage.save(im.filename,ContentFile(thumb_io.get_value()),save=False)
        CurrentUser.register.save()
        return render(request, 'Account/Info.html')
    else:
        return render(request, 'Account/Info.html')
    return render(request, 'Account/Info.html')

def History(request):
    User_History = CreateHistory.objects.filter(Name = request.user.username,Paid=True)
    UserThings = []
    FinalThingsList = []
    NGO_List = []
    for s in User_History:
        UserThings.append(s.ThingsDonated)
    for j in UserThings:
        FinalThings = j.split("'")
        FinalThings.pop(0)
        FinalThings.pop(len(FinalThings)-1)
        count = 0

        for w in range(0,int(len(FinalThings)/5)+1):
            FinalThings.pop(count+1)
            try:
                FinalThings.pop(count+2)
            except:
                pass
            count += 2
        FinalThingsList.append(FinalThings)


    for t in User_History:
        NGO_List.append([t.NGO_name,t.NGO_image.url])

    # print(NGO_List)
    # print(FinalThingsList)


    zippedList = zip(NGO_List,FinalThingsList)
    # print(HistoryList)

    # HistoryList = []
    # checker = 0
    # for i in User_History:
    #     TempList = [i.NGO_name,FinalThings[checker],FinalThings[checker+1]]
    #     HistoryList.append(TempList)
    #     count += 2

    return render(request,'Account/History.html',{'zippedList':zippedList,'FinalThingsList':FinalThingsList,'NGO_List':NGO_List})

def Database(request):
    sites = Site.objects
    return render(request,'Account/database.html',{'sites':sites})

def Detail(request,site_id):
    detailSite = get_object_or_404(Site, pk=site_id)
    return render(request, 'Account/detail.html', {'detailSite':detailSite})

@csrf_exempt
def ThankYou(request,Donation_Type,HistoryId,CollectionId):
    if Donation_Type == "MONETARY":
        form = request.POST
        response_dict={}
        for i in form.keys():
            response_dict[i] = form[i]
            if i == 'CHECKSUMHASH':
                Temp_checksum = response_dict[i]
        verify = Checksum.verify_checksum(response_dict,MERCHANT_KEY,Temp_checksum)
        if verify:
            if response_dict['RESPCODE'] == '01':
                # global mon_don_his, mon_don_col
                # mon_don_his.save()
                # mon_don_col.save()
                # Mondumdum.save()
                # Monsumsum.save()
                # print(request.user.username)
                # mon_don_his = get_object_or_404(CreateHistory,pk=MainIdMonHistory )
                # mon_don_col = get_object_or_404(MonetaryCollection,pk=MainIdMonCollection)
                # mon_don_his.Paid = True
                # mon_don_col.Paid = True
                mon_don_his = get_object_or_404(CreateHistory,pk=HistoryId )
                mon_don_his.Paid = True
                mon_don_his.save()
                mon_don_col = get_object_or_404(Collection,pk=CollectionId )
                mon_don_col.Paid = True
                mon_don_col.save()

                return render(request,'Account/ThankYou.html')
            else:
                return HttpResponse("<h1>An error has occured pls try again later</h1>")
        else:
            return HttpResponse("<h1>An error has occured pls try again later</h1>")
    if Donation_Type == "KIND":
        form = request.POST
        response_dict={}
        for i in form.keys():
            response_dict[i] = form[i]
            if i == 'CHECKSUMHASH':
                Temp_checksum = response_dict[i]
        verify = Checksum.verify_checksum(response_dict,MERCHANT_KEY,Temp_checksum)
        if verify:
            if response_dict['RESPCODE'] == '01':
                print(request.user.username)
                # kind_don_his = get_object_or_404(CreateHistory,pk=MainIdKindHistory)
                # kind_don_col = get_object_or_404(Collection,pk=MainIdKindCollection)
                # global kind_don_his, kind_don_col
                # kind_don_his.Paid = True
                # kind_don_col.Paid = True
                # kind_don_his.save()
                # kind_don_col.save()
                kind_don_his = get_object_or_404(CreateHistory,pk=HistoryId )
                kind_don_his.Paid = True
                kind_don_his.save()
                kind_don_col = get_object_or_404(Collection,pk=CollectionId )
                kind_don_col.Paid = True
                kind_don_col.save()
                return render(request,'Account/ThankYou.html')
            else:
                return HttpResponse("<h1>An error has occured pls try again later</h1>")
        else:
            return HttpResponse("<h1>An error has occured pls try again later</h1>")


def changeDetails(request,user_username):
    if request.method=='POST':
        CurrentUser = User.objects.get(username=user_username)
        CurrentRegister = Register.objects.get(user = CurrentUser)
        # CurrentUser.username = user_username
        if request.POST.get('Password',False) == request.POST.get('VerifyPassword',False) :
            CurrentUser.set_password(request.POST['Password'])
        else:
            return redirect('http://127.0.0.1:8000/Account/ChangeDetails/'+str(user_username))
        CurrentRegister.Address = request.POST['Address']
        if len(request.POST['Phone']) == 10:
            CurrentRegister.Phone = int(request.POST['Phone'])
        else:
            return redirect('http://127.0.0.1:8000/Account/ChangeDetails/'+str(user_username))
        try:
            validate_email(request.POST['Email'])
        except ValidationError as e:
            return redirect('http://127.0.0.1:8000/Account/ChangeDetails/'+str(user_username))
        CurrentRegister.Email = request.POST['Email']
        CurrentRegister.save()
        CurrentUser.save()
        return redirect('Login')
    else:
        CurrentUser = get_object_or_404(User, username=user_username)
        return render(request, 'Account/changeDetails.html', {'CurrentUser':CurrentUser})

def SiteForm(request,detailSite_id):
    if request.method=='POST':
        detailSite = get_object_or_404(Site, pk=detailSite_id)
        Nothing = {}
        ThingsRequired = detailSite.ThingsNeeded.split(',')
        Temp_user = request.user.username
        Temp_NGO_Picture = detailSite.Picture
        Temp_User_Address = request.user.register.Address
        Temp_User_Phone = request.user.register.Phone
        Temp_NGO = detailSite.Name
        Temp_NGO_Address = detailSite.Address
        for i in ThingsRequired:
            Nothing[i] = "(" + request.POST['{}_count'.format(i)] + ")"
        Collect_Deliver = [Temp_user,Temp_User_Address,Temp_User_Phone,Temp_NGO,Temp_NGO_Address,Nothing]
        check_values = request.POST.get('radio',None)
        if check_values == 'Small':
            amount = 10
        elif check_values == 'Medium':
            amount = 20
        elif check_values == 'Large':
            amount = 50
        # global kind_don_his,kind_don_col

        kind_don_his = CreateHistory(Name=Temp_user,NGO_name=Temp_NGO,ThingsDonated=Nothing,NGO_image=Temp_NGO_Picture)

        kind_don_his.save()
        # MainIdKindHistory  = kind_don_his.id
        kind_don_col = Collection(user=Temp_user,User_Address=Temp_User_Address,User_Phone=Temp_User_Phone,NGO=Temp_NGO,NGO_Address=Temp_NGO_Address,Things=Nothing,Donation_Type=check_values)
        kind_don_col.save()
        # MainIdKindCollection = kind_don_col.id

        param_dict = {
            'MID':'DhKcem03471021583928',
            'ORDER_ID': str(randint(0,1000000000000000000000)),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': str(request.user.register.Email),
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
	        'CALLBACK_URL':'http://165.22.216.110/Account/ThankYou/KIND/'+str(kind_don_his.id)+'/'+str(kind_don_col.id)+'/',
            # 'CALLBACK_URL':'http://127.0.0.1:8000/Account/ThankYou/KIND/'+str(kind_don_his.id)+'/'+str(kind_don_col.id)+'/',
        }

        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,MERCHANT_KEY)
        return render(request, 'Account/paytm.html', {'param_dict':param_dict})
        # Kindsumsum.save()
        # print(sumsum.id)
        # dishoom = CreateHistory.objects.filter(Name=Temp_user)
        # return ThankYou(request,"KIND")
    else:
        detailSite = get_object_or_404(Site, pk=detailSite_id)
        ThingsRequired = detailSite.ThingsNeeded.split(',')
        return render(request, 'Account/form.html', {'detailSite':detailSite,'ThingsRequired':ThingsRequired})

def SiteMonetaryForm(request,detailSite_id):
    if request.method=='POST':
        detailSite = get_object_or_404(Site, pk=detailSite_id)
        Nothing = {}
        Ration = {"Rice":5,"Pulses":7,"Sugar":9}
        Temp_user = request.user.username
        Temp_NGO_Picture = detailSite.Picture
        Temp_User_Address = request.user.register.Address
        Temp_User_Phone = request.user.register.Phone
        Temp_NGO = detailSite.Name
        Temp_NGO_Address = detailSite.Address
        Amount_donation = 0
        Weight_donation = 0
        for i in Ration:
            Nothing[i] = "(" + request.POST[i] + ")"
            Weight_donation += int(request.POST[i])
            Amount_donation += int(request.POST[i]) * Ration[i]
        Amount_donation += Weight_donation * 3
        Collect_Deliver = [Temp_user,Temp_User_Address,Temp_User_Phone,Temp_NGO,Temp_NGO_Address,Nothing]
        # global mon_don_his,mon_don_col
        # MainUser = Temp_user
        mon_don_his = CreateHistory(Name=Temp_user,NGO_name=Temp_NGO,ThingsDonated=Nothing,NGO_image=Temp_NGO_Picture)
        mon_don_his.save()
        mon_don_col = MonetaryCollection(Amount=Amount_donation,Weight=Weight_donation,user=Temp_user,User_Address=Temp_User_Address,User_Phone=Temp_User_Phone,NGO=Temp_NGO,NGO_Address=Temp_NGO_Address,Things=Nothing)
        mon_don_col.save()

        param_dict = {
            'MID':'DhKcem03471021583928',
            'ORDER_ID': str(randint(0,100000000000000)),
            'TXN_AMOUNT': str(Monsumsum.Amount),
            'CUST_ID': str(request.user.register.Email),
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'DEFAULT',
            'CHANNEL_ID':'http://uchitngo.org/Account/Form/1/',
	        'CALLBACK_URL':'http://165.22.216.110/Account/ThankYou/MONETARY/'+str(mon_don_his.id)+'/'+str(mon_don_col.id)+'/',
            # 'CALLBACK_URL':'http://127.0.0.1:8000/Account/ThankYou/MONETARY/'+str(kind_don_his.id)+'/'+str(kind_don_col.id)+'/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,MERCHANT_KEY)
        return render(request, 'Account/paytm.html', {'param_dict':param_dict})
    else:
        detailSite = get_object_or_404(Site, pk=detailSite_id)
        return render(request, 'Account/MonetaryForm.html',{'detailSite':detailSite})
