from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from django.core import serializers
from django.core.mail import send_mail
import random
import string
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.forms import PasswordChangeForm
# from account.api.serializers import UserSerializer, BlogsSerializer, ItemsSerializer, SourceLabelSerializer, DestinationLabelSerializer, MessageSerializer, SubjectLabelSerializer, SavedMessageSerializer, SavedMessageUserSerializer, MessageIDSerializer, MyMessagesSavedSerializer, CustomerModelSerializer, CustomerModelSerializer2, CustomerSubscribedMessageSerializer, Customergocardlessserializer, Usernameserializer, Mandateidserializer
# from account.api.serializers import PuntvilleSerializer, PuntvilleIDSerializer, SavedPuntvilleSerializer, SavedPuntvilleUserSerializer, MyPuntvilleSavedSerializer, SaturnLogSerializer, ContactMessageSerializer
from saturnstack.api.serializers import *
from saturnstack.models import *
from django.db.models import Q
from rest_framework.decorators import api_view
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response
import csv
from io import TextIOWrapper
from django.contrib import messages

# from account.models import Blogs, Items, OldItems, SourceLabel, OldSourceLabel, DestinationLabel, OldDestinationLabel, Message, SubjectLabel, OldSubjectLabel, SavedMessage, CustomerModel, SubscribedMessage, CustomerModel2, Purchases
from rest_framework.decorators import permission_classes, authentication_classes

# from account.models import Blogs, Items, OldItems, SourceLabel, OldSourceLabel, DestinationLabel, OldDestinationLabel, Message, OldMessage, SubjectLabel, OldSubjectLabel, SavedMessage, CustomerModel, SubscribedMessage, CustomerModel2, CustomerModel3, PaymentRecord, Puntville, OldPuntville, SavedPuntville, SaturnLog, PuntvilleLog
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import APIException


from django.contrib.auth.decorators import login_required
# import stripe
# v2.23.0 Adds support for the PaymentMethod resource and APIs
import gocardless_pro
import os
import json

# from django.contrib.auth.decorators import login_required

# stripe.api_key='sk_test_51JjToLEis9n0Eev0DTzbIHbSxW5PG5fvezMPyNC1BZrC0ZzeY633UGC6mh5LHbQC6bJxLc6AYBZKKumFWwvKsleT00AA50Q7Ot'
# stripe.api_key=os.environ.get('STRIPE.API_KEY')

client = gocardless_pro.Client(
    # We recommend storing your access token in an
    # environment variable for security
    # access_token=os.environ['GC_ACCESS_TOKEN'],
    access_token='sandbox_D2HTTl8B4ou4wgQQRzVtJJTim7YaVSDE0MiPgK_r',
    # Change this to 'live' when you are ready to go live.
    environment='sandbox'
)



@login_required()
def SaturnLogPage(request):
    return render(request, 'account/saturnlogs.html', {'title': 'Upload'})

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def SaturnStackLogCreate(request):
    serializer = SaturnLogSerializer(
        data=request.data)  # serializes our blogs data
    print('testing')
    if serializer.is_valid(raise_exception=True):  # save data to database if valid
        print('works')
        serializer.save()

    return Response(serializer.data)


# API Post for sending Email

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def SendContactEmail(request):
    serializer = ContactMessageSerializer(
        data=request.data)  # serializes our blogs data
    print('testing')
    if serializer.is_valid(raise_exception=True):  # save data to database if valid
        print('works')
        message_subject = serializer.data.get('message_subject')  # subject
        message = "Message from: " + \
            serializer.data.get('message_name') + ": " + \
            serializer.data.get('message_email') + " Message " + \
            serializer.data.get('message')  # message
        message_email = serializer.data.get('message_email')
        send_mail(
            message_subject,  # subject
            message,  # message
            message_email,  # from email
            ['haren.upadhayay01@gmail.com'],  # to email
        )

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def MessageList(request):
    message = Message.objects.all()  # query our data from model
    serializer = MessageSerializer(
        message, many=True)  # serializes our blogs data
    return Response(serializer.data)

