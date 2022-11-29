from rest_framework import serializers

# from account.models import User, Blogs, Items, SourceLabel, DestinationLabel, Message, SubjectLabel, SavedMessage, CustomerModel, Puntville, SavedPuntville, SaturnLog, ContactMessage, SaturnReferral
from saturnstack.models import *


# class UserSerializer(serializers.ModelSerializer):
#     """ Used to retrieve user info """

#     class Meta:
#         model = User
#         fields = '__all__'



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class SaturnLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaturnLog
        fields = '__all__'




class ConnectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConnectionCreateModel
        fields = '__all__'


class SaturnReferralSerializer(serializers.ModelSerializer):

    class Meta:
        model = SaturnReferral
        fields = '__all__'

class UserReferralSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserReferral
        fields = ('main_user',)
    
class UserReferral1Serializer(serializers.ModelSerializer):

    class Meta:
        model = UserReferral1
        fields = ('main_user',)

class UserReferral2Serializer(serializers.ModelSerializer):

    class Meta:
        model = UserReferral2
        fields = '__all__'




class SavedMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedMessage
        fields = '__all__'


class SavedMessageUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedMessage
        fields = ('user',)



class MyMessagesSavedSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedMessage
        fields = ('subject', 'body', 'author', 'currency',
                  'tileusername', 'tilepassword')


# class CustomerModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomerModel
#         fields = ('user',)



# class CustomerModelSerializer2(serializers.Serializer):
#     user = serializers.CharField()
#     paymentdata = serializers.CharField()


# class CustomerSubscribedMessageSerializer(serializers.Serializer):
#     user = serializers.CharField()
#     posts = serializers.CharField()
#     amount = serializers.IntegerField()


class Usernameserializer(serializers.Serializer):
    user = serializers.CharField()


class SaturnUserserializer(serializers.Serializer):
    SaturnUser = serializers.CharField()

class SubscribedMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribedMessage
        fields = ('user','author')
