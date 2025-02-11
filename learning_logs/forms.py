from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    """Simple form for intaking a new topic."""
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text' : ''}



class EntryForm(forms.ModelForm):
    """Simple form for adding an entry to a topic."""
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text' : ''}
        widgets = {'text' : forms.Textarea(attrs={'cols' : 80})}