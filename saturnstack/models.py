from django.db import models
from django.urls import reverse

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator

# from core.models import AbstractBaseModel
import datetime
from django.utils import timezone
from django.db.models import Q


class Message(models.Model):
    subject = models.CharField(max_length=150)
    currency = models.CharField(max_length=100)
    body = models.CharField(max_length=2000)
    SaturnTileRef = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    created_at = models.DateTimeField(default=timezone.now)
    tileusername = models.CharField(max_length=50, default="Username")
    tilepassword = models.CharField(max_length=50, default="Password")

    # def __str__(self):
    # return self.title


class OldMessage(models.Model):
    # blank=true allows blank values, if blank null=true allows database to save null
    subject = models.CharField(max_length=150)
    currency = models.CharField(max_length=100)
    body = models.CharField(max_length=2000)
    SaturnTileRef = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    created_at = models.DateTimeField(default=timezone.now)
    tileusername = models.CharField(max_length=50, default="Username")
    tilepassword = models.CharField(max_length=50, default="Password")

    def __str__(self):
        return self.title


class SavedMessage(models.Model):
    user = models.CharField(max_length=150)
    subject = models.CharField(max_length=150)
    currency = models.CharField(max_length=100)
    body = models.CharField(max_length=2000)
    SaturnTileRef = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    tileusername = models.CharField(max_length=50, default="Username")
    tilepassword = models.CharField(max_length=50, default="Password")

    # def __str__(self):
    # return self.title


# # customer model

# class CustomerModel(models.Model):
#     user = models.CharField(max_length=100)
#     stripe_customer_id = models.CharField(max_length=100)



# class CustomerModel3(models.Model):
#     user = models.CharField(max_length=100)
#     customerid = models.CharField(max_length=100)
#     mandateid = models.CharField(max_length=100)

# # saving payment record objects from gocardless api


# class PaymentRecord(models.Model):
#     paymentrecord = models.TextField()

# saving customer basket payment


# class Purchases(models.Model):
#     user = models.CharField(max_length=150)
#     subject = models.CharField(max_length=150)
#     currency = models.CharField(max_length=100)
#     body = models.CharField(max_length=2000)
#     author = models.CharField(max_length=150)
#     tileusername = models.CharField(max_length=50, default="Username")
#     tilepassword = models.CharField(max_length=50, default="Password")
#     purchasedate = models.DateTimeField(default=timezone.now)


# Logs for Saturnstack

class SaturnLog(models.Model):
    SaturnUser = models.CharField(max_length=150)
    SaturnAction = models.CharField(max_length=150)
    SaturnTileRef = models.CharField(max_length=150)
    date = models.DateTimeField(default=timezone.now)


# Model For Emails

class ContactMessage(models.Model):
    message_name = models.CharField(max_length=150)
    message_email = models.CharField(max_length=150)
    message_subject = models.CharField(max_length=150)
    message = models.CharField(max_length=150)


class ConfirmationMessage(models.Model):
    message_name = models.CharField(max_length=150)
    message_email = models.CharField(max_length=150)
    message_subject = models.CharField(max_length=150)
    message = models.CharField(max_length=150)


# Saturn Referral Code
class UserReferral(models.Model): # store first-degree connections
    created_at = models.DateTimeField(auto_now=True, editable=False)
    main_user = models.CharField(max_length=50,blank=True,editable=True)
    first_degree_users = models.CharField(max_length=50)
    is_deleted   = models.BooleanField(default=False, verbose_name="Is Deleted")

    class Meta:
        unique_together = ["main_user", "first_degree_users"]

class UserReferral1(models.Model): # store second-degree connections
    created_at = models.DateTimeField(auto_now=True, editable=False)
    main_user = models.CharField(max_length=50)
    second_degree_users = models.CharField(max_length=50)
    is_deleted   = models.BooleanField(default=False, verbose_name="Is Deleted")

    class Meta:
        unique_together = ["main_user", "second_degree_users"]

class UserReferral2(models.Model): # store third-degree connections
    created_at = models.DateTimeField(auto_now=True, editable=False)
    main_user = models.CharField(max_length=50)
    third_degree_users = models.CharField(max_length=50)
    is_deleted   = models.BooleanField(default=False, verbose_name="Is Deleted")

    class Meta:
        unique_together = ["main_user", "third_degree_users"]

class SaturnReferral(models.Model):
    SaturnUser = models.CharField(max_length=50)
    SaturnEmail = models.CharField(max_length=50, default="null")
    ReferralCode = models.CharField(max_length=7)
    Upvote = models.PositiveIntegerField(default=0)
    Downvote = models.PositiveIntegerField(default=0)

# Saturn Connections


class SaturnConnections(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.CharField(max_length=15) # user whose referal code will be used while signup
    friend = models.CharField(max_length=15) # main user


class ConnectionCreateModel(models.Model):
    CreatorReferral = models.CharField(max_length=7)
    FriendReferral = models.CharField(max_length=7)

# subsciption model
from saturnstack.encrypted_model_fields import fields 

class SubscribedMessage(models.Model):
    user = models.CharField(max_length=150)
    subject = models.CharField(max_length=150)
    currency = models.CharField(max_length=100)
    body = models.CharField(max_length=2000)
    SaturnTileRef = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    tileusername = fields.EncryptedCharField(max_length=50, default="Username")
    tilepassword = fields.EncryptedCharField(max_length=50, default="Username")
    # tileusername = models.EncryptedCharField(max_length=50, default="Username")
    # tilepassword = models.EncryptedCharField(max_length=50, default="Password")
    def save(self, *args, **kwargs):
        if self.author !='':
            UserReferral.objects.create(main_user=self.user,first_degree_users=self.author)
            if UserReferral1.objects.get(Q(main_user=self.user) & Q(second_degree_users=self.author))!='':
                x = UserReferral1.objects.get(Q(main_user=self.user) & Q(second_degree_users=self.author))
                x.is_deleted=True
                x.save()
            if UserReferral1.objects.get(Q(main_user=self.author) & Q(second_degree_users=self.user))!='':
                y = UserReferral1.objects.get(Q(main_user=self.author) & Q(second_degree_users=self.user))
                y.is_deleted=True
                y.save()
            
            # if UserReferral2.objects.get(Q(main_user=self.user) & Q(second_degree_users=self.author))!='':
            #     x = UserReferral2.objects.get(Q(main_user=self.user) & Q(second_degree_users=self.author))
            #     x.is_deleted=True
            #     x.save()
            # if UserReferral2.objects.get(Q(main_user=self.author) & Q(second_degree_users=self.user))!='':
            #     y = UserReferral2.objects.get(Q(main_user=self.author) & Q(second_degree_users=self.user))
            #     y.is_deleted=True
            #     y.save()

            mydata2 = UserReferral.objects.filter(main_user=self.author).values('first_degree_users')
            referred1 = mydata2
            for u in referred1:
                if u['first_degree_users']!=self.user:
                    UserReferral1.objects.create(main_user=self.user,second_degree_users=u['first_degree_users'])
                    UserReferral1.objects.create(main_user=u['first_degree_users'],second_degree_users=self.user)          
        super(SubscribedMessage, self).save(*args, **kwargs)
