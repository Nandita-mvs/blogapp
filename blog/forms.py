from django.db.models import fields
from django.forms import ModelForm
from django.forms import widgets
from django.forms.widgets import Textarea
from .models import Post,Author
from django import forms
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.helper import FormHelper
from ckeditor.widgets import CKEditorWidget
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class CreatePostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CreatePostForm, self).__init__(*args, **kwargs)
        self.fields['author'].queryset = Author.objects.filter(user=self.request.user)

    class Meta:
        model=Post
        fields=['title','body_text','author']

    body_text = RichTextUploadingField()
    title=forms.CharField()

    author=forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple
    )

class UpdatePostForm(forms.ModelForm):
    """
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(UpdatePostForm, self).__init__(*args, **kwargs)
        self.fields['author'].queryset = Author.objects.filter(user=self.request.user)
    """
    class Meta:
        model=Post
        fields=['title','body_text','author']

    body_text = RichTextUploadingField()
    title=forms.CharField()

    author=forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class AuthorForm(forms.ModelForm):
    class Meta:
        model=Author
        fields=['user']
        
    