@ api_view(['GET'])
@ permission_classes((IsAuthenticated, ))
def SavedMessageList(request):
    # query our data from model, need filter for current user
    savedmessage = SavedMessage.objects.all()

    serializer = SavedMessageSerializer(
        savedmessage, many=True)  # serializes our blogs data
    # username = request.user
    # return SavedMessage.objects.filter(user=username)
    return Response(serializer.data)

@ api_view(['POST'])
@ permission_classes((IsAuthenticated, ))
def SavedMessageUserList(request):
    serializer = SavedMessageUserSerializer(
        data=request.data)  # serializes data posted, username

    if serializer.is_valid(raise_exception=True):
        filteredmessages = SavedMessage.objects.filter(
            user=serializer.data.get('user'))
        print('works')
        print(serializer.data.get('user'))
        print(filteredmessages)
        serializesavedmessages = MessageSerializer(filteredmessages, many=True)
        print(serializesavedmessages.data)

    # filter by username here
    # savedmessage = SavedMessage.objects.all() #query our data from model, need filter for current user

    # serializer = SavedMessageSerializer(savedmessage, many=True) #serializes our blogs data

    # return SavedMessage.objects.filter(user=username)
    return Response(serializesavedmessages.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def SendConfirmationEmail(request):
    serializer = ContactMessageSerializer(
        data=request.data)  # serializes our blogs data
    print('testing')
    if serializer.is_valid(raise_exception=True):  # save data to database if valid
        print('works')
        message_subject = serializer.data.get('message_subject')  # subject
        message = "Message from: " + \
            serializer.data.get('message_name') + ": " + \
            serializer.data.get('message_email') + " Message " + \
            serializer.data.get('message')  # message
        message_email = serializer.data.get('message_email')
        send_mail(
            message_subject,  # subject
            message,  # message
            message_email,  # from email
            ['haren.upadhayay01@gmail.com'],  # to email
        )

    return Response(serializer.data)


@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated, ))
def CreateSaturnReferralCode(request):
    serializer = SaturnReferralSerializer(
        data=request.data)  # serializes our blogs data
    print('testing')
    if serializer.is_valid(raise_exception=True):  # save data to database if valid
        serializer.save()
        print('saturn referral')
        print(serializer.data)

    return Response(serializer.data)

@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated, ))
def CreateSubscribeMessage(request):
    serializer = SubscribedMessageSerializer(
        data=request.data)  # subsribe to author tile
    print('testing')
    if serializer.is_valid(raise_exception=True):  # save data to database if valid
        serializer.save()
        print('subscribe')
        print(serializer.data)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def MessageCreate(request):
    serializer = MessageSerializer(
        data=request.data)  # serializes our blogs data
    print('testing')
    if serializer.is_valid(raise_exception=True):  # save data to database if valid
        print('works')
        serializer.save()
        SaturnLog.objects.create(
            SaturnUser=serializer.data.get('author'),
            SaturnAction="TILE_CREATE",
            SaturnTileRef=serializer.data.get('SaturnTileRef'),
        )

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def MessageEdit(request):
    serializer = MessageSerializer(
        data=request.data)  # serializes our blogs data
    print('Edit Message')

    if serializer.is_valid(raise_exception=True):
        print(serializer.data)  # save data to database if valid
        Message.objects.filter(SaturnTileRef=serializer.data.get('SaturnTileRef')).update(
            body=serializer.data.get('body'),
        )
        SaturnLog.objects.create(
            SaturnUser=serializer.data.get('author'),
            SaturnAction="TILE_EDIT",
            SaturnTileRef=serializer.data.get('SaturnTileRef'),
        )

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def MessageSendPassword(request):
    serializer = UpdateMessageSerializer(
        data=request.data)  # serializes our blogs data

    if serializer.is_valid(raise_exception=True):  # save data to database if valid
        print(serializer.data)

        UserBoughtEmail = SaturnReferral.objects.get(
            SaturnUser=serializer.data.get('user')).SaturnEmail

        message_subject = "Tile Details Added"  # subject
        message = "Tile Details Has been added for the tile: " + \
            serializer.data.get('subject') + ". From the user " + \
            serializer.data.get('author')
        message_email = "generalenterprisess247@gmail.com"
        send_mail(
            message_subject,  # subject
            message,  # message
            message_email,  # from email
            [UserBoughtEmail],  # to email
        )

        Message.objects.filter(
            subject=serializer.data.get('subject'),
            currency=serializer.data.get('currency'),
            body=serializer.data.get('body'),
            author=serializer.data.get('author')).update(
            tileusername=serializer.data.get('tileusername'),
            tilepassword=serializer.data.get('tilepassword'))

        SavedMessage.objects.filter(subject=serializer.data.get('subject'),
                                    currency=serializer.data.get('currency'),
                                    body=serializer.data.get('body'),
                                    author=serializer.data.get('author')).update(
            tileusername=serializer.data.get('tileusername'),
            tilepassword=serializer.data.get('tilepassword'))

        SubscribedMessage.objects.filter(subject=serializer.data.get('subject'),
                                         currency=serializer.data.get(
                                             'currency'),
                                         body=serializer.data.get('body'),
                                         author=serializer.data.get('author')).update(
            tileusername=serializer.data.get('tileusername'),
            tilepassword=serializer.data.get('tilepassword'))

    return Response(serializer.data)


