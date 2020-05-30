from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import Site
from random import randint
import uuid
from .models import Collection,MonetaryCollection,ThingsDonated,Donation
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


def Homepage(request):
    return render(request, 'Account/Home.html')

def Contact(request):
    return render(request,'Account/Contact.html')

def History(request):
    return render(request,'Account/History.html')

def Database(request):
    sites = Site.objects.all()
    return render(request,'Account/Library.html',{'sites':sites})

def About(request):
    return render(request,'Account/About.html')

def Detail(request,site_id):
    detailSite = get_object_or_404(Site, pk=site_id)
    return render(request, 'Account/Ngo.html', {'Site':detailSite})

def Info(request):
    if request.method == 'POST':
        CurrentUser = request.user
        CurrentUser.register.UserImage = request.FILES["UploadedImage"]
        CurrentUser.register.save()
        return render(request, 'Account/Info.html')
    else:
        return render(request, 'Account/Info.html')

def changeDetails(request):
    if request.method=='POST':
        CurrentUser = request.user
        CurrentRegister = Register.objects.get(user = CurrentUser)
        if request.POST['Password'] != '':
            if request.POST['Password'] == request.POST['VerifyPassword']:
                CurrentUser.set_password(request.POST['Password'])
            else:
                return render(request, 'Account/changeDetails.html',{'error':'Passwords do not match'})
        if request.POST['Email'] != '':
            CurrentUser.register.Email = request.POST['Email']
        if request.POST['Address'] != '':
            CurrentUser.register.Address = request.POST['Address']
        if request.POST['Phone'] != '':
            CurrentUser.register.Phone = request.POST['Phone']
        CurrentUser.register.save()
        CurrentUser.save()
        return redirect('Login')
    else:
        return render(request, 'Account/changeDetails.html')

def Donate(request):
    if request.method == 'POST':
        amount = request.POST['Amount']
        uid = str(uuid.uuid1())
        donation = Donation(amount=amount,user=request.user,uid=uid)
        donation.save()
        param_dict = {
            'MID':'DhKcem03471021583928',
            'ORDER_ID': donation.uid,
            'TXN_AMOUNT': str(amount),
            'CUST_ID': str(request.user.register.Email),
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
	        'CALLBACK_URL':'http://165.22.216.110/Account/ThankYou/DONATION/'+str(donation.uid)+'/',
            # 'CALLBACK_URL':'http://127.0.0.1:8000/Account/ThankYou/DONATION/'+str(donation.uid)+'/',

        }

        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,MERCHANT_KEY)
        return render(request, 'Account/paytm.html', {'param_dict':param_dict})
    else:
        return render(request,'Account/Donate.html')

def SiteForm(request,detailSite_id):
    if request.method=='POST':

        site = get_object_or_404(Site, pk=detailSite_id)
        uid = str(uuid.uuid1())
        kind_donation = Collection(user=request.user,ngo=site,Paid=False,uid=uid)
        kind_donation.save()
        for i in site.ThingsNeeded.split(','):
            if request.POST['{}_count'.format(i)] != 0:
                quantity = int(request.POST['{}_count'.format(i)])
                things_donated = ThingsDonated(collection=kind_donation,name=i,quantity=quantity)
                things_donated.save()

        amount = 10


        # return redirect('History')

        param_dict = {
            'MID':'DhKcem03471021583928',
            'ORDER_ID': kind_donation.uid,
            'TXN_AMOUNT': str(amount),
            'CUST_ID': str(request.user.register.Email),
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
	        # 'CALLBACK_URL':'http://165.22.216.110/Account/ThankYou/KIND/'+str(kind_donation.uid)+'/',
            'CALLBACK_URL':'http://127.0.0.1:8000/Account/ThankYou/KIND/'+str(kind_donation.uid)+'/',

        }

        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,MERCHANT_KEY)
        return render(request, 'Account/paytm.html', {'param_dict':param_dict})

    else:
        detailSite = get_object_or_404(Site, pk=detailSite_id)
        ThingsRequired = detailSite.ThingsNeeded.split(',')
        return render(request, 'Account/KindForm.html', {'detailSite':detailSite,'ThingsRequired':ThingsRequired})

@csrf_exempt
def ThankYou(request,Donation_Type,uid):

    form = request.POST
    response_dict={}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            Temp_checksum = response_dict[i]
    verify = Checksum.verify_checksum(response_dict,MERCHANT_KEY,Temp_checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            if Donation_Type == "KIND":
                kind_donation = get_object_or_404(Collection,uid=uid)
                kind_donation.Paid = True
                kind_donation.save()
            elif Donation_Type == "DONATION":
                donation =  get_object_or_404(Donation,uid=uid)
                donation.succesful = True
                donation.save()
            # elif Donation_Type == "MONETARY":
            #     monetary_donation = get_object_or_404(MonetaryCollection,uid=CollectionId)
            #     things = kind_donation.things
            #     monetary_don_col.Paid = True
            #     things.save()
            #     monetary_don_col.save()
            return render(request,'Account/ThankYou.html')
        else:
            if Donation_Type == "KIND":
                kind_donation = get_object_or_404(Collection,uid=uid)
                kind_donation.delete()
            elif Donation_Type == "DONATION":
                donation =  get_object_or_404(Donation,uid=uid)
                donation.delete()
            return render(request,'Account/ThankYou.html',{'error':'An error occured, please try again later!'})
    else:
        return render(request,'Account/ThankYou.html',{'error':'An error occured, please try again later!'})

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
        return render(request, 'Account/MonetaryKindForm.html',{'detailSite':detailSite})
