from django.contrib import admin
from django.dispatch import receiver
from chat.models import Person_Chat, Chat
from person.models import User, Notes, Files
from django.db.models.signals import post_save

@admin.register(User)
class PersonAdmin(admin.ModelAdmin):
    who = ''
    def save_model(self, request, obj, form, change):
        Person_Chat.objects.create(users=request , chat=Chat.objects.filter(pk=3).first())
        print(Chat.objects.filter(pk=3).first())
        print('sadasdasdas')
        super(User, self).save(self, request, obj, form, change)




 #   @receiver(post_save, sender=Person_Chat)
 #   def create_profile(sender, instance, *args, **kwargs):
  #      Person_Chat.objects.create(users=self.user, chat=Chat.objects.filter(pk=3).first())
  #      print("User Profile Deleted")


admin.site.register(Notes)
admin.site.register(Files)