def export_current_saturnlog_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="SaturnStackLogs.csv"'

    # exports database into csv file and then downloads
    writer = csv.writer(response)
    writer.writerow(['SaturnUser', 'SaturnAction', 'SaturnTileRef', 'date'])

    datas = SaturnLog.objects.all().values_list(
        'SaturnUser', 'SaturnAction', 'SaturnTileRef', 'date')
    for data in datas:
        writer.writerow(data)

    return response

    export_current_puntvilled_disputes_csv


def export_current_messagetemplate_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="MessageTemplate.csv"'

    # exports database into csv file and then downloads
    writer = csv.writer(response)
    writer.writerow(['subject', 'author', 'body', 'currency'])

    return response


# Upload Messages


def MessageUpload(request):
    if request.method == 'POST':

        # first delete all entries in previous message
        # OldMessage.objects.all().delete()

        # transfer current messages to previous inventory, working
        newitems = Message.objects.all()

        new_item_list = []  # creates an empty list

        for item_obj in newitems:
            item_obj.pk = None  # removes pk for the items in NewInventory
            # adds the items in NewInventory into a list
            new_item_list.append(item_obj)

        # OldMessage.objects.bulk_create(new_item_list) #bulk create takes the list and creates the entry

        # include file upload and repopulate NewInventory
        # delete all entries in NewInventory

        # changes encoding to utf-8
        fileitem = TextIOWrapper(
            request.FILES['filename'].file, encoding='UTF-8')
        # with open(fileitem, mode='r') as csv_file: #commented this out as this function assumes file is in dir
        # open does not allow inmemoryuploaded file
        # request.FILES gives you binary files, but the csv module wants to have text-mode files instead.

        csv_reader = csv.DictReader(fileitem, delimiter='\t')

        print(csv_reader)
        for row in csv_reader:  # loops through all rows in file, ignores the first row with headings

            message = row["subject,author,body,currency"].split(
                ",")

            tileref = message[1][0:3] + ''.join(random.choice(string.digits) for i in range(
                3)) + ''.join(random.choice(string.ascii_lowercase) for i in range(3))

            print(tileref)

            Message.objects.create(
                subject=message[0],
                author=message[1],
                body=message[2],
                currency=message[3],
                SaturnTileRef=tileref

            )

    messages.success(
        request, 'Inventory upload successful, inventory has been updated')
    return render(request, 'account/message.html')


@ api_view(['GET'])
@ permission_classes((IsAuthenticated, ))
def SaturnReferralList(request):
    saturnreferral = SaturnReferral.objects.all()  # query our data from model
    serializer = SaturnReferralSerializer(
        saturnreferral, many=True)  # serializes our blogs data
    return Response(serializer.data)


@ api_view(['GET'])
@ permission_classes((IsAuthenticated, ))
def SaturnReferralReputation(request):
    serializer = SaturnReferralSerializer(
        data=request.data)
    if serializer.is_valid(raise_exception=True):
        saturnreferral = SaturnReferral.objects.filter(
            SaturnUser=serializer.data.get('SaturnUser'))  # query our data from model
    # serializes our blogs data
    return Response(saturnreferral.data)


