import datetime

from django.contrib.auth import login, get_user_model, logout
from django.contrib.auth.views import LoginView
from django.dispatch import receiver
from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, FormView, UpdateView
from requests import Response

from chat.models import Person_Chat, Chat
from publication.models import Publication
from publication.views import Home
from .forms import *
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.contrib import messages
from django.http import HttpResponseNotFound
from .models import Notes, Files


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'person/login_user.html'

    def get_success_url(self):
        return reverse_lazy('home', kwargs={'user_id': self.request.user.pk})


class RegisterUser(CreateView):
    form_class = UserRegisterForm
    template_name = 'person/register_user.html'


    def form_valid(self, form):
        user = form.save(commit=False)
        person_url = hex(User.objects.order_by('-id').first().pk+1)[2:]
        print(person_url)
        user.slug_url = str(person_url)
        user.is_active = False
        user.save()
        # Функционал для отправки письма и генерации токена
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('confirm_email', kwargs={'uidb64': uid, 'token': token})
        current_site = '127.0.0.1:8000'                     ### Site.objects.get_current().domain ### in work app
        send_mail(
            'Подтвердите свой электронный адрес',
            f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: http://{current_site}{activation_url}',
            'service.notehunter@gmail.com',
            [user.email],
            fail_silently=False,
        )
        return redirect('email_confirmation_sent')


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            Person_Chat.objects.create(users=self.request.user, chat=Chat.objects.filter(pk=3).first())
            print(user.pk)
            reverse_to_home = reverse('home', kwargs={'user_id': user.pk})
            return HttpResponseNotFound("hello")
        else:
            return redirect('email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    template_name = 'person/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context


class EmailConfirmedView(TemplateView):
    template_name = 'person/email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = 'person/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context



def logout_user(request):
    logout(request)
    return redirect('home_no_auto')


class My_Notes(Home):
    template_name = 'person/my_notes.html'

    def get_context_data(self, **kwargs):
        context = super(My_Notes, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['user_notes'] = Notes.objects.filter(users= context['user'])

        return context


class Filter_My_Notes(My_Notes):

    def get_context_data(self, *args, **kwargs):
        context = super(My_Notes, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        if self.kwargs['filter'] == 'first_new':
            context['user_notes'] = Notes.objects.filter(users=context['user']).order_by('time_create')
        elif self.kwargs['filter'] == 'first_old':
            context['user_notes'] = Notes.objects.filter(users=context['user']).order_by('-time_create')
        else:
            return HttpResponseNotFound("There is no such filter")

        return context


class Add_My_Notes(CreateView):
    template_name = 'person/add_note.html'
    model = Notes
    form_class = Create_New_notes

    def get_context_data(self, **kwargs):
        context = super(Add_My_Notes, self).get_context_data(**kwargs)
        context['curent_user'] = self.request.user
        return context

    def form_valid(self, form):
        note = form.save(commit=False)
        note.users = self.request.user
        note.time_publicate = datetime.datetime.now()
        note.save()
        return redirect('my_notes')

    def form_invalid(self, form):
        return redirect('add_notes')


class ViewNotes(Add_My_Notes, UpdateView):
    template_name = 'person/view_note.html'
    form_class = ViewNote

    def get_context_data(self, **kwargs):
        context = super(Add_My_Notes, self).get_context_data(**kwargs)
        context['curent_user'] = self.request.user
        context['object'] = Notes.objects.filter(pk=self.kwargs['number'])
        return context

    def get_object(self, queryset=None):
        pk_object = self.kwargs['number']
        need_object = Notes.objects.filter(pk=pk_object).first()
        return need_object


def Delete_Note(request, number):
    print("DELETE", number)
    Notes.objects.filter(pk=number).delete()
    return redirect("my_notes")


class My_File(TemplateView):
    template_name = 'person/my_file.html'

    def get_context_data(self, **kwargs):
        context = super(My_File, self).get_context_data(**kwargs)
        context['user'] = self.request.user ###  don't find where use in template's
        context['curent_user'] = self.request.user
        context['user_files'] = Files.objects.filter(users=context['user'])
        return context

class ViewFiles(Add_My_Notes, UpdateView):
    template_name = 'person/view_file.html'
    form_class = ViewFile

    def get_context_data(self, **kwargs):
        context = super(ViewFiles, self).get_context_data(**kwargs)
        context['curent_user'] = self.request.user
        context['current_file'] = Files.objects.filter(uuid=self.kwargs['uuid'])
        print(context['current_file'])
        return context

    def get_object(self, queryset=None):
        pk_object = self.kwargs['uuid']
        need_object = Files.objects.filter(uuid=pk_object).first()
        return need_object

    def form_valid(self, form):
        file = form.save(commit=False)
        file.users = self.request.user
        file.save()
        return redirect('my_file')


def Delete_File(request, uuid):
    Files.objects.filter(uuid=uuid).delete()
    return redirect("my_file")

class Add_My_Files(CreateView):
    template_name = 'person/add_file.html'
    form_class = CreateFile

    def get_context_data(self, **kwargs):
        context = super(Add_My_Files, self).get_context_data(**kwargs)
        context['curent_user'] = self.request.user
        return context

    def form_valid(self, form):
        file = form.save(commit=False)
        file.users = self.request.user
        file.save()
        return redirect('my_file')

    def form_invalid(self, form):
        return redirect('add_file')


class My_Active_Chat(TemplateView):
    template_name = 'person/my_active_chat.html'

    def get_context_data(self, **kwargs):
        context = super(My_Active_Chat, self).get_context_data(**kwargs)
 #       context['user'] = self.request.user ###  don't find where use in template's
  #      context['curent_user'] = self.request.user
   #     context['user_files'] = Files.objects.filter(users=context['user'])
        return context