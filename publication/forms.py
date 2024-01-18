from django import forms
from .models import *

class PublicationSendForm(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter message'}))

    class Meta:
        model = Publication
        fields = ("text",)

    def __init__(self, *args, **kwargs):
        super(PublicationSendForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['style'] = 'width:720px; height:60px;'



class Find_Publication(forms.Form):
    find_text = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Find message'}))