@ api_view(['POST','GET'])
@ permission_classes((IsAuthenticated, ))
def SaturnConnection(request):        # Return First degree connection
    serializer = UserReferralSerializer(
        data=request.data)
    print(serializer)
    if serializer.is_valid(raise_exception=True):

        user = SaturnReferral.objects.filter(SaturnUser=serializer.data.get(
            'main_user')).values_list('SaturnUser', flat=True).first()
        mydata2 = UserReferral.objects.filter(main_user=user).values('first_degree_users').distinct()
        connect = [] # stroes first degree connection
        for u in mydata2:
            connect.append(u['first_degree_users'])
        
        print(connect)
        return Response(connect)


@ api_view(['GET','POST'])
@ permission_classes((IsAuthenticated, ))
def SaturnSecondConnection(request): # Return second degree connection
    serializer = UserReferral1Serializer(
        data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = SaturnReferral.objects.filter(SaturnUser=serializer.data.get(
            'main_user')).values_list('SaturnUser', flat=True).first()
        mydata2 = UserReferral1.objects.filter(Q(main_user=user) & Q(is_deleted=False)).values('second_degree_users').distinct()
        connect = [] # stroes first degree connection
        for u in mydata2:
            connect.append(u['second_degree_users'])
        
        print(connect)
        return Response(connect)


@ api_view(['POST'])
@ permission_classes((IsAuthenticated, ))
def SaturnThirdConnection(request): # return third degree connections
    serializer = ConnectionSerializer(
        data=request.data)
    print(request.data)
    if serializer.is_valid(raise_exception=True):

        user = SaturnReferral.objects.filter(ReferralCode=serializer.data.get(
            'FriendReferral')).values_list('SaturnUser', flat=True).first()
        mydata2 = UserReferral2.objects.filter(Q(main_user=user) & Q(is_deleted=False)).values('third_degree_users').distinct()
        t_connect = [] # stroes third degree connection
        for u in mydata2:
            s_connect.append(u['third_degree_users'])
        
        print(t_connect)
        return Response(t_connect)

@ api_view(['POST','GET'])
@ permission_classes((IsAuthenticated, ))
def SaturnConnectionCreate(request):
    print("connection create")
    serializer = ConnectionSerializer(
        data=request.data)
    if serializer.is_valid(raise_exception=True):
        print(serializer.data)
        creator = SaturnReferral.objects.filter(
            ReferralCode=serializer.data.get('CreatorReferral')).values_list('SaturnUser', flat=True)
        print("asasdasd")
        friend = SaturnReferral.objects.filter(
            ReferralCode=serializer.data.get('FriendReferral')).values_list('SaturnUser', flat=True)
        print(friend) # friend = main_user
        print(creator) # creator =referror
        SaturnConnections.objects.create(
            creator=creator[0], friend=friend[0])
        SaturnConnections.objects.create(
            friend=creator[0], creator=friend[0])

        print(friend[0])
        print(creator[0])

        #first-degree connections
        
        UserReferral.objects.create(main_user=creator[0],first_degree_users=friend[0])
        UserReferral.objects.create(main_user=friend[0],first_degree_users=creator[0])

        #second-degree connections
        second_degree_from_referred = UserReferral.objects.filter(main_user=creator[0]).values('first_degree_users').distinct()
        for u1 in second_degree_from_referred:
            if friend[0] !=u1['first_degree_users']:
                UserReferral1.objects.create(main_user=friend[0],second_degree_users = u1['first_degree_users'])
                UserReferral1.objects.create(main_user=u1['first_degree_users'],second_degree_users = friend[0])
        
        # #third-degree connections
        # third_degree_from_referred = UserReferral1.objects.filter(main_user=friend[0]).values('second_degree_users').distinct()
        # for u1 in third_degree_from_referred:
        #     if friend[0] !=u1['second_degree_users']:
        #         main_user1=u1['second_degree_users']
        #         data = UserReferral.objects.filter(main_user=main_user1).values('first_degree_users').distinct()
        #         for u2 in data:
        #             if friend[0] !=u2['first_degree_users']:
        #                 UserReferral2.objects.create(main_user=friend[0],third_degree_users = u2['first_degree_users'])
        #                 UserReferral2.objects.create(main_user=u2['first_degree_users'],third_degree_users = friend[0])
    # serializes our blogs data
    return Response(serializer.data)


@ api_view(['POST'])
@ permission_classes((IsAuthenticated, ))
def SaturnReferralUpvote(request):
    serializer = SaturnReferralSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        filteredmessages = SaturnReferral.objects.filter(
            SaturnUser="haren")
        print('works')
        print(serializer.data.get('SaturnUser'))

    # API post for saved message


@ api_view(['POST'])
@ permission_classes((IsAuthenticated, ))
def SavedMessageCreate(request):
    serializer = SavedMessageSerializer(
        data=request.data)  # serializes our blogs data
    serializermessage = MessageSerializer(data=request.data)
    # if(Message.objects.filter().exists), serializer.attribute
    # print('already exists')
    # else if(serializer.is_valid(raise_exception=True)):#save data to database if valid
    #    print('does not exist so saving')
    #    serializer.save()

    if serializer.is_valid(raise_exception=True):  # save data to database if valid
        print('works')
        SavedMessage.objects.get_or_create(
            user=serializer.data.get('user'),
            currency=serializer.data.get('currency'),
            subject=serializer.data.get('subject'),
            body=serializer.data.get('body'),
            SaturnTileRef=serializer.data.get('SaturnTileRef'),
            author=serializer.data.get('author'),
            tileusername=serializer.data.get('tileusername'),
            tilepassword=serializer.data.get('tilepassword')
        )

        SaturnLog.objects.create(
            SaturnUser=serializer.data.get('user'),
            SaturnAction="ADD_TO_BASKET",
            SaturnTileRef=serializer.data.get('SaturnTileRef'),
        )
        # delete from global feed
    if serializermessage.is_valid(raise_exception=True):
        chosenmessage = Message.objects.get(subject=serializer.data.get('subject'),
                                            body=serializer.data.get('body'),
                                            currency=serializer.data.get(
            'currency'),
            SaturnTileRef=serializer.data.get('SaturnTileRef'),
            author=serializer.data.get(
            'author'),
            created_at=serializermessage.data.get(
            'created_at'),
            tileusername=serializer.data.get(
            'tileusername'),
            tilepassword=serializer.data.get(
            'tilepassword')
        )
        chosenmessage.delete()

    return Response(serializer.data)


@ api_view(['DELETE'])
@ permission_classes((IsAuthenticated, ))
def SavedMessageDelete(request):
    # blogs = Blogs.objects.get(id=pk)
    # blogs.delete() #calls delete on the model

    # return Response('Item successfully deleted!')

    serializer = SavedMessageSerializer(data=request.data)  # data sent to us
    if serializer.is_valid(raise_exception=True):
        message = SavedMessage.objects.get(user=serializer.data.get('user'),
                                           currency=serializer.data.get(
            'currency'),
            subject=serializer.data.get(
            'subject'),
            body=serializer.data.get('body'),
            SaturnTileRef=serializer.data.get('SaturnTileRef'),
            author=serializer.data.get(
            'author'),
            tileusername=serializer.data.get(
            'tileusername'),
            tilepassword=serializer.data.get(
            'tilepassword')
        )
        message.delete()
        Message.objects.get_or_create(subject=serializer.data.get('subject'),
                                      currency=serializer.data.get('currency'),
                                      body=serializer.data.get('body'),
                                      author=serializer.data.get('author'),
                                      SaturnTileRef=serializer.data.get(
                                          'SaturnTileRef'),
                                      tileusername=serializer.data.get(
                                          'tileusername'),
                                      tilepassword=serializer.data.get(
                                          'tilepassword')
                                      )

        SaturnLog.objects.create(
            SaturnUser=serializer.data.get('user'),
            SaturnAction="REMOVE_FROM_BASKET",
            SaturnTileRef=serializer.data.get('SaturnTileRef')
        )

    return Response('Item successfully deleted!')


# delete message from saved message(my messages delete)
@ api_view(['DELETE'])
@ permission_classes((IsAuthenticated, ))
def SavedMessageDeleteUser(request):
    # blogs = Blogs.objects.get(id=pk)
    # blogs.delete() #calls delete on the model

    # return Response('Item successfully deleted!')

    serializer = MyMessagesSavedSerializer(
        data=request.data)  # data sent to us
    print(serializer)
    if serializer.is_valid(raise_exception=True):
        print(serializer.data.get('currency'))
        print(serializer.data.get('author'))
        message = SavedMessage.objects.get(
            subject=serializer.data.get('subject'),
            currency=serializer.data.get('currency'),
            body=serializer.data.get('body'),
            author=serializer.data.get('author'),
            tileusername=serializer.data.get('tileusername'),
            tilepassword=serializer.data.get('tilepassword')
        )
        print('test')
        message.delete()

    return Response('Item successfully deleted!')


# delete message from global messages(my messges delete)
@ api_view(['POST'])
@ permission_classes((IsAuthenticated, ))
def MyMessagesGlobalDelete(request):
    # serializer = SavedMessageSerializer(data=request.data) #serializes our blogs data
    serializermessage = MessageSerializer(data=request.data)
    # if(Message.objects.filter().exists), serializer.attribute
    # print('already exists')
    # else if(serializer.is_valid(raise_exception=True)):#save data to database if valid
    #    print('does not exist so saving')
    #    serializer.save()
    print(serializermessage)

    # delete from global feed
    if serializermessage.is_valid(raise_exception=True):
        chosenmessage = Message.objects.get(subject=serializermessage.data.get('subject'),
                                            currency=serializermessage.data.get(
            'currency'),
            body=serializermessage.data.get(
            'body'),
            author=serializermessage.data.get(
            'author'),
            created_at=serializermessage.data.get(
            'created_at'),
            tileusername=serializermessage.data.get(
            'tileusername'),
            tilepassword=serializermessage.data.get(
            'tilepassword'),
        )

        tileRef = serializermessage.data.get(
            'author') + serializermessage.data.get('body') + serializermessage.data.get('subject')

        SaturnLog.objects.create(
            SaturnUser=serializermessage.data.get('author'),
            SaturnAction="TILE_DELETE",
            SaturnTileRef=tileRef
        )
        print(chosenmessage)
        chosenmessage.delete()

    return Response(serializermessage.data)


# view for get_or_create amplify user to customer model and create a customer object on stripe
@ api_view(['POST'])
@ permission_classes((IsAuthenticated, ))
def CreateCustomer(request):
    # stripe.api_key=os.environ.get('STRIPE_SK')
    # stripe.api_key='sk_test_51JjToLEis9n0Eev0DTzbIHbSxW5PG5fvezMPyNC1BZrC0ZzeY633UGC6mh5LHbQC6bJxLc6AYBZKKumFWwvKsleT00AA50Q7Ot'
    serializermessage = CustomerModelSerializer(data=request.data)
    print(serializermessage)
    if serializermessage.is_valid(raise_exception=True):
        print('test one')
        if CustomerModel.objects.filter(user=serializermessage.data.get('user')).exists() == False:
            customer = stripe.Customer.create()
            print('customer.id is this '+customer.id)
            CustomerModel.objects.create(user=serializermessage.data.get(
                'user'), stripe_customer_id=customer.id)

    return Response('customer created')

# view to check if user is in customer


@ api_view(['POST'])
@ permission_classes((IsAuthenticated, ))
def CheckCustomer(request):
    serializermessage = CustomerModelSerializer(data=request.data)
    print(serializermessage)

    if serializermessage.is_valid(raise_exception=True):
        if CustomerModel.objects.filter(user=serializermessage.data.get('user')).exists():
            print('customer exists')
            return Response(True)
        else:
            print('customer does not exist')
            return Response(False)


"""
# view to create checkout session
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def CreateCheckoutSession(request):
    # stripe.api_key='sk_test_51JjToLEis9n0Eev0DTzbIHbSxW5PG5fvezMPyNC1BZrC0ZzeY633UGC6mh5LHbQC6bJxLc6AYBZKKumFWwvKsleT00AA50Q7Ot'
    serializermessage=CustomerModelSerializer(data=request.data)

    if serializermessage.is_valid(raise_exception=True):
         session = stripe.checkout.Session.create(
          payment_method_types=['card'],
          mode='setup',
          customer=CustomerModel.objects.filter(user=serializer.message.data.get('user')).stripe_customer_id,
          success_url='http://localhost:3000',
          cancel_url='http://localhost:3000',
        )

    return Response('done')

# view to add payment method
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def AddPaymentMethod(request):
    # stripe.api_key='sk_test_51JjToLEis9n0Eev0DTzbIHbSxW5PG5fvezMPyNC1BZrC0ZzeY633UGC6mh5LHbQC6bJxLc6AYBZKKumFWwvKsleT00AA50Q7Ot'
    serializermessage=CustomerModelSerializer2(data=request.data)
    print(serializermessage.initial_data.get('paymentdata'))
    print(serializermessage.initial_data['paymentdata']['paymentMethod']['id'])
    paymentid=serializermessage.initial_data['paymentdata']['paymentMethod']['id']
    customerid=CustomerModel.objects.get(user=serializermessage.initial_data.get('user')).stripe_customer_id

    # if serializermessage.is_valid(raise_exception=True):
        # print(serializer.message.data.get('user'))


    # creating setupintent, need payment method and customer id
    setupintent=stripe.SetupIntent.create(
        payment_method_types=["card"],
        customer=customerid,
        payment_method=paymentid,
        confirm=True,
    )
    print('setupintent added')
    print(setupintent.id)

    return Response('done')

# view to get payment method
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def GetPaymentMethod(request):
    # stripe.api_key='sk_test_51JjToLEis9n0Eev0DTzbIHbSxW5PG5fvezMPyNC1BZrC0ZzeY633UGC6mh5LHbQC6bJxLc6AYBZKKumFWwvKsleT00AA50Q7Ot'
    serializermessage=CustomerModelSerializer(data=request.data)
    customerid=CustomerModel.objects.get(user=serializermessage.initial_data.get('user')).stripe_customer_id

    paymentmethod=stripe.PaymentMethod.list(
      customer=customerid,
      type="card",
    )
    return Response(paymentmethod)


# view to charge saved paymentmethod with amount
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def ChargePaymentMethod(request):
    # stripe.api_key='sk_test_51JjToLEis9n0Eev0DTzbIHbSxW5PG5fvezMPyNC1BZrC0ZzeY633UGC6mh5LHbQC6bJxLc6AYBZKKumFWwvKsleT00AA50Q7Ot'

    #
    # stripe.PaymentMethod.list(
    # customer="cus_KSJZ8woOriiO51",
    # type="card",
    # )
    #

    serializermessage=CustomerSubscribedMessageSerializer(data=request.data)
    customerid=CustomerModel.objects.get(user=serializermessage.initial_data.get('user')).stripe_customer_id
    paymentmethodid=stripe.PaymentMethod.list(
    customer=customerid,
    type="card",
    ).data[0].id;
    for post in serializermessage.initial_data.get('posts'):
        SubscribedMessage.objects.create(user =serializermessage.initial_data.get('user'),
                                            subject = post['subject'],
                                            currency = post['currency'],
                                            body = post['body'],
                                            author = post['author'])

        SavedMessage.objects.filter(user =serializermessage.initial_data.get('user'),
                                            subject = post['subject'],
                                            currency = post['currency'],
                                            body = post['body'],
                                            author = post['author']).delete()






    # working payment of amount in frontend
    stripe.PaymentIntent.create(
        amount=serializermessage.initial_data.get(
            'amount'),#will be from frontend
        currency='gbp',#frontend set to gbp for now
        customer=customerid,#backend
        payment_method=paymentmethodid,#backend
        off_session=True,#?
        confirm=True,#?
    )



    return Response('test')

"""

# get subscribed posts


@ api_view(['POST'])
@ permission_classes((IsAuthenticated, ))
def SubscribedList(request):
    serializer = SavedMessageUserSerializer(
        data=request.data)  # serializes data posted, username

    if serializer.is_valid(raise_exception=True):
        filteredmessages = SubscribedMessage.objects.filter(
            user=serializer.data.get('user'))
        print('works')
        print(serializer.data.get('user'))
        print(filteredmessages)
        serializesavedmessages = MessageSerializer(filteredmessages, many=True)
        print(serializesavedmessages.data)

    # filter by username here
    # savedmessage = SavedMessage.objects.all() #query our data from model, need filter for current user

    # serializer = SavedMessageSerializer(savedmessage, many=True) #serializes our blogs data

    # return SavedMessage.objects.filter(user=username)
    return Response(serializesavedmessages.data)
