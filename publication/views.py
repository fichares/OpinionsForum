from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView, FormView, UpdateView

from chat.models import Chat
from person.models import User
from publication.forms import PublicationSendForm, Find_Publication
from publication.models import Publication


class Home_No_Auto(TemplateView):
    template_name = "publication/home_no_auto.html"


class Home(TemplateView, FormView):
    template_name = "publication/home.html"
    form_class = PublicationSendForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated == True:
            # Try to dispatch to the right method; if a method doesn't exist,
            # defer to the error handler. Also defer to the error handler if the
            # request method isn't on the approved list.
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            return handler(request, *args, **kwargs)
        else:
            return redirect("home_no_auto")


    def get_context_data(self, **kwargs):
        context = super(Home, self ).get_context_data(**kwargs)
        context['curent_user'] = self.request.user
        context['chat'] = Chat.objects.filter(name='General Chat').first()
        context['message'] = Publication.objects.filter(chats=context['chat'])

        now_ip = self.find_ip_adress()
      #  e = User.objects.filter(username=self.request.user.username)
     #   context['tt']= e.location
        return context

    def find_ip_adress(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
       # print('IP WHERE',  self.request.user.last_ip_adress )
        return ip

    def form_valid(self, form):
        new_message = form.save(commit=False)
        new_message.users = self.request.user
        new_message.chats = Chat.objects.filter(pk=3).first()
        new_message.save()
        return redirect(self.request.META['HTTP_REFERER'])


class Find_message(Home):
    template_name = "publication/home.html"
    form_class = Find_Publication

    def form_valid(self, form):
        new_message = form.save(commit=False)
        new_message.users = self.request.user
        new_message.chats = Chat.objects.filter(pk=3).first()
        new_message.save()
        return redirect(self.request.META['HTTP_REFERER'])

