from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('/login', LoginUser.as_view(), name='login'),
    path('/register', RegisterUser.as_view(), name='register'),
    path('/logout', logout_user, name='logout'),

    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm-email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('confirm-email-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),
    path('/my_notes/', My_Notes.as_view(), name='my_notes'),
    path('/my_notes/<int:number>/<slug:name>/', ViewNotes.as_view(), name='view_note'),
    path('/my_notes/delete_note/<int:number>', Delete_Note, name='delete_note'),
    path('/my_notes/<str:filter>', Filter_My_Notes.as_view(), name='filter_my_notes'),
    path('/my_notes/add_note/', Add_My_Notes.as_view(), name='add_notes'),
    path('/my_file/', My_File.as_view(), name='my_file'),
    path('/my_file/<slug:uuid>/<slug:name>/', ViewFiles.as_view(), name='file_view'),
    path('/my_file/delete_file/<slug:uuid>', Delete_File, name='delete_file'),
    path('/my_file/add_file/', Add_My_Files.as_view(), name='add_file'),
    path('/my_active_chat/', My_Active_Chat.as_view(), name='my_active_chat'),
    ]