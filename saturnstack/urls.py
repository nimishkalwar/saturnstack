from django.urls import path
from .api import views

urlpatterns = [

    #    SaturnStack Pages
    path('upload/SaturnLog/', views.SaturnLogPage, name="file-upload"),

    path('contact-email/', views.SendContactEmail, name='contact-email'),

    path('subscribe-tile/', views.CreateSubscribeMessage,
         name="subscribe-tile"),

        #   SaturnStack Functions

    path('saturnreferral-create/', views.CreateSaturnReferralCode,
         name="saturnreferral-create"),
    path('saturnreferral-list/', views.SaturnReferralList,
         name="saturnreferral-list"),
    path('saturnreferral-upvote/', views.SaturnReferralUpvote,
         name="saturnreferral-upvote"),
    path('saturnreferral-reputation/', views.SaturnReferralReputation,
         name="saturnreferral-reputation"),

    path('create-saturn-connection/', views.SaturnConnectionCreate,
         name="saturnreferral-connection"),
    path('check-saturn-connection/', views.SaturnConnection,
         name="saturncheck-connection"),
    path('check-second-saturn-connection/', views.SaturnSecondConnection,
         name="saturncheck-secondconnection"),
    path('check-third-saturn-connection/', views.SaturnThirdConnection,
         name="saturncheck-thirdconnection"),


    path('saturnstack-log/', views.SaturnStackLogCreate,
         name='saturnstacklog-create'),

    path('export-current-saturnlog/', views.export_current_saturnlog_csv,
        name='export-current-saturnstacklog-csv'),

    path('export-saturn-message-template/', views.export_current_messagetemplate_csv,
        name='export-saturn-message-template'),

    path('upload-message/', views.MessageUpload, name='upload-message'),
    path('message-edit/', views.MessageEdit, name="message-edit"),
    path('message-sendpassword/', views.MessageSendPassword,
         name="message-editsendpassword"),
    path('message-create/', views.MessageCreate, name="message-create"),
    path('message-list/', views.MessageList, name="message-list"),
    
    path('savedmessage-create/', views.SavedMessageCreate,
         name="savedmessage-create"),
        path('savedmessage-list/', views.SavedMessageList, name="savedmessage-list"),
    path('savedmessageuser-list/', views.SavedMessageUserList,
         name="savedmessageuser-list"),
    path('savedmessage-delete/', views.SavedMessageDelete,
         name="savedmessage-delete"),

    path('savedmessage-delete-user/', views.SavedMessageDeleteUser,
         name="savedmessage-delete-user"),
    path('message-delete/', views.MyMessagesGlobalDelete, name="message-delete"),
    path('subscribed-list/', views.SubscribedList, name="subscribed-list"),
]